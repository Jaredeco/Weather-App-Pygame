import pygame
import requests
from datetime import datetime
from datetime import timedelta
import pytz
import matplotlib.pyplot as plt

pygame.init()
pygame.display.set_caption('Weather')
screen_width = 1000
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
logo = pygame.image.load('weather_images/logo.png')
pygame.display.set_icon(logo)
FONT = pygame.font.Font(None, 32)
f_t = pygame.font.Font(None, 37)
white = (255, 255, 255)
red = (238, 59, 59)
black = (0, 0, 0)
green = (127, 255, 0)
clock = pygame.time.Clock()
FPS = 60
plt.style.use('fivethirtyeight')

bg = pygame.image.load('weather_images/bg.png')
rainy = pygame.image.load('weather_images/rain.png')
sunny = pygame.image.load('weather_images/sunny.png')
cloudy = pygame.image.load('weather_images/cloudy.png')
anemometer = pygame.image.load('weather_images/anemometer.png')
snowy = pygame.image.load('weather_images/snow.png')

er = False
name = ''
days = ['Today', 1, 2, 3, 4, 5, 6, 7]
temper = []
fore_temps = []


class InputBox(object):
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = black
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global name, description, temp, wind_speed, latitude, longitude, er, dom, feel, time, hum, pres, day, temper, offset, min_temp, max_temp
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = red if self.active else black
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.color = black
                    self.active = False
                    name = self.text
                    API_key = "9a38794d0adcf6788479964bf571f787"
                    base_url = "http://api.openweathermap.org/data/2.5/weather?"
                    fore_url = 'http://api.openweathermap.org/data/2.5/forecast?'
                    fore_final = fore_url + 'q=' + name + '&appid=' + API_key
                    Final_url = base_url + "appid=" + API_key + "&q=" + name
                    fore_data = requests.get(fore_final).json()
                    weather_data = requests.get(Final_url).json()
                    try:
                        if name != '':
                            dom = weather_data['sys']['country']
                            temp = int(weather_data['main']['temp'] - 273.15)
                            min_temp = int(weather_data['main']['temp_min'] - 273.15)
                            max_temp = int(weather_data['main']['temp_max'] - 273.15)
                            feel = int(weather_data['main']['feels_like'] - 273.15)
                            wind_speed = weather_data['wind']['speed']
                            description = weather_data['weather'][0]['description']
                            hum = weather_data['main']['humidity']
                            pres = weather_data['main']['pressure']
                            latitude = weather_data['coord']['lat']
                            longitude = weather_data['coord']['lon']
                            offset = (weather_data['timezone'] / 3600) - 1
                            for item in fore_data['list']:
                                temper.append(item['main']['temp'])
                                # days.append()
                                if len(temper) % 5 == 0 and len(temper) > 0:
                                    fore_temp = int((sum(temper[(len(temper) - 5):]) / 5) - 273.15)
                                    fore_temps.append(fore_temp)
                            plt.figure(figsize=(5.9, 4.5))
                            plt.clf()
                            plt.rcParams['text.color'] = 'red'
                            plt.title('Average temperature next 7 days', y=1.02)
                            plt.plot(days, fore_temps, '--go')
                            fore_temps.clear()
                            plt.savefig('weather_images/plot.png', transparent=True)
                            er = False
                    except:
                        er = True
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(250, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, win):
        if self.text == '' and not self.active:
            sug = FONT.render('Enter location', True, self.color)
            win.blit(sug, (self.rect.x + 5, self.rect.y + 5))
        win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(win, self.color, self.rect, 2)


def redrawWin():
    win.blit(bg, (0, 0))
    if not er:
        if name != '':
            ci = FONT.render(name.upper(), True, white)
            win.blit(ci, (25, 70))
            x = 25
            for i in range(len(name)):
                x += 19
            do = FONT.render(dom.upper(), True, red)
            win.blit(do, (x, 70))
            t = FONT.render(str(temp) + '°C', True, white)
            win.blit(t, (25, 110))
            fe = FONT.render('FEEL : ' + str(feel) + '°C', True, red)
            win.blit(fe, (95, 110))
            mt = FONT.render('MIN : ' + str(min_temp) + '°C', True, white)
            win.blit(mt, (25, 150))
            mxt = FONT.render('MAX : ' + str(max_temp) + '°C', True, red)
            win.blit(mxt, (150, 150))
            if 'clouds' in description:
                win.blit(cloudy, (25, 190))
                des = FONT.render(description.upper(), True, white)
                win.blit(des, (112, 215))
            elif 'clear' in description:
                win.blit(sunny, (25, 190))
                des1 = FONT.render(description.upper(), True, white)
                win.blit(des1, (112, 215))
            elif 'rain' in description or 'storm' in description:
                win.blit(rainy, (25, 190))
                des2 = FONT.render(description.upper(), True, white)
                win.blit(des2, (112, 215))
            elif 'snow' in description:
                win.blit(snowy, (25, 190))
                des3 = FONT.render(description.upper(), True, white)
                win.blit(des3, (112, 215))
            else:
                win.blit(cloudy, (25, 190))
                des = FONT.render(description.upper(), True, white)
                win.blit(des, (112, 215))
            win.blit(anemometer, (25, 255))
            ws = FONT.render(str(wind_speed) + ' m/s', True, white)
            win.blit(ws, (112, 283))
            pre = FONT.render('PRESSURE : ' + str(pres) + ' hPA', True, white)
            win.blit(pre, (25, 335))
            hu = FONT.render('HUMIDITY : ' + str(hum) + ' %', True, white)
            win.blit(hu, (25, 375))
            lat = FONT.render('LAT :  ' + str(latitude), True, white)
            win.blit(lat, (25, 415))
            lon = FONT.render('LON :  ' + str(longitude), True, white)
            win.blit(lon, (25, 455))
            plot = pygame.image.load('weather_images/plot.png')
            win.blit(plot, (400, 65))
            tz = pytz.timezone('Europe/London')
            time = datetime.now(tz)
            tm = timedelta(hours=offset)
            location_time = str(time + tm)
            lt = f_t.render(location_time[10:19] , True, black)
            win.blit(lt, (290, 21))
            dt = f_t.render(location_time[5:7] + '/' + location_time[8:10] + ' ' + location_time[0:4], True, green)
            win.blit(dt, (415, 21))

    else:
        err = FONT.render('LOCATION NOT FOUND!', True, red)
        win.blit(err, (110, 90))
    input_box1.draw(win)
    pygame.display.update()


input_box1 = InputBox(15, 15, 140, 32)
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        input_box1.handle_event(event)
    input_box1.update()
    redrawWin()
pygame.quit()