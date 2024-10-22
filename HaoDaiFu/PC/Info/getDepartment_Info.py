# ===========================================================================================================
# Author    ：LuShangWu
# Date      ：2024-10-22
# Version   ：1.0
# Description：用于爬取hao网站"找专家"页面的 按科室进行分类 的专家信息列表的URL
# Copyright  ：LuShangWu
# License   ：MIT
# ===========================================================================================================
import requests
from bs4 import BeautifulSoup

from HaoDaiFu.PC.Info.getDoctorUrl_Info import getDoctorUrl

baseUrl = "https://www.haodf.com/citiao/list-jibing-"  # 基础URL,后面拼接具体的科室的名称，例如内科：neike
departmentCN = ["neike","waike","fuchanke","xiaoerke","guke","yanke","kouqiangke","erbiyanhoutoujingke","zhongliuke","pifuxingbing","nanke","yiliaomeirongke","shaoshangke","jingshenxinlike","zhongyike","zhongxiyijieheke","chuanranbingke","kangfuyixueke","mazuiyixueke","zhiyebingke","yixueyingxiangxue","binglike","qitakeshi"] # 具体科室的中文拼音

def getDepartment_Info(cursor,connection):
    for i in departmentCN:
        tempUrl = baseUrl + i + ".html"
        headers ={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "max-age=0",
            "cookie": "g=77490_1728828402072; tfstk=gi_Sbr_cSYDSxnnPXyF2fOeF93YQQ9aw9XOds63r9UL-pvC939PkzJmCc9BD4LeHzpOdH6J-v0dpMqdB12HJ9UKQRt6Gz9PlTvsfE1Ky8w1nRBCdK7vUZo5lZeYLQR8Q7_fuUFG6Pai-HICDTDh87BqKOnTLQRzq0jKuUeBrVNpmlspDOQHKy9pAMKAIJepJvxnv6KppJ9dKHqd9ODd-2eFfMKApJphFr-OQPL17ithMGpNv__pjJ2Q8-3963DuIR3AJV_fJh_15lQtWBnAWUc7R36QPrnqibefVf9sdHrg5d_IOpL7YB29FjB1p1FUi1KQ5OZtl0YnJ1U9WXaKx_V16vi_Xzaenjs5XehTV0o2yYU65jdx8m-XCGLWdPnH73pSNgaKfB-ufKHsRFILO4ygwCvP-AjtiRI9aGSinxXaRuF-_HsKp2IA57SNjF9xJiIO4GSinx3dDNtPbGY6h.; userinfo[id]=11039421678; userinfo[time]=1729473347; userinfo[hostid]=0; userinfo[key]=USxQYVdkAWFROFJsAjRSMl8wDTdSZQZtBy4Ab1BiXzQBYlFpVC9TZlo3Bm4BO1B0ByVSblpz; userinfo[ver]=1.0.2; userinfo[name]=hdf68ye7o8v; sdmsg=1; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1729422262,1729561346,1729563046,1729578457; HMACCOUNT=50BB06D570729B92; acw_sc__v2=671749671a3910a6eb2fdd9befd7c794a145c31c; acw_tc=76fdae2817295808406843934e6df97c37dde83d1b6bc2645d729c0d6d; g=HDF.206.671605df34b42; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1729581406",
            "priority": "u=0, i",
            "referer": "https://www.haodf.com/citiao/list-jibing-waike.html",
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
        response = requests.get(tempUrl, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        urlListInfo = soup.find_all('div', {'class':'m_ctt_green'})  # 为包含疾病专家URL的HTML代码部分
        for i in urlListInfo:
            tempList = i.find_all('a')  # 找到包含疾病专家URL的a标签
            for j in tempList:
                tempUrl = j['href']
                print(f"{j.text.strip()}:"+tempUrl)  # 打印疾病专家URL
                nextUrl = "https://www.haodf.com"+tempUrl
                getDoctorUrl(nextUrl,cursor,connection)


if __name__ == '__main__':
    getDepartment_Info(None,None)