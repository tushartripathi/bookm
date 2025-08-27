#!/usr/bin/env python3
"""
Flask Backend for AI Alignment Forum News Scraper
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
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
            
            for post_span in post_spans[:15]:  # Limit to 15 posts
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

# Global scraper instance
scraper = AlignmentForumScraper()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template_string(open('alignment_news.html').read())

@app.route('/api/scrape', methods=['GET'])
def scrape_endpoint():
    """API endpoint to scrape news"""
    try:
        news_data = scraper.scrape_news()
        return jsonify(news_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Alignment Forum Scraper"
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Get scraper status"""
    return jsonify({
        "scraper_ready": True,
        "last_scrape": getattr(scraper, 'last_scrape', None),
        "base_url": scraper.base_url
    })

if __name__ == '__main__':
    print("🚀 Starting AI Alignment Forum News Scraper...")
    print("📱 Frontend: http://localhost:5001")
    print("🔌 API: http://localhost:5001/api/scrape")
    print("💚 Health: http://localhost:5001/api/health")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
