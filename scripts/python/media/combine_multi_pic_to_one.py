import os
from pathlib import Path

from PIL import Image


class ConcatenateMultiPics:
    def __init__(self, source_path: str, save_path: str) -> None:
        self.folder_path = source_path
        self.save_path = save_path

    def read_pics(self):
        pics = []
        with os.scandir(self.folder_path) as it:
            for entry in it:
                if entry.is_file():
                    pics.append(Path(self.folder_path) / entry.name)

        return pics

    def combine(self):
        total_pics = self.read_pics()

        pic_contents = [Image.open(image) for image in total_pics]

        widths, heights = zip(*(i.size for i in pic_contents))
        print(widths, heights)
        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new("RGB", (total_width, max_height))
        x_offset = 0

        try:
            for im in pic_contents:
                new_im.paste(im, (x_offset, 0))
                x_offset += im.size[0]

            new_im.save(self.save_path)
        except KeyError:
            ...
        except AttributeError:
            ...
        except Exception:
            ...
        else:
            print("Done! Good job.")


if __name__ == "__main__":
    cmp = ConcatenateMultiPics("./images/", "./images/merge.png")
    cmp.combine()
