import urllib.request
import bs4 as bs
import email_to

#sending email as a third party with yahoo mail.
def send_email():
    server = email_to.EmailServer('smtp.mail.yahoo.com', 587, 'automessage6@yahoo.com', 'arnpkayviqxuiijk')
    print('login success ')
    message='emailto test!'
    server.quick_email('orhank.ozbakir@gmail.com', 'TEST',
                   ['acele et indirim var', urlmiz],
                   style='h1 {color: blue}')

    print('message has been sent!!')

#the code to parse the target webpage and get the title and price ...This is just for Otto.de products

urlmiz=input('Please enter the url of product : ')

sauce=urllib.request.urlopen(urlmiz).read()
soup= bs.BeautifulSoup(sauce,'lxml')

nav=soup.body
#print(nav)

for div in nav.find_all('span',id='oldPriceAmount'):

    oldprice=div.get_text()
    print('the old price is:',oldprice[:9])

for div in nav.find_all('div',class_='prd_price__main js_prd_price__main'):

    price=div.get_text()
    print('the new price is:',price[:9])
    #print(price[3:6])
    fiyat=int(price[3:6])
    if fiyat<75:
        send_email()
    else:print('the price has not changed since')
