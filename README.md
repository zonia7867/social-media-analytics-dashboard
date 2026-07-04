# Social Media Sentiments Analytics Dashboard
**Transform Social Media Data Into Actionable Insights**

##  Overview

Social Media Sentiments Analytics Dashboard is a comprehensive data visualization platform that helps marketing teams, social media managers, and business analysts transform raw social media data into actionable business insights. Built with Python and Streamlit, this interactive dashboard provides real-time analytics across multiple social media platforms.

###  Why This Project?

-  **Instant Insights**: Upload CSV, get insights in seconds
-  **Multi-Platform Support**: Analyze data from Twitter, Instagram, Facebook, LinkedIn, and more
-  **Beautiful Visualizations**: Modern, interactive charts and graphs
-  **Smart Filtering**: Filter by sentiment, platform, country, and date
-  **AI-Driven Recommendations**: Get data-backed content strategies

---

##  Features

### **Engagement Analysis**
- Track total likes, retweets, and overall engagement
- Sentiment-based engagement comparison
- Platform performance analytics
- Time-series engagement trends

###  **Content Performance**
- Identify top 10 best-performing posts
- Discover optimal posting hours (24-hour analysis)
- Find best days of the week for maximum reach
- Content length optimization

###  **Trend Detection**
- Top 15 trending hashtags visualization
- Interactive word cloud generation
- Sentiment trends over time
- Emerging topic identification

###  **Content Strategy Optimization**
- Data-driven posting time recommendations
- Best-performing sentiment analysis
- Content length guidelines
- Actionable do's and don'ts

###  **Interactive Filtering**
- Filter by sentiment (Positive, Negative, Neutral, etc.)
- Filter by platform (Twitter, Instagram, Facebook, etc.)
- Filter by geographical location
- Custom date range selection

---

##  Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/social-media-analytics-dashboard.git
cd social-media-analytics-dashboard
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

or

```bash
python -m streamlit run app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

---

##  Dependencies

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0
wordcloud>=1.9.0
```

---

##  Project Structure

```
social-media-analytics-dashboard/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
│
│
└── screenshots/                # Dashboard screenshots
    ├── landing_page.png
    ├── dashboard.png
    └── analytics.png
```

---

##  Usage

### 1. **Prepare Your Data**

Your CSV file should contain the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| Text | Post content | ✅ Yes |
| Sentiment | Emotion (Positive, Negative, etc.) | ✅ Yes |
| Timestamp | Date and time | ✅ Yes |
| User | User identifier | ✅ Yes |
| Platform | Social media platform | ✅ Yes |
| Hashtags | Comma-separated hashtags | ✅ Yes |
| Likes | Number of likes | ✅ Yes |
| Retweets | Number of retweets | ✅ Yes |
| Country | Geographical location |  Optional |

**Example CSV format:**

```csv
Text,Sentiment,Timestamp,User,Platform,Hashtags,Likes,Retweets,Country
"Excited about the new AI features!",Positive,2024-01-15 10:30:00,user123,Twitter,"#AI,#Tech",150,50,USA
"This product is amazing!",Excited,2024-01-16 14:20:00,user456,Instagram,#Amazing,200,75,UK
```

### 2. **Upload Your Data**

1. Launch the dashboard
2. Drag and drop your CSV file or click to browse
3. Wait for automatic data cleaning and processing
4. Explore your insights!

### Use Xquik or TweetClaw exports

The uploader also accepts reviewed Xquik/TweetClaw exports in JSON, JSONL, or
NDJSON format. Common export fields such as `text`, `full_text`,
`author_username`, `created_at`, `like_count`, and `retweet_count` are mapped
into the dashboard columns automatically. Missing hashtags are extracted from
post text, and missing sentiment values default to `Neutral` so the existing
filters, engagement charts, trend detection, and raw-data download continue to
work without manual spreadsheet cleanup.

### 3. **Explore Analytics**

Navigate through 5 interactive tabs:

- **📊 Engagement Analysis**: View overall performance metrics
- **🎯 Content Performance**: Identify what works best
- **📈 Trend Detection**: Discover trending topics
- **🔮 Content Strategy**: Get optimization recommendations
- **📋 Raw Data**: Access and download filtered data

### 4. **Apply Filters**

Use the sidebar to refine your analysis:

- Select specific sentiments
- Choose platforms
- Filter by country
- Set custom date ranges

---

##  Screenshots

### Landing Page
<img width="1862" height="898" alt="image" src="https://github.com/user-attachments/assets/b9e65674-1923-4416-9389-d352d36ee4a2" />

*Modern landing page with drag-and-drop upload*

### Analytics Dashboard
<img width="1845" height="862" alt="image" src="https://github.com/user-attachments/assets/61b0dcf7-288f-4c72-8a65-24877498a1fc" />

*Interactive dashboard with real-time metrics*

### Engagement Analysis
<img width="1832" height="880" alt="image" src="https://github.com/user-attachments/assets/e7de72ac-7c92-4b42-bd3b-6f7936d71696" />

*Comprehensive engagement analysis charts*

---

## 🛠️ Data Cleaning Process

The dashboard automatically handles:

✅ Missing value imputation  
✅ Duplicate removal  
✅ Text normalization  
✅ Data type conversion  
✅ Engagement metric calculation  
✅ Time feature extraction  
✅ Hashtag processing  
✅ Invalid data filtering  

---





##  Key Metrics Explained

| Metric | Formula | Purpose |
|--------|---------|---------|
| Total Engagement | Likes + Retweets | Overall content performance |
| Engagement Rate | (Total Engagement / Followers) × 100 | Relative performance measure |
| Avg Engagement | Total Engagement / Number of Posts | Per-post performance |

---

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

##  Troubleshooting

### Issue: "No columns to parse from file"
**Solution**: Ensure your CSV has headers and is not empty

### Issue: White text in charts
**Solution**: Charts are now styled with dark text (#2C3E50)

### Issue: Dashboard not loading
**Solution**: Check if all dependencies are installed: `pip install -r requirements.txt`

### Issue: Upload fails
**Solution**: Verify CSV format matches expected structure (see Usage section)

---

##  Future Enhancements

- [ ] Real-time social media API integration
- [ ] Sentiment analysis using NLP models
- [ ] Automated report generation (PDF/PowerPoint)
- [ ] Multi-language support
- [ ] Competitor analysis features
- [ ] Machine learning predictions
- [ ] Mobile-responsive design
- [ ] User authentication and data persistence


---

##  Author

**Zonia Amer**

- LinkedIn: `https://www.linkedin.com/in/zonia-amer-78572022b/`
- GitHub: https://github.com/zonia7867
- Email: zoniaamer22@gmail.com

---


[⬆ Back to Top](#social-media-sentiments-analytics-dashboard)

</div>
