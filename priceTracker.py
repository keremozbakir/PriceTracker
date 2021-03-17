import urllib.request
import bs4 as bs
import email_to
from pymongo import MongoClient

# connection to cluster
cluster = MongoClient(
    "mongodb+srv://kerem4022:kerem4022@nodetuts.7fmw3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["priceTracker"]
collection = db["priceTracker"]


# sending email as a third party with yahoo mail.
def send_email():
    server = email_to.EmailServer('smtp.mail.yahoo.com', 587, 'automessage6@yahoo.com', 'arnpkayviqxuiijk')
    print('login success ')
    message = 'emailto test!'
    server.quick_email('orhank.ozbakir@gmail.com', 'TEST',
                       ['acele et indirim var', urlmiz],
                       style='h1 {color: blue}')

    print('message has been sent!!')

# function to add new product to database
def new_product():
    urlmiz = input('Please enter the url of product : ')
    seller = input('please enter the website name such as otto,mediamarkt,zara,amazon,hnm : ')
    product_name = input('what would you like to call the product? : ')
    target_price = input('at what price would you like to get notified? : ')
    target_price = int(target_price)

    # inserting to database by passing variables to a dictionary
    hashmap = {}
    hashmap["produckt name"] = product_name
    hashmap["product url"] = urlmiz
    hashmap["target price "] = target_price
    hashmap["seller name"] = seller
    collection.insert_one(hashmap)

    print('successfully inserted to database')


# the code to parse the target webpage and get the title and price ...This is just for Otto.de products
purpose = input('would you like to track a new product? y/n :')
if purpose == 'y':
    new_product()









##running db queries to seek the prices
#burada db icinde aratarak otto ise sunu yap media markt ise sunu yap demek lazim


def price_check():
    if seller == 'otto':

        sauce = urllib.request.urlopen(urlmiz).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        nav = soup.body
        # print(nav)

        for div in nav.find_all('span', id='oldPriceAmount'):
            oldprice = div.get_text()
            print('the old price is:', oldprice[:9])

        for div in nav.find_all('div', class_='prd_price__main js_prd_price__main'):

            price = div.get_text()
            print('the new price is:', price[:9])
            # print(price[3:6])
            fiyat = int(price[3:6])
            if fiyat >= target_price:
                send_email()
            else:
                print('the price has not changed since')

    else:
        print('we are currently just supporting otto.de ....')
