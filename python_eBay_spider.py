# -*- coding=utf-8 -*-
__author__ = 'Sr'
import re
import time
from urllib import request
####################单独爬第一页
url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_sop=10&_nkw=camera+cage&rt=nc"
print(url)
# url="http://www.ebay.com/sch/i.html?_odkw=camera+cage&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.TRS0&_nkw=camera+cage&_sacat=0"
###########获取当页所有产品链接
rps = request.Request(url)
rps.add_header('User-Agent', 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:47.0) Gecko/20100101 Firefox/47.0')

while 1:
    try:
        response = request.urlopen(rps, timeout=10) #timeout设置超时的时间
        html = response.read().decode('utf-8')
        #result = response.read()
        #print(result)
    except :
        print ('time out and error page is '+str(url))
        time.sleep(60)
        continue
    else:
        break


#response = request.urlopen(rps)
#html = response.read().decode('utf-8')
qual = 'http://www.ebay.com/itm/[^\"]*'
quallist = re.findall(qual, html)
quallist = set(quallist)
################################
##########获取下一页链接（eBay有固定格式此处不需要）
# qual1='<td class="pagn-next" _sp="p2045573.m1686.l1581"><a  aria-label="Next page of results"  class="gspr next" href=".*"></a></td>'
# link_nextpage=re.findall(qual1,html)
# print(str(link_nextpage))
#####################################################
# print(quallist)
# print(response.read())

response.close()
for url_product in quallist:
    # print(url_product)
    # url_product=list(quallist)[0]
    # url_product = url_product.encode()

    # 截取产品名称
    search_product = re.search(r'http://www.ebay.com/itm/(.*)-/', str(url_product), re.M | re.I)
    # res=url_product.search(url_product).groups()
    product_name = search_product.group(1)
    #############

    rps_product = request.Request(url_product)
    rps_product.add_header('User-Agent', 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:47.0) Gecko/20100101 Firefox/47.0')
    while 1:
        try:
            response_product = request.urlopen(rps_product, timeout=10)  # timeout设置超时的时间
            html_1 = response_product.read().decode('utf-8')
            # result = response.read()
            # print(result)
        except:
            print('time out and error page is '+str(url_product))
            time.sleep(20)
            continue
        else:
            break

   # response_product = request.urlopen(rps_product)
    #html_1 = response_product.read().decode('utf-8').timeout(20)

    qual1 = '[1-9]* sold</a></span>'
    sold_num = re.findall(qual1, html_1)
    if sold_num == []:
        sold_num = ['0 sold</a></span>']
    search_sold_num = re.search(r'([0-9]*) sold</a></span>', str(sold_num), re.M | re.I)
    sold_num = search_sold_num.group(1)
    # f = open(r'C:\Users\LQ\Documents\QQEIM Files\3001162039\FileRecv\第三方平台简单运营统计\第三方平台\源码.txt', 'a',encoding='UTF-8 ')
    # f.write(str(html_1))
    # f.close()
    print(str(product_name) + '  sold:' + str(sold_num))
    time.sleep(5)






    counter = 2
    while counter < 200:
        print(counter)
        url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_sop=10&_nkw=camera+cage&_pgn=1&_skc=50&rt=nc"
        print(url)
        # url="http://www.ebay.com/sch/i.html?_odkw=camera+cage&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.TRS0&_nkw=camera+cage&_sacat=0"
        ###########获取当页所有产品链接
        rps = request.Request(url)
        rps.add_header('User-Agent', 'Mozilla/5.0(Windows NT 6.1;WOW64;rv:47.0) Gecko/20100101 Firefox/47.0')

        while 1:
            try:
                response = request.urlopen(rps, timeout=10)  # timeout设置超时的时间
                html = response.read().decode('utf-8')
                # result = response.read()
                # print(result)
            except:
                print('time out and error page is ' + str(url))
                time.sleep(60)
                continue
            else:
                break



        #response = request.urlopen(rps)
        #html = response.read().decode('utf-8')
        qual = 'http://www.ebay.com/itm/[^\"]*'
        quallist = re.findall(qual, html)
        quallist = set(quallist)
        ################################
        ##########获取下一页链接（eBay有固定格式此处不需要）
        # qual1='<td class="pagn-next" _sp="p2045573.m1686.l1581"><a  aria-label="Next page of results"  class="gspr next" href=".*"></a></td>'
        # link_nextpage=re.findall(qual1,html)
        # print(str(link_nextpage))
        #####################################################
        # print(quallist)
        # print(response.read())

        response.close()
        for url_product in quallist:
            # print(url_product)
            # url_product=list(quallist)[0]
            # url_product = url_product.encode()

            # 截取产品名称
            search_product = re.search(r'http://www.ebay.com/itm/(.*)-/', str(url_product), re.M | re.I)
            # res=url_product.search(url_product).groups()
            product_name = search_product.group(1)
            #############

            rps_product = request.Request(url_product)
            rps_product.add_header('User-Agent',
                                   'Mozilla/5.0(Windows NT 6.1;WOW64;rv:47.0) Gecko/20100101 Firefox/47.0')

            while 1:
                try:
                    response_product = request.urlopen(rps_product, timeout=10)  # timeout设置超时的时间
                    html_1 = response_product.read().decode('utf-8')
                    # result = response.read()
                    # print(result)
                except:
                    print('time out and error page is ' + str(url_product))
                    time.sleep(20)
                    continue
                else:
                    break

            #response_product = request.urlopen(rps_product)
            #html_1 = response_product.read().decode('utf-8')

            qual1 = '[1-9]* sold</a></span>'
            sold_num = re.findall(qual1, html_1)
            if sold_num == []:
                sold_num = ['0 sold</a></span>']
            search_sold_num = re.search(r'([0-9]*) sold</a></span>', str(sold_num), re.M | re.I)
            sold_num = search_sold_num.group(1)
            # f = open(r'C:\Users\LQ\Documents\QQEIM Files\3001162039\FileRecv\第三方平台简单运营统计\第三方平台\源码.txt', 'a',encoding='UTF-8 ')
            # f.write(str(html_1))
            # f.close()
            print(str(product_name) + '  sold:' + str(sold_num))
            time.sleep(5)
        counter += 1
