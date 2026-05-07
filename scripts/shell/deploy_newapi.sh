#!/bin/bash

# Docker容器部署脚本 - New API
# 用于部署 calciumion/new-api 容器

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置参数
CONTAINER_NAME="new-api"
IMAGE_NAME="calciumion/new-api:latest"
HOST_PORT="13000"
CONTAINER_PORT="3000"
TIMEZONE="Asia/Shanghai"
DATA_PATH="/home/project/new-api/data"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印分隔线
print_separator() {
    echo -e "${BLUE}========================================${NC}"
}

# 检查Docker是否安装
check_docker() {
    print_info "检查Docker环境..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker服务未运行，请启动Docker服务"
        exit 1
    fi
    
    print_success "Docker环境检查通过"
}

# 检查并创建数据目录
check_data_dir() {
    print_info "检查数据目录: $DATA_PATH"
    
    if [ "$DATA_PATH" = "/your/data/path" ]; then
        print_warning "数据路径为默认值，建议修改为实际路径"
        print_info "正在使用默认路径..."
    fi
    
    if [ ! -d "$DATA_PATH" ]; then
        print_warning "数据目录不存在，正在创建..."
        mkdir -p "$DATA_PATH" || {
            print_error "无法创建数据目录: $DATA_PATH"
            exit 1
        }
        print_success "数据目录创建成功: $DATA_PATH"
    else
        print_info "数据目录已存在: $DATA_PATH"
    fi
}

# 停止并删除已存在的容器
clean_existing() {
    if docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        print_warning "发现已存在的容器: $CONTAINER_NAME"
        print_info "正在停止容器..."
        docker stop "$CONTAINER_NAME" &> /dev/null || true
        print_info "正在删除容器..."
        docker rm "$CONTAINER_NAME" &> /dev/null || true
        print_success "已清理旧容器"
    fi
}

# 拉取最新镜像
pull_image() {
    print_info "正在拉取镜像: $IMAGE_NAME"
    if docker pull "$IMAGE_NAME"; then
        print_success "镜像拉取成功"
    else
        print_error "镜像拉取失败"
        exit 1
    fi
}

# 启动容器
start_container() {
    print_info "正在启动容器..."
    
    if docker run --name "$CONTAINER_NAME" \
        -d \
        --restart always \
        -p "${HOST_PORT}:${CONTAINER_PORT}" \
        -e "TZ=${TIMEZONE}" \
        -v "${DATA_PATH}:/data" \
        "$IMAGE_NAME"; then
        print_success "容器启动成功"
    else
        print_error "容器启动失败"
        exit 1
    fi
    
    # 等待容器完全启动
    print_info "等待服务启动..."
    sleep 5
}

# 显示容器状态
show_status() {
    print_separator
    echo -e "${GREEN}========== 容器部署完成 ==========${NC}"
    print_separator
    
    # 检查容器是否在运行
    if docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        print_success "容器状态: 运行中"
        
        # 获取容器详细信息
        CONTAINER_ID=$(docker ps --filter "name=${CONTAINER_NAME}" --format "{{.ID}}")
        CREATED=$(docker inspect --format '{{.Created}}' "$CONTAINER_NAME" | cut -d'.' -f1)
        STATUS=$(docker inspect --format '{{.State.Status}}' "$CONTAINER_NAME")
        IP_ADDRESS=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$CONTAINER_NAME")
        
        echo ""
        echo -e "${BLUE}容器信息:${NC}"
        echo -e "  容器名称: ${GREEN}${CONTAINER_NAME}${NC}"
        echo -e "  容器ID:   ${GREEN}${CONTAINER_ID:0:12}${NC}"
        echo -e "  镜像:     ${GREEN}${IMAGE_NAME}${NC}"
        echo -e "  创建时间: ${GREEN}${CREATED}${NC}"
        echo -e "  状态:     ${GREEN}${STATUS}${NC}"
        echo -e "  内部IP:   ${GREEN}${IP_ADDRESS}${NC}"
        echo ""
        echo -e "${BLUE}访问信息:${NC}"
        echo -e "  URL:      ${GREEN}http://localhost:${HOST_PORT}${NC}"
        echo ""
        echo -e "${BLUE}数据目录:${NC}"
        echo -e "  路径:     ${GREEN}${DATA_PATH}${NC}"
        
        print_separator
        echo -e "${YELLOW}常用命令:${NC}"
        echo -e "  查看日志: ${GREEN}docker logs -f ${CONTAINER_NAME}${NC}"
        echo -e "  进入容器: ${GREEN}docker exec -it ${CONTAINER_NAME} /bin/sh${NC}"
        echo -e "  停止容器: ${GREEN}docker stop ${CONTAINER_NAME}${NC}"
        echo -e "  启动容器: ${GREEN}docker start ${CONTAINER_NAME}${NC}"
        echo -e "  重启容器: ${GREEN}docker restart ${CONTAINER_NAME}${NC}"
        echo -e "  删除容器: ${GREEN}docker rm -f ${CONTAINER_NAME}${NC}"
        print_separator
        
        # 检查端口是否监听
        if command -v ss &> /dev/null; then
            if ss -tlnp | grep -q ":${HOST_PORT}"; then
                print_success "端口 ${HOST_PORT} 正在监听"
            fi
        elif command -v netstat &> /dev/null; then
            if netstat -tlnp | grep -q ":${HOST_PORT}"; then
                print_success "端口 ${HOST_PORT} 正在监听"
            fi
        fi
        
        # 显示最近日志
        print_info "最近的容器日志:"
        echo -e "${BLUE}----------------------------------------${NC}"
        docker logs --tail 10 "$CONTAINER_NAME" 2>&1
        echo -e "${BLUE}----------------------------------------${NC}"
        
    else
        print_error "容器状态: 未运行"
        print_info "查看错误日志:"
        docker logs "$CONTAINER_NAME" 2>&1 || true
        exit 1
    fi
}

# 主函数
main() {
    print_separator
    echo -e "${GREEN}New API - Docker容器部署脚本${NC}"
    print_separator
    echo ""
    
    print_info "配置信息:"
    echo -e "  容器名称: ${YELLOW}${CONTAINER_NAME}${NC}"
    echo -e "  镜像:     ${YELLOW}${IMAGE_NAME}${NC}"
    echo -e "  端口映射: ${YELLOW}${HOST_PORT}:${CONTAINER_PORT}${NC}"
    echo -e "  时区:     ${YELLOW}${TIMEZONE}${NC}"
    echo -e "  数据目录: ${YELLOW}${DATA_PATH}${NC}"
    echo ""
    
    print_separator
    echo ""
    
    # 执行部署步骤
    check_docker
    check_data_dir
    clean_existing
    pull_image
    start_container
    show_status
}

# 运行主函数
main
