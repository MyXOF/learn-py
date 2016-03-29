# -*- encoding=utf-8 -*-

import pycurl
from io import BytesIO
import demjson

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://api.heweather.com/x3/weather?cityid=CN101220101&key=ad2f1de2a94640fcbc70c926d3b63b6f')
c.setopt(c.WRITEDATA, buffer)
c.setopt(pycurl.SSL_VERIFYHOST, False)
c.setopt(pycurl.SSL_VERIFYPEER, False)
c.perform()
c.close()
body = buffer.getvalue()
# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
json = body.decode('utf-8')

data = demjson.decode(json)
data = data['HeWeather data service 3.0']
data = data[0]
aqi = data['aqi']
basic = data['basic']
daily_forecast = data['daily_forecast']
hourly_forecast = data['hourly_forecast']
now = data['now']
status = data['status']
suggestion = data['suggestion']
print('aqi', aqi)
print('basic', basic)
print('daily_forecast', daily_forecast)
print('hourly_forecast', hourly_forecast)
print('now', now)
print('status', status)
print('suggestion', suggestion)
