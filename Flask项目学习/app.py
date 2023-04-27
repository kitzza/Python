# @author： zhc
# @Time: 2023/4/26
# @FileName: app
import contextlib

from flask import Flask, render_template, request
import pymysql




app = Flask(__name__)

@app.route('/index')
def index():
    # data_list = ["小王", "小张", "小心"]
    data_list = [{"name": "小王", "age": 18, "sex": "男"}, {"name": "小张", "age": 20, "sex": "女"}, {"name": "小风", "age": 22,"sex": "男"}]
    return render_template("index.html", h1="首页1", data_list=data_list)

@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/input_data', methods = ['POST','GET'])
def input_data():
    username = request.form.get('username')
    phone = request.form.get('iphone')
    password = request.form.get('password')
    # 1 连接数据库
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='p@ss0rd', charset='utf8', db='study')
    cursor = conn.cursor()


    # 2 发送指令
    sql = "INSERT INTO wangye (email,phone, pwd) VALUE (%s,%s, %s)"
    gpt_data = (username, phone, password)
    with contextlib.suppress(Exception):
        cursor.execute(sql, gpt_data)  # 执行sql语句
        conn.commit()  # 提交至数据库
    # 3 关闭连接
    cursor.close()
    conn.close()

    print(username, password)
    # 在这里处理用户输入的数据
    return render_template('success.html')

@app.route('/show/user')
def show_user():
    # 1 连接数据库
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='写自己的密码', charset='utf8', db='study')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2 发送指令
    sql = "SELECT * FROM wangye"
    with contextlib.suppress(Exception):
        cursor.execute(sql)  # 执行sql语句
        data_list = cursor.fetchall()

    # 3 关闭连接
    cursor.close()
    conn.close()

    print(data_list)

    return render_template("show_user.html", data_list=data_list)



if __name__ == '__main__':
    app.run(debug=True)