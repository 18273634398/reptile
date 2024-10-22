# ===========================================================================================================
# Author    ：LuShangWu
# Date      ：2024-10-22
# Version   ：1.0
# Description：用于爬取hao网站的多条问诊信息并保存到本地
# Copyright  ：LuShangWu
# License   ：MIT
# ===========================================================================================================
from getDepartment import getDepartment
import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'lushangwu;2004',
    'db': 'reptile',
    'charset': 'utf8mb4',
}

if __name__ == '__main__':
    # 连接数据库
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    infoIndex = 1
    department = getDepartment(infoIndex,cursor,connection)
    # 关闭连接
    cursor.close()
    connection.close()