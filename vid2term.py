import os
import sys
import cv2 as cv
from PIL import Image

# fix windows cmd
from colorama import just_fix_windows_console
just_fix_windows_console()



# get distance of 2 tuples
def tuple_distance(tuple1: tuple,tuple2: tuple):
    d1 = max(tuple1[0],tuple2[0]) - min(tuple1[0],tuple2[0])
    d2 = max(tuple1[1],tuple2[1]) - min(tuple1[1],tuple2[1])
    d3 = max(tuple1[2],tuple2[2]) - min(tuple1[2],tuple2[2])
    return d1 + d2 + d3
# get best match for tuple in list
def get_closest(tuplelist: list,tuple: tuple):
    nearest = min(tuplelist, key=lambda x: tuple_distance(x, tuple))
    return nearest
# to move cursor 
def move (y, x):
    sys.stdout.write("\033[%d;%dH" % (y, x))

colors = {(0,0,0):40,
          (255,0,0):41,
          (0,255,0):42,
          (255,255,0):43,
          (0,0,255):44,
          (255,0,255):45,
          (0,255,255):46,
          (255,255,255):47}
cap = cv.VideoCapture(sys.argv[1])
while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        sys.stderr.write("Can't receive frame (stream end?). Exiting ...")
        break
    im = Image.fromarray(frame)
    # resize
    width,height = os.get_terminal_size()
    im = im.resize((width,height))
    frame = ""
    for y in range(height):
        for x in range(width):
            pixel = im.getpixel((x,y))
            
            frame+=f"\033[{colors[get_closest(colors.keys(),pixel)]}m "
    sys.stdout.write(frame)
    # return to 0 0
    move(0,0)
