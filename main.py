from  selenium import webdriver
import smtplib
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import time


load_dotenv()



FROM= os.getenv("FROM")
TO= os.getenv("TO")
PASSWORD = os.getenv("PASSWORD")

URL="https://appbrewery.github.io/instant_pot/"
ZALANDO_URL = "https://www.zalando.nl/birkenstock-muiltjes-concretegray-bi112i01b-c11.html"
AMAZON_URL ="https://www.amazon.nl/-/en/BIRKENSTOCK-2570-576080-2570-576088-2570-576120-2570-576128/dp/B00H2NMBI2/ref=sr_1_2?dib=eyJ2IjoiMSJ9.oE9kZo9hna5G4X4J2pEFtCuFwG5qg1ZPrB8DZEU8Sf637qv7KiZOQAQaSWRg0trzf4epo7uaB3pp1AdadlnJJb_ocA3WKmgCP7ShSL-YluLmxp9wtpSlubCD9wA_nPh8lYAbxaPawO-ozAb-WnxPcA4PPXownjQ-PmJkGspKWLFLfO_DWGQNb6pv9ELm4-WDB_HvuHjx6zUWFiEfaGWdMjkkfC4GzKSUUgSs-gqKO6sERlqHGGeVq5IB4FISQO2DQY_qTC3654h7Z1tvEW5yovpyQRHIApielclHzfARymM.yf_JQ2QMZXB-BASotvc3C1aS-wH00SbXH2qqSC6tZvw&dib_tag=se&qid=1750326400&refinements=p_4%3ABirkenstock&s=fashion&sr=1-2&th=1"


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}



# Amazon Scraping
# response = requests.get(url=AMAZON_URL, headers=headers)
#
# html_doc =response.text
# soup = BeautifulSoup(html_doc, "html.parser")
# print(soup.prettify())
# price_whole = soup.find(name="span", class_="a-price-whole").getText()
# print(price_whole)
# price_fraction = soup.find(name="span", class_="a-price-fraction").getText()
# print(price_fraction)
# whole_price = float((price_whole + price_fraction))
# print(whole_price)



# Zalando Scraping. Due to javascript dynamically renders the website. Hence, need to use module Selenium

driver =webdriver.Chrome()
driver.get(url=ZALANDO_URL)
time.sleep(5)
html_doc = driver.page_source
soup = BeautifulSoup(html_doc, "html.parser")
price= soup.find(name="span", class_="Km7l2y").getText()
if price:
    price_actual = price.replace("\xa0", " ").split(" ")[-1]
    price_whole = price_actual.split(",")[0]
    price_fraction = price_actual.split(",")[-1]
    whole_price = float(f"{price_whole}.{price_fraction}")
else:
    price = "Price not found"
print(price)


# Send emails under certain price amount

if whole_price <= 150:
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=FROM, password=PASSWORD)
            connection.sendmail(from_addr=FROM, to_addrs=TO,
                                msg="Subject: PRICE DROP\n\n price of the item dropped under 150euros")
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