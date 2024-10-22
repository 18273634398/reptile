# ===========================================================================================================
# Author    ：LuShangWu
# Date      ：2024-10-20
# Version   ：1.0.1
# Description：用于爬取hao网站的单个问诊记录的详细数据并保存到本地
# Copyright  ：LuShangWu
# License   ：MIT
# ===========================================================================================================
import requests
from bs4 import BeautifulSoup


def getDetailRecord_Question(url, infoIndex, cursor, connection):
    print("[getting detail record]" + url)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "g=77490_1728828402072; g=HDF.114.670bd3f219434; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1728828403,1729422262; HMACCOUNT=50BB06D570729B92; tfstk=gi_Sbr_cSYDSxnnPXyF2fOeF93YQQ9aw9XOds63r9UL-pvC939PkzJmCc9BD4LeHzpOdH6J-v0dpMqdB12HJ9UKQRt6Gz9PlTvsfE1Ky8w1nRBCdK7vUZo5lZeYLQR8Q7_fuUFG6Pai-HICDTDh87BqKOnTLQRzq0jKuUeBrVNpmlspDOQHKy9pAMKAIJepJvxnv6KppJ9dKHqd9ODd-2eFfMKApJphFr-OQPL17ithMGpNv__pjJ2Q8-3963DuIR3AJV_fJh_15lQtWBnAWUc7R36QPrnqibefVf9sdHrg5d_IOpL7YB29FjB1p1FUi1KQ5OZtl0YnJ1U9WXaKx_V16vi_Xzaenjs5XehTV0o2yYU65jdx8m-XCGLWdPnH73pSNgaKfB-ufKHsRFILO4ygwCvP-AjtiRI9aGSinxXaRuF-_HsKp2IA57SNjF9xJiIO4GSinx3dDNtPbGY6h.; userinfo[id]=11039421678; userinfo[time]=1729473347; userinfo[hostid]=0; userinfo[key]=USxQYVdkAWFROFJsAjRSMl8wDTdSZQZtBy4Ab1BiXzQBYlFpVC9TZlo3Bm4BO1B0ByVSblpz; userinfo[ver]=1.0.2; userinfo[name]=hdf68ye7o8v; acw_tc=76fdae1e17295232303353524e3e4c6ab3fba4a0b453beee9c6fec7f6a; acw_sc__v2=67167034612834c42a67af7697d46757f01458d8; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1729524011",
        "if-none-match": "W/\"a828-IQN9Q82gkUD4wNQmTQW4qMxIBSo\"",
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
    # print(html)

    # 解构医生数据
    try:
        print(f"INFO[{infoIndex}]")
        soup = BeautifulSoup(html, 'html.parser')
        doctorName = soup.find('span', {'class':'info-text-name'}).text
        doctorGrade = soup.find('span', {'class':'info-text-grade'}).text
        doctorStatus = soup.find('span', {'class':'info-text-status'}).text
        hospitalName = soup.find('a', {'class':'hospital'}).text
        doctorSuggestInfo = soup.find_all('div',{'class':'suggestions-text paddingLeft20'})
        doctorSuggest = ""
        for i  in doctorSuggestInfo:
            temp = "|".join(i.text.split())  # 数据处理
            doctorSuggest = f"{doctorSuggest}{temp}"
        # 打印医生数据及问诊建议
        print(doctorName,doctorGrade,doctorStatus,hospitalName,doctorSuggest)


        # 解构问诊数据的代码部分
        info_start_str = '<span class="diseaseinfotitle">病例信息</span></br>'
        info_start_index = html.find(info_start_str)
        info_start_length = len(info_start_str)
        info_end_str = '</p>'
        info_end_index = html[info_start_index+info_start_length:].find(info_end_str)
        medicalInfo = html[info_start_index+info_start_length:info_start_index+info_start_length+info_end_index]
        # print(medicalInfo)  #  网页HTML中病例信息部分代码

        # 解构问诊数据的索引信息
        title_list_index = [] # 问诊记录中每一个字段的开始位置索引
        index = 0
        while(1):
            title_start_str = '<span class="info3-title ">'
            title_index = medicalInfo[index:].find(title_start_str)
            if title_index != -1:
                title_list_index.append(title_index+index)
                index += title_index + len(title_start_str)
            else:
                break

        infoSum =[]

        # 获取问诊数据的患者文本信息
        for i in range(len(title_list_index)-1):
            tempInfo = medicalInfo[title_list_index[i]:title_list_index[i+1]]
            soup = BeautifulSoup(tempInfo, 'html.parser')
            title = soup.find('span', {'class':'info3-title'}).text[:-1]
            spans = soup.find_all('span')
            combined_text = ""
            # 遍历所有span标签，提取并合并文本
            for span in spans:
                combined_text += span.get_text() + " "  # 使用空格分隔每个提取的文本
            # 解构问诊数据
            value_index =combined_text.find(title)+len(title)+1
            value = combined_text[value_index:]
            tempInfo = title + ":" + value
            infoSum.append(tempInfo)
        # 打印最后的解构结果
        print(infoSum)
        infoStr = str(infoSum)

        # 保存问诊数据到本地数据库
        try:
            sql = "INSERT INTO record_of_medical (id,name, grade, status, hospital, records,summary,doctorSuggest) VALUES (%s,%s, %s,%s, %s, %s,%s,%s)"
            cursor.execute(sql, (infoIndex, doctorName, doctorGrade, doctorStatus, hospitalName, infoStr,infoStr[0:31],doctorSuggest))
            connection.commit()
        except Exception as e:
            print(f"Error: unable to insert data,because{e}")
            connection.rollback()
    except Exception as e:
        print(f"Error: unable to insert data,because{e}")


# 该函数泛化能力不强 v1.0
# def getDetailRecord(url):
#     print("getting detail record"+url)
#     url = 'https://www.haodf.com/bingcheng/8904489169.html'
#     headers = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "accept-encoding": "gzip, deflate, br, zstd",
#         "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#         "cache-control": "max-age=0",
#         "cookie": "g=77490_1728828402072; g=HDF.114.670bd3f219434; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1728828403,1729422262; HMACCOUNT=50BB06D570729B92; acw_tc=71dbc9a417294241024417056e7022928533552f083577bb054f2b55ec; acw_sc__v3=6714eaf93d7bbe38d6ad01bb1fabd32be56c0971; tfstk=grHmAbaQAjPXKlf753yXsEfrv0O8hiw_vVBTWRUwazz5kZBxbG2iz2lT_EwxI40IPxBTH53u4krT0NWa087zvztsDcHYSG0KyqFZBPHMj-M-MOUvlRmZJRYpJppKcmN_QeLLzr51gJrLbi7T__rzCgFDMMpKcmsPmN-KapQgDZyZ_Puag8SzczW47VPVa3qaXZ5N3VoyqzZOQozN377zxlEaQRuZ43qsMpO4-floUEtwsCQaFWkumS4E4B6NIsqVJym2mOXZEDN08d4lQOkum0Ew61XH6ylQkWUSzLB0I0ri-k0czU2ZqxM3ax85I20oT8qSNFfg-foxOfPk0KounrVne7IVs-cZlAVjiGtI4-uSOyN2NUZoHvFgR7byu0nuuWcikU6akXmrrWHRy9erYb2l4Y1PTvghCu-tU11_guZuJX7sLGtwpedDq3fBfSr7cHKkq1sbguZuJ3xlOEN4Votd.; acw_sc__v2=6714eb80c3d57fab354bd2a31e8ccdc9b6978fe6; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1729424345",
#         "if-none-match": "W/\"9cf1-MgTWDJYnBNmzd5rnfPkYD/E8Sv8\"",
#         "priority": "u=0, i",
#         "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": "\"Windows\"",
#         "sec-fetch-dest": "document",
#         "sec-fetch-mode": "navigate",
#         "sec-fetch-site": "none",
#         "sec-fetch-user": "?1",
#         "upgrade-insecure-requests": "1",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
#     }
#     response = requests.get(url,headers=headers)
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup解析HTML代码
#
#     # 找到问诊记录的详细数据
#     detail ={}  # 存储问诊记录的详细数据 以键值对存储
#     titleList = []  # 存储问诊记录的详细数据的键值
#     infoTitle = soup.find_all('span', {"class":'info3-title'})
#     if(infoTitle == []):
#         return
#     else:
#         # 处理问诊记录数据字段（键） 并存入列表titleList
#         for i in range(len(infoTitle)):
#             detail[infoTitle[i].text.replace('：','')] = ''
#             titleList.append(infoTitle[i].text.replace('：',''))
#
#         # 获取问诊数据的数据值
#         infoValue = soup.find_all('span', {"class":'info3-value'})
#         for i in range(len(infoValue)):
#             print(f"index[{i}]:"+str(infoValue[i]))
#         exit()
#         index = 0
#         for i in range(len(infoValue)):
#             info = str(infoValue[i])
#             if(info.find('newline') != -1):
#                 detail[titleList[index]]=infoValue[i].text
#                 index += 1
#             else:
#                 detail[titleList[index]]=detail[titleList[index]]+infoValue[i].text
#                 i+=1
#                 if(str(infoValue[i]).find('newline') != -1 and i!= len(infoValue)-1):
#                     index +=1
#                     i-=1
#                 elif(i!= len(infoValue)-1):
#                     i-=1
#                 else:
#                     break
#         print(detail)
#


if __name__ == '__main__':
    getDetailRecord_Question('https://www.haodf.com/bingcheng/8904512091.html', 0, None, None)
