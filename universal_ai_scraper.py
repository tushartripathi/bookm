#!/usr/bin/env python3
"""
Universal AI News Scraper
Scrapes AI news from multiple sources:
- AI Alignment Forum
- MIT News AI
- Towards AI
- MarkTechPost
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
from typing import Dict, List, Any

class UniversalAIScraper:
    def __init__(self):
        self.sources = {
            "ai_alignment_forum": {
                "url": "https://www.alignmentforum.org/",
                "name": "AI Alignment Forum",
                "type": "forum"
            },
            "mit_news": {
                "url": "https://news.mit.edu/topic/artificial-intelligence2",
                "name": "MIT News AI",
                "type": "news"
            },
            "towards_ai": {
                "url": "https://towardsai.net/p",
                "name": "Towards AI",
                "type": "publication"
            },
            "marktechpost": {
                "url": "https://www.marktechpost.com/",
                "name": "MarkTechPost",
                "type": "tech_news"
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_source(self, source_key: str) -> Dict[str, Any]:
        """Scrape a specific source"""
        source = self.sources[source_key]
        print(f"\n🔍 Scraping {source['name']}...")
        
        try:
            response = requests.get(source['url'], headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if source_key == "ai_alignment_forum":
                return self._scrape_alignment_forum(soup, source)
            elif source_key == "mit_news":
                return self._scrape_mit_news(soup, source)
            elif source_key == "towards_ai":
                return self._scrape_towards_ai(soup, source)
            elif source_key == "marktechpost":
                return self._scrape_marktechpost(soup, source)
            else:
                return {"error": f"Unknown source: {source_key}"}
                
        except requests.RequestException as e:
            return {"error": f"Request failed for {source['name']}: {str(e)}"}
        except Exception as e:
            return {"error": f"Scraping failed for {source['name']}: {str(e)}"}
    
    def _scrape_alignment_forum(self, soup: BeautifulSoup, source: Dict) -> Dict[str, Any]:
        """Scrape AI Alignment Forum"""
        posts_container = soup.find('div', class_='PostsList2-postsBoxShadow')
        
        if not posts_container:
            posts_container = soup.find('div', class_=re.compile(r'PostsList.*'))
            if not posts_container:
                return {"error": "Posts container not found"}
        
        post_spans = posts_container.find_all('span', class_=re.compile(r'post_.*'))
        if not post_spans:
            post_spans = posts_container.find_all('span', class_=re.compile(r'.*post.*'))
        
        news_items = []
        
        for post_span in post_spans[:10]:
            try:
                title_element = post_span.find('span', class_='PostsTitle-eaTitleDesktopEllipsis')
                if not title_element:
                    title_element = post_span.find('span', class_=re.compile(r'.*Title.*')) or post_span.find('a')
                
                title = title_element.get_text(strip=True) if title_element else None
                if not title:
                    continue
                
                link_element = post_span.find('a')
                link = link_element.get('href') if link_element else None
                if link and not link.startswith('http'):
                    link = source['url'].rstrip('/') + link
                
                news_items.append({
                    "title": title,
                    "author": "Unknown",
                    "date": "Unknown",
                    "excerpt": "",
                    "link": link,
                    "source": source['name'],
                    "scraped_at": datetime.now().isoformat()
                })
                
            except Exception as e:
                continue
        
        return {
            "success": True,
            "source": source['url'],
            "source_name": source['name'],
            "total_articles": len(news_items),
            "articles": news_items,
            "scraped_at": datetime.now().isoformat()
        }
    
    def _scrape_mit_news(self, soup: BeautifulSoup, source: Dict) -> Dict[str, Any]:
        """Scrape MIT News AI"""
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'.*article.*|.*news.*|.*story.*'))
        
        if not articles:
            articles = soup.find_all('div', class_=re.compile(r'.*'))
        
        news_items = []
        
        for article in articles[:10]:
            try:
                title_element = article.find(['h3', 'h2', 'h1']) or article.find('a', href=True)
                if not title_element:
                    continue
                
                title = title_element.get_text(strip=True)
                if len(title) < 10 or title.lower() in ['mit news', 'artificial intelligence', 'topics']:
                    continue
                
                link_element = article.find('a', href=True)
                link = link_element.get('href') if link_element else None
                if link and not link.startswith('http'):
                    link = "https://news.mit.edu" + link
                
                news_items.append({
                    "title": title,
                    "author": "MIT News",
                    "date": "Unknown",
                    "excerpt": "",
                    "link": link,
                    "source": source['name'],
                    "scraped_at": datetime.now().isoformat()
                })
                
            except Exception as e:
                continue
        
        return {
            "success": True,
            "source": source['url'],
            "source_name": source['name'],
            "total_articles": len(news_items),
            "articles": news_items,
            "scraped_at": datetime.now().isoformat()
        }
    
    def _scrape_towards_ai(self, soup: BeautifulSoup, source: Dict) -> Dict[str, Any]:
        """Scrape Towards AI"""
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'.*article.*|.*post.*|.*card.*|.*content.*'))
        
        if not articles:
            articles = soup.find_all('div', class_=re.compile(r'.*'))
        
        news_items = []
        
        for article in articles[:10]:
            try:
                title_element = article.find(['h3', 'h2', 'h1']) or article.find('a', href=True)
                if not title_element:
                    continue
                
                title = title_element.get_text(strip=True)
                if len(title) < 10 or title.lower() in ['towards ai', 'artificial intelligence', 'latest']:
                    continue
                
                link_element = article.find('a', href=True)
                link = link_element.get('href') if link_element else None
                if link and not link.startswith('http'):
                    link = "https://towardsai.net" + link
                
                news_items.append({
                    "title": title,
                    "author": "Towards AI",
                    "date": "Unknown",
                    "excerpt": "",
                    "link": link,
                    "source": source['name'],
                    "scraped_at": datetime.now().isoformat()
                })
                
            except Exception as e:
                continue
        
        return {
            "success": True,
            "source": source['url'],
            "source_name": source['name'],
            "total_articles": len(news_items),
            "articles": news_items,
            "scraped_at": datetime.now().isoformat()
        }
    
    def _scrape_marktechpost(self, soup: BeautifulSoup, source: Dict) -> Dict[str, Any]:
        """Scrape MarkTechPost"""
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'.*article.*|.*post.*|.*card.*|.*content.*|.*entry.*'))
        
        if not articles:
            articles = soup.find_all('div', class_=re.compile(r'.*'))
        
        news_items = []
        
        for article in articles[:10]:
            try:
                title_element = article.find(['h1', 'h2', 'h3', 'h4']) or article.find('a', href=True)
                if not title_element:
                    continue
                
                title = title_element.get_text(strip=True)
                if len(title) < 10 or title.lower() in ['marktechpost', 'artificial intelligence', 'latest']:
                    continue
                
                link_element = article.find('a', href=True)
                link = link_element.get('href') if link_element else None
                if link and not link.startswith('http'):
                    link = "https://www.marktechpost.com" + link
                
                news_items.append({
                    "title": title,
                    "author": "MarkTechPost",
                    "date": "Unknown",
                    "excerpt": "",
                    "link": link,
                    "source": source['name'],
                    "scraped_at": datetime.now().isoformat()
                })
                
            except Exception as e:
                continue
        
        return {
            "success": True,
            "source": source['url'],
            "source_name": source['name'],
            "total_articles": len(news_items),
            "articles": news_items,
            "scraped_at": datetime.now().isoformat()
        }
    
    def scrape_all_sources(self) -> Dict[str, Any]:
        """Scrape all sources and combine results"""
        print("🚀 Starting Universal AI News Scraper...")
        print("=" * 50)
        
        all_results = {}
        combined_articles = []
        total_articles = 0
        
        for source_key in self.sources.keys():
            result = self.scrape_source(source_key)
            all_results[source_key] = result
            
            if result.get("success"):
                total_articles += result.get("total_articles", 0)
                combined_articles.extend(result.get("articles", []))
                print(f"✅ {result['source_name']}: {result['total_articles']} articles")
            else:
                print(f"❌ {self.sources[source_key]['name']}: {result.get('error', 'Unknown error')}")
        
        # Sort combined articles by scraped time (newest first)
        combined_articles.sort(key=lambda x: x.get('scraped_at', ''), reverse=True)
        
        return {
            "success": True,
            "total_sources": len(self.sources),
            "total_articles": total_articles,
            "sources": all_results,
            "combined_articles": combined_articles,
            "scraped_at": datetime.now().isoformat()
        }
    
    def save_to_file(self, data: Dict[str, Any], filename: str = "universal_ai_news.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Data saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")

def main():
    scraper = UniversalAIScraper()
    
    # Scrape all sources
    all_news = scraper.scrape_all_sources()
    
    if all_news.get("success"):
        print(f"\n🎉 Successfully scraped {all_news['total_articles']} articles from {all_news['total_sources']} sources!")
        
        print("\n📰 Sample Articles from All Sources:")
        print("-" * 40)
        
        for i, article in enumerate(all_news['combined_articles'][:10], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Author: {article['author']}")
            if article['link']:
                print(f"   Link: {article['link']}")
        
        # Save to file
        scraper.save_to_file(all_news)
        
    else:
        print(f"❌ Error: {all_news.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
