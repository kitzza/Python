import pymysql
from pymysql import pool

# 创建连接池
POOL = pool.ConnectionPool(
    # 连接池中的最小连接数
    minsize=5,
    # 连接池中的最大连接数
    maxsize=20,
    # 连接超时时间
    connect_timeout=10,
    # MySQL数据库连接信息
    host='127.0.0.1',
    port=3306,
    user='root',
    password='p@ss0rd',
    database='cov',
    charset='utf8mb4',
    autocommit=False
)


