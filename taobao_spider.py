# -*- coding=utf-8 -*-
__author__ = 'Sr'
import re
import time
from urllib import request
import pymysql
#爬取任意中文关键字下淘宝商品信息，注意不止要在此处更换url，还需要在下层对第一页之后的内容更换url
def keyword():
    m = input('搜索关键字为')
    m_incode=str(m.encode())
    m_incode=m_incode.replace(r'\x','%')
    m_incode_search=re.search(r"b'(.*)'",m_incode)
    m_incode=m_incode_search.group(1)
    m_incode_search=m_incode.upper()
    return m_incode_search
def url_gen_first_page(m_incode_search):
    url = "https://s.taobao.com/search?q="+m_incode_search+"&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20161117&ie=utf8&sort=sale-desc"
    return url
def url_gen_next_pages(counter,keyword):
    url='https://s.taobao.com/search?q='+keyword+'&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20161117&ie=utf8&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s='+str(counter*44)
    return url
def conn_db():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='smallrig', charset='utf8mb4')
    return conn
def curosr_db(conn):
    cursor = conn.cursor()
    return cursor
def close_conn(conn,cursor):
    cursor.close()
    conn.close()
def crwal_first_page_data(url):
    rps = request.Request(url)
    rps.add_header('User-Agent', 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:47.0) Gecko/20100101 Firefox/47.0')
    while 1:
        try:
            response = request.urlopen(rps, timeout=5)  # timeout设置超时的时间
            html = response.read().decode('utf-8')
            # result = response.read()
            # print(result)
            response.close()
        except:
            print('time out and error page is ' + str(url))
            time.sleep(5)
            continue
        else:
            break
    return html
def html_quallist(html):
    qual = '"raw_title":".*?","shopcard'
    quallist = re.findall(qual, html)
    quallist = set(quallist)
    return quallist
def crawl_max_page(html):
    # response = request.urlopen(rps)
    # html = response.read().decode('utf-8')
    # qual = '"raw_title":"[^\"]*","pic_url"'
    qual = '"raw_title":".*?","shopcard'
    quallist = re.findall(qual, html)
    quallist = set(quallist)

    max_page = re.search('"totalPage":([0-9]*)', html)
    max_page = max_page.group(1)
    return max_page
def detail_insert(quallist,cursor):
    for qual_data in quallist:
        # print(url_product)
        # qual_data=list(quallist)[0]
        # url_product = url_product.encode()

        # 截取产品名称

        search_product = re.search('"raw_title":"(.*?)","', qual_data, re.M | re.I)
        product_name = search_product.group(1)
        # print(product_name)
        # 截取价格
        search_price = re.search('"reserve_price":"(.*?)","', qual_data, re.M | re.I)
        product_price = search_price.group(1)
        # print(product_price)
        # 截取付款人数
        search_pay_people = re.search('","view_sales":"([0-9]*)', qual_data, re.M | re.I)
        pay_people = search_pay_people.group(1)
        # print(pay_people)
        # 截取累计评论数
        search_comment = re.search('"comment_count":"(.*?)","', qual_data, re.M | re.I)
        comment = search_comment.group(1)
        if comment == '':
            comment = '0'
        # print(comment)
        # 截取商家名
        search_store = re.search('","nick":"(.*?)","', qual_data, re.M | re.I)
        store = search_store.group(1)
        # print(store)

        drop_txt = "drop TABLE taobao_spider"
        creat_txt = '''CREATE TABLE `taobao_spider` (
        `name`  varchar(255) NULL ,
        `price`  double(20,2) NULL ,
        `monthly_sell_num`  int(20) NULL ,
        `comment_num`  int(20) NULL ,
        `store`  varchar(255) NULL
        )
        ENGINE=MyISAM
        DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
        CHECKSUM=0
        DELAY_KEY_WRITE=1
        ;
        '''
        insert_txt = "INSERT INTO `taobao_spider` VALUES('" + str(product_name) + "'," + str(product_price) + "," + str(
            pay_people) + "," + str(comment) + ",'" + str(store) + "')"
        # update_txt="UPDATE `taobao_spider` SET `name` = "+str(product_name)+" WHERE product_name = '"+str(product_name)+"'"
        while 1:
            try:
                cursor.execute(insert_txt)
            except (pymysql.err.InterfaceError, pymysql.err.ProgrammingError):
                conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='smallrig',
                                       charset='utf8mb4')
                cursor = conn.cursor()
            # except pymysql.err.IntegrityError:
            #    while 1:
            #        try:
            #            cursor.execute(update_txt)
            #        except (pymysql.err.InterfaceError,pymysql.err.ProgrammingError):
            #            conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='smallrig',
            #                                   charset='utf8mb4')
            #            cursor = conn.cursor()
            #        else:break
            #    break
            else:
                break
        #print(
            #str(product_name) + ' price:' + str(product_price) + '  pay_people:' + str(pay_people) + '  comment:' + str(
                #comment) + '  store:' + str(store))

conn=conn_db()
cursor=curosr_db(conn)
keyword=keyword()
url=url_gen_first_page(keyword)
html=crwal_first_page_data(url)
quallist=html_quallist(html)
max_page=crawl_max_page(html)
detail_insert(quallist,cursor)
counter=1
while counter<int(max_page):
    url=url_gen_next_pages(counter,keyword)
    html = crwal_first_page_data(url)
    quallist = html_quallist(html)
    detail_insert(quallist, cursor)
    counter+=1
close_conn(conn, cursor)


