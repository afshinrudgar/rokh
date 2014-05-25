
import os
from os import path
import cv2
import cv2.cv as cv
from mimetypes import guess_type

types_map = {
    'image': ['jpg']
}

def check_file_type(filename, type):
    return filename.split('.')[-1] in types_map[type]

def is_in_rect(point, rect):
    xp, yp = point
    xr, yr, w, h = rect
    return xr < xp < xr + w \
        and yr < yp < yr + h

def check_and_color(copy, faces, filename, truth):
    filename = path.basename(filename)
    for face in faces:
        if truth == None:   
            draw_rects(copy, face, (128, 128, 128)); 
            continue;

        flag = True
        for fact in truth.get(filename, []):
            if all(
                [is_in_rect(i, face) for i in fact.values()]
            ):
                truth[filename].remove(fact)
                flag = False
                draw_rects(copy, face, (0, 255, 0)); 
                break
        if flag:
            draw_rects(copy, face, (0, 0, 255))

    for fact in truth.get(filename, []):
        face_width = abs(fact['right-eye'][0] - fact['left-eye'][0])
        face_height =  abs(fact['center-mouth'][1] - fact['right-eye'][1])
        draw_rects(
            copy,
            (
                fact['left-eye'][0] - face_width,
                fact['left-eye'][1] - face_height,
                fact['right-corner-mouth'][0] - fact['left-eye'][0] + face_width,
                fact['right-corner-mouth'][1] - fact['left-eye'][1] + face_height
            ),
            (255, 0, 0)
        )

def read_truth_file(fn):
    truth = {}
    with open(fn, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):
                # every line is like below
                # filename left-eye right-eye nose left-corner-mouth center-mouth right-corner-mouth
                item = line.strip().split()
                filename = item[0]
                item = {
                    'left-eye':             (int(float(item[1])),   int(float(item[2]))),
                    'right-eye':            (int(float(item[3])),   int(float(item[4]))),
                    'nose':                 (int(float(item[5])),   int(float(item[6]))),
                    'left-corner-mouth':    (int(float(item[7])),   int(float(item[8]))),
                    'center-mouth':         (int(float(item[9])),   int(float(item[10]))),
                    'right-corner-mouth':   (int(float(item[11])),   int(float(item[12]))),
                }
                try:
                    truth[filename].append(item)
                except KeyError:
                    truth.setdefault(filename, [item])
    return truth

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

def draw_rects(img, face, color):
    x, y, w, h = face
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
