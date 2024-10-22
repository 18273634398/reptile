# ===========================================================================================================
# Author    ：LuShangWu
# Date      ：2024-10-22
# Version   ：1.0
# Description：利用上一级函数传递的URL获取指定科室中的所有医生主页的URL
# Copyright  ：LuShangWu
# License   ：MIT
# ===========================================================================================================
import requests
from bs4 import BeautifulSoup
from HaoDaiFu.PC.Info.getDoctorDetail_Info import getDoctorDetail


def getDoctorUrl(url,cursor,connection):
    headers={
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "g=77490_1728828402072; tfstk=gi_Sbr_cSYDSxnnPXyF2fOeF93YQQ9aw9XOds63r9UL-pvC939PkzJmCc9BD4LeHzpOdH6J-v0dpMqdB12HJ9UKQRt6Gz9PlTvsfE1Ky8w1nRBCdK7vUZo5lZeYLQR8Q7_fuUFG6Pai-HICDTDh87BqKOnTLQRzq0jKuUeBrVNpmlspDOQHKy9pAMKAIJepJvxnv6KppJ9dKHqd9ODd-2eFfMKApJphFr-OQPL17ithMGpNv__pjJ2Q8-3963DuIR3AJV_fJh_15lQtWBnAWUc7R36QPrnqibefVf9sdHrg5d_IOpL7YB29FjB1p1FUi1KQ5OZtl0YnJ1U9WXaKx_V16vi_Xzaenjs5XehTV0o2yYU65jdx8m-XCGLWdPnH73pSNgaKfB-ufKHsRFILO4ygwCvP-AjtiRI9aGSinxXaRuF-_HsKp2IA57SNjF9xJiIO4GSinx3dDNtPbGY6h.; userinfo[id]=11039421678; userinfo[time]=1729473347; userinfo[hostid]=0; userinfo[key]=USxQYVdkAWFROFJsAjRSMl8wDTdSZQZtBy4Ab1BiXzQBYlFpVC9TZlo3Bm4BO1B0ByVSblpz; userinfo[ver]=1.0.2; userinfo[name]=hdf68ye7o8v; sdmsg=1; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1729422262,1729561346,1729563046,1729578457; HMACCOUNT=50BB06D570729B92; g=HDF.120.67169922aad24; acw_tc=76fdae2017295828304213495e18b19f302b1030f3b760a455229ede93; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1729582835",
        "if-none-match": "W/\"1909d-jJyWr6Uq6I+K1jwhkOEjP1OcSvs\"",
        "priority": "u=0, i",
        "referer": "https://www.haodf.com/citiao/list-jibing-neike.html",
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
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    doctorInfo = soup.find_all('a', {'class': 'item-bd'})
    for i in doctorInfo:
        tempUrl = i['href']
        getDoctorDetail(tempUrl,cursor,connection)

if __name__ == '__main__':
    getDoctorUrl('https://www.haodf.com/citiao/jibing-guanxinbing/tuijian-doctor.html',None,None)