import forecastio
import time
from datetime import datetime
import numpy as np
import colorsys
import sys
from pytz import timezone
from Composite import Composite

class HourSet():
    def __init__(self, tmax,tmin,t,p,icon):
        self.tmax = tmax
        self.tmin = tmin
        self.t = t
        self.p = p
        self.icon = icon

api_key = "DARK_SKY_API_KEY"
lat = 47.34638
lng = 0.45873

MAX_WIDTH       = 640
MAX_HEIGHT      = 384
wait = 1800

#ref_icons = dict(['clear',0],['clear-day',1],['clear-night',2],['cloudy',3],['fog',4],['hail',5],['NA',6],['partly-cloudy-day',7],['partly-cloudy-night',8],['rain',9],['sleet',10],['snow',11],['thunderstorm',12],['tornado',13],['wind',14])

screen = Composite(False)
hour = dict()
hour[4] = HourSet(0,0,0,0,'clear')
hour[8] = HourSet(0,0,0,0,'clear')
hour[12] = HourSet(0,0,0,0,'clear')

paris = timezone('Europe/Paris')
fmt = '%d/%m/%Y\n%H:%M'
now = datetime.now(paris)
fstLine = "Last update :\n"
title = now.strftime(fmt)
screen.AddText(fstLine+title,10,0,40,'title')


text4 = "Now"
screen.AddText(text4,340,0,20,'tup'+str(4),1)
screen.AddImg('./icons/'+hour[4].icon+'.bmp',455, 0,(100,100),'i'+str(4),1)
text4 = "Temp:"+str(hour[4].t)+"\nPluie:"+str(hour[4].p)+"%"
screen.AddText(text4,360,110,20,'t'+str(4))

text8 = "+6h"
screen.AddText(text8,20,150,20,'tup'+str(8),1)
screen.AddImg('./icons/'+hour[8].icon+'.bmp',135, 150,(100,100),'i'+str(8),1)
text8 = "Temp:"+str(hour[8].t)+"\nPluie:"+str(hour[8].p)+"%"
screen.AddText(text8,40,260,20,'t'+str(8))

text12 = "+10h"
screen.AddText(text12,340,150,20,'tup'+str(12),1)
screen.AddImg('./icons/'+hour[12].icon+'.bmp',455, 150,(100,100),'i'+str(12),1)
text12 = "Temp:"+str(hour[12].t)+"\nPluie:"+str(hour[12].p)+"%"
screen.AddText(text12,360,260,20,'t'+str(12))

#preparation des emplacement pour les mini icon sur les 12 prochain heures
screen.AddImg('./icons/clear.bmp',0, 320,(50,50),'i+0')
screen.AddText("+1h",0,370,15,'it+0')
screen.AddImg('./icons/clear.bmp',50, 320,(50,50),'i+1')
screen.AddText("+2h",50,370,15,'it+1')
screen.AddImg('./icons/clear.bmp',100, 320,(50,50),'i+2')
screen.AddText("+3h",100,370,15,'it+2')
screen.AddImg('./icons/clear.bmp',150, 320,(50,50),'i+3')
screen.AddText("+4h",150,370,15,'it+3')
screen.AddImg('./icons/clear.bmp',200, 320,(50,50),'i+4')
screen.AddText("+5h",200,370,15,'it+4')
screen.AddImg('./icons/clear.bmp',250, 320,(50,50),'i+5')
screen.AddText("+6h",250,370,15,'it+5')
screen.AddImg('./icons/clear.bmp',300, 320,(50,50),'i+6')
screen.AddText("+7h",300,370,15,'it+6')
screen.AddImg('./icons/clear.bmp',350, 320,(50,50),'i+7')
screen.AddText("+8h",350,370,15,'it+7')
screen.AddImg('./icons/clear.bmp',400, 320,(50,50),'i+8')
screen.AddText("+9h",400,370,15,'it+8')
screen.AddImg('./icons/clear.bmp',450, 320,(50,50),'i+9')
screen.AddText("+10h",450,370,15,'it+9')
screen.AddImg('./icons/clear.bmp',500, 320,(50,50),'i+10')
screen.AddText("+11h",500,370,15,'it+10')
screen.AddImg('./icons/clear.bmp',550, 320,(50,50),'i+11')
screen.AddText("+12h",550,370,15,'it+11')


while True:
    try:
        temp = np.array([])
        rain = 0
        tempMed = 0
        forecast = forecastio.load_forecast(api_key, lat, lng)
        byHour = forecast.hourly()
        now = datetime.now(paris)
        title = now.strftime(fmt)
        screen.UpdateText('title',fstLine+title)

        compteurHour = 0
        icon = 'clear'
        for hourlyData in byHour.data[:12]:
            screen.UpdateImg('i+'+str(compteurHour),'./icons/'+hourlyData.icon+'.bmp')

            if(hourlyData.precipProbability > rain):
                icon = hourlyData.icon
                rain = round(hourlyData.precipProbability*100)

            temp = np.append(temp, hourlyData.temperature)
            compteurHour = compteurHour + 1
            if(compteurHour % 4 == 0):
                hour[compteurHour].t = round(np.median(temp),1)
                hour[compteurHour].tmax = round(temp.max(),1)
                hour[compteurHour].tmin = round(temp.min(),1)
                hour[compteurHour].p = rain
                hour[compteurHour].icon = icon
                icon = 'clear'
                temp = np.array([])
                rain = 0
                tempMed = 0

        screen.UpdateImg('i'+str(4),'./icons/'+hour[4].icon+'.bmp')
        text4 = "Temp:"+str(hour[4].t)+"\nPluie:"+str(hour[4].p)+"%"
        screen.UpdateText('t'+str(4),text4)

        screen.UpdateImg('i'+str(8),'./icons/'+hour[8].icon+'.bmp')
        text8 = "Temp:"+str(hour[8].t)+"\nPluie:"+str(hour[8].p)+"%"
        screen.UpdateText('t'+str(8),text8)

        screen.UpdateImg('i'+str(12),'./icons/'+hour[12].icon+'.bmp')
        text12 = "Temp:"+str(hour[12].t)+"\nPluie:"+str(hour[12].p)+"%"
        screen.UpdateText('t'+str(12),text12)

        screen.WriteAll()
        time.sleep(wait)
    except KeyboardInterrupt:
        screen.Clear()
        sys.exit(-1)