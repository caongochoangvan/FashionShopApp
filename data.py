import os
basepath = "fashionshop\static\img\product"
from fashionshop import db
from fashionshop.models import *
import random
for folder in os.listdir(basepath):
    category = Category(name = folder)
    db.session.add(category)
    db.commit()
    print(folder)
    for img in os.listdir(os.path.join(basepath, folder)):
        text =img.split()
        text = ' '.join([w for w in text[:-1]])
        product = Product(title = text, description = 'Best sales of ' + folder + 'category!', img_file = img, type = category, price = random.randint(100, 1000))
        db.session.add(product)
        db.commit()
import os
            

