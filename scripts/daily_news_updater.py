#!/usr/bin/env python3
"""
Daily UPSC News Updater — runs at 6:00 AM IST daily.
Fetches news from RSS feeds, summarizes them for UPSC relevance,
and pushes to Firebase Realtime Database.

Usage: python3 daily_news_updater.py
"""

import requests
import feedparser
import time
import json
from datetime import datetime

DATABASE_URL = "https://upsc-prep-b2336-default-rtdb.firebaseio.com"

def push_to_db(path, data):
    url = f"{DATABASE_URL}/{path}.json"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"  ✅ {data.get('title', 'N/A')[:60]}...")
    else:
        print(f"  ❌ Failed: {response.text[:100]}")


# RSS Feeds for UPSC-relevant news
RSS_FEEDS = [
    {
        "url": "https://www.thehindu.com/news/national/feeder/default.rss",
        "source": "The Hindu",
        "category": "Polity",
    },
    {
        "url": "https://indianexpress.com/section/india/feed/",
        "source": "Indian Express",
        "category": "Polity",
    },
    {
        "url": "https://www.thehindu.com/business/Economy/feeder/default.rss",
        "source": "The Hindu",
        "category": "Economy",
    },
    {
        "url": "https://www.thehindu.com/sci-tech/science/feeder/default.rss",
        "source": "The Hindu",
        "category": "Science & Tech",
    },
    {
        "url": "https://www.downtoearth.org.in/rss/environment.xml",
        "source": "Down To Earth",
        "category": "Environment",
    },
    {
        "url": "https://www.thehindu.com/news/international/feeder/default.rss",
        "source": "The Hindu",
        "category": "International Relations",
    },
]

# UPSC-relevant keywords to filter news
UPSC_KEYWORDS = [
    "supreme court", "parliament", "lok sabha", "rajya sabha", "amendment",
    "gdp", "inflation", "rbi", "fiscal", "budget", "economy", "fdi",
    "isro", "drdo", "satellite", "missile", "space", "nuclear",
    "climate", "environment", "wildlife", "forest", "pollution", "biodiversity",
    "foreign policy", "bilateral", "g20", "un", "security council", "treaty",
    "election", "commission", "governor", "president", "prime minister",
    "scheme", "yojana", "mission", "policy", "reform", "act", "bill",
    "unesco", "world heritage", "ramsar", "national park", "tiger",
    "education", "nep", "university", "iit", "research",
    "defence", "army", "navy", "air force", "border",
    "agriculture", "farmer", "msp", "crop", "irrigation",
    "digital", "technology", "ai", "cyber", "blockchain",
    "health", "who", "disease", "vaccine", "ayushman",
    "niti aayog", "finance commission", "gst",
]


def is_upsc_relevant(title, summary):
    """Check if a news item is relevant for UPSC preparation."""
    text = (title + " " + summary).lower()
    return any(keyword in text for keyword in UPSC_KEYWORDS)


def truncate_summary(text, max_chars=500):
    """Truncate summary to a reasonable length."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."


def categorize_news(title, summary, default_category):
    """Auto-categorize news based on keywords."""
    text = (title + " " + summary).lower()

    category_keywords = {
        "Polity": ["supreme court", "parliament", "election", "governor", "amendment", "lok sabha", "rajya sabha", "act", "bill", "constitution"],
        "Economy": ["gdp", "inflation", "rbi", "budget", "fiscal", "fdi", "gst", "tax", "economy", "trade"],
        "Science & Tech": ["isro", "drdo", "space", "satellite", "technology", "ai", "digital", "nuclear", "missile"],
        "Environment": ["climate", "environment", "wildlife", "forest", "pollution", "biodiversity", "emission", "green"],
        "International Relations": ["bilateral", "g20", "un", "security council", "foreign", "treaty", "summit", "diplomatic"],
        "Geography": ["earthquake", "flood", "cyclone", "monsoon", "drought", "river", "glacier"],
        "History & Culture": ["unesco", "heritage", "archaeological", "monument", "festival", "tradition"],
    }

    for category, keywords in category_keywords.items():
        if any(kw in text for kw in keywords):
            return category

    return default_category


def fetch_and_push_news():
    """Fetch news from RSS feeds and push UPSC-relevant ones to Firebase."""
    today = datetime.now().strftime("%b %d, %Y")
    pushed_count = 0
    seen_titles = set()

    print(f"📰 Fetching daily UPSC news for {today}...")

    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            source = feed_info["source"]
            default_category = feed_info["category"]

            print(f"\n  📡 {source} — {len(feed.entries)} entries found")

            for entry in feed.entries[:10]:  # Limit to 10 per feed
                title = entry.get("title", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                link = entry.get("link", "")

                # Skip duplicates
                if title in seen_titles or not title:
                    continue
                seen_titles.add(title)

                # Only push UPSC-relevant news
                if not is_upsc_relevant(title, summary):
                    continue

                # Clean and categorize
                clean_summary = truncate_summary(summary)
                category = categorize_news(title, summary, default_category)

                data = {
                    "title": title,
                    "summary": f"[{source}] {clean_summary}",
                    "category": category,
                    "source_url": link,
                    "date": today,
                    "timestamp": int(time.time() * 1000),
                    "auto_generated": True,
                }

                push_to_db("current_affairs/UPSC", data)
                pushed_count += 1
                time.sleep(0.3)  # Rate limiting

        except Exception as e:
            print(f"  ⚠️ Error fetching {feed_info['source']}: {e}")

    print(f"\n✅ Done! Pushed {pushed_count} UPSC-relevant news articles.")
    return pushed_count


if __name__ == "__main__":
    print("=" * 60)
    print("  UPSC Daily News Updater")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("=" * 60)
    fetch_and_push_news()
