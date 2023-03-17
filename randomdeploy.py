import cv2
# import matplotlib.pyplot as plt
import os
import numpy as np
import glob
import random
from PIL import Image, ImageFilter
import numpy as np

person_list = glob.glob("/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/shadow_result/*")
img_list = glob.glob("/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/synthetic_result/*")

# len(img_list)):
for i in range(0, len(img_list)):
    img_name = img_list[i].split("road_background")[-1]
    img_name = img_name[1:]
    print(img_name)
    background = Image.open(img_list[i]).convert('RGBA')
    # background = cv2.resize(background, dsize=(1920, 1080))
    n = random.randint(0, len(person_list) - 1)
    ## for
    person = Image.open(person_list[n]).convert('RGBA')
    background_height, background_width = background.size
    person = person.resize((int(person.width / 4), int(person.height / 4)), Image.ANTIALIAS) #전경 객체 스케일 조정
    person_height, person_width = person.size
    # person_x, person_y = random.randint(0, 1920), random.randint(0, 1080)
    person_x, person_y = random.randint(500, 1500), random.randint(300, 1000)
    # person = person.resize((int(person.width / 13), int(person.height / 13)))
    tmp_img = Image.new('RGBA', background.size, color=(0, 0, 0, 0))
    # person = person.filter(ImageFilter.GaussianBlur(0.8))
    tmp_img.paste(person, (person_x, person_y))
    background.alpha_composite(tmp_img)
    background = background.convert('RGB')
    num_img = np.array(background)
    print(num_img)

    x_min = person_x
    y_min = person_y
    x_max = person_x + person_height
    y_max = person_y + person_width

    center_x = round(((x_min + x_max) / 2.0) / background_height, 3)
    center_y = round(((y_min + y_max) / 2.0) / background_width, 3)
    w = round((x_max - x_min) / background_height, 3)
    h = round((y_max - y_min) / background_width, 3)

    label = 0
    line = "0" + " " + str(center_x) + " " + str(center_y) + " " + str(w) + " " + str(h)
    # background.show()
    print(img_name)
    background.save("/" + img_name)
    # img_path = "C:/Users/jh397/sjh/Dropshadow/results/" + img_name
    # txt_path = img_path.replace("results","annotation").replace("png","txt")
    txt_path = "/" + img_name.replace("jpg", "txt")
    with open(txt_path, "w") as file:
        file.write(line)
    # with open("C:/Users/jh397/sjh/Dropshadow/results/.txt", "w") as file:
    # background.save("C:/Users/jh397/sjh/Dropshadow/results/" + img_name)

    # txt_path = img_list[i].replace(img_list[i].split(".")[-1], "txt")




