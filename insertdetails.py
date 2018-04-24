import sqlite3
from housedetail import houseinfo

dbfile = 'housedetails.db'
tableexist = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' and name = 'house'"
createtable = '''CREATE TABLE house (housecode text primary key ,
              releasetime text,houseaddress text,community text,area text,total text,
              unitprice text,storey text, detailurl text,downpayment text,createdate text,
              housetype text,longitude text,latitude text)'''
insertnewhouse = '''insert into house (releasetime, housecode, houseaddress,
 community, area, total, unitprice, storey, detailurl,
  downpayment, createdate, housetype,longitude,latitude ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
houseexist = '''SELECT housecode FROM house WHERE housecode like ?'''
showhouselist = '''SELECT * FROM house'''


def intert_newdetails(housedetail):
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute(tableexist)
    values = cursor.fetchall()
    if values.pop(0)[0] == 0:
        cursor.execute(createtable)
    insertdate(cursor, housedetail)
    conn.commit()
    conn.close()


def insertdate(cursor, housedetail):
    values = cursor.execute(houseexist, (housedetail.housecode,)).fetchall()
    if not values:
        cursor.execute(insertnewhouse, (housedetail.releasetime, housedetail.housecode,
                                        housedetail.houseaddress, housedetail.community,
                                        housedetail.area, housedetail.total,
                                        housedetail.unitprice, housedetail.storey,
                                        housedetail.detailurl, housedetail.downpayment,
                                        housedetail.createdate, housedetail.housetype,
                                        housedetail.longitude, housedetail.latitude))
        cursor.close()
        print(cursor.rowcount)


def showallhouse():
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute(tableexist)
    values = cursor.fetchall()
    if values.pop(0)[0] == 1:
        values = cursor.execute(showhouselist).fetchall()
        print(len(values))
        print(values)
    return sqlDate2Objcet(values)


def sqlDate2Objcet(values):
    objList = []
    for item in values:
        houseItem = houseinfo()
        houseItem.housecode = item[0]
        houseItem.releasetime = item[1]
        houseItem.houseaddress = item[2]
        houseItem.community = item[3]
        houseItem.area = item[4]
        houseItem.total = item[5]
        houseItem.unitprice = item[6]
        houseItem.storey = item[7]
        houseItem.detailurl = item[8]
        houseItem.downpayment = item[9]
        houseItem.createdate = item[10]
        houseItem.housetype = item[11]
        houseItem.longitude = item[12]
        houseItem.latitude = item[13]
        objList.append(houseItem)
    for house in objList:
        print(house.__dict__)
    return objList
