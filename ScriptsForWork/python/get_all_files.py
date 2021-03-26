import os
import sys
import time
from collections import deque
from typing import Iterator


def get_all_dir_files(input_path: str) -> Iterator:
    # create a queue
    queue = deque()
    queue.append(input_path)

    while len(queue) != 0:
        dir_path = queue.popleft()
        # find all files or folders
        file_folder_iterator = os.scandir(dir_path)

        for entry_item in file_folder_iterator:
            if entry_item.is_dir(follow_symlinks=False):
                # print(f'catalogue:{entry_item.path}')
                queue.append(entry_item.path)
            else:
                yield entry_item.path



if __name__ == "__main__":
    ts = time.time()
    input_path = sys.argv[1]
    result = get_all_dir_files(input_path)
    print(result)
    # result2list = [item for item in result]
    # print(result2list)
    # print('result length: ', len(result2list))
    print(f'# Total time cost: {time.time() - ts}(s)')
