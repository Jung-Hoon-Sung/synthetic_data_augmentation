from PIL import Image
import os.path
targerdir = "/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/SOD_result/"
files = os.listdir(targerdir)
format = [".jpg",".png",".jpeg","bmp",".JPG",".PNG","JPEG","BMP"]
files = os.listdir(targerdir)

for (path,dirs,files) in os.walk(targerdir):
    for file in files:
        if file.endswith(tuple(format)):
            image = Image.open(path+"/"+file)
            image.size
            image.getbbox()
            im = image.crop(image.getbbox())
            im.size
            im.save(path+"/"+file)