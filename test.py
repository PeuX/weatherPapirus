from papirus  import PapirusComposite
screen = PapirusComposite()

screen.AddImage('./icons/rain.bmp',0, 0,(20,20),"img_weather")
screen.AddText("text rain",50,0,20,'txt_weather')

screen.UpdateImg("img_weather",'./icons/clear.bmp')
screen.UpdateText("txt_weather","text clear")
