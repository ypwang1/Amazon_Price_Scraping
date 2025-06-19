import smtplib
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()

FROM= os.getenv("FROM")
TO= os.getenv("TO")
PASSWORD = os.getenv("PASSWORD")

URL="https://appbrewery.github.io/instant_pot/"

response = requests.get(url=URL)
html_doc =response.text
soup = BeautifulSoup(html_doc, "html.parser")
price_whole = soup.find(name="span", class_="a-price-whole").getText()
price_fraction = soup.find(name="span", class_="a-price-fraction").getText()
whole_price = float(price_whole + price_fraction)
print(whole_price)

if whole_price <= 100:
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=FROM, password=PASSWORD)
            connection.sendmail(from_addr=FROM, to_addrs=TO,
                                msg="Subject: PRICE DROP\n\n price of the cocking pot dropped under 100$")
    except:
        print("failed to send email")



# ANOTHER WAY OF PROCESSING:

    # try:
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.login(user=FROM, password=PASSWORD)
        # server.sendmail(from_addr=FROM, to_addrs=TO,
        #                     msg="Subject: PRICE DROP\n\n price of the cocking pot dropped under 100$")
    # except:
    #     print("failed to send email")