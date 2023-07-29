from sys import argv
import cv2
import numpy as np
from enum import Enum
from collections import OrderedDict

from utils import RandColorIterator


class Select(Enum):
    init = 0
    new_select = 1

cap = cv2.VideoCapture(argv[1])
i = 0
while True:
    _, image = cap.read()
    i += 1
    if i > 20:
        break


points = OrderedDict()
select = Select.init
i = 0
prev_state = i
color_map = {}
canvas = image.copy()


def click_callback(event, x, y, flags, param):
    global points, canvas, select, i
    if event == cv2.EVENT_LBUTTONDOWN and select == Select.new_select:
        if i not in points:
            points[i] = []
        points[i].append((x, y))
    # elif event == cv2.EVENT_MOUSEMOVE:
    #     cv2.line(canvas, (0, y), (w - 1, y), (0, 255, 0), 1)
    #     cv2.line(canvas, (x, 0), (x, h - 1), (0, 255, 0), 1)


h, w = image.shape[:2]
offset = 0
cv2.namedWindow('image')
cv2.setMouseCallback('image', click_callback)

while True:
    canvas = image.copy()
    cv2.rectangle(canvas, (0, 0), (w - 1, 40), (0, 0, 0), -1)
    cv2.putText(canvas, "Press 'n' to create new polygon, 'q' to exit, 'u' to undo",
                (10, 25), 0, 0.5, (255, 255, 255), 1)
    if points and select == Select.new_select:
        for idx, pset in points.items():
            color = color_map[idx]
            for x, y in pset:
                cv2.circle(canvas, (x, y), 3, color, -1)
            if len(pset) >= 3:
                poly = np.array(pset, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(canvas, [poly], True, color, 2)

    cv2.imshow('image', canvas)
    key = cv2.waitKey(20) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('u'):
        points[i].pop()
    elif key == ord('n'):
        select = Select.new_select
        if prev_state < 0:
            prev_state = i + 1
            color_map[prev_state] = next(RandColorIterator())
        else:
            prev_state = i
        i += 1
        color_map[i] = next(RandColorIterator())


print('Selected areas:')
for i, pset in points.items():
    print(i, np.array(pset).reshape(-1).tolist())
