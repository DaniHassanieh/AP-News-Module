import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Set up the driver
options = Options()
# options.add_argument("--headless")
options.add_extension("./ublock.crx")
driver = webdriver.Chrome(options=options)

# Get the page
driver.get("https://apnews.com/hub/ap-top-news")

# Get the HTML
html = driver.page_source

# Parse the HTML
soup = BeautifulSoup(html, "lxml")

# Get the links
article_links = soup.find_all("a", class_="Link")

usable_links = []

# Get the links that are articles
for link in article_links:
    if re.search(r"apnews.com/article", link["href"]):
        usable_links.append(link["href"])

# Remove duplicates
usable_links = set(usable_links)

# get a random article
article = usable_links.pop()
print(article)
driver.get(article)

# Get the HTML
html = driver.page_source

# Parse the HTML
soup = BeautifulSoup(html, "lxml")

# Get the title
title = soup.find("h1").text
print(title)

# Get the content
content = soup.find("div", class_="RichTextStoryBody RichTextBody")
body = ""

for p in content.find_all("p"):
    body += p.text + '\n'

img = soup.find("img").attrs["src"]

print(img)

driver.close()
