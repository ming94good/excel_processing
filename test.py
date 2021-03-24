import requests
import pandas as pd
import json
import sqlite3
import xlwt 
from xlwt import Workbook
import pymongo
def insert(user_id, recommend):
    if(count(user_id) > 0):
        for r in recommend:
            update(user_id, r)
    else:
        d={'user_id': user_id, 'recommend': recommend}
        return col.insert_one(d)
def count(user_id):
    return col.count_documents({"user_id": user_id})
def update(user_id, recommend):
    query = { "user_id": user_id}
    newvalues = { "$push": { "recommend": recommend } }
    return col.update_one(query, newvalues)
def search(user_id):
    query = { "user_id": user_id}
    return col.find(query)
def recommend(user_id):
    for x in search(user_id):
        return x['recommend']
def delete(user_id):
    query = { "user_id": user_id}
    return col.delete_many(query)
def vtv(video_id):
    conn = sqlite3.connect('model_info.db')
    sql_cmd = f"SELECT recommended_videos FROM recommended_videos where video_id={video_id}"
    cur = conn.cursor()
    cur.execute(sql_cmd)
    videos = cur.fetchone()
    videos = [int(video) for video in videos[0].split(",")][:50]
    conn.close()
    return videos

df = pd.read_csv("test_watch_log.csv")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
col = mydb["recommend"]

c=0
d=0

wb = Workbook()
sheet = wb.add_sheet('video_recommend') 
sheet.write(0,0,'user_id')
sheet.write(0,1,'video_id')
sheet.write(0,2,'video is in recommend list')
sheet.write(0,3,'True')
sheet.write(0,4,'False')
sheet.write(0,5,'Accuracy')
for index, row in df.iterrows():
    try:
        recommend_num = 50
        rmd = vtv(str(row['video_id']))
        id = int(row['user_id'])

        recommend_list = recommend(id)
        rst = '#'
        if recommend_list:
            if row['video_id'] in recommend_list:
                c+=1
                rst = 'True'
            else:
                d+=1
                rst = 'False'
        insert(id,rmd)
        
        sheet.write(index+1,0,str(row['user_id']))
        sheet.write(index+1,1,str(row['video_id']))
        sheet.write(index+1,2,str(rst))
    except Exception as e:
        print(e)
        continue

    print(index)
    
sheet.write(1,4,str(c))
sheet.write(1,5,str(d))
sheet.write(1,6,str(c/ (c+d)))
wb.save('result.xls')
print(c)
print(d)
print(index)
print(c/ (c+d))