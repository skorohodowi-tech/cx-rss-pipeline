import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import html
import os

FEEDS = [
    "https://customerthink.com/feed/",
    "https://feeds2.feedburner.com/CMSWire",
    "https://behavioralscientist.org/feed/",
    "https://www.nngroup.com/feed/rss/",
    "https://sloanreview.mit.edu/feed/",
    "https://www.intercom.com/blog/feed",
    "https://www.zendesk.com/blog/feed/",
    "https://www.medallia.com/blog/feed/",
    "https://www.qualtrics.com/blog/feed/",
    "https://www.forrester.com/blogs/feed",
    "https://www.mckinsey.com/insights/rss",
    "https://www.totango.com/feed/",
    "https://www.gainsight.com/feed/",
    "https://cx-ai.com/feed/",
    "https://experiencematters.blog/feed/",
    "https://cxm.co.uk/feed/",
    "https://www.customerexperiencedive.com/feeds/news/",
    "https://www.cxnetwork.com/rss",
    "https://www.mycustomer.com/feed",
]

MAX_ITEMS = 30


def fetch_all():
    items = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                pub = entry.get("published_parsed") or entry.get("updated_parsed")
                if pub:
                    dt = datetime(*pub[:6], tzinfo=timezone.utc)
                else:
                    dt = datetime.now(timezone.utc)
                items.append({
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "description": entry.get("summary", entry.get("description", ""))[:500],
                    "pubDate": dt,
                    "source": feed.feed.get("title", url),
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    items.sort(key=lambda x: x["pubDate"], reverse=True)
    return items[:MAX_ITEMS]


def build_rss(items):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "CX Content Pipeline"
    ET.SubElement(channel, "description").text = "Aggregated CX, Service, AI, Behavioral Science feeds"
    ET.SubElement(channel, "link").text = "https://github.com"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    for item in items:
        el = ET.SubElement(channel, "item")
        ET.SubElement(el, "title").text = item["title"]
        ET.SubElement(el, "link").text = item["link"]
        desc_text = item["description"]
        # Strip HTML tags simply
        import re
        desc_text = re.sub(r"<[^>]+>", "", desc_text)
        desc_text = html.unescape(desc_text)[:400]
        ET.SubElement(el, "description").text = desc_text
        ET.SubElement(el, "pubDate").text = item["pubDate"].strftime("%a, %d %b %Y %H:%M:%S +0000")
        ET.SubElement(el, "source").text = item["source"]

    return ET.tostring(rss, encoding="unicode", xml_declaration=True)


def main():
    os.makedirs("public", exist_ok=True)
    items = fetch_all()
    xml = build_rss(items)
    with open("public/feed.xml", "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Generated feed with {len(items)} items")


if __name__ == "__main__":
    main()
