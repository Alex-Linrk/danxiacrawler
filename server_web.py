#! usr/env/bin python
# -*-encoding:gbk-*-
import web
import importlib
import sys
import insertdetails
import json
from housedetail import houseinfo

importlib.reload(sys)

urls = (
    '/show', 'Show',
    '/(.*)', 'Index',
)

app = web.application(urls, globals())
render = web.template.render('templates/', cache=False)


class Index:
    def GET(self, name):
        print('index-------')
        print(name)
        for case in Switch(name):
            if case('$config.templates/map.js'):
                return open(r'./templates/map.js', 'rb').read()
            if case('$config.templates/myrequest.js'):
                return open(r'./templates/myrequest.js', 'rb').read()
            else:
                return open(r'./templates/index.html', 'rb').read()


class Show:
    def GET(self):
        print('------------------')
        return json.dumps(insertdetails.showallhouse(), cls=HouseInfoEncoder)


class HouseInfoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, houseinfo):
            print(obj.__dict__)
            return "{\"housecode\":\"" + obj.housecode + \
                   "\",\"releasetime\":\"" + obj.releasetime + \
                   "\",\"houseaddress\":\"" + obj.houseaddress + \
                   "\",\"community\":\"" + obj.community + \
                   "\",\"area\":\"" + obj.area + \
                   "\",\"total\":\"" + obj.total + \
                   "\",\"unitprice\":\"" + obj.unitprice + \
                   "\",\"storey\":\"" + obj.storey + \
                   "\",\"detailurl\":\"" + obj.detailurl + \
                   "\",\"downpayment\":\"" + obj.downpayment + \
                   "\",\"createdate\":\"" + obj.createdate + \
                   "\",\"housetype\":\"" + obj.housetype + \
                   "\",\"longitude\":\"" + obj.longitude + \
                   "\",\"latitude\":\"" + obj.latitude + "\"}"
        return json.JSONEncoder.default(self, obj)


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *arges):
        if self.fall or not arges:
            return True
        elif self.value in arges:
            self.fall = True
            return True
        else:
            return False

    if __name__ == '__main__':
        app.run()
