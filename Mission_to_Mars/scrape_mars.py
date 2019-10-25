import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver

def init_browser():
	executable_path = {"executable_path": "Mission_to_Mars/chromedriver"}
	return Browser("chrome", **executable_path, headless=False)

def scrape():
	mars_data = {}

	mars_data['news_data'] = nasa_mars_news()
	mars_data['featured_image_url'] = jpl_images()
	mars_data['mars_weather'] = mars_weather()
	mars_data['mars_facts'] = mars_facts()
	mars_data['mars_hemispheres'] = mars_hemispheres()

	return mars_data

def nasa_mars_news():
	nasa_news_data = {}

	nasa_news_url = 'https://mars.nasa.gov/news/'
	response_1 = requests.get(nasa_news_url)                                               

	nasa_soup = bs(response_1.text, 'html.parser')

	soup_div = nasa_soup.find(class_="slide")                                  
	news_title = (soup_div.find(class_="content_title").a.get_text())[1:-1]                                           
	news_paragraph = (soup_div.find(class_="rollover_description_inner").get_text())[1:-1]

	nasa_news_data['news_title'] = news_title
	nasa_news_data['news_paragraph'] = news_paragraph

	return nasa_news_data

def jpl_images():
	#
	browser = init_browser()
	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(jpl_url)
	time.sleep(1)

	# Scrape page into soup
	html = browser.html
	soup = bs(html, 'html.parser')

	# Find the src for the first image
	jpl_fullsize_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/'

	relative_image_path = soup.find_all('img')[3]["src"]

	image_id = relative_image_path[-20:-12]
	featured_image_url = jpl_fullsize_url + image_id + '_hires.jpg'

	browser.quit()

	return featured_image_url

def mars_weather():
	# visit jpl website
	browser = init_browser()
	tweet_url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(tweet_url)
	time.sleep(1)

	# Scrape page into soup
	html = browser.html
	soup = bs(html, 'html.parser')

	mars_weather = (soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text())[:-30]

	browser.quit()

	return mars_weather

def mars_facts():
	facts_url = 'https://space-facts.com/mars/'

	fact_list = pd.read_html(facts_url)

	facts_df = fact_list[1]

	facts_table = facts_df.to_html(header=False, index=False)

	return facts_table

def mars_hemispheres():
	# Visit jpl website
	browser = init_browser()
	usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(usgs_url)
	time.sleep(1)

	# Scrape page into soup
	html = browser.html
	soup = bs(html, 'html.parser')

	products = soup.find('div', class_='collapsible results')                       
	hemispheres = products.find_all('div', class_='item')

	hemisphere_image_urls = []                                                                      

	for hemisphere in hemispheres:         
		title = hemisphere.find('div', class_='description')
	
		title_text = title.a.text                                
		browser.click_link_by_partial_text(title_text)               
	
		usgs_html = browser.html                                      
		usgs_soup = bs(usgs_html, 'html.parser')            
	
		image = usgs_soup.find('div', class_='downloads').find('ul').find('li') 
		img_url = image.a['href']
	
		hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})   
	
		browser.back()

	browser.quit()

	return hemisphere_image_urls
	

if __name__ == "__main__":
	print(scrape())
