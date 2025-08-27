#!/usr/bin/env python3
"""
AI Alignment Forum News Scraper
Scrapes news posts from https://www.alignmentforum.org/
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import re

class AlignmentForumScraper:
    def __init__(self):
        self.base_url = "https://www.alignmentforum.org/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_news(self):
        """Scrape news posts from the main page"""
        try:
            print(f"Scraping {self.base_url}...")
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the posts container
            posts_container = soup.find('div', class_='PostsList2-postsBoxShadow')
            
            if not posts_container:
                print("Posts container not found. Looking for alternative selectors...")
                # Try alternative selectors
                posts_container = soup.find('div', class_=re.compile(r'PostsList.*'))
                if not posts_container:
                    return {"error": "Posts container not found"}
            
            # Find all post spans
            post_spans = posts_container.find_all('span', class_=re.compile(r'post_.*'))
            
            if not post_spans:
                print("Post spans not found. Looking for alternative selectors...")
                # Try alternative selectors
                post_spans = posts_container.find_all('span', class_=re.compile(r'.*post.*'))
            
            news_items = []
            
            for post_span in post_spans[:10]:  # Limit to 10 posts
                try:
                    # Find title in the span
                    title_element = post_span.find('span', class_='PostsTitle-eaTitleDesktopEllipsis')
                    
                    if not title_element:
                        # Try alternative title selectors
                        title_element = post_span.find('span', class_=re.compile(r'.*Title.*'))
                        if not title_element:
                            title_element = post_span.find('a')  # Sometimes title is in an anchor tag
                    
                    title = title_element.get_text(strip=True) if title_element else "No title found"
                    
                    # Try to find link
                    link_element = post_span.find('a')
                    link = link_element.get('href') if link_element else None
                    if link and not link.startswith('http'):
                        link = self.base_url.rstrip('/') + link
                    
                    # Try to find author and date
                    author = "Unknown"
                    date = "Unknown"
                    
                    # Look for author info
                    author_element = post_span.find('span', class_=re.compile(r'.*Author.*')) or \
                                  post_span.find('span', class_=re.compile(r'.*User.*'))
                    if author_element:
                        author = author_element.get_text(strip=True)
                    
                    # Look for date info
                    date_element = post_span.find('span', class_=re.compile(r'.*Date.*')) or \
                                 post_span.find('span', class_=re.compile(r'.*Time.*'))
                    if date_element:
                        date = date_element.get_text(strip=True)
                    
                    # Try to find excerpt/description
                    excerpt = ""
                    excerpt_element = post_span.find('div', class_=re.compile(r'.*Excerpt.*')) or \
                                   post_span.find('div', class_=re.compile(r'.*Body.*'))
                    if excerpt_element:
                        excerpt = excerpt_element.get_text(strip=True)[:200] + "..." if len(excerpt_element.get_text(strip=True)) > 200 else excerpt_element.get_text(strip=True)
                    
                    news_item = {
                        "title": title,
                        "author": author,
                        "date": date,
                        "excerpt": excerpt,
                        "link": link,
                        "scraped_at": datetime.now().isoformat()
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error processing post: {e}")
                    continue
            
            if not news_items:
                # If no posts found, try to get any text content
                print("No structured posts found. Getting general content...")
                all_text = posts_container.get_text(strip=True)
                if all_text:
                    news_items.append({
                        "title": "Content Found",
                        "author": "System",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "excerpt": all_text[:300] + "..." if len(all_text) > 300 else all_text,
                        "link": self.base_url,
                        "scraped_at": datetime.now().isoformat()
                    })
            
            return {
                "success": True,
                "source": self.base_url,
                "total_posts": len(news_items),
                "posts": news_items,
                "scraped_at": datetime.now().isoformat()
            }
            
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Scraping failed: {str(e)}"}
    
    def save_to_file(self, data, filename="alignment_forum_news.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")

def main():
    scraper = AlignmentForumScraper()
    news_data = scraper.scrape_news()
    
    if news_data.get("success"):
        print(f"\n✅ Successfully scraped {news_data['total_posts']} posts from AI Alignment Forum")
        print("\n📰 Latest Posts:")
        for i, post in enumerate(news_data['posts'][:5], 1):
            print(f"\n{i}. {post['title']}")
            print(f"   Author: {post['author']}")
            print(f"   Date: {post['date']}")
            if post['excerpt']:
                print(f"   Excerpt: {post['excerpt']}")
            if post['link']:
                print(f"   Link: {post['link']}")
        
        # Save to file
        scraper.save_to_file(news_data)
        
    else:
        print(f"❌ Error: {news_data.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
