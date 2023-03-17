import cv2
import numpy as np
import os

def bg_ref_cutout(img, bb):
    copy = img.copy()

    p = bb.split(' ')

    x1 = (float(p[1]) - ((float(p[3])) / 2)) * image_w
    y1 = (float(p[2]) - ((float(p[4])) / 2)) * image_h
    x2 = (float(p[1]) + ((float(p[3])) / 2)) * image_w
    y2 = (float(p[2]) + ((float(p[4])) / 2)) * image_h

    obj = copy[int(y1):int(y2), int(x1):int(x2)]

    obj_h, obj_w = obj.shape[:2]

    ref_left = 0
    ref_top = 0

    while True:

        ref_left = np.random.randint(0, image_w - obj_w)
        ref_top = np.random.randint(0, image_h - obj_h)

        if not ((x1 - obj_w) < ref_left < (x2+obj_w) and (y1-obj_h) < ref_top < (y2+obj_h)):
            break


    copy[int(y1):int(y2), int(x1):int(x2)] = copy[ref_top : ref_top + obj_h, ref_left : ref_left + obj_w]

    return copy



if __name__ == '__main__':

    img_dir = os.path.join("/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/background/")
    img_list = os.listdir(img_dir)
    img_list.sort()

    label_dir = os.path.join("/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/background_label/")
    label_list = os.listdir(label_dir)
    label_list.sort()


    save_dir = os.path.join("/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/background/")

    for i, file_name in enumerate(img_list):
        image = cv2.imread(img_dir + file_name)

        image_h, image_w = image.shape[:2]

        f = open(label_dir + label_list[i], 'r')
        bb = f.readline()


        bg_ref_cutout_img = bg_ref_cutout(image, bb)
        save_dir2 = "/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/synthetic_result/"
        cv2.imwrite(save_dir2 + file_name.split('.')[0] + '_cutout_img.jpg', bg_ref_cutout_img)

