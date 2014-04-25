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


# مقدمه
اولین قدم در فرایند پردازش چهره‌، تشخیص چهره است.
هدف از تشخیص چهره پاسخ به این سوال خواهد بود که آیا در یک عکس چهره -و یا چهره‌هایی- وجود دارد یا نه؟ و اگر بله مکان هر کدام از چهره‌ -و یا چهره‌ها- کجاست؟

از موارد زیر می‌توان به عنوان چالش‌های پیش‌رو در زمینه‌ی تشخیص چهره‌ نام برد:

+ **زاویه چهره**. این‌که دوربین از کدام زاویه (تمام‌رخ، نیم‌رخ و ...) از چهره عکس گرفته باشد می‌توان فاکتور مهمی در درجه‌ی سختی تشخیص چهره محسوب گردد.
+ **وجود یا عدم وجود اجزای مختلف صورت**. اجزای مختلف صورت از جمله محاسن، سبیل و ... می‌توانند در چهره‌ی فرد موجود باشند یا نباشند. از طرفی دیگر تفاوت‌های زیادی بین شکل‌های مختلف این اجزا وجود دارد.
+ **حالات چهره**. نمای صورت در حالات مختلف چهره (لبخند، خنده، گریه و ...) متفاوت خواهد بود.
+ **پوشش**. ممکن است قسمتی از چهره بخاطر *زاویه چهره* و یا قرارگیری پشت اشیاء دیگر قابل مشاهده نباشد.
+ **زاویه عکس**. اشیاء مختلف با قرارگیری در زاویه‌های مختلف نسبت به صفحه مماس اشکال خاصی به خود می‌گیرند.
+ **شرایط عکاسی**. فاکتور‌های مختلف محیطی نظیر شرایط نوری و مشخصات دوربین عکاسی از جمله لنز‌ می‌توانند تاثیر زیادی در پروسه تشخیص چهره داشته باشند.

<img src="http://upload.wikimedia.org/wikipedia/en/2/24/Lenna.png" style="width:512px;-webkit-border-radius:20px;-moz-border-radius: 20px;border-radius: 20px;  box-shadow: 0px 0px 7px 1px #202020;-webkit-box-shadow: 0px 0px 7px 1px #202020;-moz-box-shadow: 0px 0px 7px 1px #202020;" alt="Lenna" >

در ادبیات تشخیص چهره، مفهومی مرتبط وجود دارد که از آن به عنوان *مکان‌یابی چهره* یاد می‌کنیم. خواننده محترم باید این نکته را در نظر داشته باشد که هدف از *مکان‌یابی چهره* درست همانند *تشخیص چهره* هست اما تفاوت اندکی موجود خواهد بود و آن این که در *مکان‌یابی چهره* تصویر موجود فقط شامل یک چهره در نظر گرفته می‌شود.
یکی از روش‌های مرسوم در زمینه تشخیص اشیاء در نظر گرفتن قابی کوچک روی تصویر اصلی و تشخیص این خواهد بود که آیا شیء مورد نظر در آن پنجره وجود دارد یا نه؟ پس اگر از این روش استفاده شود باید در جستجوی الگوریتمی بود تا توانایی تشخیص وجود یا عدم وجود چهره در یک قاب کوچک، متشکل از چند صد پیکسل داشته باشد.
در این دیدگاه تشخیص چهره را می‌توان به صورت مساله‌ی دسته بندی نیز در نظر گرفت. به این صورت که عامل هوش مصنوعی باید قاب‌های مختلف موجود در تصویر را در دو گروه *چهره* و *غیرچهره* در نظر گرفت.

المان‌های مختلفی را می‌توان در ارزیابی یک سیستم تشخیص چهره مؤثر دانست مانند زمان یادگیری، زمان اجرا، تعداد مثال‌های مورد نیاز برای یادگیری و نسبت بین میزان تشخیص و خطای منفی.
*میزان تشخیص* را می‌توان به نسبت تعداد چهره‌های درست تشخیص داده شده توسط عامل هوش مصنوعی به تعداد چهره‌های تشخیص داده شده توسط انسان تعریف کرد.
در صورتی قابی توسط عامل تشخیص داده شده است به عنوان چهره در نظر گرفته می‌شود که قاب مورد نظر بیشتر از میزان خاصی از چهره‌ی فرد را پوشش دهد.
از طرف دیگر *خطای منفی* زمانی رخ می‌دهد که عامل در تشخیص چهره ناموفق باشد که این خود ریشه در پایین بودن *میزان تشخیص* خواهد بود. در مقابل *خطای منفی* مفهوم دیگری به نام *خطای مثبت* وجود دارد که وقتی قابی به عنوان چهره از طرف عامل هوش‌ مصنوعی معرفی می‌شود اما عامل انسانی تایید نمی‌کند، رخ می‌دهد.

detection rate = correctyle detected / determined by hum

نکته‌ی مهم در رابطه با *خطای منفی* یا *خطای مثبت* این است که هر چه قوانین پیاده‌سازی شده سخت‌تر و به واسطه‌ی آن رفتار عامل سخت‌گیرانه تر باشد *خطای منفی* بالاتر و *خطای مثبت* پایین‌تر خواهد بود و بالعکس.
<!--
پس برای این‌که وجود روش *مکان‌یابی چهره* بی‌معنی جلوه نکند این‌گونه در نظر بگیرید که که در تشخیص چهره پنجره‌های ممکن روی تصویر اعمال می‌شود و با استفاده از روش‌های *مکان‌یابی چهره* می‌توان تشخیص داد که در آن ناحیه چهره‌ای موجود است یا خیر؟ مساله‌ی دیگری که وجود دارد *تشخیص اجزای صورت* خواهد بود که هدف از آن به‌دست آوردن جوابی برای وجود یا عدم وجود و مکان اجزای مختلف صورت از جمله چشم‌ها، لب‌ و ... خواهد بود.
-->

## روش‌های موجود
روش‌های موجود در تشخیص چهره را می‌توان به چهار گروه مختلف تقسیم کرد:

1. **روش‌های دانش‌ محور**
2. **روش‌های جزئیات محور**
3. **روش‌های الگو محور**
4. **روش‌های ظاهر محور**

### روش‌های دانش محور
مشکل اساسی در این روش پیاده‌سازی دانش انسانی خواهد بود. از طرف دیگر عمل‌کرد این نوع عامل‌ها در تشخیص چهره بسیار خوب بوده است.

یکی از استراتژی‌های جالب توجه در این روش استفاده از الگوریتم‌های ابتکاری خواهد بود. بدین صورت که ابتدا با اعمال بعضی قوانین ساده‌تر بر روی تصویر با کیفیت پایین‌تر به راحتی تعداد زیادی از قاب‌ها را حذف کرده و در مراحل بعدی با اعمال قوانین سخت‌گیرانه‌تر قاب‌های باقی‌مانده را فیلتر کرد. در پایان هر کدام از قاب‌ها که همه‌ی قوانین را پشت سر گذاشته است به عنوان چهره تشخیص داده می‌شود.

<img src="http://cesaserver.iust.ac.ir:7000/public.php?service=files&t=84640ecf3af587a24c981dd955c3b232&download" style="width:250px;-webkit-border-radius:20px;-moz-border-radius: 20px;border-radius: 20px;  box-shadow: 0px 0px 7px 1px #202020;-webkit-box-shadow: 0px 0px 7px 1px #202020;-moz-box-shadow: 0px 0px 7px 1px #202020;" alt="Knowledge-based Methods" >

یک تصویر مورد استفاده در روش‌های بالا-به-پایین دانش محور تولید شده بر اساس دانش انسانی درباره خصوصیات چهره انسان.بر گرفته از **[4]**

### روش‌های جزئیات محور
برعکس روش دانش‌ محور محققان در این روش به دنبال یافتن اجزای مختلف صورت برای تشخیص چهره خواهند بود.
فرض بنیادین در این روش این مشاهده بوده که انسان بدون دشواری در زوایای مختلف چهره و شرایط نوری متفاوت می‌تواند به‌راحتی چهره را تشخیص دهد.
اجزای مختلف چهره مانند ابروها، چشم‌ها، بینی و دهان براحتی توسط آشکارساز لبه استخراج می‌شوند. بر اساس اجزای استخراج شده مدلی آماری از رابطه‌ی اجزای صورت با هم ساخته می‌شود تا در تأیید وجود چهره مورد‌ استفاده قرار گیرد.

یکی از مشکلات این نوع روش‌ها این است که تصویر اجزای مختلف صورت بخاطر شرایط نوری نامناسب، نویز و یا پوشش خراب شود. وجود این مشکل احتمال بروز این مسأله که مرز‌های اجزای صورت از دست برود و یا بخاطر ایجاد سایه‌های زیاد الگوریتم بی‌فایده گردد را نیز افزایش می‌دهد.

### روش‌های الگو محور
در روش الگو محور الگوی استانداردی از چهره‌ی انسان به صورت دستی و یا به صورت تابعی ریاضی از پیش تعیین گردد.با دریافت تصویر ورودی، همبستگی میان تصویر در مرزهای صورت، چشم‌ها و.. با الگو بدست می‌آید. تصمیم نهایی در خصوص تشخیص تصویر بر اساس مقدار همبستگی خواهد بود.

اگر چه این روش به راحتی قابلیت پیاده سازی دارد اما از آنجایی که در مصاف با تصاویر با مقیاس مختلف‌، زاویه چهره و اشکال متفاوت باز می‌ماند گزینه‌ی خوبی برای استفاده در مساله‌هایی که تصاویر چهره در آن در شرایط مختلف وجود دارد نخواهد بود.

<img src="http://cesaserver.iust.ac.ir:7000/public.php?service=files&t=36e20a132b37cbfe71a34213d32ee2bd&download" style="width:350px;-webkit-border-radius:20px;-moz-border-radius: 20px;border-radius: 20px;  box-shadow: 0px 0px 7px 1px #202020;-webkit-box-shadow: 0px 0px 7px 1px #202020;-moz-box-shadow: 0px 0px 7px 1px #202020;" alt="Template-based Methods">

الگوی نسبی تولید شده جهت تشخیص چهره (بر گرفته از **[5]**)

### روش‌های ظاهر محور
بر خلاف روش الگو محور که در آن الگوی مورد استفاده توسط گروهی متخصص تولید می‌گردد در روش ظاهر محور این الگو از آموزش عامل هوش مصنوعی بوسیله‌ی تعدادی مثال‌ از تصاویر چهره حاصل می‌شود. به طور معمول روش‌های ظاهر محور بر اساس آنالیز آماری و یادگیری ماشین استوار است. در همین حال از کاهش کیفیت تصاویر نیز در جهت بهبود عملکرد محاسباتی استفاده می‌شود.

# کارهای مرتبط
وایولا و جونز در **[2]** روشی برای حل مسأله تشخیص اشیاء مبتنی بر یادگیری ماشینی را معرفی کرده‌اند که قادر به پردازش سریع تصاویر با میزان نشخیص بالا خواهد بود.

<!--
# آزمایش‌ها
-->
# کارهای آینده
هدف این پروژه در فاز بعدی پیاده‌سازی روش ارائه شده توسط **[2]** خواهد بود.

# مراجع
+ **[1]** D. A. Forsyth and J. Ponce, Computer Vision: A Modern Approach, 2nd ed. .
+ **[2]** P. Viola and M. Jones, “Rapid object detection using a boosted cascade of simple features,” Proc. 2001 IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recognition. CVPR 2001, vol. 1, 2001.
+ **[3]** M.-H. Y. M.-H. Yang, D. J. Kriegman, and N. Ahuja, “Detecting faces in images: a survey,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 24, no. 1, pp. 34–58, 2002.
+ **[4]** G. Yang and T. S. Huang, “Human Face Detection in Complex Background,” Pattern Recognition, vol. 27, no. 1, pp. 53-63, 1994.
+ **[5]** B. Scassellati,“EyeFindingvia Face Detection for a Foevated, Active Vision System,” Proc. 15th Nat’l Conf. Artificial Intelligence, 1998.

# پیوندهای مفید #
+ [کتابخانه اپن‌سی‌وی](http://opencv.org)
+ [تشخیص چهره انسان در اپن‌سی‌وی](http://docs.opencv.org/trunk/doc/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html)
+ [اپن‌سی‌وی در پایتون](http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html)
+ [نصب اپن‌سی‌وی در ابونتو](https://help.ubuntu.com/community/OpenCV)
+ [شناسایی اجسام در تصاویر با اپن‌سی‌وی](http://note.sonots.com/SciSoftware/haartraining.html)
+ [مهم‌ترین مقاله در این زمینه](https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf)
+ [بینایی کامپیوتری در جاوااسکریپت](http://inspirit.github.io/jsfeat/)
+ [تشخیص چهره در جاوااسکریپت ۱](http://inspirit.github.io/jsfeat/#haar)
+ [تشخیص چهره در جاوااسکریپت ۲](http://inspirit.github.io/jsfeat/#bbf)
