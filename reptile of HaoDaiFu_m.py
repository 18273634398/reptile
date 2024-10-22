'''
信息源：好大夫
字段：
'''
import requests
class Faculty:
    def __init__(self,name,id,childFaculties):
        self.name = name
        self.id = id
        self.childFaculties = childFaculties

facultyList = []
count = 0
url="https://m.haodf.com/ndoctor/tuijian/AjaxTuijianDoctorList"
headers={
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "cookie": "g=HDF.114.670bd3f219434; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1728828403; HMACCOUNT=50BB06D570729B92; Hm_lvt_d4ad3c812a73edcda8ff2df09768997d=1728828411; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1728868910; acw_tc=78e2995117288689118113637eed729d56d690b0df7b4569a5b4d6c0dd; Hm_lpvt_d4ad3c812a73edcda8ff2df09768997d=1728869177",
    "priority": "u=1, i",
    "referer": "https://m.haodf.com/doctor/index.html",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36 Edg/127.0.0.0",
    "x-requested-with": "XMLHttpRequest"
}
payload={
    "placeId": "0",
    "diseaseId": "",
    "facultyId": 34000000,
    "serviceArr": [],
    "nowPage": 1,
    "pageSize": 10
}


'''
    获取所有科室ID
'''
def get_faculty_id():
    url="https://m.haodf.com/ndoctor/ajaxfacultylist?randomNumber=02722865957962166"
    headers={
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "cookie": "g=HDF.114.670bd3f219434; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1728828403; HMACCOUNT=50BB06D570729B92; Hm_lvt_d4ad3c812a73edcda8ff2df09768997d=1728828411; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1728868910; acw_tc=78e2995117288689118113637eed729d56d690b0df7b4569a5b4d6c0dd; Hm_lpvt_d4ad3c812a73edcda8ff2df09768997d=1728869177",
        "priority": "u=1, i",
        "referer": "https://m.haodf.com/doctor/index.html",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36 Edg/127.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    response=requests.get(url,headers=headers).json()
    data = response['data']
    if len(data) == 0:
        print("未获取到科室信息")
        exit(0)
    else:
        for faculty in data:
            # 父科室信息
            facultyName = faculty['parentName']  # 科室名称
            facultyId = faculty['parentId']  # 科室ID
            tempFaculty = Faculty(facultyName,facultyId,[])  # 父科室对象
            facultyList.append(tempFaculty)
            facultyInfo = faculty['childFaculty']
            # 获取子科室
            for childFaculty in facultyInfo:
                childName = childFaculty['name']  # 子科室名称
                childId = childFaculty['id']  # 子科室ID
                tempChildFaculty = Faculty(childName,childId,[])
                tempFaculty.childFaculties.append(tempChildFaculty)

        for faculty in facultyList:
            print(f"父科室：{faculty.name}({faculty.id})")
            for childFaculty in faculty.childFaculties:
                print(f"子科室：{childFaculty.name}({childFaculty.id})")
                get_doctor_info(childFaculty.id)
            print("\n"*2)


'''
    根据科室ID获取指定科室的所有医生信息
'''
def get_doctor_info(facultyId):
    global count
    global url
    global headers
    global payload
    payload['facultyId'] = facultyId
    response = requests.post(url, headers=headers, json=payload)
    pageCount = response.json()['pageInfo']['totalPage']
    for i in range(1, pageCount+1):
        get_doctor_info_signal(i)



'''
    格式化获取信息，若信息非空则直接返回，否则返回"未知"
'''
def get_Infom(info):
    if info:
        return info
    else:
        return "未知"



'''
    获取单一科室的所有医生信息
'''
def get_doctor_info_signal(pageNum):
    global count
    global url
    global headers
    global payload
    payload['nowPage'] = pageNum
    response = requests.post(url, headers=headers, json=payload)
    doctorInfoms = response.json()['data']
    if doctorInfoms:
        for doctorInfo in doctorInfoms:
            # 医生基础信息
            baseInfo = get_Infom(doctorInfo['baseDoctorInfo'])
            name = get_Infom(baseInfo['name'])  # 姓名
            hospital = get_Infom(baseInfo['hospitalCommonName'])  # 医院名称
            department = get_Infom(baseInfo['hospitalFacultyName'])   # 科室名称
            jobPosition = get_Infom(baseInfo['grade'])  # 职位
            jobTitle = get_Infom(baseInfo['educateGrade'])  # 职称
            specialize = get_Infom(baseInfo['specialize'])  # 擅长领域

            # 医生评价信息
            rankInfo1 = get_Infom(doctorInfo['otherDoctorInfo'])
            skill = get_Infom(rankInfo1['skill'])  # 主观疗效
            attitude = get_Infom(rankInfo1['attitude'])  # 服务态度
            rankInfo2 = get_Infom(doctorInfo['commentRankInfo'])
            score = get_Infom(rankInfo2['hotRank'])  # 病友推荐度

            # 医生服务信息
            serverInfo = get_Infom(doctorInfo['serviceInfo'])
            onlineClinicDesc = get_Infom(serverInfo['onlineClinicDesc'])  # 在线问诊
            registerDesc = get_Infom(serverInfo['registerDesc'])  # 预约挂号
            detailInfo = (serverInfo['productList'])
            serverInfoDetail = {"图文问诊":"未开启","电话问诊":"未开启"}
            if detailInfo:
                for detail in detailInfo:
                    # detail是一个字典
                    if detail['desc'] == "图文问诊":
                        serverInfoDetail['图文问诊'] = str(detail['price'])+" 元起"

            # 输出
            count += 1
            print("="*20)
            print("【医生信息】")
            print("[{}]姓名：{}\t医院：{}\n科室：{}\t职位(职称)：{}({})\n擅长领域：{}".format(count,name, hospital, department, jobPosition, jobTitle,specialize))
            print("【服务信息】")
            print("在线问诊：{}\t预约挂号：{}\n主观疗效：{}/100\t服务态度：{}/100\t病友推荐度：{}/5.0".format(onlineClinicDesc, registerDesc, skill, attitude, score))
            print("【服务详情】")
            print(f"图文问诊：{serverInfoDetail['图文问诊']}\t电话问诊：{serverInfoDetail['电话问诊']}")
            print("\n"*3)
    else:
        print("未获取到数据")




# 主函数部分
get_faculty_id()