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
    seller = input('please enter the website name such as otto,mediamarkt,zara,amazon,hnm : ')
    urlmiz = input('please paste the url of the product: ')
    product_name = input('what would you like to call the product? : ')
    target_price = input('at what price would you like to get notified? : ')
    target_price = int(target_price)

    # inserting to database by passing variables to a dictionary
    hashmap = {}
    hashmap["product_name"] = product_name
    hashmap["product_url"] = urlmiz
    hashmap["target_price"] = target_price
    hashmap["seller_name"] = seller
    collection.insert_one(hashmap)

    print('successfully inserted to database')


##this is to see all your products

def see_collection():
    for obj in collection.find({}):
        print(obj['seller_name'], obj['product_name'], 'expected price => ', obj['target_price'], 'EU')


##running db queries to seek the prices
# burada db icinde aratarak otto ise sunu yap media markt ise sunu yap demek lazim


def price_check():
    for obj in collection.find({}):
        if obj['seller_name'] == 'otto':
            sauce = urllib.request.urlopen(obj['product_url']).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')

            nav = soup.body
            # print(nav)

            for div in nav.find_all('span', id='oldPriceAmount'):
                oldprice = div.get_text()
                print('the old price is:', oldprice[:9])

            for div in nav.find_all('div', class_='prd_price__main js_prd_price__main'):

                price = div.get_text()
                print('the current price of the ', obj['product_name'], ' is:', price[:9])
                # print(price[3:6])
                fiyat = int(price[3:6])
                if fiyat < obj['target_price']:
                    print('the', obj['product_name'], 'is on sale!!')
                    print('##########################################')
                    # send_email()
                else:
                    print('the price', obj['product_name'], 'has not changed since')
                    print('##########################################')

        elif obj['seller_name'] == 'zara':
            url = obj['product_url']
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )

            f = urllib.request.urlopen(req)
            soup = bs.BeautifulSoup(f, 'lxml')
            nav = soup.body
            for div in nav.find_all('span', class_='price__amount'):
                price = div.get_text()
                price = int(price[3:6])

                if price <= obj['target_price']:
                    print('the', obj['product_name'], 'is on sale!!')
                    print('##########################################')
                    # send_email()
                else:
                    print('the price', obj['product_name'], 'has not changed since')
                    print('##########################################')
        elif obj['seller_name'] == 'hnm':
            url = obj['product_url']
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )

            f = urllib.request.urlopen(req)
            soup = bs.BeautifulSoup(f, 'lxml')
            nav = soup.body

            for div in nav.find_all('div', class_='primary-row product-item-price'):
                for i in div.find_all('span'):
                    price = str(i)

                    intprice = int(price[44:46])
                    if intprice < obj['target_price']:
                        print('the', obj['product_name'], 'is on sale!!')
                        print('##########################################')
                        # send_email()
                    else:
                        print('the price', obj['product_name'], 'has not changed since')
                        print('##########################################')

                    # print(price[44:51])
                    # intprice = price[44:46]

                    # print(len(price))

        else:
            print('we only support zara and otto ...')
            print('#####################################')


# command line
print("to track a new product type 'add' to the console")
print("to see if there is any discount type 'check' to the console")
print("to see all your products type 'see' to the console")

purpose = input('Please type your answer :')

if purpose == 'add':
    new_product()

if purpose == 'see':
    see_collection()
if purpose == 'check':
    price_check()
