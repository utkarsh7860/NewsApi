import flask
from flask import request, jsonify
from selenium import webdriver
import time
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json  



app = flask.Flask(__name__)


option = webdriver.ChromeOptions()
option.add_argument('headless')

# Here chrome webdriver is used
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver" ,options=option)


# A route to return all of the available entries in our catalog.
@app.route('/')
def news_api():
    article_link = request.args['article_link']


    url = 'https://outline.com/'+article_link

    # Opening the URL
    driver.get(url)
    #time.sleep(5)
    # Getting current URL
    get_url = driver.current_url

    # Printing the URL
    #print(get_url)
    driver.refresh()

    # Initialising string 
    ini_string = get_url

    # initializing string 
    sstring = 'https://outline.com/'

    code = ini_string.replace(sstring,'')

    url = 'https://outline.com/stat1k/'+code+'.html'


    response = requests.get(url)

    page_contents = response.text

    doc = BeautifulSoup(page_contents, 'lxml')

    # News Title
    title = doc.select('.yue h1')
    title = title[0].get_text()

    # News Author
    author = doc.select('.yue a')
    author = author[0].get_text().replace('â\x80º', '').strip()

    # News Date
    date = doc.select('.date')
    date = date[0].get_text()

    # Actual News
    content = []
    for data in doc.find_all("p"):
        content.append(data.get_text().replace('\n', ''))
    NewsContent = "".join(content)

    # News Image
    images = doc.select('.yue figure img')
    image_src = [x['src'] for x in images]
    related_img = []
    for image in image_src:
        related_img.append(image)
    ImageContent = " ; ".join(related_img)


    Total_news_data = {
        "News_Link":article_link,
        'News_Title': title,
        'News_Author':author,
        'News_Date': date,
        'News_Content':NewsContent,
        'News_Images':ImageContent,
    }

    return jsonify(Total_news_data)

if __name__ == "__main__":
      app.run(host='0.0.0.0',debug = True)
