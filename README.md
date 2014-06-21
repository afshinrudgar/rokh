رُخ
=====
# فاز اجرایی

1. Install OpenCV & get OpenCV source

        brew tap homebrew/science
        brew install --with-tbb opencv
        wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.8/opencv-2.4.5.tar.gz
        tar xvzf opencv-2.4.8.tar.gz

2. Clone this repository

        git clone https://github.com/afshinrodgar/rokh

3. Put your positive images in the `./opencv_training/positive_images` folder and create a list
of them:

        find ./opencv_training/positive_images -iname "*.jpg" > positives.txt

4. Put the negative images in the `./opencv_training/negative_images` folder and create a list of them:

        find ./opencv_training/negative_images -iname "*.jpg" > negatives.txt

5. Create positive samples with the `./opencv_training/scripts/createsamples.pl` script and save them
to the `./opencv_training/samples` folder:

        perl opencv_training/scripts/createsamples.pl positives.txt negatives.txt samples 1500\
          "opencv_createsamples -bgcolor 0 -bgthresh 0 -maxxangle 1.1\
          -maxyangle 1.1 maxzangle 0.5 -maxidev 40 -w 80 -h 40"

6. Compile the `mergevec.cpp` file in the `./src` directory:

        cp opencv_training/src/mergevec.cpp ~/opencv-2.4.8/apps/haartraining
        cd ~/opencv-2.4.8/apps/haartraining
        g++ `pkg-config --libs --cflags opencv` -I. -o mergevec mergevec.cpp\
          cvboost.cpp cvcommon.cpp cvsamples.cpp cvhaarclassifier.cpp\
          cvhaartraining.cpp\
          -lopencv_core -lopencv_calib3d -lopencv_imgproc -lopencv_highgui -lopencv_objdetect

7. Use the compiled executable `mergevec` to merge the samples in `./samples`
into one file:

        find ./opencv_training/samples -name '*.vec' > samples.txt
        ./mergevec samples.txt samples.vec

8. Start training the classifier with `opencv_traincascade`, which comes with
OpenCV, and save the results to `./classifier`:

        opencv_traincascade -data opencv_training/classifier -vec samples.vec -bg negatives.txt\
          -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 1000\
          -numNeg 600 -w 80 -h 40 -mode ALL -precalcValBufSize 1024\
          -precalcIdxBufSize 1024

9. Wait until the process is finished (which takes a long time — a couple of
days probably, depending on the computer you have and how big your images are).

10. Use your finished classifier!

        cd ~/opencv-2.4.8/samples/c
        chmod +x build_all.sh
        ./build_all.sh
        ./facedetect --cascade="~/finished_classifier.xml"
