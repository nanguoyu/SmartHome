# -*- coding: utf-8 -*-
import requests

key = "b355e4ca7a964580ba95230673e37a52"


def get_ip_address():
    # response = requests.get('http://tool.nanguoyu.us/ip.php')
    # return response.content.decode()
    return "123.138.87.11"


def get_city_name(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip
    req = requests.get(url)
    city = req.json()['data']['city']
    return city


def get_city_id(cityname):
    url = 'https://search.heweather.com/find?location=%s&key=%s' % (cityname, key)
    req = requests.get(url)
    cityId = req.json()["HeWeather6"][0]["basic"][0]["cid"]
    return cityId


def getWeather(city_id):
    '''获取city与id'''
    url = 'https://free-api.heweather.com/s6/weather/now?location=%s&key=%s' % (city_id, key)
    x = requests.get(url).json()
    '''数据解析'''
    out_tmp, out_hum = x["HeWeather6"][0]["now"]["tmp"], x["HeWeather6"][0]["now"]["hum"]

    urlLifeStyle = 'https://free-api.heweather.com/s6/weather/lifestyle?location=%s&key=%s' % (city_id, key)
    y = requests.get(urlLifeStyle).json()
    drsg = y["HeWeather6"][0]["lifestyle"][1]
    brf, txt = drsg['brf'], drsg['txt']
    # print(brf, txt)
    # print(out_tmp, out_hum)
    return out_tmp, out_hum, brf, txt


def weatherPrint():
    out_tmp, out_hum, brf, txt = getWeather(get_city_id(get_city_name(get_ip_address())[0:2]))
    outhum = str(out_hum) + '%'
    outtmp = str(out_tmp) + '度'
    return str("现在室外" + outtmp + " 湿度 " + outhum + "穿衣指数：" + brf.encode('utf8') + " " + txt.encode('utf8'))


if __name__ == '__main__':
    weatherPrint()
