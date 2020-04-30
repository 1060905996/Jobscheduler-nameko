# coding=utf-8
import pymysql

def connmysql():
    conn = pymysql.connect(host='192.168.5.130', user='automl', password='automl', database='automl', charset='utf8')
    return conn

def getdata():
    conn = connmysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 定义要执行的SQL语句
    sql = "select * from test"
    # 执行SQL语句
    cursor.execute(sql)
    results = cursor.fetchall()  # 用于返回多条数据
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return results

def upddata():
    conn = connmysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 定义要执行的SQL语句
    sql = "update test set model_name = 'name'"
    # 执行SQL语句
    result = cursor.execute(sql)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return result

if __name__ == '__main__':
    res = getdata()
    for r in res:
        print(r)