# OttoPriceTracker
This programme helps you to track certain products price and get notified by email on sale immediately.
It works just on otto.de at the moment more options will come.

There are a few things you have to do before running the programme
1-)Set up smtp settings according to your own email address.i used yahoo mail.You can also use gmail. But dont forget to allow
third party access to the sender email.Change the sender and receiver email addresses.


2-)Set up using your own mongodb database.Ofcourse with your database username and password.

Note:The programme isnt finished at the moment .i will continue to add more and more websites to choose from

After these settings are done you need to go to otto.de and copy a link of a product .Here is an example link you can use: https://www.otto.de/p/call-of-duty-modern-warfare-xbox-one-904656898/#variationId=904656899
paste this link when it is asked.Then you will be asked a product name.Product name is the name you want to save the product in to mongodb database.it can be anything
The target price is the price you want to get notified .For example the product is 90 Euros and when it is 70 Euros you want to be notified.Just write 70 to the target price.It is pretty straight forward actually.

P.S : the programme isnt finished yet.

