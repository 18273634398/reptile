# ===========================================================================================================
# Author    ：LuShangWu
# Date      ：2024-10-20
# Version   ：1.0
# Description：用于爬取hao网站科室信息
# Copyright  ：LuShangWu
# License   ：MIT
# ===========================================================================================================

import requests
from bs4 import BeautifulSoup
from getMedicalRecords import getMedicalRecords


def getDepartment(infoIndex,cursor,connection):
    url = "https://www.haodf.com/bingcheng/list.html"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "g=77490_1728828402072; g=HDF.114.670bd3f219434; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1728828403,1729422262; HMACCOUNT=50BB06D570729B92; acw_tc=71dbc9a417294241024417056e7022928533552f083577bb054f2b55ec; acw_sc__v3=6714eaf93d7bbe38d6ad01bb1fabd32be56c0971; tfstk=grHmAbaQAjPXKlf753yXsEfrv0O8hiw_vVBTWRUwazz5kZBxbG2iz2lT_EwxI40IPxBTH53u4krT0NWa087zvztsDcHYSG0KyqFZBPHMj-M-MOUvlRmZJRYpJppKcmN_QeLLzr51gJrLbi7T__rzCgFDMMpKcmsPmN-KapQgDZyZ_Puag8SzczW47VPVa3qaXZ5N3VoyqzZOQozN377zxlEaQRuZ43qsMpO4-floUEtwsCQaFWkumS4E4B6NIsqVJym2mOXZEDN08d4lQOkum0Ew61XH6ylQkWUSzLB0I0ri-k0czU2ZqxM3ax85I20oT8qSNFfg-foxOfPk0KounrVne7IVs-cZlAVjiGtI4-uSOyN2NUZoHvFgR7byu0nuuWcikU6akXmrrWHRy9erYb2l4Y1PTvghCu-tU11_guZuJX7sLGtwpedDq3fBfSr7cHKkq1sbguZuJ3xlOEN4Votd.; acw_sc__v2=6714eb6a2fb6b5802f8074649fff56f926b4c1f8; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1729424673",
        "priority": "u=0, i",
        "referer": "https://www.haodf.com/bingcheng/list-xinxueguanneike.html",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }
    response = requests.get(url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup解析HTML代码

    # 找到所有的科室信息
    departments = soup.find_all('li', attrs={'class':'izixun-department-list'})

    if not departments:
        print("没有找到科室信息，请检查网址是否正确或可能网站已更新防爬技术")
    else:
        all_departments = {}
        print("科室信息如下：")
        index = 1
        for department in departments:
            # 科室信息转化为字符串方便处理
            department = str(department)

            # 解析HTML代码 获取科室信息
            startInfo = "'<li class=\"izixun-department-list\">'"
            endInfo = "</li>"
            department_index_start = department.find(startInfo)  # 找到科室信息的开始位置
            start_string_length = len(startInfo)
            department_index_end = department.find(endInfo)  # 找到科室信息的结束位置
            department_info = department[department_index_start+start_string_length:department_index_end]

            # 解析科室信息
            for line in department_info.splitlines():
                index_start_1=line.find('"//')+3
                index_end_1=line.find('">')
                index_start_2=line.find('">')+2
                index_end_2=line.find('</a>')
                index+=1
                # 获取与处理科室链接
                link = line[index_start_1:index_end_1]
                link = "https://"+link
                # 获取科室姓名
                name = line[index_start_2:index_end_2]
                # 保存科室信息到字典
                all_departments[name] = link
                # 打印科室信息
                print(f"{index}. {name}, 链接: {link}")
                getMedicalRecords(link,infoIndex,cursor,connection)

