# @author： zhc
# @Time: 2023/5/16
# @FileName: config
SECRET_KEY = "dsadsadsajkdgsa"

# 数据库的配置信息
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "flask_study"

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "37772311@qq.com"
MAIL_PASSWORD = "邮箱码"
MAIL_DEFAULT_SENDER = "37772311@qq.com"