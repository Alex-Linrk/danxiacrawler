from bs4 import BeautifulSoup
import requests
from housedetail import houseinfo
import threading
import insertdetails

headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
urls = ['https://danxiafangchan.anjuke.com/gongsi-esf/tongana/a363-b310-m402/',
        'https://danxiafangchan.anjuke.com/gongsi-esf/haicang/a363-b310-m402/',
        'https://danxiafangchan.anjuke.com/gongsi-esf/xiangana/a363-b310-m402/',
        'https://danxiafangchan.anjuke.com/gongsi-esf/jimei/a363-b310-m402/']
threads = []


def main():
    for itemUrl in urls:
        hostThread = threading.Thread(target=crewlerUrl, args=[itemUrl])
        hostThread.start()
        threads.append(hostThread)
    while True:
        lives = 0
        for activity in threads:
            if activity.isAlive():
                lives += 1
        if lives == 0:
            break


def crewlerUrl(url):
    threadmain = threading.Thread(target=houselsit, args=[url])
    threadmain.start()
    threads.append(threadmain)
    allpage = countpage(url)
    if len(allpage) < 1:
        return
    for page in allpage:
        newthread = threading.Thread(target=houselsit, args=[page])
        newthread.start()
        threads.append(newthread)


def houselsit(pageurl):
    source = requests.get(pageurl, headers=headers)
    sourcesoup = BeautifulSoup(source.text, 'html.parser')
    sourcesouphouselistcontent = sourcesoup.findAll(attrs={'class': 'houselist-mod houselist-mod-new'})
    listcontent = sourcesouphouselistcontent[0]
    sourcesouphouseitemcontent = BeautifulSoup(str(listcontent), 'lxml')
    itemlist = sourcesouphouseitemcontent.findAll(attrs={'class': 'list-item'})
    for content in itemlist:
        detailurl = content.find(attrs={'class': 'house-title'}).find('a').get('href')
        houseinfo = detailsmsg(detailurl)
        houseinfo.area = content.find(attrs={'class': 'details-item'}).findAll('span')[1].text
        houseinfo.total = str(content.find('strong').text) + '万'
        details = str(content.find(attrs={'class': 'comm-address'}).text).split()
        houseinfo.houseaddress = details[1]
        houseinfo.longitude, houseinfo.latitude = geocodeG(houseinfo.houseaddress)
        houseinfo.community = details[0]
        print(houseinfo.__dict__)
        insertdetails.intert_newdetails(houseinfo)


# 使用高德API
def geocodeG(address):
    par = {'address': address, 'key': '17c3dafb5516338e16cfa45628b08920'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    print(answer)
    GPS = answer['geocodes'][0]['location'].split(",")
    return GPS[0], GPS[1]


def detailsmsg(detailsurl):
    house = houseinfo()
    source = requests.get(detailsurl, headers=headers)
    sourcesoup = BeautifulSoup(source.text, 'html.parser')
    detailcol = sourcesoup.find(attrs={'class': 'houseInfoBox'})
    countmsg = str(detailcol.find(attrs={'class': 'house-encode'}).text)
    house.housecode = countmsg.split('，')[0].split('：')[1]
    house.releasetime = countmsg.split('，')[1].split('：')[1]
    house.downpayment = str(detailcol.find(attrs={'class', 'third-col detail-col'}).findAll('dd')[1].text).split()[0]
    house.unitprice = "".join(str(
        detailcol.find(attrs={'class', 'third-col detail-col'}).findAll('dd')[0].text).split())
    house.detailurl = detailsurl
    house.housetype = str(
        detailcol.find(attrs={'class', 'first-col detail-col'}).findAll('dd')[3].text).lstrip().rstrip()
    house.createdate = str(
        detailcol.find(attrs={'class', 'first-col detail-col'}).findAll('dd')[2].text).lstrip().rstrip()
    house.storey = str(
        detailcol.find(attrs={'class', 'second-col detail-col'}).findAll('dd')[-1].text).lstrip().rstrip()
    return house


def countpage(url):
    pagearr = []
    pagesource = requests.get(url, headers=headers)
    sourcesoup = BeautifulSoup(pagesource.text, 'lxml')
    pageitem = sourcesoup.find(attrs={'class': 'multi-page'})
    listpage = pageitem.findAll('a')
    for item in listpage:
        nexturl = item.get('href')
        if pagearr.count(nexturl) == 0:
            pagearr.append(nexturl)
    return pagearr


if __name__ == '__main__':
    # print(",".join("锦辉国际花园\xa0\r\n                            同安-同集北路-瑶江里101-128号".split()))
    main()
    # detailsmsg("https://danxiafangchan.anjuke.com/gongsi-esf/A1148009628.html?from=gsdp_esflist")
    # instertdetails.showallhouse()
