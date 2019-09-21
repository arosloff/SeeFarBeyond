from PIL import Image
from resizeimage import resizeimage

with open('coins_close1.jpg','r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_width(image,200)
        image.save('test_coins.jpg',image.format)
        f.close()
