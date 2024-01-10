import os
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import date


# Set up the driver
options = Options()
options.add_argument("--headless")
options.add_extension("./ublock.crx")
# create webdriver
driver = webdriver.Chrome(options=options)

# navigate to homepage url (will add access to other AP news pages later)
driver.get("https://apnews.com/hub/ap-top-news")
# Get the source
soup = BeautifulSoup(driver.page_source, "lxml")

# Get all links
links = soup.find_all("a", class_="Link")

article_links = []

# Get the links that are articles
for link in links:
    if re.search(r"apnews.com/article", link["href"]):
        article_links.append(link["href"])

# Remove duplicates
article_links = set(article_links)

articles = []

for article_link in article_links:
    article = {"article link": article_link}

    # get a random article
    driver.get(article_link)
    # Get the source of the article
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Get the title
    title = soup.find("h1").text
    article["title"] = title

    # Get author and time
    author_time_element = soup.find("div", {"class": "Page-byline-info"})

    # get authors
    author_div_element = author_time_element.find_next("div").find_all(attrs={"class": "Link"})
    authors = []
    for author_span_element in author_div_element:
        authors.append(author_span_element.text)

    # get time
    time_element = soup.find("div", {"class": "Page-dateModified"}).find("span")
    article["authors"] = authors
    article["time"] = time_element.text

    # Get the content
    content = soup.find("div", class_="RichTextStoryBody RichTextBody")
    body = ""
    for p in content.find_all("p"):
        body += p.text + '\n'
    article["body"] = body

    # will add image support in the future

    articles.append(article)

# check if output directory doesn't exist
if not os.path.exists("./ap-news-output/"):
    os.makedirs("./ap-news-output/")

with open(f"./ap-news-output/ap-news-{date.today()}.json", "w") as outfile:
    data_write = json.dumps(articles, indent=4)
    outfile.write(data_write)

driver.quit()
