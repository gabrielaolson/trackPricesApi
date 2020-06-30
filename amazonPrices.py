import requests
from bs4 import BeautifulSoup
import smtplib
import yaml
import os


URL = 'https://www.amazon.com.br/iPhone-Apple-Dourado-Tela-C%C3%A2mera/dp/B0762WTVBM/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=IKO19W66Q6OW&dchild=1&keywords=iphone+8&qid=1593528367&sprefix=iphone%2Caps%2C293&sr=8-1'

headers = {
    "User agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

keys = {}
with open(os.path.join(__location__, "keys.yml"), 'r+') as keys_file:
    keys = yaml.load(keys_file, Loader=yaml.FullLoader)


def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text().replace("R", "").replace("$", "").replace(".", "").replace(",",
                                                                                                                  ".")
    converted_price = float(price)
    if converted_price < 3.000:
        send_mail()

    print(converted_price)
    print(title.strip())

    if converted_price < 3.000:
        send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(keys["email"], keys["email_key"])

    subject = 'Price fell down'
    body = 'Check the amazon link https://www.amazon.com.br/iPhone-Apple-Dourado-Tela-C%C3%A2mera/dp/B0762WTVBM/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=IKO19W66Q6OW&dchild=1&keywords=iphone+8&qid=1593528367&sprefix=iphone%2Caps%2C293&sr=8-1'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'gabiolson@gmail.com',
        'gabriela.olson@icloud.com',
        msg
    )
    print('HEY EMAIL HAS BEEN SENT! ')

    server.quit()

check_price()
