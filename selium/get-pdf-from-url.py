# python = 3.7

# import sys
import re
import os
# from lxml import etree
import requests
import bs4
from tqdm import tqdm
import winreg
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
# import json
import random


def get_desktop():
    """
    获取桌面路径
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def mkdir(path):
    """
    如果path不存在则创建目录
    """
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def get_pdf(savename, filename, url):
    """
    下载pdf
    """
    response = requests.get(url, stream="TRUE")
    # stream=True的作用是仅让响应头被下载，连接保持打开状态，
    content_size = int(response.headers['Content-Length']) / 1024
    # 确定整个安装包的大小
    # pdf = response.content
    pbar = tqdm(total=content_size, initial=0, unit='B',
                unit_scale=True, desc=filename)
    with open(savename, 'wb') as f:
        # 下载文件
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                # 更新文件大小
                pbar.update(1024)
    pbar.close()


def get_soup(url):
    """
    获取
    """
    r = requests.get(url)
    r.encoding = 'utf-8'  # 用utf-8解码文档
    rt = r.text
    soup = bs4.BeautifulSoup(rt, 'lxml')
    return soup


if __name__ == '__main__':

    # 创建文件保存目录
    # path = get_desktop() + "\\" + '教师教育图书库'    #保存在桌面
    path = os.getcwd() + "\\" + '教师教育图书库\\'  # 保存在当前路径
    mkdir(path)

    #创建md文件
    with open(path + "PDF链接.md", 'w', encoding='utf-8') as f2:
        f2.writelines("# PDF链接\n")
        f2.close()

    # 初始化变量
    page = 1
    url = "http://219.244.185.33:8080/node/272_" + str(page) + ".jspx"    # 获取陕西师范大学自建图书馆图书
    nexturl = url
    Number = page*10-9
    while nexturl:

        soup = get_soup(url=nexturl)
        booklist = soup.find_all("a", class_="fontBlue rs_title")
        """
        获得下页的url
        """
        nextpage = soup.find("a", string="下页")
        nexturl = "http://219.244.185.33:8080" + nextpage['href'].replace(" ", "%20")

        for i in booklist:
            # time.sleep(random.uniform(0, 1))    # 随机睡眠 防止被禁止爬虫
            href = i['href']
            bookurl = 'http://219.244.185.33:8080' + href     # 书籍界面地址
            bookname = i.string  # 书名
            bookname = re.sub('[\/:*?"<>|]\s', '-', bookname)  # 使 文件命名 符合命名规定
            bookname = re.su = re.sub(r'\s', "", bookname)      # 删除文件名中的空白字符
            booksoup = get_soup(url=bookurl)    # 获取页面html
            content_raw = booksoup.find("div", class_="con").text.replace(
                "\n", "").replace('\t', '').replace(' ', '').replace('【', '\n    【')    # 书籍信息
            url_raw = booksoup.find("a", string="全文阅读")    # 找到pdf链接
            pdfurl = 'http://219.244.185.33:8080' + url_raw["href"]     # 找到pdf链接
            filename = path + bookname + ".txt"    # 文件命名

            with open(path+"PDF链接.md", 'a+', encoding='utf-8') as f:
                f.write(str(Number) + "、" +
                        "[" + bookname + "](" + pdfurl + ")\n")
                f.write(content_raw+", \n    【书籍界面】"+bookurl+"\n\n")
                f.close()
            print("page: ", page, "number: ", Number, bookname)
            Number += 1
        page += 1
        
    print("下载完成")