import glob
from pathlib import Path

import cv2

img_array = []
for filename in glob.glob("./test/*.[pj][np]g"):
    print(str(Path(filename).absolute()))
    img = cv2.imread(str(Path(filename).absolute()))
    width, height, layers = img.shape
    frameSize = (width, height)
    img_array.append(img)


print("frameSize", frameSize)
out = cv2.VideoWriter(
    "./videos/output_video.avi", cv2.VideoWriter_fourcc(*"XVID"), 60, frameSize
)

for img in img_array:
    out.write(img)

out.release()
