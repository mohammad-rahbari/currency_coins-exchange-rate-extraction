import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


import requests 
from bs4 import BeautifulSoup 


def putText(image, text,location ,font_size):
    fontFile = "files/B YEKAN.TTF"
    font = ImageFont.truetype(fontFile, font_size)


    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)   

    draw = ImageDraw.Draw(image)
    draw.text(location, bidi_text, (255,255,255), font=font)
    draw = ImageDraw.Draw(image)
    return image




data={} 

URL = "https://www.tgju.org/" 

try: 
    r = requests.get(URL, allow_redirects=False, timeout=10)
except requests.exceptions.Timeout as err: 
    print(err)


soup = BeautifulSoup(r.content, 'html5lib')
for i in soup.find_all('span'):
    if "dynamic-clock" in str(i):
        data["date"] = i.text.split("-")[0]



def get_price(url):
    print(url)
    try: 
        r = requests.get(url, allow_redirects=False, timeout=10)
    except requests.exceptions.Timeout as err: 
        print(err)
    soup = BeautifulSoup(r.content, 'html5lib')  

    for i in soup.find_all("h3"):
        if "نرخ فعلی" in str(i):
            result = i.find_all("span", attrs={"class":"value"})[0].findChildren()[0].text
    return result


data["dollar"] = get_price("https://www.tgju.org/profile/price_dollar_rl")
data["euro"] = get_price("https://www.tgju.org/profile/price_eur")
data["coin_ememi"] = get_price("https://www.tgju.org/profile/sekee")
data["coin_ba"] = get_price("https://www.tgju.org/profile/sekeb")
data["coin_half"] = get_price("https://www.tgju.org/profile/nim")
data["coin_quarter"] = get_price("https://www.tgju.org/profile/rob")


space_index = data['date'].index(" ")
data['date'] = f"{data['date'][:space_index]} {' '*(20 - len(data['date']))} {data['date'][space_index:]} "

print(data)


image = Image.open("files/frame.jpg")
putText(image,data['dollar'],(250, 725),55)
putText(image,data['euro'],(250, 835),55)

putText(image,data['coin_ememi'],(695, 1060),45)
putText(image,data['coin_ba'],(235, 1060),45)


putText(image,data['coin_ememi'],(695, 1245),45)
putText(image,data['coin_ba'],(235, 1245),45)


putText(image,data["date"],(580, 1680),41)

image =image.save(data["date"]+".jpg")