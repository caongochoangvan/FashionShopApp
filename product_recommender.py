import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]

df = pd.read_csv("products_data.csv")
# print(df.columns)

features = ['title', 'description', 'brand', 'tags']
# df['combined_tags'] = ' '.join(word for word in df['tags'])
# from ast import literal_eval
# def combined_tags(r):
#     return ' '.join(word for word in literal_eval(r['tags']))
# df['combined_tags'] = df.apply(combined_tags, axis = 1)
# def combine_features(r):
#     return r['title'] + ' ' + r['description'] + ' ' + r['brand'] + ' ' + r['tags']
# df['combined_features'] = df.apply(combine_features, axis = 1)
# df.to_csv('products_data.csv', index = False)
# print(df['combined_features'])
def recommender(index):
    cv = CountVectorizer()

    count_matrix = cv.fit_transform(df['combined_features'])

    cosine_sim = cosine_similarity(count_matrix)
    # print(cosine_sim)

    # product_user_choose = input('type the product')

    similar_products = list(enumerate(cosine_sim[index]))
    sorted_similar_products = sorted(similar_products, key = lambda x:x[1], reverse = True)
    # print(sorted_similar_products)
    i = 1
    index_of_similar_products = []
    for j in sorted_similar_products:
        # print(j[0])
        if i < 6 and i > 1:
            index_of_similar_products.append(j[0])
        i+=1
    # print(index_of_similar_products)
    return index_of_similar_products
# print("inside", recommender(1))


