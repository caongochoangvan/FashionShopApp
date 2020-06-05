import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
source = requests.get('https://us.shein.com/trends/Casual-Wear-sc-00621943.html?icn=trends&ici=us_tab01navbar03banner03&adp=951847&srctype=category&userpath=category%3EWOMEN%3E#SHEINathome%3ECasual-Wear&scici=navbar_2~~tab01navbar03banner03~~3_3~~itemPicking_00621943~~~~0~~0').text

soup = BeautifulSoup(source,'lxml')
products = soup.find_all('a', class_ = 'c-goodsitem__goods-name she-visibility0')
print(products)
i = 0
women_clothing = []
for product in products[0:16]:
    print(i)
    words = re.findall(r'\w+',product.text)
    women_clothing.append(' '.join(word for word in words))
    i = i + 1
# print(women_clothing)
title = pd.Series(women_clothing)
print(title)
df = pd.read_csv('index_data.csv')
df['title'] = title
df['description'] = 'Dress for women'
imgs = []
for i in range(1,16):
    img = 'image-'+str(i)+'.jpg'
    imgs.append(img)
# print(imgs)
df['image_file'] = imgs
print(df)

df.to_csv('index_data.csv', index = False)

