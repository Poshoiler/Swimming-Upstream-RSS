import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import urllib.parse

# URL of your blog
BLOG_URL = "https://dcsalmonbooks.com/blog"

# Fetch the blog page
response = requests.get(BLOG_URL)
soup = BeautifulSoup(response.text, "html.parser")

# Initialize the RSS feed
fg = FeedGenerator()
fg.title("DC Salmon Books Blog")
fg.link(href=BLOG_URL, rel="alternate")
fg.description("Updates and news from DC Salmon Books")
fg.language("en")

# Extract blog posts (adjust CSS selectors if Webador changes layout)
for article in soup.select("article"):
    title_elem = article.select_one("h2, h3, .blog-title, a")
    if not title_elem:
        continue

    title = title_elem.get_text(strip=True)
    link_tag = title_elem.find("a") or article.find("a")
    if link_tag and link_tag.get("href"):
        link = urllib.parse.urljoin(BLOG_URL, link_tag["href"])
    else:
        link = BLOG_URL

    date_tag = article.find("time")
    if date_tag and date_tag.get("datetime"):
        pub_date = datetime.fromisoformat(date_tag["datetime"])
    else:
        pub_date = datetime.utcnow()

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.pubDate(pub_date)

# Write RSS file
fg.rss_file("rss.xml")
print("✅ RSS feed generated successfully: rss.xml")
