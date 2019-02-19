import json
import urllib.request
from datetime import date, datetime
import requests
import time

# Globaali muuttuja menua varten
menu = {}

def getMenu():
    global menu
    # Määritetään päivämäärä
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    # Muodostetaan url päivän ruokalistalle
    url = "https://www.sodexo.fi/ruokalistat/output/daily_json/31332/"+str(year)+"/"+str(month)+"/"+str(day)+"/fi"


    # Haetaan päivän ruokalista Sodexolta
    response = urllib.request.urlopen(url).read()
    menu = json.loads(response.decode("utf-8"))

def sendToDiscord():
    global menu
    # Rakennetaan WebHook
    data = {"content":"Sodexo Riihimäki"}
    embeds = []

    for course in menu["courses"]:
        embeds.append({"title":course["category"], "description":course["title_fi"]})

    data["embeds"] = embeds

    # Määritellään lähetettävän POST-pyynnön otsaketiedot ja url
    headers = {'Content-Type':'application/json'}
    webhookURL = "WEBHOOK_URL"

    # Lähetetään pyyntö
    r = requests.post(webhookURL,data = json.dumps(data), headers = headers)

def main():
    lastUpdate = 0
    while(True):
        now = datetime.now() # Aika nyt
        today = date.today().day # Kuukaudenpäivä
        weekday = date.today().isoweekday() # Viikonpäivä

        # HAETAAN ruokalista ja lähetetään se discordiin JOS
        #   - Kello on 6 (UTC), eli klo 8 (UTC+2)
        #   - Ruokalistaa ei ole vielä haettu tänään
        #   - Viikonpäivä on 1-5 (ma-pe)
        if (now.hour == 6 and today != lastUpdate and weekday<6):
            getMenu()
            sendToDiscord()
            lastUpdate = today

        # Odotetaan 30 minuuttia, ennen seuraavaa tarkastusta
        time.sleep(1800) 


if __name__ == "__main__":
    main()