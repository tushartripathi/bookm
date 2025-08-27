#!/usr/bin/env python3
"""
Demo script for AI Alignment Forum News Scraper
Shows how to use the scraper programmatically
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrape_alignment_forum import AlignmentForumScraper
import json
from datetime import datetime

def main():
    print("🤖 AI Alignment Forum News Scraper - Demo")
    print("=" * 50)
    
    # Create scraper instance
    scraper = AlignmentForumScraper()
    
    print(f"🎯 Target: {scraper.base_url}")
    print("🔄 Starting scrape...")
    print()
    
    # Scrape the news
    news_data = scraper.scrape_news()
    
    if news_data.get("success"):
        print(f"✅ Successfully scraped {news_data['total_posts']} posts!")
        print(f"📅 Scraped at: {news_data['scraped_at']}")
        print()
        
        # Display first 5 posts
        print("📰 Latest Posts:")
        print("-" * 30)
        
        for i, post in enumerate(news_data['posts'][:5], 1):
            print(f"\n{i}. {post['title']}")
            print(f"   👤 Author: {post['author']}")
            print(f"   📅 Date: {post['date']}")
            if post['excerpt']:
                print(f"   📝 Excerpt: {post['excerpt'][:100]}...")
            if post['link']:
                print(f"   🔗 Link: {post['link']}")
        
        # Save to file
        filename = f"demo_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        scraper.save_to_file(news_data, filename)
        print(f"\n💾 Data saved to: {filename}")
        
        # Show statistics
        print(f"\n📊 Statistics:")
        print(f"   Total posts: {news_data['total_posts']}")
        print(f"   Source: {news_data['source']}")
        print(f"   Timestamp: {news_data['scraped_at']}")
        
    else:
        print(f"❌ Error: {news_data.get('error', 'Unknown error')}")
        return 1
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Run 'python app.py' to start the web server")
    print("   2. Open http://localhost:5001 in your browser")
    print("   3. Use the web interface to scrape and view news")
    
    return 0

if __name__ == "__main__":
    exit(main())
