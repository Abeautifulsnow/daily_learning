import os
import psutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Union
from yaolu.log import logger


def init_worker(worker_id: int, cores: list, task_name: str):
    """worker初始化函数"""
    try:
        p = psutil.Process()
        p.cpu_affinity(cores)
        logger.info(
            f"Task {task_name} - Worker {worker_id} (PID: {os.getpid()}) 绑定到核心 {cores}"
        )
        return True
    except Exception as e:
        logger.error(f"Task {task_name} - Worker {worker_id} 核心绑定失败: {e}")
        return False


class TaskCPUAffinityManager:
    """多任务CPU亲和性管理器"""

    def __init__(self, total_cores: int = 16, reserved_cores: int = 4):
        self.total_cores = total_cores
        self.reserved_cores = reserved_cores

        if reserved_cores >= total_cores:
            raise ValueError("reserved_cores 必须小于 total_cores")

        self.available_cores = list(
            range(reserved_cores, total_cores)
        )  # 从保留核心之后开始分配
        self.task_executors: Dict[str, ProcessPoolExecutor] = {}
        self.assigned_cores: Dict[str, List[int]] = {}  # 记录每个任务分配的核心
        self.core_usage_count: Dict[int, str] = {}  # 记录核心被哪个任务使用

    def _validate_core_availability(
        self, required_cores: int, task_name: str
    ) -> List[int]:
        """验证核心可用性并分配核心"""
        available_cores = [
            core for core in self.available_cores if core not in self.core_usage_count
        ]

        if len(available_cores) < required_cores:
            raise ValueError(
                f"任务 {task_name} 需要 {required_cores} 个核心，但只有 {len(available_cores)} 个核心可用"
            )

        assigned_cores = available_cores[:required_cores]

        # 检查是否有重复分配
        for core in assigned_cores:
            if core in self.core_usage_count:
                raise ValueError(
                    f"核心 {core} 已被任务 {self.core_usage_count[core]} 使用"
                )

        return assigned_cores

    def _assign_cores_by_strategy(
        self, task_name: str, num_workers: int, cores_per_worker: int = 1
    ) -> List[List[int]]:
        """按策略分配核心给任务的workers"""
        total_required_cores = num_workers * cores_per_worker

        assigned_cores = self._validate_core_availability(
            total_required_cores, task_name
        )

        # 将分配的核心按worker数量分组
        worker_cores = []
        for i in range(num_workers):
            start_idx = i * cores_per_worker
            end_idx = start_idx + cores_per_worker
            worker_core_group = assigned_cores[start_idx:end_idx]
            worker_cores.append(worker_core_group)

        # 记录分配信息
        self.assigned_cores[task_name] = assigned_cores
        for core in assigned_cores:
            self.core_usage_count[core] = task_name

        return worker_cores

    def create_task_executors(
        self, task_configs: Dict[str, Union[int, Dict]]
    ) -> Dict[str, ProcessPoolExecutor]:
        """
        创建任务执行器

        Args:
            task_configs: 任务配置字典
                - key: 任务名称
                - value: 可以是int（worker数量）或dict（包含worker数量和其他配置）

        Returns:
            Dict[str, ProcessPoolExecutor]: 任务名称到执行器的映射
        """
        task_executors = {}

        # 解析任务配置
        parsed_configs = {}
        for task_name, config in task_configs.items():
            if isinstance(config, int):
                parsed_configs[task_name] = {
                    "num_workers": config,
                    "cores_per_worker": 1,
                }
            elif isinstance(config, dict):
                parsed_configs[task_name] = {
                    "num_workers": config.get("num_workers", 1),
                    "cores_per_worker": config.get("cores_per_worker", 1),
                }
            else:
                raise ValueError(f"任务 {task_name} 的配置格式错误，应为int或dict")

        # 验证所有任务的核心需求
        total_required_cores = sum(
            cfg["num_workers"] * cfg["cores_per_worker"]
            for cfg in parsed_configs.values()
        )

        if total_required_cores > len(self.available_cores):
            raise ValueError(
                f"总需求核心数 {total_required_cores} 超过可用核心数 {len(self.available_cores)}"
            )

        # 为每个任务创建执行器
        for task_name, config in parsed_configs.items():
            num_workers = config["num_workers"]
            cores_per_worker = config["cores_per_worker"]

            logger.info(
                f"为任务 {task_name} 分配 {num_workers} 个worker，每个worker {cores_per_worker} 个核心"
            )

            # 分配核心给该任务的workers
            worker_cores = self._assign_cores_by_strategy(
                task_name, num_workers, cores_per_worker
            )

            logger.debug(f"任务 {task_name} 分配到的核心: {worker_cores}")

            # 创建执行器
            executor = ProcessPoolExecutor(max_workers=num_workers)

            # 预初始化worker进程
            self._pre_init_workers(executor, task_name, worker_cores)

            task_executors[task_name] = executor
            self.task_executors[task_name] = executor

            logger.info(f"任务 {task_name} 执行器创建完成，分配核心: {worker_cores}")

        return task_executors

    def _pre_init_workers(
        self,
        executor: ProcessPoolExecutor,
        task_name: str,
        worker_cores: List[List[int]],
    ):
        """预初始化worker进程，绑定CPU核心"""

        # 提交初始化任务
        futures = []
        for worker_id, cores in enumerate(worker_cores):
            future = executor.submit(init_worker, worker_id, cores, task_name)
            futures.append(future)

        # 等待初始化完成
        for future in as_completed(futures):
            try:
                result = future.result(timeout=10)
                if not result:
                    logger.warning(f"Task {task_name} worker 初始化失败")
            except Exception as e:
                logger.error(f"Task {task_name} worker 初始化异常: {e}")

    def get_executor(self, task_name: str) -> ProcessPoolExecutor:
        """获取指定任务的执行器"""
        if task_name not in self.task_executors:
            raise ValueError(f"任务 {task_name} 不存在")
        return self.task_executors[task_name]

    def get_all_executors(self) -> Dict[str, ProcessPoolExecutor]:
        """获取所有执行器"""
        return self.task_executors.copy()

    def submit_task(self, task_name: str, func, *args, **kwargs):
        """向指定任务提交任务"""
        executor = self.get_executor(task_name)
        return executor.submit(func, *args, **kwargs)

    def get_allocation_info(self) -> Dict:
        """获取分配信息"""
        return {
            "total_cores": self.total_cores,
            "reserved_cores": self.reserved_cores,
            "available_cores": self.available_cores,
            "assigned_cores": self.assigned_cores.copy(),
            "core_usage_count": self.core_usage_count.copy(),
            "tasks_count": len(self.task_executors),
        }

    def shutdown(self):
        """关闭所有执行器"""
        for task_name, executor in self.task_executors.items():
            executor.shutdown(wait=True)
            logger.info(f"任务 {task_name} 的执行器已关闭")

        self.task_executors.clear()
        self.assigned_cores.clear()
        self.core_usage_count.clear()


def sample_task(task_name, worker_id):
    """示例任务函数 - 需要在模块级别定义"""
    import time

    time.sleep(1)
    return f"{task_name} - Worker {worker_id} completed"


# 使用示例
if __name__ == "__main__":
    # 创建管理器，总核心数32，保留4个
    manager = TaskCPUAffinityManager(total_cores=3, reserved_cores=4)

    # 定义任务配置：任务名 -> worker数量 或详细配置
    task_configs = {
        "task1": 3,  # 任务1需要3个worker，每个worker使用1个核心
        "task2": 2,  # 任务2需要2个worker，每个worker使用1个核心
        "task3": {
            "num_workers": 4,
            "cores_per_worker": 1,
        },  # 任务3需要4个worker，每个worker使用1个核心
        "task4": {
            "num_workers": 2,
            "cores_per_worker": 1,
        },  # 任务4需要2个worker，每个worker使用2个核心
    }

    try:
        # 创建任务执行器
        executors = manager.create_task_executors(task_configs)

        print("任务执行器创建完成:")
        for task_name, executor in executors.items():
            print(f"  {task_name}: {executor._max_workers} workers, {executor}")

        print("\n核心分配信息:")
        info = manager.get_allocation_info()
        for task, cores in info["assigned_cores"].items():
            print(f"  {task}: 核心 {cores}")

        # 为每个任务提交一些示例任务
        futures = []
        for task_name in task_configs.keys():
            future = manager.submit_task(task_name, sample_task, task_name, 0)
            futures.append((task_name, future))

        # 等待结果
        for task_name, future in futures:
            result = future.result()
            print(f"任务结果: {result}")

    except Exception as e:
        logger.error(f"创建任务执行器失败: {e}")

    finally:
        # 关闭所有执行器
        manager.shutdown()
        print("所有执行器已关闭")
