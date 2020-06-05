from PIL import Image
import os

basepath = 'fashionshop\static\img\product\Fragrance'
# os.chdir(basepath)
def save_img(img):
    i = Image.open(os.path.join(basepath,img))
    t, f_ext = os.path.splitext(i.filename)
    text = t.replace("-"," ")
    f = text + f_ext
    print('infor:',img, i.format, i.size, i.mode)
    if i.mode == 'RGBA':
        i = i.convert('RGB')
    output = (264,363)
    i.thumbnail(output, Image.ANTIALIAS)
    # i = i.resize(output, Image.ANTIALIAS)
    i.save(f, "JPEG")
    print('infor changed:',img, i.format, i.size, i.mode)
    pass

for img in os.listdir(basepath):
    save_img(img)
    