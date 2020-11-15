#!python 3

import os
import re
import imghdr
import glob
import time
from urllib.request import urlretrieve
import urllib.request
from pyquery import PyQuery as pq

import logging as logger

logger.basicConfig(format='%(asctime)s\t%(pathname)s\t%(message)s', level=logger.INFO)

ptCode = re.compile(r'(.*?)福利汇总第(.*?)期', re.I | re.S | re.M)
APP_PATH = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(os.path.dirname(APP_PATH), "fuliimages")

logger.info("----------当前运行路径: "+APP_PATH+" ----------")
logger.info("----------图片存储路径: "+IMG_PATH+" ----------")

def main():
    for i in range(1, 8):
        get_list(i)
    logger.info("请求完成,一小时后重试")
    time.sleep(3600)
    main()

def get_list(page_index):
    url = 'https://fuliba2020.net/category/flhz'
    if (page_index != 1):
        url = url + "/page/" + str(page_index)
    logger.debug("列表页请求开始:" + url)

    try:
        doc = pq(url=url)
    except Exception:
        logger.info("列表页请求失败:" + url)
        return

    logger.info("列表页请求成功:" + url)

    for el in doc('h2 a').items():
        # 准备 参数
        content_title = el.attr('title')
        page_url = el.attr('href')

        # 测试查看参数
        logger.debug("content_title:" + content_title)
        logger.debug("page_url:" + page_url)

        # 开始调用 get_page
        get_page(page_url, content_title)

def get_page(page_url,page_title):
    try:
        doc = pq(url=page_url)
    except Exception:
        logger.info("----内容页请求失败:" + page_url)
        return
    
    logger.info("----内容页请求成功:" + page_url)

    for el in doc('.article-paging a').items():
        # 准备 参数
        content_url = el.attr('href')
        # 开始调用 get_content
        get_content(content_url, page_title,el.text())


def get_content(content_url, content_title,content_index):
    try:
        doc = pq(url=content_url)
    except Exception:
        logger.info("--------详情页请求失败:"+content_index+":" + content_title)
        return

    logger.info("--------详情页请求成功:"+content_index+":" + content_title)

    teg = ptCode.findall(content_title)
    for el in doc(".article-content img").items():
        # 准备 参数
        img_src = el.attr["src"]
        if img_src is None:
            logger.error("src为空:" + content_index + ":" + content_title)
            continue

        img_path = os.path.join(IMG_PATH,teg[0][0], teg[0][1],content_index, os.path.basename(img_src))

        # 测试查看参数
        logger.debug("img_src:" + img_src)
        logger.debug("img_path:" + img_path)

        # 开始调用 save_img
        save_img(img_src, img_path)


def save_img(img_src, img_path):
    logger.debug("--------开始下载图片:" + img_src)

    if (os.path.exists(img_path)):
        logger.debug("--------图片已下载过:" + img_src)
        logger.debug("--------图片保存位置:" + img_path)
        return

    if len(glob.glob(img_path + "*")) > 0:  # 如果图片是没有后缀名的
        logger.debug("--------图片已下载过:" + img_src)
        logger.debug("--------图片保存位置:" + img_path)
        return

    try:
        img_path = os.path.join(APP_PATH, img_path)
        img_folder = os.path.dirname(img_path)
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
    except Exception:
        logger.error('--------文件夹创建失败:' + img_src + "\t" + img_path)
        return

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [("user-agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36")]
        request = opener.open(img_src, timeout=3)
        res = request.read()
    except Exception:
        logger.error("--------图片请求失败:" + img_src)
        logger.error("--------      地址:" + img_path)
        return

    if os.path.splitext(img_src)[1] == '':
        ext = imghdr.what(None, res)
        if ext == None:
            logger.error("--------图片解析失败:" + img_src)
            logger.error("--------      地址:" + img_path)
            return
        elif ext == 'jpeg':
            img_path = img_path + '.jpg'
        else:
            img_path = img_path + '.' + ext

    try:
        with open(img_path, 'wb') as op:
            op.write(res)
            logger.debug('--------图片保存成功:' + img_src)
    except Exception:
        logger.error("--------图片保存失败:" + img_src)
        logger.error("--------      地址:" + img_path)


# response = requests.get(url='https://fulibus.net/2019001.html/2', timeout=999)
# doc = pq(url='https://fulibus.net/category/flhz/')
# urlretrieve("https://tva1.sinaimg.cn/large/007awY0bly1g0ffv4elpqg308h09l7qg.gif", "007awY0bly1g0ffv4elpqg308h09l7qg.gif")
# get_content("https://fulibus.net/2019001.html/2", "2019福利汇总第1期：不忘初心，方得始终")
# save_img("https://p.pstatp.com/origin/fe520000eb30ecd6b3f3", "fe520000eb30ecd6b3f3")

main()
