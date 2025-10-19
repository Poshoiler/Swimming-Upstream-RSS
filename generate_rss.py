import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime

BLOG_URL = "https://dcsalmonbooks.com/blog"

def fetch_blog_posts():
    response = requests.get(BLOG_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    posts = []
    # Adjust this selector if Webador’s blog layout changes
    for article in soup.select("article"):
        title_tag = article.find("h2")
        link_tag = article.find("a", href=True)
        date_tag = article.find("time")

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = link_tag["href"]
            if not link.startswith("http"):
                link = BLOG_URL.rstrip("/") + "/" + link.lstrip("/")
            pub_date = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else datetime.datetime.utcnow().isoformat()
            posts.append({"title": title, "link": link, "pub_date": pub_date})
    return posts

def generate_rss(posts):
    fg = FeedGenerator()
    fg.title("Swimming Upstream Blog")
    fg.link(href=BLOG_URL, rel="alternate")
    fg.description("Updates from the Swimming Upstream blog by DC Salmon.")
    fg.language("en")

    for post in posts:
        fe = fg.add_entry()
        fe.title(post["title"])
        fe.link(href=post["link"])
        fe.pubDate(post["pub_date"])

    fg.rss_file("rss.xml")

if __name__ == "__main__":
    posts = fetch_blog_posts()
    if posts:
        generate_rss(posts)
        print("RSS feed generated with", len(posts), "posts.")
    else:
        print("No posts found!")

