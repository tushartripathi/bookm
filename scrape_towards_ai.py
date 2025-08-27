#!/usr/bin/env python3
"""
Towards AI Scraper
Scrapes AI articles from https://towardsai.net/p
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

class TowardsAIScraper:
    def __init__(self):
        self.base_url = "https://towardsai.net/p"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_news(self):
        """Scrape AI articles from Towards AI"""
        try:
            print(f"Scraping {self.base_url}...")
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Towards AI typically uses article tags or specific div classes
            # Look for articles in the main content area
            articles = soup.find_all(['article', 'div'], class_=re.compile(r'.*article.*|.*post.*|.*card.*|.*content.*'))
            
            if not articles:
                # Fallback: look for any divs that might contain articles
                articles = soup.find_all('div', class_=re.compile(r'.*'))
            
            news_items = []
            
            for article in articles[:15]:  # Limit to 15 articles
                try:
                    # Look for title - Towards AI often uses h3 or h2 tags
                    title_element = article.find(['h3', 'h2', 'h1']) or article.find('a', href=True)
                    
                    if not title_element:
                        continue
                    
                    title = title_element.get_text(strip=True) if title_element else "No title found"
                    
                    # Skip if title is too short or generic
                    if len(title) < 10 or title.lower() in ['towards ai', 'artificial intelligence', 'latest', 'categories']:
                        continue
                    
                    # Try to find link
                    link_element = article.find('a', href=True)
                    link = link_element.get('href') if link_element else None
                    if link and not link.startswith('http'):
                        link = "https://towardsai.net" + link
                    
                    # Try to find date - Towards AI shows dates in various formats
                    date = "Unknown"
                    date_element = article.find(text=re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'))
                    if date_element:
                        date = date_element.strip()
                    else:
                        # Look for date patterns like "August 26, 2025"
                        date_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b')
                        date_match = article.find(text=date_pattern)
                        if date_match:
                            date = date_match.strip()
                    
                    # Try to find excerpt/description
                    excerpt = ""
                    excerpt_element = article.find(['p', 'div'], class_=re.compile(r'.*excerpt.*|.*summary.*|.*description.*|.*content.*'))
                    if excerpt_element:
                        excerpt = excerpt_element.get_text(strip=True)[:200] + "..." if len(excerpt_element.get_text(strip=True)) > 200 else excerpt_element.get_text(strip=True)
                    
                    # Try to find author
                    author = "Towards AI"
                    author_element = article.find(text=re.compile(r'By\s+\w+')) or article.find(text=re.compile(r'Author.*:\s*\w+'))
                    if author_element:
                        author = author_element.strip()
                    
                    # Look for author in specific elements
                    author_div = article.find(['div', 'span'], class_=re.compile(r'.*author.*|.*byline.*'))
                    if author_div:
                        author_text = author_div.get_text(strip=True)
                        if author_text and len(author_text) < 50:  # Reasonable author name length
                            author = author_text
                    
                    # Only add if we have a meaningful title and link
                    if title and link and title != "No title found":
                        news_item = {
                            "title": title,
                            "author": author,
                            "date": date,
                            "excerpt": excerpt,
                            "link": link,
                            "source": "Towards AI",
                            "scraped_at": datetime.now().isoformat()
                        }
                        
                        news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
            
            if not news_items:
                # If no structured articles found, try to get any text content
                print("No structured articles found. Getting general content...")
                all_text = soup.get_text(strip=True)
                if all_text:
                    news_items.append({
                        "title": "Towards AI Content Found",
                        "author": "Towards AI",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "excerpt": all_text[:300] + "..." if len(all_text) > 300 else all_text,
                        "link": self.base_url,
                        "source": "Towards AI",
                        "scraped_at": datetime.now().isoformat()
                    })
            
            return {
                "success": True,
                "source": self.base_url,
                "total_articles": len(news_items),
                "articles": news_items,
                "scraped_at": datetime.now().isoformat()
            }
            
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Scraping failed: {str(e)}"}
    
    def save_to_file(self, data, filename="towards_ai_news.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")

def main():
    scraper = TowardsAIScraper()
    news_data = scraper.scrape_news()
    
    if news_data.get("success"):
        print(f"\n✅ Successfully scraped {news_data['total_articles']} articles from Towards AI")
        print("\n📰 Latest Articles:")
        for i, article in enumerate(news_data['articles'][:5], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Author: {article['author']}")
            print(f"   Date: {article['date']}")
            if article['excerpt']:
                print(f"   Excerpt: {article['excerpt']}")
            if article['link']:
                print(f"   Link: {article['link']}")
        
        # Save to file
        scraper.save_to_file(news_data)
        
    else:
        print(f"❌ Error: {news_data.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
