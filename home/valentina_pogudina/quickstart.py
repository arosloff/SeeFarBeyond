#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from PIL import Image

coin = [0.01, 0.05, 0.1, 0.25, 1, 1, 1, 1]
f_name = ['c1.jpg', 'c5.jpg', 'c10.jpg', 'c25.jpg', 'c100.jpg', 'test.jpg', 'test1.jpg', 'test2.jpg']
spoon_px = 0
spoon_in = 2.85
ratio = 0
denom = int(sys.argv[1]);

def run_quickstart():
    # [START vision_quickstart]
    import io
    import os
    from resizeimage import resizeimage
    fname = '/var/www/hope2/upload/'+f_name[denom]
    
    im = Image.open(fname)
    width, height = im.size


    new_w = 400
    new_h = new_w * height/ width
    with open(fname,'r+b') as f:
        with Image.open(f) as image:
            image = image.resize((new_w,new_h),Image.ANTIALIAS)
    image.save(fname,image.format)
       
    # Imports the Google Cloud client library
    # [START vision_python_migration_import]
    from google.cloud import vision
    from google.cloud.vision import types
    # [END vision_python_migration_import]

    # Instantiates a client
    # [START vision_python_migration_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_python_migration_client]

    # The name of the image file to annotate
    #file_name = os.path.abspath('resources/q4.jpg')
    file_name = os.path.abspath(fname)
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

    localize_objects(file_name)

    # [END vision_quickstart]
def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    from PIL import Image
    im = Image.open(path)
    width, height = im.size

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
     
    objects = client.object_localization(
    image=image).localized_object_annotations
    import numpy as np

    print('Number of objects found: {}'.format(len(objects)))
    #obj = np.zeros(len(objects))
    obj = []
    ref = []
    ref.append([])
    i = 0
    ccount = 0
    a = 0
    b = 0

    for ob_ in objects:
        if ob_.name == "Coin":
            ccount += 1
    print("Coins: " + str(ccount))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        
        print('Normalized bounding polygon vertices: ')
        if object_.name == "Coin":
            obj.append([])
        sp = 0
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
            print('Index: '+str(i))
            if object_.name == "Coin":
                obj[i].append((vertex.x*width, vertex.y*height))
            
            if object_.name == "Spoon":
                ref[0].append((vertex.x*width, vertex.y*height))
                if sp == 0:
                    a = vertex.x*width
                if sp == 1:
                    b = vertex.x*width
                sp += 1
        if object_.name == "Coin":
            i = i+1
    spoon_px = int(b - a)
    print("Spoon size in px: "+ str(b-a))
    show_objects(path,obj,ccount,ref, spoon_px)

def determine_coin(le, spoon_px):
    min = 100
    lpx = le / spoon_px
    if (abs(le / 60 - spoon_px / 201) < min):
        min = abs(le / 60 - spoon_px / 201)
    if (abs(le / 55 - spoon_px / 201) < min):
        min = abs(le / 55 - spoon_px / 201)
    if (abs(le / 63 - spoon_px / 201) < min):
        min = abs(le / 63 - spoon_px / 201)
    if (abs(le / 70 - spoon_px / 201) < min):
        min = abs(le / 70 - spoon_px / 201)
    if (abs(le / 60 - spoon_px / 201) == min):
        return 60
    if (abs(le / 55 - spoon_px / 201) == min):
        return 55
    if (abs(le / 63 - spoon_px / 201) == min):
        return 63
    if (abs(le / 70 - spoon_px / 201) == min):
        return 70


def show_objects(path,obj,ccount,ref, spoon_px):
    #if sys.version_info[0] == 3:

    #else:
    # for Python2
    #import Tkinter as tk ## notice capitalized T in Tkinter
    #from PIL import ImageTk, Image, ImageDraw
    #image_window = tk.Tk()
    #img = ImageTk.PhotoImage(Image.open(path))
    #panel = tk.Label(image_window, image=img)
    #panel.pack(side="bottom", fill="both", expand="yes")
    #x = [10,30,70]
    #y = [15,45,90]
    #img2 = img
    #draw = ImageDraw.Draw(img2)
    #draw.polygon(zip(x,y), fill = "wheat")
    #image3 = Image.blend(img,img2,0.5)
    #image3.save('out.png')
    #image_window.mainloop()
    #xy=[(0.391171455383,0.319341510534),(0.547501385212,0.319341510534),(0.547501385212,0.436120271683),(0.391171455383,0.436120271683)]
    #xy=[1,2,4,2,4,1,1,1]
    #img.Draw.polygon(xy,fill="red",outline="red")
    #with Image.open(path) as img:
     #   img.show()
    import PIL.ImageDraw as ImageDraw
    import PIL.Image as Image
    import PIL.ImageFont as ImageFont

    
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",40)


    image = Image.open(path)
    width,height = image.size
    print("Width and height: ")
    print(width, height)
    draw = ImageDraw.Draw(image)
    print("Here is first list")
    print(obj[0])
    points = ((100,100), (200,100), (200,200), (100,200), (50,150))
    new_w = 400
    new_h = new_w * height / width
    c60 = 0
    c63 = 0
    c70 = 0
    c55 = 0
    my_coins = [0,0,0,0,0]
    
    ratio = spoon_px / spoon_in

#    if ratio != 0:
#        c0 = 
#        c1 = 
#        c2 = 
##        c3 = 
 #       c4 = 
    #image = image.resize((new_w,new_h),Image.ANTIALIAS)
    for i in range (ccount):
        draw.polygon(obj[i],fill=None, outline="red")
        le = obj[i][1][0] - obj[i][0][0]
        ple = determine_coin(le, spoon_px)
        print("=======")
 #       print(spoon_px)
 #       print(1.0 * spoon_px / 201)
#        print(le / 70)
        le = spoon_px * le / 201
        #le = int(le)

#        if (abs(1 - le/60) < 0.01):
#            c60 = c60 + 1
#            my_coins[0] += 1
#            print("=== 60")
#        elif (abs(1 - le/63) < 0.01):
#            c63 = c63 + 1
#            my_coins[1] += 1
#            print("=== 63")
#        elif (abs(1 - le/70) < 0.01):
#            c70 = c70 + 1
#            my_coins[3] += 1
#            print("=== 70")
#        elif (abs(1 - le/55) < 0.01):
#            c55 = c55 + 1
#            print("=== 55")
#            my_coins[2] += 1
#        else:
#            print("ERROR")
        le = ple
        if (int(le) == 60):
            c60 = c60 + 1
            my_coins[0] += 1
            print("=== 60")
        elif (int(le) == 63):
            c63 = c63 + 1
            my_coins[1] += 1
            print("=== 63")
        elif (int(le) == 70):
            c70 = c70 + 1
            my_coins[3] += 1
            print("=== 70")
        elif (int(le) == 55):
            c55 = c55 + 1
            print("=== 55")
            my_coins[2] += 1
        else:
            print("ERROR")
        print(le)
    #coin = 0.25
    #coin = 0.01
    if spoon_px != 0:
        draw.polygon(ref[0],fill=None, outline="blue")
    amount = 0
    for i in range (5):
        amount += my_coins[i]*coin[i]
    if spoon_px == 0:
        amount = coin[denom] * ccount
    #amount = coin[denom]*ccount
    #draw.textsize('$'+str(amount),font = font)
    draw.text((20,20),'Total: $ '+str(amount),font=font,fill=(45,90,60,255))
    #image = image.resize((new_w,new_h),Image.ANTIALIAS)
    
    image.show()

if __name__ == '__main__':
    run_quickstart()
