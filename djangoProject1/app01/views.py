from django.shortcuts import render, HttpResponse,redirect
import requests
from app01.models import UserInfo

# Create your views here.


def index(request):
    return HttpResponse("欢迎使用")


def user_list(request):
    # 去app目录下的templates目录下去寻找user_list.html （根据app的注册顺序，逐一去它们的templates目录中找）
    return render(request, "user_list.html")


def user_add(request):
    return HttpResponse("添加用户")


def tpl(request):
    name = "韩信"
    roles = ["管理员", "CEO", "保安"]
    user_info = {"name": "张三", "salary": 100000, "role": "CTO"}
    data_list = [
        {"name": "张三", "salary": 100000, "role": "CTO"},
        {"name": "王二", "salary": 100000, "role": "保安"},
        {"name": "麻子", "salary": 100000, "role": "管理员"},
    ]
    return render(request, 'tpl.html', {"n1": name, "n2": roles, "n3": user_info, "n4": data_list})

def news(request):
    # 1、定义一些新闻（字典或者列表） 或 去数据库 网络请求获取联通新闻
    # 向地址：http://www.chinaunicom.com/api/article/NewsByIndex/2/2023/04/news
    headers = {
        'Referer': 'http://www.chinaunicom.com/news/list202304.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58'
    }
    res = requests.get('http://www.chinaunicom.com/api/article/NewsByIndex/2/2023/04/news', headers=headers)
    data_list = res.json()

    print(data_list)

    return render(request, "news.html", {"news_list":data_list})

def something(request):
    # request是一个对象，封装了用户发送过来的所有请求相关数据

    # 1、过去请求方式 GET
    print(request.method)

    # 2、在URL上传递 /something/?n1=123&n2=999
    print(request.GET)

    # 3、在请求体中提交数据
    print(request.POST)

    # 4、【响应】HttpResponse("返回的内容")，字符串内容返回给请求者
    # return HttpResponse("返回的内容")

    # 5、【响应】读取HTML的内容 + 渲染（替换） -> 字符串，返回给用户浏览器
    # return render(request, "something.html", {"title":"来了"})

    # 6、【响应】 让浏览器重定向到其它的页面
    return redirect("http://www.baidu.com")

def login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    else:
        # 如果是POST请求，获取用户提交的数据
        # print(request.POST)
        username = request.POST.get('user')
        password = request.POST.get('pwd')

        # 校验
        if username == "root" and password == "123456":
            return HttpResponse("登录成功")
        else:
            # return HttpResponse("登录失败")
            msg = "登录失败"
            return render(request, "login.html", {"error":msg})


def orm(request):
    UserInfo.objects.create(name="张三", password="123456", age=18)
    UserInfo.objects.create(name="张四", password="123333", age=20)
    UserInfo.objects.create(name="张五", password="124444", age=22)
    return HttpResponse("成功")

def info_list(request):
    # 1、获取数据库中所有的用户信息
    data_list = UserInfo.objects.all()
    print(data_list)

    return render(request, "info_list.html", {"data_list":data_list})



def info_add(request):
    if request.method == "GET":
        return render(request, "info_add.html")
    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get("age")
    # 将数据添加到数据库
    UserInfo.objects.create(name=user,password=pwd,age=age)
    # return HttpResponse("添加成功")
    # return redirect('http://127.0.0.1:8000/info/list/')
    return redirect('/info/list/')


def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/info/list/')