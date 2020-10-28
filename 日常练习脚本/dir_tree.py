import os
import sys
from pathlib import Path


# method 1
# def list_files(startpath):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))


# method 2
# def showFolderTree(path, show_files=False, indentation=2, file_output=False):
#     """
#     Shows the content of a folder in a tree structure.
#     path -(string)- path of the root folder we want to show.
#     show_files -(boolean)-  Whether or not we want to see files listed.
#                             Defaults to False.
#     indentation -(int)- Indentation we want to use, defaults to 2.   
#     file_output -(string)-  Path (including the name) of the file where we want
#                             to save the tree.
#     """
#     tree = []

#     if not show_files:
#         for root, dirs, files in os.walk(path):
#             level = root.replace(path, '').count(os.sep)
#             indent = ' '*indentation*(level)
#             tree.append('{}{}/'.format(indent,os.path.basename(root)))

#     if show_files:
#         for root, dirs, files in os.walk(path):
#             level = root.replace(path, '').count(os.sep)
#             indent = ' '*indentation*(level)
#             tree.append('{}{}/'.format(indent,os.path.basename(root)))    
#             for f in files:
#                 subindent=' ' * indentation * (level+1)
#                 tree.append('{}{}'.format(subindent,f))

#     if file_output:
#         output_file = open(file_output,'w')
#         for line in tree:
#             output_file.write(line)
#             output_file.write('')
#     else:
#         # Default behaviour: print on screen.
#         for line in tree:
#             print(line)


# method 3
class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path
                               for path in root.iterdir()
                               if criteria(path)),
                          key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path):
        return True

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))


if __name__ == "__main__":
    # method 1
    # list_files('/Users/dapeng/Desktop/code/flask')

    # method 2
    # showFolderTree('/Users/dapeng/Desktop/code/flask', show_files=True)

    # method 3
    paths = DisplayablePath.make_tree(Path('/Users/dapeng/Desktop/code/flask'))
    for path in paths:
        print(path.displayable())


###################### method 3 --- directory tree #######################
"""
flask/
└── job_data_analysis/
    ├── .DS_Store
    ├── .gitignore
    ├── lagou_data_analysis/
    │   ├── run.py
    │   ├── static/
    │   │   ├── css/
    │   │   │   └── comon0.css
    │   │   ├── font/
    │   │   │   └── DS-DIGIT.TTF
    │   │   ├── images/
    │   │   │   ├── bg.jpg
    │   │   │   ├── head_bg.png
    │   │   │   └── line.png
    │   │   ├── js/
    │   │   │   ├── china.js
    │   │   │   ├── echarts.min.js
    │   │   │   ├── index.html
    │   │   │   ├── jquery.js
    │   │   │   └── js.js
    │   │   └── picture/
    │   │       ├── jt.png
    │   │       ├── lbx.png
    │   │       ├── loading.gif
    │   │       ├── map.png
    │   │       └── weather.png
    │   └── templates/
    │       ├── index.html
    │       └── test.html
    ├── lagou_spider/
    │   ├── __init__.py
    │   ├── create_lagou_tables.py
    │   ├── handle_crawl_lagou.py
    │   └── handle_insert_data.py
    ├── README.md
    └── study_echarts/
        ├── html/
        │   ├── bar.html
        │   ├── bar2.html
        │   ├── bar_test.html
        │   ├── line.html
        │   ├── map1.html
        │   ├── map2.html
        │   ├── pie.html
        │   ├── pie2.html
        │   └── word_cloud.html
        ├── image/
        │   ├── 地图1.png
        │   ├── 地图2.png
        │   ├── 折线图.png
        │   ├── 柱形图.png
        │   ├── 柱形图2.png
        │   ├── 词云.png
        │   ├── 饼图1.png
        │   ├── 饼图2.png
        │   └── 饼图3.png
        └── js/
            ├── bmap.js
            ├── china.js
            ├── echarts-wordcloud.js
            └── echarts.js
"""
