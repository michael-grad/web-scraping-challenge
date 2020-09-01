from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # MARS NEWS
    # Read url
    url = 'https://mars.nasa.gov/news/'

    # Retreive page
    #response = requests.get(url)
    browser = init_browser()
    #response = browser.visit(url)
    browser.visit(url)
    time.sleep(5)
    html= browser.html

    # Create beautiful soup object and parse
    soup = bs(html, 'html.parser')

    # Examine results
    #print(soup.prettify())

    # Assign title
    # comment out .a.text
    
    title = soup.find_all('div', class_="content_title")
    nasa_news_title = title[1].a.text

    # Modeled after Activity 12.2.2
    print(nasa_news_title)
    nasa_news_description = soup.find('div', class_="article_teaser_body").text
    print(nasa_news_description)


    # JPL FEATURED IMAGE
    # Define URL and go to it
    # URL for JPL Featured Space Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(5)
    # Extract full size jpg image from page
    html = browser.html
    soup = bs(html, 'html.parser')

    #print(soup)
    title = soup.find_all('div', class_="content_title")
    btn_url = soup.find('a', class_="button fancybox")['data-fancybox-href']
    print(btn_url)
    featured_img_url = jpl_url + btn_url
    print(featured_img_url)


    # MARS FACTS TABLE
    # modeled after Activity 12.2.9
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_tables = pd.read_html(mars_facts_url)
    time.sleep(5)
    print(type(mars_facts_tables))
    mars_facts_table = mars_facts_tables[0]

    # Renaming column headers sourced from https://cmdlinetips.com/2018/03/how-to-change-column-names-and-row-indexes-in-pandas/
    mars_facts_table.columns=["Attribute", "Value"]
    type(mars_facts_table)

    # Set index to Attribute Column sourced from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html
    mars_facts_table = mars_facts_table.set_index("Attribute")
    print(mars_facts_table)

    # to html
    mars_facts_html = mars_facts_table.to_html()


    # HEMISPHERES
    # Define URL
    usgs_astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    html_hemi = browser.html
    soup_hemi = bs(html_hemi, 'html.parser')

    # Define URL and go to it
    browser.visit(usgs_astrogeology_url)
    time.sleep(10)

    # define lists
    hemi_title_list = []
    hemi_image_list = []
    hemi_image_final_list = []

    # Assign title
    hemi_title_list = soup_hemi.find_all('h3')
    print(hemi_title_list[0].text)
    
    hemi_image_list = soup_hemi.find_all('a', class_="itemLink product-item", href=True)
    print(hemi_image_list)
    
    # Loop through hemi_image_list to get just href
    i = 0

    for image in hemi_image_list:
        print(image['href'])
        full_url = usgs_astrogeology_url + image['href']
        if full_url not in hemi_image_final_list:
            hemi_image_final_list.append(full_url)
    print(f"Hemi Image Final List: {hemi_image_final_list}")

    # Create list of dictionaries
    hemi_dict = {}
    hemi_list =[]
    for i in range(0,4):
        hemi_dict = {"title":  hemi_title_list[i].text,
                    "img_url":  hemi_image_final_list[i]
        }
        hemi_list.append(hemi_dict)
        hemi_dict = {}
    print(hemi_list)

    # Create a dictionary to return with all the values
    mars_dict_data = {
        'news_title': nasa_news_title,
        'news_desc':  nasa_news_description,
        'featured_img':  featured_img_url,
        'mars_facts':  mars_facts_html,
        'hemi_1':  hemi_list[0],
        'hemi_2':  hemi_list[1],
        'hemi_3':  hemi_list[2],
        'hemi_4':  hemi_list[3]
    }
    print(mars_dict_data)

    # Return results
    return mars_dict_data
