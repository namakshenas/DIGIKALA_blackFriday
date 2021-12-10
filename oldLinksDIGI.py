# old links generator

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import random
import csv
import threading
import logging
import time


def getdata(url):
    r = requests.get(url)
    return r.text


def ext_url(page_no):
    url = 'https://www.digikala.com/treasure-hunt/products/?pageno=' + str(page_no) + '&sortby=4'
    reqs = getdata(url)
    soup = BeautifulSoup(reqs, 'html.parser')

    urls = []
    J5 = ' '
    list_URL = []
    for link in soup.find_all('a'):
        J1 = str(link.get('href'))
        J2 = J1.find('/product/')
        if J2 != -1:
            try:
                J3 = J1.split("/product/")[1]
                if J3 != J5:
                    list_URL.append("https://www.digikala.com/product/" + J3)
                J5 = J3
            except:
                pass
    return list_URL


def getJPG(URL):
    jpg_URL = []
    htmldata = getdata(URL)
    soup = BeautifulSoup(htmldata, 'html.parser')
    for item in soup.find_all("img"):
        J1 = str(item)
        J2 = J1.find("https://dkstatics-public.digikala.com/digikala-products/")
        if J2 != -1:
            try:
                J3 = J1.split("data-src=")[1].split("?x-oss")[0]
                jpg_URL.append(J3)
            except:
                pass
    return jpg_URL


def ext_csv(pn):
    total_pixs_page = []
    page_num = "00" + str(pn)
    list_url = ext_url(pn)
    for uu in list_url:
        jppG_uurl = getJPG(uu)
        total_pixs_page.extend(jppG_uurl)
    with open("./old/" + page_num + ".csv", 'a+', newline='') as f:
        write = csv.writer(f, delimiter=';')
        temp_list = [i.replace('"', '') for i in total_pixs_page]
        write.writerows([elt] for elt in temp_list)
    print(page_num, " processed!")


if __name__ == "__main__":

    page_start = 1
    page_end = 46

    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )
    Path("./old").mkdir(parents=True, exist_ok=True)
    page_num_rand = random.sample(range(page_start, page_end + 1), page_end - page_start + 1)
    for pn in page_num_rand:
        thread = threading.Thread(target=ext_csv, args=(pn,))
        thread.start()
        time.sleep(5)
        print("thread ", str(pn), " started on ", time.ctime(time.time()))