import forecastio
import time
from datetime import datetime
import numpy as np
import colorsys
import sys
from composite import PapirusComposite

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


wait = 1800

#ref_icons = dict(['clear',0],['clear-day',1],['clear-night',2],['cloudy',3],['fog',4],['hail',5],['NA',6],['partly-cloudy-day',7],['partly-cloudy-night',8],['rain',9],['sleet',10],['snow',11],['thunderstorm',12],['tornado',13],['wind',14])

screen = PapirusComposite(False)
hour = dict()
hour[4] = HourSet(0,0,0,0,'clear')
hour[8] = HourSet(0,0,0,0,'clear')
hour[12] = HourSet(0,0,0,0,'clear')

screen.AddImg('./icons/'+hour[4].icon+'.bmp',0, 0,(50,50),'i'+str(4))
text4 = "Maintenant\n T:"+str(hour[4].t)+" \ P:"+str(hour[4].p)+"%"
screen.AddText(text4,50,0,20,'t'+str(4))

screen.AddImg('./icons/'+hour[8].icon+'.bmp',0, 55,(50,50),'i'+str(8))
text8 = "+6h\n T:"+str(hour[8].t)+" \ P:"+str(hour[8].p)+"%"
screen.AddText(text8,50,55,20,'t'+str(8))

screen.AddImg('./icons/'+hour[12].icon+'.bmp',0, 110,(50,50),'i'+str(12))
text12 = "+10h\n T:"+str(hour[12].t)+" \ P:"+str(hour[12].p)+"%"
screen.AddText(text12,50,110,20,'t'+str(12))

#preparation des emplacement pour les mini icon sur les 12 prochain heures
screen.AddImg('./icons/clear.bmp',0, 158,(20,20),'i+0')
screen.AddImg('./icons/clear.bmp',22, 158,(20,20),'i+1')
screen.AddImg('./icons/clear.bmp',44, 158,(20,20),'i+2')
screen.AddImg('./icons/clear.bmp',66, 158,(20,20),'i+3')
screen.AddImg('./icons/clear.bmp',88, 158,(20,20),'i+4')
screen.AddImg('./icons/clear.bmp',110, 158,(20,20),'i+5')
screen.AddImg('./icons/clear.bmp',132, 158,(20,20),'i+6')
screen.AddImg('./icons/clear.bmp',154, 158,(20,20),'i+7')
screen.AddImg('./icons/clear.bmp',176, 158,(20,20),'i+8')
screen.AddImg('./icons/clear.bmp',198, 158,(20,20),'i+9')
screen.AddImg('./icons/clear.bmp',220, 158,(20,20),'i+10')
screen.AddImg('./icons/clear.bmp',242, 158,(20,20),'i+11')


while True:
    try:
        temp = np.array([])
        rain = 0
        tempMed = 0
        forecast = forecastio.load_forecast(api_key, lat, lng)
        byHour = forecast.hourly()
        
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
        text4 = "Maintenant\n T:"+str(hour[4].t)+" \ P:"+str(hour[4].p)+"%"
        screen.UpdateText('t'+str(4),text4)

        screen.UpdateImg('i'+str(8),'./icons/'+hour[8].icon+'.bmp')
        text8 = "+6h\n T:"+str(hour[8].t)+" \ P:"+str(hour[8].p)+"%"
        screen.UpdateText('t'+str(8),text8)

        screen.UpdateImg('i'+str(12),'./icons/'+hour[12].icon+'.bmp')
        text12 = "+10h\n T:"+str(hour[12].t)+" \ P:"+str(hour[12].p)+"%"
        screen.UpdateText('t'+str(12),text12)

        screen.WriteAll()
        time.sleep(wait)
    except KeyboardInterrupt:
        screen.Clear()
        sys.exit(-1)