import urllib.request
import bs4 as bs
#import email_to

from pymongo import MongoClient
import re
from DBConnection import cluster
from DBConnection import db
from DBConnection import collection
# connection to cluster
# Replace this string with your own connection string from Mongodb

db = db
cluster = cluster

def price_tag(price):
    kerem = re.findall('[0-9]+[,]?[0-9]+', price)
    newlist = []
    for i in kerem:
        for x in i:
            if x != ',':
                newlist.append(x)
            elif x == ',':
                newlist.append('.')
    # print('demene 1 ',newlist)
    newprice = "".join(newlist)
    # newprice = newprice[1:]
    price = float(newprice)
    # price = int(price[3:6])
    price_tag.tag = price



##the process if there is a sale
def sale_pozitiv(obj,actual_price):
    print(obj['seller_name'], obj['product_name'], 'is on sale!! =>  ',actual_price)
    print('##########################################')


## passing User Agent in header to bypass error code 403
def request(url):
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
    request.navi = soup.body


# function to add new product to database
def new_product():
    seller = input('please enter the website name such as otto,zara,amazon,hnm : ')
    urlmiz = input('please paste the url of the product: ')
    product_name = input('what would you like to call the product? : ')
    target_price = input('at what price would you like to get notified? : ')
    target_price = int(target_price)
    sale = 0
    # inserting to database by passing variables to a dictionary
    hashmap = {}
    hashmap["product_name"] = product_name
    hashmap["product_url"] = urlmiz
    hashmap["target_price"] = target_price
    hashmap["seller_name"] = seller
    hashmap["sale"] = sale
    collection.insert_one(hashmap)

    print('successfully inserted to database')


##this is to see all your products

def see_collection():
    for obj in collection.find({}):
        print(obj['seller_name'], obj['product_name'])

        print('expected price => ', obj['target_price'], 'EU')
        print('############################################')
        if KeyError:
            print("no data yet")

## function to delete the items that we have seen to be on sale
def delete_sale():
    delete_question = input('would you like to delete the items that are on sale ? :(y/n)')
    if delete_question == 'y':
        # print('here is the funktion to delete from database')
        q2 = input('are you sure?:  y/n')
        if q2 == 'y':
            collection.delete_many({"sale": 1})
            print('successfully deleted from database')

    else:
        print('dont do anything')


# updates sale field on database
def sale_update():
    old_query = {"sale": 0}
    new_query = {"$set": {"sale": 1}}
    collection.update_one(old_query, new_query)


# when there is no sale
def sale_negativ(obj, price):
    print(obj['seller_name'], obj['product_name'], 'still same => ', price)
    print('##########################################')


##running db queries to seek the prices

def price_check():
    for obj in collection.find({}):
        if obj['seller_name'] == 'otto':
            sauce = urllib.request.urlopen(obj['product_url']).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')

            nav = soup.body
            # print(nav)

            for div in nav.find_all('div', class_='prd_price__main js_prd_price__main'):
                price = div.get_text()
                price_tag(price)
                price = price_tag.tag
                price = float(price)
                if price < obj['target_price']:
                    sale_pozitiv(obj,price)
                    # send_email(urlmiz)
                else:
                    sale_negativ(obj,price)
        elif obj['seller_name'] == 'zara':
            url = obj['product_url']
            request(url)
            nav = request.navi
            for div in nav.find_all('span', class_='price__amount'):
                price = div.get_text()
                price_tag(price)
                price=price_tag.tag
                price = float(price)
                #price = int(price[3:6])

                if price <= obj['target_price']:
                    sale_update()
                    sale_pozitiv(obj, price)

                    # send_email()
                else:
                    sale_negativ(obj, price)
                    #print('sale_negative funktion')
        elif obj['seller_name'] == 'hnm':
            url = obj['product_url']
            request(url)
            nav = request.navi
            for div in nav.find_all('div', class_='primary-row product-item-price'):
                for div in div.find_all('span'):
                    price = div.get_text()
                    # price = int(price[1:4])
                    price_tag(price)
                    price = price_tag.tag
                    price = float(price)

                    if price <= int(obj['target_price']):

                        sale_pozitiv(obj, price)

                    else:
                        sale_negativ(obj,price)
                # print(price[44:51])
                # intprice = price[44:46]

                # print(len(price))

        elif obj['seller_name'] == 'amazon':
            url = obj['product_url']
            request(url)
            nav = request.navi
            for div in nav.find_all('span', class_='a-size-medium a-color-price priceBlockBuyingPriceString'):
                price = div.get_text()
                price_tag(price)
                price = price_tag.tag
                price = float(price)
                if price <= int(obj['target_price']):
                    sale_pozitiv(obj,price)

                    # send_email()
                else:
                    sale_negativ(obj,price)


        else:
            print('we only support zara,otto,hnm and amazon ...')
            print('#####################################')


# command line
print("to track a new product type 'add' to the console")
print("to see if there is any discount type 'check' to the console")
print("to see all your products type 'see' to the console")
print("to delete the items which are on sale type 'delete' to the console")
purpose = input('Please type your answer :')

if purpose == 'add':
    new_product()

elif purpose == 'see':
    see_collection()
elif purpose == 'delete':

    delete_sale()
elif purpose == 'check':

    price_check()
else:
    print('unknown command')
