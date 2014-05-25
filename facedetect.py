#!/usr/bin/python2

from optparse import OptionParser

from config import *
from utils import *

def facedetect(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage(
        (img.width,img.height),
        8,
        1
    )
    small_img = cv.CreateImage(
        (cv.Round(img.width / image_scale),cv.Round (img.height / image_scale)),
        8,
        1
    )
    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    t = cv.GetTickCount()
    faces = cv.HaarDetectObjects(
        small_img, 
        cascade, 
        cv.CreateMemStorage(0),
        haar_scale, 
        min_neighbors, 
        haar_flags, 
        min_size
    )
    t = cv.GetTickCount() - t
    print "detection time = %dus" % (t/(cv.GetTickFrequency()))
    return faces


def main():
    # Option Parser
    parser = OptionParser(usage = "usage: %prog [options] [-f filename|-d dirname|-c cascade]")
    parser.add_option(
        "-c", "--cascade", 
        action="store", 
        dest="cascade", 
        type="str", 
        help="Haar cascade file, default %default", 
        default = "cascades/haarcascade_frontalface_default.xml",
    )
    parser.add_option(
        "-f", "--file", 
        action="append", 
        dest="file", 
        type="str", 
        help="Input file for face-detector"
    )
    parser.add_option(
        "-d", "--directory",
        action="append", 
        dest="dir", 
        type="str", 
        help="Addrress of Input files for face-detector"
    )
    (options, args) = parser.parse_args()

    cascade = cv.Load(options.cascade)

    for filename in process_options(options, args):
        try:
            img = read_image_as_array(filename)
            faces = [face[0] for face in facedetect(cv.fromarray(img), cascade)]

            copy = img.copy()
            draw_rects(copy, faces, (0, 255, 0))
            save_img(filename, copy, options.cascade)
        except:
            print_warning("Can not open file > %s" %(filename))

if __name__ == "__main__":
    main()
