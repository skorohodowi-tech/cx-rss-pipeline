import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import html
import os

FEEDS = [
    # Рівень 1: щоденні новини + data-driven журналістика
    "https://www.customerexperiencedive.com/feeds/news/",
    "https://customerthink.com/feed/",
    "https://www.cmswire.com/feed/",
    "https://www.cxnetwork.com/rss",
    "https://cxm.world/feed/",

    # Рівень 2: незалежні практики і консультанти
    "https://cx-journey.com/feed",
    "https://www.adrianswinscoe.com/feed/",
    "https://experienceinvestigators.com/feed/",
    "https://heartofthecustomer.com/feed/",
    "https://hyken.com/feed/",

    # Рівень 3: Substack-автори
    "https://www.dcxnewsletter.com/feed",
    "https://cxstories.substack.com/feed",
    "https://www.thecscafe.com/feed",
    "https://metricstack.substack.com/feed",

    # Рівень 4: дослідження і стратегія
    "https://hbr.org/feed",
    "https://sloanreview.mit.edu/feed/",
    "https://www.forrester.com/blogs/feed",
    "https://www.gartner.com/en/newsroom/rss",
    "https://www.strategy-business.com/rss",

    # Рівень 5: behavioral science і метрики
    "https://behavioralscientist.org/feed/",
    "https://bcfg.substack.com/feed",
    "https://thedecisionlab.com/feed/",
    "https://www.nngroup.com/feed/rss/",

    # Рівень 6: XM дослідження і AI в сервісі
    "https://www.qualtrics.com/blog/feed/",
    "https://www.intercom.com/blog/feed",
]

MAX_ITEMS = 60


def fetch_all():
    items = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
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
