# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
import time
from selenium import webdriver

import tweepy
import json
from config import consumer_key, consumer_secret, access_token, access_token_secret

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    # create dictionary for scraped data
    mars_data = {}
    # NASA Mars News
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html = browser.html
    soup = bs(html, 'html.parser')
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    
    mars_data["news_data"] = news_date
    mars_data["news_title"] =news_title
    mars_data["news_p"] = news_p

    # JPL Mars Space Images - Featured Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://jpl.nasa.gov"+image
    mars_data["featured_image_url"] = featured_image_url

    # Mars Weather
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    target_user = "marswxreport"
    latest_tweet = api.user_timeline(target_user, count = 1)
    mars_weather = latest_tweet[0]['text']
    mars_data["mars_weather"] = mars_weather

    # Mars Facts
    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    type(tables)
    df = tables[0]
    df.columns = ['Mars', 'Data']
    mars_table = df.set_index('Mars')
    marsinfo = mars_table.to_html(classes='marsinfo')
    marsinfo = marsinfo.replace('\n', '')
    mars_data["mars_table"] = marsinfo

    # Mars Hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_hemis=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_ ="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
    
    mars_data['mars_hemis'] = mars_hemis

    return mars_data