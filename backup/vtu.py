import requests
import pandas as pd
import json
import sqlite3
import xlwt 
from xlwt import Workbook

col_list = ["user_id", "video_id"]
df = pd.read_csv("test_watch_log.csv", usecols=col_list)

wb = Workbook()
sheet = wb.add_sheet('video_recommend') 
sheet.write(0,0,'user_id')
sheet.write(0,1,'video_id')
sheet.write(0,2,'video recommend 500 users')
sheet.write(0,3,'user_is_in_list')

for index, row in df.iterrows():
    #print(row['id'])
    # do recommend
    recommend_num = 500
    result = requests.get('http://localhost:5000/video_id_to_user?video_id=' \
                          + str(row['video_id']) +'&nums=' + str(recommend_num))
    r = json.loads(result.text)

    sheet.write(index+1,0,str(row['user_id']))
    sheet.write(index+1,1,str(row['video_id']))
    sheet.write(index+1,2,str(r['users_id']))
    sheet.write(index+1,3,str(row['user_id']) in r['users_id'])
    print(str(row['user_id'])+' , '+ str(row['video_id']) + ' , ' + str(row['user_id']) in r['users_id'])
wb.save('result.xls')