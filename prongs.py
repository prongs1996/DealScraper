#pip3 install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup, Comment
import urllib
from tkinter import *
import webbrowser

#to convert the query into url friendly format
def remove_whitespace(x):
	try:
		x = x.replace(" ", "+")
	except:
		pass
	return x

#to take input from user and return it in a search query
def TakeQuery():
	product_input = svalue.get()
	product_input = remove_whitespace(product_input)
	return product_input

#for amazon headers are needed
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}



def Searching():
	product_name = TakeQuery();

	#amazon
	try:
		search_query_amazon="https://www.amazon.in/s/url=search-alias%3Daps&field-keywords=" + product_name
		r1=requests.get(search_query_amazon, headers=headers)
		soup_amazon = BeautifulSoup(r1.content, 'html.parser')

	# This is fetching how much you save
	#amazonPrice = soup_amazon.findAll('span', class_='a-color-price')[0].contents[1].replace(',', '')

	#Getting the amazon url
		amazonLink = soup_amazon.findAll('a', class_='a-link-normal')[0]

		amazonPrice = soup_amazon.findAll('span', class_='a-price-whole')
		if(len(amazonPrice) > 0):
			amazonPrice = amazonPrice[0].string.replace(',', '')
		else:
	# fallback code for now, but shows how much you save. Most likely not required
			amazonPrice = soup_amazon.findAll('span', class_='a-color-price')[0].contents[1].replace(',', '')
	# print('yo!')
		amazonPrice=int(amazonPrice);

		amazonUrl = amazonLink['href']
	# Get the parameters to redirect to from search url
		for amzu in amazonUrl.split('&'):
	# Look for url to redirect to
			if amzu.find('url=') > -1:
				amazonUrl = amzu.split('=')[1]
				break
	# Decode the encoded string and remove the additional information
		amazonUrl = urllib.parse.unquote(urllib.parse.unquote(amazonUrl)).split('?')[0]
	except:
		amazonPrice = 'Product Unavailable'
		search_query_amazon = '----------'
		amazonUrl = '----------'


#flipkart
	try:
		search_query_flipkart="https://www.flipkart.com/search?q=" + product_name
		r2=requests.get(search_query_flipkart);
		soup_flipkart = BeautifulSoup(r2.content, 'html.parser')

		flipkartPrice = soup_flipkart.findAll('div', class_='_1vC4OE')[0].contents[-2].replace(',','')
		flipkartPrice = int(flipkartPrice)

		flipkartUrl = soup_flipkart.find('div', class_='_1vC4OE').parent.parent['href']
		flipkartUrl = 'https://www.flipkart.com' + flipkartUrl.split('?')[0]
	except:
		flipkartPrice = 'Product Unavailable'
		search_query_flipkart = '----------'
		flipkartUrl = '----------'


#snapdeal
	try:
		search_query_snapdeal="https://www.snapdeal.com/search?keyword="+product_name;
		r3=requests.get(search_query_snapdeal);
		soup_snapdeal = BeautifulSoup(r3.content, 'html.parser')

		snapdealPrice = soup_snapdeal.findAll('span', class_='product-price')[0]['data-price']
		snapdealPrice = int(snapdealPrice)
# snapdealUrl = soup_snapdeal.find('span', {'class': 'product-desc-rating'}).find('span', {'class':['dp-widget-link', 'noUdLine', 'hashAdded']}).findAll('a')[0]['href']
		snapdealUrl = soup_snapdeal.find('span', class_='product-price').parent.parent.parent['href']
	except:
		snapdealPrice = 'Product Unavailable'
		search_query_snapdeal = '----------'
		snapdealUrl = '----------'

	amazonTrigger=0
	flipkartTrigger=0
	snapdealTrigger=0

	if (amazonPrice <= flipkartPrice)and(amazonPrice <= snapdealPrice):
		amazonTrigger=1
	if (flipkartPrice <= amazonPrice)and(flipkartPrice <= snapdealPrice):
		flipkartTrigger=1
	if (snapdealPrice <= amazonPrice)and(snapdealPrice <= flipkartPrice):
		snapdealTrigger=1

	# -------------------TKINTER-----------------------


	Lb1.delete(0, END)
	LbPrice.delete(0, END)
	LbLink.delete(0, END)
	LbQuery.delete(0, END)
	LbDeal.delete(0, END)
	Lb1.insert(1, 'WebSite')
	Lb1.insert(2, '		')
	Lb1.insert(3, 'Amazon ')
	Lb1.insert(4, 'Flipkart')
	Lb1.insert(5, 'Snapdeal')
	LbPrice.insert(1, 'Price ( ₹ )')
	LbPrice.insert(2, '		')
	LbPrice.insert(3, amazonPrice)
	LbPrice.insert(4, flipkartPrice)
	LbPrice.insert(5, snapdealPrice)
	LbLink.insert(1, 'Direct Link')
	LbLink.insert(2, '		')
	LbLink.insert(3, amazonUrl)
	LbLink.insert(4, flipkartUrl)
	LbLink.insert(5, snapdealUrl)
	LbQuery.insert(1, 'Your Query Results')
	LbQuery.insert(2, '		')
	LbQuery.insert(3, search_query_amazon)
	LbQuery.insert(4, search_query_flipkart)
	LbQuery.insert(5, search_query_snapdeal)
	LbDeal.insert(1, '		')
	LbDeal.insert(2, '		')
	if (amazonTrigger == 1):
		LbDeal.insert(3, 'BEST DEAL!')
	else:
		LbDeal.insert(3, '		')
	if (flipkartTrigger == 1):
		LbDeal.insert(4, 'BEST DEAL!')
	else:
		LbDeal.insert(4, '		')
	if (snapdealTrigger == 1):
		LbDeal.insert(5, 'BEST DEAL!')
	else:
		LbDeal.insert(5, '		')
	Lb1.pack(side=LEFT)
	LbPrice.pack(side=LEFT)
	LbLink.pack(side=LEFT)
	LbQuery.pack(side=LEFT)
	LbDeal.pack(side=LEFT)



root = Tk(className="dealScraper")
root.geometry("1400x150")
svalue = StringVar()  # defines the widget state as string
w = Entry(root, textvariable=svalue, width=70)  # adds a textarea widget
w.pack()
Lb1 = Listbox(root, width=20)
LbPrice = Listbox(root, width=20)
LbLink = Listbox(root,width=80)
LbQuery = Listbox(root, width=90)
LbDeal = Listbox(root, width=20)
def internet(event):
    weblink = LbLink.get(ACTIVE)
    webbrowser.open(weblink)
def internet2(event):
    weblink = LbQuery.get(ACTIVE)
    webbrowser.open(weblink)
LbLink.bind( "<Double-Button-1>" , internet)
LbQuery.bind( "<Double-Button-1>" , internet2)
Enter = Button(root, text="Search", command=Searching,width=30,height=2)
Enter.pack()


root.mainloop()