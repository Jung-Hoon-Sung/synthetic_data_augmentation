from PIL import Image, ImageFilter, ImageDraw
import os

PATH = "/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/SOD_result/"
Copy_to_path = "/home/sungjunghoon/synthetic_data_augmentation/test_Sample_image/shadow_result/"

# blur radius and diameter
# radius, diameter = 10, 20

for filename in os.listdir(PATH):
    image = Image.open(os.path.join(PATH, filename)) # images are color images
    # image= image.filter(EDGE_ENHANCE)
    # image.putalpha(180)
    wip_img = Image.new("RGBA", image.size, (0, 0, 0, 0))
    wip_img = wip_img.resize((int(wip_img.width), int(wip_img.height)))

    shadow = Image.new("RGBA", image.size, (0, 0, 0, 1))
    shadow = Image.new("RGBA", image.size, color="black")
    # shadow.putalpha(100) #opacity


    # distance
    image_coords = (0, 0)
    shadow_coords = (0, 0)

    wip_img.paste(shadow, shadow_coords, mask=image)
    # wip_img.save("Result.png", "PNG")
    wip_img = wip_img.filter(ImageFilter.GaussianBlur(20))
    # wip_img = wip_img.filter(ImageFilter.GaussianBlur(1))
    # wip_img.save("Result.png", "PNG")
    # wip_img.show()
    # wip_img = wip_img.resize((int(wip_img.width + 30), int(wip_img.height + 30))) # shadow resize
    # wip_img = wip_img.resize((int(wip_img.width + 1), int(wip_img.height + 1))) # shadow resize
    wip_img.paste(image, box=image_coords, mask=image)

    # wip_img = wip_img.convert("RGBA")

    pixdata = wip_img.load()

    width, height = wip_img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (0, 0, 0, 255)

    sharpened1 = wip_img.filter(ImageFilter.SHARPEN)
    wip_img = sharpened1.filter(ImageFilter.SHARPEN)
    wip_img = wip_img.filter(ImageFilter.BoxBlur(1.5))
    wip_img = wip_img.filter(ImageFilter.GaussianBlur(0.5))
    wip_img = wip_img.filter(ImageFilter.ModeFilter)
    wip_img.filter(ImageFilter.SMOOTH)
    wip_img.filter(ImageFilter.SMOOTH_MORE)
    # wip_img.putalpha(100)
    wip_img = wip_img.convert("RGBA")

    wip_img.save(Copy_to_path + filename + '.png')
    print(wip_img)

