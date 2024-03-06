import os


def tree(dir_path, padding="", print_files=True):
    entries = os.listdir(dir_path)
    entries.sort()  # 排序,使输出结果有序

    for i, entry in enumerate(entries):
        entry_path = os.path.join(dir_path, entry)
        is_dir = os.path.isdir(entry_path)

        if i == len(entries) - 1:  # 最后一个条目
            prefix = "└─"
            child_padding = padding + "    "
        else:
            prefix = "├─"
            child_padding = padding + "│   "

        if is_dir:
            print(f"{padding}{prefix}📁 {entry}")
            tree(entry_path, child_padding, print_files)
        elif print_files:
            print(f"{padding}{prefix}📄 {entry}")
