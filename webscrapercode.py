from bs4 import BeautifulSoup
import urllib.error,urllib.parse,urllib.request
import pandas
import csv
import json

def scraping(url):
    html=urllib.request.urlopen(url)

    soup=BeautifulSoup(html)
    title=soup.findAll("a",{'class':"catalog-item-name"})  #finding title tag using inspect element in webpage
    titles=[]
    for i in range(0,len(title)):
        titles.append(title[i].get_text())
    price = [x.get_text() for x in soup.find_all("span",{"class":"price"})] #finding price tag
    x=len(price)
    for i in range(x):
        prices=price[i][1:]
    prices=float(prices)                                            #converting price into float
    stock_status=soup.find_all("span",{"class":"status"})           #finding stocks of product
    stock_st=[]
    stock_st_mod=[]
    for i in range(0,len(stock_status)):
        stock_st.append(stock_status[i].get_text())
        if stock_st[i]=='Out of Stock':                                       
            stock_st_mod.append('False')
        else:
            stock_st_mod.append('True')
    manufacturers = [x.get_text() for x in soup.find_all("a",{"class":"catalog-item-brand"})] #finding manufacturer
    df=pd.DataFrame()                                                 #dataframing the information
    df['title']=titles
    df['price']=prices
    df['status']=stock_st_mod
    df['manufacturer']=manufacturers
    df.to_csv('projectpython.csv')                                   #converting it into csv file
    

def csv_to_json(csvFilePath, jsonFilePath):                         #creating json format
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'a', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
          

pages = [1]
x=len(pages)
for i in range(x):
    url = 'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={}'.format(pages[i])
   # print(new_url)
    scraping(url)
    print(url)
    csvFilePath = r'projectpython.csv'
    jsonFilePath = r'projectpython.json'
    csv_to_json(csvFilePath, jsonFilePath)
