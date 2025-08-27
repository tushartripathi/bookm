# 🤖 AI Alignment Forum News Scraper

A web application that scrapes and displays the latest news and posts from the [AI Alignment Forum](https://www.alignmentforum.org/), a community focused on AI safety and alignment research.

## ✨ Features

- **Real-time Scraping**: Fetches latest posts from AI Alignment Forum
- **Modern UI**: Beautiful, responsive interface with dark theme
- **News Cards**: Displays posts with titles, authors, dates, and excerpts
- **Export Functionality**: Save scraped data as JSON files
- **File Loading**: Load previously scraped data from files
- **Statistics**: View scraping statistics and metadata
- **API Endpoints**: RESTful API for programmatic access

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask backend:**
   ```bash
   python app.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
bookm/
├── app.py                          # Flask backend server
├── scrape_alignment_forum.py      # Standalone Python scraper
├── alignment_news.html            # Frontend HTML interface
├── requirements.txt               # Python dependencies
├── index.html                     # Original AI Links Vault
└── README.md                      # This file
```

## 🛠️ Usage

### Web Interface

1. **Scrape News**: Click "🔍 Scrape Latest News" to fetch latest posts
2. **View Posts**: Browse through the scraped news cards
3. **Export Data**: Click "💾 Export to JSON" to save data locally
4. **Load Data**: Use "📁 Load from File" to load previously saved data
5. **Clear Data**: Use "🗑️ Clear News" to reset the display

### API Endpoints

- **`GET /`** - Main web interface
- **`GET /api/scrape`** - Scrape news from AI Alignment Forum
- **`GET /api/health`** - Health check endpoint
- **`GET /api/status`** - Scraper status information

### Standalone Script

You can also run the scraper independently:

```bash
python scrape_alignment_forum.py
```

This will scrape the news and save it to `alignment_forum_news.json`.

## 🔧 Configuration

### Target Elements

The scraper targets specific CSS classes from the AI Alignment Forum:

- **Posts Container**: `div` with class `PostsList2-postsBoxShadow`
- **Post Spans**: `span` elements with class `post_*`
- **Titles**: `span` with class `PostsTitle-eaTitleDesktopEllipsis`

### Fallback Selectors

The scraper includes fallback selectors to handle potential changes in the website structure:

- Alternative post container selectors
- Flexible title element detection
- Author and date extraction with multiple patterns

## 📊 Data Structure

Each scraped post contains:

```json
{
  "title": "Post Title",
  "author": "Author Name",
  "date": "Publication Date",
  "excerpt": "Post excerpt or description...",
  "link": "Full post URL",
  "scraped_at": "ISO timestamp"
}
```

## 🌐 Web Scraping Details

### Target Website
- **URL**: https://www.alignmentforum.org/
- **Focus**: AI safety, alignment research, and community discussions
- **Content**: Academic posts, research papers, community discussions

### Scraping Strategy
1. **User-Agent**: Uses realistic browser headers to avoid blocking
2. **Error Handling**: Graceful fallbacks for missing elements
3. **Rate Limiting**: Built-in delays to be respectful to the server
4. **Content Extraction**: Intelligent parsing of post metadata

## 🚨 Important Notes

### Ethical Scraping
- **Respectful**: Includes delays and realistic user agents
- **Educational**: Intended for learning and research purposes
- **Compliance**: Follows website terms of service and robots.txt

### Limitations
- **Dynamic Content**: May not capture JavaScript-rendered content
- **Rate Limits**: Subject to website's rate limiting policies
- **Structure Changes**: Website updates may require selector updates

## 🐛 Troubleshooting

### Common Issues

1. **"Posts container not found"**
   - The website structure may have changed
   - Check if the site is accessible from your location
   - Verify internet connection

2. **"No posts found"**
   - The CSS selectors may need updating
   - Check browser developer tools for current structure
   - Try running the standalone script for debugging

3. **Connection errors**
   - Check if the Flask server is running
   - Verify port 5000 is not blocked
   - Check firewall settings

### Debug Mode

Run the Flask app with debug mode enabled:

```bash
export FLASK_ENV=development
python app.py
```

## 🔮 Future Enhancements

- **Scheduled Scraping**: Automatic periodic updates
- **Database Storage**: Persistent storage of scraped data
- **Email Notifications**: Alerts for new posts
- **Advanced Filtering**: Search and filter by topics/authors
- **Mobile App**: Native mobile application
- **Real-time Updates**: WebSocket-based live updates

## 📚 Related Resources

- [AI Alignment Forum](https://www.alignmentforum.org/)
- [AI Safety Resources](https://aisafety.org/)
- [LessWrong](https://www.lesswrong.com/) - Related community
- [MIRI](https://intelligence.org/) - Machine Intelligence Research Institute

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Enhanced CSS selectors for better scraping
- Additional data extraction features
- UI/UX improvements
- Performance optimizations
- Error handling enhancements

## 📄 License

This project is for educational and research purposes. Please respect the terms of service of the websites being scraped.

## ⚠️ Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for ensuring compliance with website terms of service and applicable laws. The developers are not responsible for any misuse of this tool.

---

**Happy Scraping! 🚀**

For questions or issues, please check the troubleshooting section or create an issue in the project repository.
