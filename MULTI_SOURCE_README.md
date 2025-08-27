# 🤖 Multi-Source AI News Scraper Collection

A comprehensive collection of web scrapers for multiple AI news sources, built with Python and BeautifulSoup. This collection includes individual scrapers for each source and a universal scraper that can handle all sources simultaneously.

## 🌟 **What's Included**

### **Individual Scrapers**
1. **`scrape_alignment_forum.py`** - AI Alignment Forum posts
2. **`scrape_mit_news.py`** - MIT News AI articles  
3. **`scrape_towards_ai.py`** - Towards AI publication
4. **`scrape_marktechpost.py`** - MarkTechPost tech news

### **Universal Scraper**
- **`universal_ai_scraper.py`** - Scrapes all sources in one go

### **Web Interfaces**
- **`alignment_news.html`** - Single source interface
- **`multi_source_news.html`** - Multi-source aggregator interface

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### **2. Run Individual Scrapers**
```bash
# AI Alignment Forum
python scrape_alignment_forum.py

# MIT News AI
python scrape_mit_news.py

# Towards AI
python scrape_towards_ai.py

# MarkTechPost
python scrape_marktechpost.py
```

### **3. Run Universal Scraper**
```bash
# Scrape all sources at once
python universal_ai_scraper.py
```

### **4. Start Web Server**
```bash
# Start Flask backend
python app.py

# Or use the startup script
./start_server.sh
```

### **5. Access Web Interfaces**
- **Single Source**: http://localhost:5001
- **Multi-Source**: http://localhost:5001/multi-source

## 📊 **Scraping Results**

### **AI Alignment Forum**
- **Target**: https://www.alignmentforum.org/
- **Content**: AI safety, alignment research, community discussions
- **Structure**: Forum posts with titles, authors, dates, and links
- **CSS Selectors**: 
  - Container: `div.PostsList2-postsBoxShadow`
  - Posts: `span.post_*`
  - Titles: `span.PostsTitle-eaTitleDesktopEllipsis`

### **MIT News AI**
- **Target**: https://news.mit.edu/topic/artificial-intelligence2
- **Content**: Academic AI research, university news, scientific breakthroughs
- **Structure**: News articles with titles, dates, and excerpts
- **CSS Selectors**:
  - Articles: `article`, `div.*article*`, `div.*news*`
  - Titles: `h1`, `h2`, `h3` tags
  - Dates: Text patterns like "August 26, 2025"

### **Towards AI**
- **Target**: https://towardsai.net/p
- **Content**: AI tutorials, research papers, industry insights
- **Structure**: Publication articles with titles, authors, and content
- **CSS Selectors**:
  - Articles: `article`, `div.*article*`, `div.*post*`
  - Titles: `h1`, `h2`, `h3` tags
  - Authors: `div.*author*`, `span.*byline*`

### **MarkTechPost**
- **Target**: https://www.marktechpost.com/
- **Content**: Tech industry news, AI developments, startup updates
- **Structure**: Tech news articles with titles and metadata
- **CSS Selectors**:
  - Articles: `article`, `div.*article*`, `div.*post*`
  - Titles: `h1`, `h2`, `h3`, `h4` tags
  - Content: `div.*content*`, `div.*entry*`

## 🔧 **Technical Details**

### **Scraping Strategy**
Each scraper uses a multi-layered approach:

1. **Primary Selectors**: Target specific CSS classes and HTML elements
2. **Fallback Selectors**: Use regex patterns to find alternative elements
3. **Content Validation**: Filter out non-article content and duplicates
4. **Error Handling**: Graceful fallbacks for missing elements

### **Data Extraction**
- **Titles**: Article headlines and post titles
- **Authors**: Writer information when available
- **Dates**: Publication dates in various formats
- **Excerpts**: Article summaries and descriptions
- **Links**: Direct URLs to full articles
- **Source**: Website identification
- **Metadata**: Timestamps and scraping info

### **Output Format**
```json
{
  "success": true,
  "source": "https://example.com",
  "source_name": "Source Name",
  "total_articles": 10,
  "articles": [
    {
      "title": "Article Title",
      "author": "Author Name",
      "date": "Publication Date",
      "excerpt": "Article excerpt...",
      "link": "Full article URL",
      "source": "Source Name",
      "scraped_at": "ISO timestamp"
    }
  ],
  "scraped_at": "ISO timestamp"
}
```

## 🌐 **Web Interface Features**

### **Single Source Interface**
- Clean, focused display for individual sources
- News cards with titles, authors, dates, and excerpts
- Export/import functionality
- Responsive design for all devices

### **Multi-Source Interface**
- **Source Selection**: Checkboxes to choose which sources to scrape
- **Unified Display**: Combined view of all sources
- **Advanced Filtering**: Search by title, author, or content
- **Source Filtering**: Filter by specific news source
- **Statistics**: Per-source article counts and totals
- **Export Options**: Save combined data as JSON

## 🛠️ **API Endpoints**

### **Flask Backend Routes**
- **`GET /`** - Main single-source interface
- **`GET /api/scrape`** - AI Alignment Forum scraper
- **`GET /api/universal-scrape`** - Multi-source scraper
- **`GET /api/health`** - Health check
- **`GET /api/status`** - Scraper status

### **Usage Examples**
```bash
# Health check
curl http://localhost:5001/api/health

# Scrape single source
curl http://localhost:5001/api/scrape

# Scrape all sources
curl http://localhost:5001/api/universal-scrape
```

## 📁 **File Structure**
```
bookm/
├── Individual Scrapers/
│   ├── scrape_alignment_forum.py      # AI Alignment Forum
│   ├── scrape_mit_news.py            # MIT News AI
│   ├── scrape_towards_ai.py          # Towards AI
│   └── scrape_marktechpost.py        # MarkTechPost
├── Universal Scraper/
│   └── universal_ai_scraper.py       # All sources combined
├── Web Interfaces/
│   ├── alignment_news.html           # Single source
│   └── multi_source_news.html        # Multi-source
├── Backend/
│   ├── app.py                        # Flask server
│   └── requirements.txt              # Dependencies
├── Utilities/
│   ├── start_server.sh               # Startup script
│   ├── demo.py                       # Demo script
│   └── README.md                     # Documentation
└── Output Files/
    ├── alignment_forum_news.json     # Scraped data
    ├── mit_news_ai.json              # Scraped data
    ├── towards_ai_news.json          # Scraped data
    ├── marktechpost_news.json        # Scraped data
    └── universal_ai_news.json        # Combined data
```

## 🚨 **Important Notes**

### **Ethical Scraping**
- **Respectful**: Uses realistic user agents and reasonable delays
- **Educational**: Intended for learning and research purposes
- **Compliance**: Follows website terms of service and robots.txt
- **Rate Limiting**: Built-in delays to avoid overwhelming servers

### **Limitations**
- **Dynamic Content**: May not capture JavaScript-rendered content
- **Structure Changes**: Website updates may require selector updates
- **Rate Limits**: Subject to website policies and restrictions
- **Content Availability**: Depends on website accessibility

## 🔮 **Future Enhancements**

### **Planned Features**
- **Scheduled Scraping**: Automatic periodic updates
- **Database Storage**: Persistent storage with SQLite/PostgreSQL
- **Email Notifications**: Alerts for new articles
- **Advanced Analytics**: Content analysis and trend detection
- **Mobile App**: Native mobile application
- **Real-time Updates**: WebSocket-based live updates

### **Potential Sources**
- **ArXiv**: Academic AI papers
- **Reddit**: AI community discussions
- **Twitter**: AI researcher updates
- **YouTube**: AI tutorial videos
- **Podcasts**: AI-focused audio content

## 🐛 **Troubleshooting**

### **Common Issues**

1. **"Posts container not found"**
   - Website structure may have changed
   - Check if site is accessible from your location
   - Verify internet connection

2. **"No articles found"**
   - CSS selectors may need updating
   - Check browser developer tools for current structure
   - Try running individual scrapers for debugging

3. **Connection errors**
   - Check if Flask server is running
   - Verify port 5001 is not blocked
   - Check firewall settings

4. **Import errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed
   - Check Python version compatibility

### **Debug Mode**
```bash
# Enable Flask debug mode
export FLASK_ENV=development
python app.py

# Run scrapers with verbose output
python -u universal_ai_scraper.py
```

## 📚 **Related Resources**

### **AI News Sources**
- [AI Alignment Forum](https://www.alignmentforum.org/) - AI safety research
- [MIT News AI](https://news.mit.edu/topic/artificial-intelligence2) - Academic AI research
- [Towards AI](https://towardsai.net/) - AI tutorials and research
- [MarkTechPost](https://www.marktechpost.com/) - Tech industry news

### **Web Scraping Resources**
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [Requests Library](https://requests.readthedocs.io/)
- [Flask Framework](https://flask.palletsprojects.com/)

## 🤝 **Contributing**

Contributions are welcome! Areas for improvement:

- **Enhanced Selectors**: Better CSS selectors for improved scraping
- **Additional Sources**: New AI news sources and websites
- **UI/UX Improvements**: Better web interface design
- **Performance Optimization**: Faster scraping and better error handling
- **Content Analysis**: AI-powered content categorization

## 📄 **License & Disclaimer**

This project is for educational and research purposes. Users are responsible for ensuring compliance with website terms of service and applicable laws. The developers are not responsible for any misuse of this tool.

---

**Happy Scraping! 🚀**

For questions or issues, please check the troubleshooting section or create an issue in the project repository.
