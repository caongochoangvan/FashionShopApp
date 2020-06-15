# Test for search function 
import csv
# data_list = [["id","title","description","price","image_file","type"],
#              [1,"Shirt 1", "Shirt for men",11, 'img-1.jpg',"Women"], 
#              [2,"Shirt 2", "Shirt for men",12, 'img-1.jpg',"Women"],
#              [3,"Shirt 3", "Shirt for men",13, 'img-1.jpg',"Women"],
#              [4,"Shirt 4", "Shirt for men",14, 'img-1.jpg',"Women"],
#              [5,"Shirt 5", "Shirt for men",15, 'img-1.jpg',"Women"],
#              [6,"Shirt 6", "Shirt for men",16, 'img-1.jpg',"Women"],
#              [7,"Shirt 7", "Shirt for men",17, 'img-1.jpg',"Women"],
#              [8,"Shirt 8", "Shirt for men",18, 'img-1.jpg',"Women"],
#              [9,"Shirt 9", "Shirt for men",19, 'img-1.jpg',"Women"],
#              [10,"Shirt 10", "Shirt for men",110, 'img-1.jpg',"Women"],
#              [11,"Shirt 11 ", "Shirt for men",111,  'img-1.jpg',"Women"],
#              [12,"Shirt 12", "Shirt for men",112, 'img-1.jpg',"Women"],
#              [13,"Shirt 13", "Shirt for men",113, 'img-1.jpg',"Women"],
#              [14,"Shirt 14", "Shirt for men",114, 'img-1.jpg',"Women"],
#              [15,"Shirt 15", "Shirt for men",115, 'img-1.jpg',"Women"], 
#             ]
# with open('index_data.csv','w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(data_list)
import os
import pandas as pd
from fashionshop import es
# from fashionshop import es
import requests
csv_file = pd.read_csv('products_data.csv')
search_file = pd.concat([csv_file['title'], csv_file['description']], axis = 1)
print(search_file)
# r = requests.get('http://localhost:9200')
# print(r.content)

index_name = 'fashionshop'
doc_type = 'product'
for i, t in enumerate(search_file['title']):
    # print(i,t)
    s = es.index(index = index_name, doc_type = doc_type, id = i, body = {'title': t})
    print(s)
product = es.get(index= index_name, doc_type = doc_type, id = 10)
print(product)
query = es.search(index = index_name, body={'query':{'match': {'title':'1'}}})
print(query['hits']['total'])
print(query['hits']['hits'])