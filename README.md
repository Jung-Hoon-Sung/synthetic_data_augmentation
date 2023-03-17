1. Separating foreground and background through salient object detection:

(1) Go to the "rembg" folder.

(2) Install rembg by typing "pip install rembg" (Python version = 3.8).

(3) Install required packages by typing "pip install -r requirements.txt".

(4) Run "rembg.py" by typing "rembg -p /input/path /output/path" command.

2. Cropping for auto labeling:

(1) Work on "image_crop_boxsize.py".

(2) Set the input and output paths for the images.

(3) Run "image_crop_boxsize.py".

3. Creating shadows:

(1) Work on "Make shadow.py".

(2) Set the input and output paths for the images, which are the outputs of step 2.

(3) Run "Make shadow.py".

4. Cutting out the background:

(1) Work on "cutout_background.py".

(2) Set the input and output paths for the images (input: ./test_Sample_image/background/, output: ./test_Sample_image/background_cutout_result/).

(3) Run "cutout_background.py". (Note: The background images to be cut out and the label values must exist in the designated path.)

5. Compositing refined foreground mask and background images:

(1) Work on "randomdeploy.py".

(2) Install OpenCV-Python by typing "pip install opencv-python".

(3) Set the output image of step 3 as the foreground object and the output image of step 4 as the background image. Set the output path for the resulting image (and an additional path to save the bounding box labels).

(4) Rescale the image of step 3 as a parameter for composition.

(5) Run "randomdeploy.py".





