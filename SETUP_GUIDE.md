# 🚀 Quick Setup Guide - AI Alignment Forum News Scraper

## ⚡ Get Started in 3 Steps

### 1. Install Dependencies
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Scraper
```bash
# Option A: Standalone scraper (command line)
python scrape_alignment_forum.py

# Option B: Web interface (recommended)
python app.py

# Option C: Use the startup script
./start_server.sh
```

### 3. Access the Application
- **Web Interface**: http://localhost:5001
- **API Endpoint**: http://localhost:5001/api/scrape
- **Health Check**: http://localhost:5001/api/health

## 🎯 What You Get

✅ **Real-time news scraping** from AI Alignment Forum  
✅ **Beautiful web interface** with modern design  
✅ **JSON export/import** functionality  
✅ **RESTful API** for programmatic access  
✅ **Responsive design** that works on all devices  

## 🔍 Sample Output

The scraper extracts:
- Post titles
- Author information  
- Publication dates
- Post excerpts
- Direct links to full posts

## 🛠️ Troubleshooting

**Port 5000 in use?** The app now uses port 5001 by default.

**Dependencies not found?** Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

**Scraping fails?** Check your internet connection and try again later.

## 📚 Learn More

- **README.md** - Comprehensive documentation
- **demo.py** - Example usage script
- **scrape_alignment_forum.py** - Core scraping logic

---

**Happy Scraping! 🎉**
