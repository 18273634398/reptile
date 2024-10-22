# ===========================================================================================================
# Author    ：LuShangWu
# Date      ：2024-10-20
# Version   ：1
# Description：用于爬取hao网站的问诊记录的链接并保存到本地
# Copyright  ：LuShangWu
# License   ：MIT
# ===========================================================================================================
import requests
from bs4 import BeautifulSoup
from getDetailRecord import getDetailRecord
import random
import time


def getMedicalRecords(url,infoIndex,cursor,connetion):
    print("【Get Medical Records】"+url)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "g=77490_1728828402072; g=HDF.114.670bd3f219434; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1728828403,1729422262; HMACCOUNT=50BB06D570729B92; acw_tc=71dbc9a417294241024417056e7022928533552f083577bb054f2b55ec; acw_sc__v3=6714eaf93d7bbe38d6ad01bb1fabd32be56c0971; tfstk=grHmAbaQAjPXKlf753yXsEfrv0O8hiw_vVBTWRUwazz5kZBxbG2iz2lT_EwxI40IPxBTH53u4krT0NWa087zvztsDcHYSG0KyqFZBPHMj-M-MOUvlRmZJRYpJppKcmN_QeLLzr51gJrLbi7T__rzCgFDMMpKcmsPmN-KapQgDZyZ_Puag8SzczW47VPVa3qaXZ5N3VoyqzZOQozN377zxlEaQRuZ43qsMpO4-floUEtwsCQaFWkumS4E4B6NIsqVJym2mOXZEDN08d4lQOkum0Ew61XH6ylQkWUSzLB0I0ri-k0czU2ZqxM3ax85I20oT8qSNFfg-foxOfPk0KounrVne7IVs-cZlAVjiGtI4-uSOyN2NUZoHvFgR7byu0nuuWcikU6akXmrrWHRy9erYb2l4Y1PTvghCu-tU11_guZuJX7sLGtwpedDq3fBfSr7cHKkq1sbguZuJ3xlOEN4Votd.; acw_sc__v2=6714eb80c3d57fab354bd2a31e8ccdc9b6978fe6; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1729424345",
        "if-none-match": "W/\"9cf1-MgTWDJYnBNmzd5rnfPkYD/E8Sv8\"",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }
    response = requests.get(url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup解析HTML代码

    all_links = []
    # 找到所有的问诊记录
    records = soup.find_all('a', attrs={'class':'fl'})
    for record in records:
        all_links.append(record['href'])
        # time.sleep(5+random.randint(0,60))
        getDetailRecord(record['href'],infoIndex,cursor,connetion)
        infoIndex+=1
        time.sleep(5+random.randint(1,10))