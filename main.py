import requests
import pandas as pd
import json
import sqlite3
import xlwt 
from xlwt import Workbook

def create_table(): 
    conn = sqlite3.connect('video.db') 
    c = conn.cursor() 
    c.execute('CREATE TABLE IF NOT EXISTS video (id INT, name TEXT, category TEXT)') 
    c.close() 
    conn.close() 
def data_entry(id,name,category): 
    conn = sqlite3.connect('video.db') 
    c = conn.cursor() 
    c.execute("INSERT INTO video (id, name, category) VALUES(?, ?, ?)", (id, name,category)) 
    c.close() 
    conn.commit() 
    conn.close() 
def select_all_video():
    conn = sqlite3.connect('video.db') 
    cur = conn.cursor()
    cur.execute("SELECT * FROM video")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for row in rows:
        print(row)
def search_video(id):
    conn = sqlite3.connect('video.db') 
    cur = conn.cursor()
    cur.execute("SELECT * FROM video WHERE id = "+ str(id))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

col_list = ["id", "name_tc", "category"]
df = pd.read_csv("video.csv", usecols=col_list)
data = {}
data['vtv'] = []
create_table() 
for index, row in df.iterrows():
    data_entry(row['id'],row['name_tc'],row['category'])

wb = Workbook()
sheet = wb.add_sheet('video_recommend') 
sheet.write(0,0,'video_id')
sheet.write(0,1,'name')
sheet.write(0,2,'category')
for i in range(3,53):
    sheet.write(0,i,'recommend'+ str(i-2))
for index, row in df.iterrows():
    #print(row['id'])
    # do recommend
    recommend_num = 50
    result = requests.get('http://localhost:5000/video_id_to_video?video_id=' \
                          + str(row['id']) +'&nums=' + str(recommend_num))
    r = json.loads(result.text)
    sheet.write(index+1,0,row['id'])
    sheet.write(index+1,1,row['name_tc'])
    sheet.write(index+1,2,row['category'])
    for i in range(3,53):
        r_id = r['videos_id'][i-3]
        sheet.write(index+1, i, str(search_video(r_id)))
wb.save('result.xls')