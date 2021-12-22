import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sentence_transformers import SentenceTransformer
import mysql.connector
import random
from itertools import chain
import os.path
import re
BASE = os.path.dirname(os.path.abspath(__file__))
def get_Data():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="goodboy123",
      database="nexus360"
    )
    return pd.read_sql("SELECT * FROM nexus_360_news_post",mydb)


def get_embeddings():
    data=get_Data()
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    document_embeddings = sbert_model.encode(data["News_content"])
    np.save('embeddings.npy', cosine_similarity(document_embeddings))


def most_similar(doc_id,similarity_matrix,matrix):
    df=get_Data()
    similar_articles = []
    #print (f'Document: {df.iloc[doc_id]["ArticleId"]}')
    #print ('Top 10 Similar Documents:\n')
    if matrix=='Cosine Similarity':
        similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
    elif matrix=='Euclidean Distance':
        similar_ix=np.argsort(similarity_matrix[doc_id])
    for ix in similar_ix:
        if ix==doc_id:
            continue
        similar_articles.append({'id' : df.iloc[ix-1]["id"], 'Similarity Score' : similarity_matrix[doc_id][ix-1]})
    return similar_articles
def check_content_similarity(doc_id):
  document_embeddings = np.load((os.path.join(BASE, "embeddings.npy")))
  pairwise_similarities=cosine_similarity(document_embeddings)
  pairwise_differences=euclidean_distances(document_embeddings)
  result1 = sorted(most_similar(doc_id,pairwise_similarities,'Cosine Similarity'), key=lambda d: d['Similarity Score'], reverse=True)
  result2 = sorted(most_similar(doc_id,pairwise_differences,'Euclidean Distance'), key=lambda d: d['Similarity Score'], reverse=True)
  combine_value = []
  for i in range(0,len(result1)):
    for j in range(0,len(result2)):
      if(result1[i]["id"] == result2[j]["id"]):
        avg_score_combined = ((result1[i]["Similarity Score"]*100) + result2[i]["Similarity Score"])/2
        combine_value.append({'id' : result1[i]["id"], 'Similarity Score' : avg_score_combined})
  combine_value = sorted(combine_value, key=lambda d: d['Similarity Score'], reverse=True)
  return combine_value[:10]
def calculate_weights(session):
  weights = []
  for i in range(0,len(session)):
    current_res = check_content_similarity(session[i])
    temp = 0
    for j in range(0,len(current_res)):
      temp+=current_res[j]["Similarity Score"]
    temp = temp/len(current_res)
    if not weights:
      weights.append(temp)
    else:
      weights.append(temp+weights[i-1])
  return weights
def calculate_article_weights(current_res):
  weights = []
  temp = 0
  for i in range(0,len(current_res)):
    temp+=current_res[i]["Similarity Score"]
    if not weights:
      weights.append(temp)
    else:
      weights.append(temp+weights[i-1])
  return weights
def predictions(user_session):
  combine_predictions = []
  predict_values = []
  final_predictions = []
  c_weights = []
  prev_value = 0
  c_weights = calculate_weights(user_session)
  for i in range(0,len(user_session)):
    current_res = check_content_similarity(user_session[i])
    combine_predictions.append({'id' : user_session[i], 'Predictions': current_res})
    predict_values.append(random.choices(user_session, cum_weights=c_weights, k=1))
  predict_values = list(chain.from_iterable(predict_values))
  ac_weights = []
  for i in range(0,5):
    if i >= len(predict_values):
      i = 0
    for k in range(0,len(combine_predictions)):
      if(predict_values[i] == combine_predictions[k]["id"]):
        current_res_values = combine_predictions[k]["Predictions"]
        ac_weights = calculate_article_weights(current_res_values)
        temp_article_data = []
        for a in range(0,len(current_res_values)):
          temp_article_data.append(current_res_values[a]["id"])
        final_predictions.append(random.choices(temp_article_data, cum_weights=ac_weights, k=1))
  return list(chain.from_iterable(final_predictions))

def get_pred(user_session):
    pred=predictions(user_session)
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="goodboy123",
      database = "nexus360")
    mycursor = mydb.cursor()
    print(pred)
    headlines=[]
    for i in pred:
        mycursor.execute("SELECT title FROM nexus_360_news_post where id=" +str(i))
        myresult = mycursor.fetchall()
        string = re.sub("[()]","", str(myresult))
        headlines.append(string)
    print(headlines)
    return pred,list(chain.from_iterable(headlines))       
# most_similar(0,pairwise_similarities,'Cosine Similarity')