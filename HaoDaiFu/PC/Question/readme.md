#  问诊 Question
## 说明
本目录用于存放所有与获取好大夫网医生问诊数据有关的代码文件

## 程序运行说明
启动时调用getDepartment_Question.py，该函数将获取问诊页面中各科室的问诊页的URL，然后将获取到的URL传递给getMedicalRecords函数，该函数用于获取指定科室问诊页的所有具体问诊记录的URL，并传递给函数getDetailRecord，最后由getDetailRecord函数提取出具体某一条问诊数据中的病患及医生建议数据。

### 其他说明
在调用getDepartment及之后的函数时，还需要传入数据库游标cursor与连接对象connection，用于执行SQL语句和提交事务。SQL执行依赖于pymysql。

---
Author:LuShangWu