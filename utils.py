
import os
from os import path
import cv2
import cv2.cv as cv

def read_image(filename):
    return cv.fromarray(read_image_array())

def read_image_as_array(filename):
    return cv2.imread(filename)

def process_options(options, args):
    """
    it's seems kind of funny
    I just make an option parser and then I'm parsing it myself
    :)
    """
    if options.file:
        for file in options.file:
            if path.isfile(file):
                yield options.file
            else:
                print_warning("You have to enter an filename after -f option")

    stack = []
    if options.dir:
        for dir in options.dir:
            if path.isdir(dir):
                stack.append(options.dir)
            else:
                print_warning("You have to enter an dirname after -d option")

    # stack of options containing file or directory
    # TODO: I must find a way for collecting multivariable option to get
    #       more file and folder just in one command
    for arg in args:
        if path.isfile(arg):
            yield arg
        elif path.isdir(arg):
            for file in os.listdir(arg):
                filename = path.join(arg, file)
                if path.isfile(filename):
                    yield filename
        else:
            print_warning("There's an unknown option > %s" %arg)

def print_warning(msg):
    print "Warning:", msg

def draw_rects(img, faces, color):
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

def save_img(filename, img, filtername):
    dirname = path.join(
        path.dirname(filename), 
        path.basename(filtername).split('.')[0]
    )
    basename = path.basename(filename)

    if not path.isdir(dirname):
        os.mkdir(dirname)
    filename = path.join(
        dirname, 
        basename.split('.')[-2] + "-" \
            + "faced" + '.' \
            + basename.split('.')[-1]
    )
    cv2.imwrite(filename, img)


