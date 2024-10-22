# ===========================================================================================================
# Author    ：LuShangWu
# Date      ：2024-10-22
# Version   ：1.0
# Description：利用上一级函数传递的URL获取指定医生的详细信息，并保存到本地数据库中
# Copyright  ：LuShangWu
# License   ：MIT
# ===========================================================================================================
import requests
from bs4 import BeautifulSoup

def getDoctorDetail(url,cursor,connection):
    url = url[:-5]+"/xinxi-jieshao.html"
    print(f"Getting doctor detail...[{url}]")
    headers={
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "g=77490_1728828402072; userinfo[id]=11039421678; userinfo[time]=1729473347; userinfo[hostid]=0; userinfo[key]=USxQYVdkAWFROFJsAjRSMl8wDTdSZQZtBy4Ab1BiXzQBYlFpVC9TZlo3Bm4BO1B0ByVSblpz; userinfo[ver]=1.0.2; userinfo[name]=hdf68ye7o8v; sdmsg=1; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1729422262,1729561346,1729563046,1729578457; HMACCOUNT=50BB06D570729B92; g=HDF.120.67169922aad24; tfstk=gCI-EmNb1SVo5kkqYXaD-C_ToK20jMBPh_WsxBAoRsCACOlkRM4P9pC9igAlE39d9666ZpxWFx6XUIyFE9jk9vCGi_YCxBjLp3ScrDAuaHBCsHFgslqGUT8eA5Vic3tYLh9-PpGHRjGXYo1xB3qGUTkjeXwGllcKZ6DORB1BPnMXCIiWO6TWh-pBKbgIV66bHIJnNXgWPEMXppOBAH1Ch-pETiDJGbOIvwkcglutjBoIAipJlrXWGvxAcLdy6Ts-ADM6eUd1FIFaL5o9l98dYvoprT_NTd1SN7KCHdC9B_UnLQQfIgbCeoF6qgW55es_T21926L1VEHIvT-k9npffJ0wiidlOgLbIcLHcGY6VZ44ZexJB6sPwvnC1tXG4ESL6jOFrd-Xe6Z_MgSPjGeQHfA9K4wYH2uePKu_JmcD4UqUAKdge43E8EV2HC2Y62uePKJvs8HK8280g; acw_tc=76fdae2617296037613805084e2e155a70f20bd1aad9c5e849f8da9671; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1729603766",
        "if-none-match": "W/\"85d2-n0i7O4efWSQdHI99BUn/6Q\"",
        "priority": "u=0, i",
        "referer": "https://www.haodf.com/doctor/5808.html",
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
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.text,'html.parser')
    # print(response.text)
    infoHTML = soup.find('div',{'class':'content'})
    try:
        infoStr = "|".join(infoHTML.text.split())
        # 医生姓名
        name = soup.find('h1',{'class':'doctor-name js-doctor-name'}).text
        # 病友推荐度
        recommend = soup.find('span',{'class':'value'}).text
        # 医生职称
        grade = soup.find('span',{'class':'doctor-title'}).text
        # 医生职位
        status = soup.find('span',{'class':'doctor-educate-title'}).text
        # 医生专长
        startIndex = infoStr.find('专业擅长')+5  # 5 由于'专业擅长'的长度为4和分隔符'|'的长度为1 组成
        endIndex = infoStr[startIndex:].find('|')+startIndex
        specialty = infoStr[startIndex:endIndex]
        # 医生简介
        startIndex = infoStr.find('个人简介')+5  # 5 由于'个人简介'的长度为4和分隔符'|'的长度为1 组成
        endIndex = infoStr[startIndex:].find('|')+startIndex
        resume = infoStr[startIndex:endIndex]
        # 医生经验
        experienceInfo = soup.find_all('li',{'class':'clearfix'})[-1]
        a_tags = experienceInfo.find_all('a')
        experiences =[]
        for a in a_tags:
            a_text = a.get_text(strip=True)  # 获取a标签的文本
            experiences.append(a_text)
        # 其他数据
        otherInfo = "|".join(soup.find('ul',{'class':'item-body'}).text.split())
        # 存入数据库
        try:
            sql="Insert into doctor_info(name,grade,status,specialty,resume,experience,other_info) values(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(name,grade,status,specialty,resume,str(experiences),otherInfo))
            connection.commit()
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

if __name__=='__main__':
    getDoctorDetail('https://www.haodf.com/doctor/5808.html',None,None)