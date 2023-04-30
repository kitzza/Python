# @author： zhc
# @Time: 2023/4/29
# @FileName: 异步编程
import contextlib
import time
import sys
import aiohttp
import asyncio
import re
import os
from uitls.Log import logger
import pymysql


# os.environ['NO_PROXY'] = 'www.baidu.com'


class Asyn():

    def __init__(self):
        self.__headers = {
            'authority': 'go.drugbank.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'cookie': '_omx_drug_bank_session=ZiQulkyeNWQN4VxewoUdpvpjebs36v3xv0adS0ywsWTDX9cXowdJblYyKE0AHmpM9gOmiAlfQyAy2SR0tOFqctQ0APTCNNYzM2Q7hFst70od%2FfCQ7oGSC46qq7bjvdbzwMbrpxtBM0%2BYNK6r3iNyzZHw1d5n%2BvBvkVNDJBaRzB404tsju33MhMrhBJv6lNBjGxH84Dqgu8Ma7oWGC8dWeeZNl9gkZ0yHsMj2F04xDOxu0VLo4Q3LOCjHSALrqoHZrk55%2FGSxYwtfTsHXF%2FUzJ6phGpkHRq519NWQH%2FnsDL9Rc%2FLX8JHYq3LjKdGV%2B8GjdTP%2Bchgn2lv%2BUDFyqIbrnp5NP0cJFLvDB2FSfW4TCItVAsKaI7dIqWC0xcNRbsfQAnRQ0Ix5Jp%2Ft1Za11jirI5OZoEGbDZ9n9dfbBfxFO5aIECa7pOj%2BO668OqXq%2Fd8kEw0YNLw07NFkHDXT3iCMgTiMjyg77aMTFUI7HXF0h2elSRSL8S1oh9e9YcGtAA%3D%3D--0sEdP1iupQN5%2BS4%2B--IpfLjfkZLpD7tOPGb8MAPQ%3D%3D; path=/; HttpOnly; SameSite=Lax',
            'referer': 'https://go.drugbank.com/unearth/q?query=*&button=&searcher=drugs',
            'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
        }

    def __get_conn(self):
        # 建立连接
        conn = pymysql.connect(host="127.0.0.1", user="root", password="p@ss0rd", db="cov", charset="utf8")
        # 创建游标
        cursor = conn.cursor()
        return conn, cursor

    def __close_conn(self, conn, cursor):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    async def __fetch(self, session, url):
        print("发送请求：", url)
        async with session.get(url, verify_ssl=False, headers=self.__headers) as response:
            content = await response.text()
            # print(content)
            try:
                info1 = re.findall(r'href="/indications/.*?">(.*?)</a', content)  # 第一列表
                if not info1:
                    print(f"最大限度页")
                    return
            except Exception as e:
                print(f"最大限度页，error={e}")
                return
            # print(info1)
            # print(len(info1))
            info2 = re.findall(r'<div class="db-matches"><a (.*?)</a></div>', content)
            info2_new = []  # 第二列表
            for i in info2:
                # i = i.replace('href="/drugs/', '').replace('">', ':').replace('</a>', '').replace('<a', '')
                i = i.replace('href="/drugs/', '').replace('">', ':').replace('</a>', '').replace('<a', '').replace(
                    ' / ',
                    '【/】')  # 修改的

                # print(i)
                info2_new.append(i)
            # print(len(info1), info1)
            # print(len(info2_new), info2_new)

            for yaoming, chenfen in zip(info1, info2_new):
                dic = {
                    "药名": yaoming,
                    "成分": chenfen
                }
                # total_list.append(dic)
                # print(dic)
                logger.info(dic)

                conn, cursor = self.__get_conn()
                try:
                    sql = "INSERT INTO drug (drug_name, element) VALUE (%s, %s)"
                    gpt_data = (yaoming, chenfen)
                    with contextlib.suppress(Exception):
                        cursor.execute(sql, gpt_data)  # 执行sql语句
                        conn.commit()  # 提交至数据库
                except Exception as e:
                    print("出问题了", e)
                finally:
                    self.__close_conn(conn, cursor)

            # with open('异步采集.txt', 'a', encoding='utf-8') as f:
            #     f.write(f'{len(info1), info1}\n{len(info2_new), info2_new}\n')
            # time.sleep(0.5)  # 加了这个没啥效果

    async def main(self):
        page = int(input("输入页数："))
        async with aiohttp.ClientSession() as session:
            url_list = [
                f'https://go.drugbank.com/unearth/q?approved=1&ca=0&eu=0&page={i}&query=%2A&searcher=indications'
                for i in range(1, page + 1)]
            tasks = [asyncio.create_task(self.__fetch(session, url)) for url in url_list]
            await asyncio.wait(tasks)

    @staticmethod
    def run():
        print("""
        _____ _  Author: 十架bgm         __
        _________   ___ ___    _____________________________________________
        \_   ___ \ /   |   \  /  _  \__    ___/  _____/\______   \__    ___/
        /    \  \//    ~    \/  /_\  \|    | /   \  ___ |     ___/ |    |
        \     \___\    Y    /    |    \    | \    \_\  \|    |     |    |
         \______  /\___|_  /\____|__  /____|  \______  /|____|     |____|
                \/       \/         \/               \/        version=0.1

        """)



if __name__ == '__main__':
    l = len(sys.argv)
    if l == 1:
        s = """
        请输入参数
        参数说明
        start：开启
        """
        print(s)
    else:
        order = sys.argv[1]
        if order == "start":
            Asyn.run()
            spide = Asyn()
            asyncio.run(spide.main())
