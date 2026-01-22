import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from data_cleaning import clean_social_media_data, get_data_summary
from collections import Counter
import io

# Page configuration
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with gradient backgrounds and modern styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global */
* {
    font-family: 'Inter', sans-serif;
}

/* Main background – subtle cool gray-blue */
.main {
    background: linear-gradient(135deg, #eef2f7 0%, #e6ebf2 100%);
    background-attachment: fixed;
}

/* Content wrapper */
.block-container {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
}

/* Header gradient – professional blue-teal */
.gradient-header {
    background: linear-gradient(90deg, #1e3a8a 0%, #0f766e 50%, #2563eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;
}

/* Hero text */
.hero-headline {
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    color: #0f172a;
}

.hero-subheadline {
    font-size: 1.3rem;
    text-align: center;
    color: #475569;
    margin-bottom: 2rem;
}

/* Upload zone */
.upload-zone {
    border: 2px dashed #2563eb;
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    background: #f8fafc;
    margin: 2rem 0;
    transition: all 0.3s ease;
}

.upload-zone:hover {
    border-color: #0f766e;
    background: #f1f5f9;
}

/* Feature cards */
.feature-card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    border: 1px solid #e5e7eb;
}

.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.15);
    border-color: #2563eb;
}

.feature-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0f172a;
}

.feature-desc {
    font-size: 1rem;
    color: #64748b;
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.07);
    border-left: 4px solid #2563eb;
}

.metric-card:hover {
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.18);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .element-container {
    color: #e5e7eb !important;
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #2563eb 0%, #0f766e 100%);
    color: white;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1.05rem;
}

.stButton>button:hover {
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    background: #f8fafc;
    border-radius: 10px 10px 0 0;
    padding: 1rem 2rem;
    font-weight: 600;
    border: 1px solid #e5e7eb;
    color: #334155;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb 0%, #0f766e 100%);
    color: white !important;
    border-color: #2563eb;
}

/* Tables */
.dataframe tbody tr:nth-child(even) {
    background-color: #f8fafc;
}

.dataframe tbody tr:hover {
    background-color: rgba(37, 99, 235, 0.08);
}

.dataframe td {
    color: #0f172a;
}

/* Alerts */
.stAlert {
    border-left: 4px solid #2563eb;
    border-radius: 10px;
}

/* Section title */
.section-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f172a;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df_clean' not in st.session_state:
    st.session_state.df_clean = None

# Check if file has been uploaded
if not st.session_state.data_loaded:
    # ========== LANDING PAGE ==========
    
    # Header with gradient logo
    st.markdown("<div class='gradient-header'>Social Media Sentiments Analytics Dashboard</div>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("<div class='hero-headline'>Transform Social Media Data Into Actionable Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subheadline'>Upload, Analyze, Optimize - All in One Platform</div>", unsafe_allow_html=True)
    
    # Upload Zone
    st.markdown("<div class='upload-zone'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("📁 Drag and drop your CSV file here or click to browse", type=['csv'], label_visibility="visible")
    
    if uploaded:
        try:
            # Read the file properly
            uploaded.seek(0)  # Reset file pointer
            df = pd.read_csv(uploaded)
            
            if df.empty or len(df.columns) == 0:
                st.error(" The uploaded file is empty or has no columns. Please upload a valid CSV file.")
            else:
                with st.spinner(" Cleaning and processing your data..."):
                    df_clean = clean_social_media_data(df)
                    st.session_state.df_clean = df_clean
                    st.session_state.data_loaded = True
                    st.success("Data loaded successfully!")
                    st.rerun()
        except pd.errors.EmptyDataError:
            st.error(" The uploaded file is empty. Please upload a valid CSV file with data.")
        except Exception as e:
            st.error(f" Error loading file: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Preview Section
    st.markdown("<div class='section-title'>Expected Data Format</div>", unsafe_allow_html=True)
    st.markdown("<div class='preview-table'>", unsafe_allow_html=True)
    sample_data = pd.DataFrame({
        'Text': ['Sample post about AI technology', 'Another exciting post about innovation'],
        'Sentiment': ['Positive', 'Excited'],
        'Timestamp': ['2024-01-15 10:30:00', '2024-01-16 14:20:00'],
        'User': ['user123', 'user456'],
        'Platform': ['Twitter', 'Instagram'],
        'Hashtags': ['#AI, #Tech', '#Innovation'],
        'Likes': [150, 200],
        'Retweets': [50, 75],
        'Country': ['USA', 'UK']
    })
    st.dataframe(sample_data, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("<div class='section-title'>Key Features</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <div class='feature-title'>Engagement Tracking</div>
            <div class='feature-desc'>Monitor likes, shares, and comments across all platforms in real-time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <div class='feature-title'>Performance Analysis</div>
            <div class='feature-desc'>Identify top-performing content and optimize your strategy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📈</div>
            <div class='feature-title'>Trend Detection</div>
            <div class='feature-desc'>Spot viral topics and trending hashtags before they peak</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔮</div>
            <div class='feature-title'>Strategy Optimization</div>
            <div class='feature-desc'>Get data-driven recommendations for maximum impact</div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ========== MAIN DASHBOARD ==========
    
    df_clean = st.session_state.df_clean
    
    # Top header
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.data_loaded = False
            st.session_state.df_clean = None
            st.rerun()
    with col2:
        st.markdown("<div class='gradient-header' style='font-size: 2.5rem;'>Social Media Sentiments Analytics Dashboard</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: right; font-size: 1.5rem;'>👤 ⚙️</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("<h2 style='color: white; text-align: center;'> Filters</h2>", unsafe_allow_html=True)
        st.markdown("---")
        for col in ['Sentiment', 'Platform', 'Country']:
            if col in df_clean.columns:
                df_clean[col] = (
                    df_clean[col]
                    .astype(str)
                    .str.strip()        
                    .str.title()        
                )
        # Sentiment filter
        if 'Sentiment' in df_clean.columns:
            sentiments = ['All'] + sorted(df_clean['Sentiment'].dropna().unique().tolist())
            selected_sentiment = st.selectbox("Sentiment", sentiments, key='sentiment_filter')
        else:
            selected_sentiment = 'All'

        
        # Platform filter
        if 'Platform' in df_clean.columns:
            platforms = ['All'] + sorted(df_clean['Platform'].dropna().unique().tolist())
            selected_platform = st.selectbox("Platform", platforms, key='platform_filter')
        else:
            selected_platform = 'All'

        
        # Country filter
        if 'Country' in df_clean.columns:
            df_clean['Country'] = (
            df_clean['Country']
            .astype(str)
            .str.strip()
            .str.title()
            )
            countries = ['All'] + sorted(df_clean['Country'].dropna().unique().tolist())

            selected_country = st.selectbox(
            "Country",
            countries,
            key='country_filter'
            )
        else:
            selected_country = 'All'
        
        # Date filters
        st.markdown("---")
        start_date = st.date_input("Start Date", value=None, key='start_date')
        end_date = st.date_input("End Date", value=None, key='end_date')
        
        st.markdown("---")
        col_reset = st.columns(1)[0]
        with col_reset:
            if st.button("Reset Filters", use_container_width=True):
                st.rerun()
    
    # Apply filters
    df_filtered = df_clean.copy()
    if selected_sentiment != 'All':
        df_filtered = df_filtered[df_filtered['Sentiment'] == selected_sentiment]
    if selected_platform != 'All':
        df_filtered = df_filtered[df_filtered['Platform'] == selected_platform]
    if selected_country != 'All':
        df_filtered = df_filtered[df_filtered['Country'] == selected_country]
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_data = [
        ("Total Posts", len(df_filtered), "+12.5%", "↑"),
        ("Total Likes", df_filtered['Likes'].sum(), "+8.3%", "↑"),
        ("Total Retweets", df_filtered['Retweets'].sum(), "+15.7%", "↑"),
        ("Avg Engagement", df_filtered['Total_Engagement'].mean(), "+5.2%", "↑"),
        ("Unique Users", df_filtered['User'].nunique() if 'User' in df_filtered.columns else 0, "+3.1%", "↑")
    ]
    
    for col, (label, value, change, arrow) in zip([col1, col2, col3, col4, col5], metrics_data):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem; color: #7F8C8D; margin-bottom: 0.5rem;'>{label}</div>
                <div style='font-size: 2rem; font-weight: 700; color: #2C3E50; margin-bottom: 0.5rem;'>
                    {value if isinstance(value, int) else f"{value:,.1f}"}
                </div>
                <div style='color: #2CA02C; font-size: 0.9rem;'>
                    <span style='font-size: 1.2rem;'>{arrow}</span> {change}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        " Engagement Analysis", 
        " Content Performance", 
        " Trend Detection",
        " Content Strategy",
        " Raw Data"
    ])    
    # TAB 1: Engagement Analysis
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Sentiment' in df_filtered.columns:
                sentiment_engagement = df_filtered.groupby('Sentiment').agg({
                    'Likes': 'sum',
                    'Retweets': 'sum'
                }).reset_index()
                
                fig = px.bar(
                    sentiment_engagement,
                    x='Sentiment',
                    y=['Likes', 'Retweets'],
                    title='Engagement by Sentiment',
                    barmode='group',
                    color_discrete_sequence=['#667eea', '#764ba2']
                )
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Platform' in df_filtered.columns:
                platform_engagement = df_filtered.groupby('Platform')['Total_Engagement'].sum().reset_index()
                
                fig = px.pie(
                    platform_engagement,
                    values='Total_Engagement',
                    names='Platform',
                    title='Engagement Distribution by Platform',
                    color_discrete_sequence=px.colors.sequential.Purples_r
                )
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)
        
        if 'Timestamp' in df_filtered.columns:
            daily_engagement = df_filtered.groupby(df_filtered['Timestamp'].dt.date).agg({
                'Likes': 'sum',
                'Retweets': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_engagement['Timestamp'], y=daily_engagement['Likes'], 
                                    mode='lines+markers', name='Likes', line=dict(color='#667eea', width=3)))
            fig.add_trace(go.Scatter(x=daily_engagement['Timestamp'], y=daily_engagement['Retweets'], 
                                    mode='lines+markers', name='Retweets', line=dict(color='#764ba2', width=3)))
            fig.update_layout(title='Engagement Trends Over Time', xaxis_title='Date', yaxis_title='Count',
                            plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Content Performance
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("###  Top 10 Posts by Engagement")
            top_posts = df_filtered.nlargest(10, 'Total_Engagement')[['Text', 'Likes', 'Retweets', 'Total_Engagement']]
            top_posts['Text'] = top_posts['Text'].str[:50] + '...'
            st.dataframe(top_posts, use_container_width=True, hide_index=True)
        
        with col2:
            if 'Hour' in df_filtered.columns:
                hourly_engagement = df_filtered.groupby('Hour')['Total_Engagement'].mean().reset_index()
                
                fig = px.line(
                    hourly_engagement,
                    x='Hour',
                    y='Total_Engagement',
                    title='Average Engagement by Hour of Day',
                    markers=True,
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)
        
        if 'DayOfWeek' in df_filtered.columns:
            st.markdown("###  Engagement by Day of Week")
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_engagement = df_filtered.groupby('DayOfWeek')['Total_Engagement'].mean().reindex(day_order).reset_index()
            
            fig = px.bar(
                day_engagement,
                x='DayOfWeek',
                y='Total_Engagement',
                title='Average Engagement by Day',
                color='Total_Engagement',
                color_continuous_scale=[[0, '#667eea'], [1, '#764ba2']]
            )
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: Trend Detection
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Trending Hashtags")
            all_hashtags = []
            for hashtags in df_filtered['Hashtags'].dropna():
                if hashtags != 'none':
                    all_hashtags.extend([h.strip() for h in str(hashtags).split(',')])
            
            if all_hashtags:
                hashtag_counts = Counter(all_hashtags).most_common(15)
                hashtag_df = pd.DataFrame(hashtag_counts, columns=['Hashtag', 'Count'])
                
                fig = px.bar(
                    hashtag_df,
                    x='Count',
                    y='Hashtag',
                    orientation='h',
                    title='Top 15 Hashtags',
                    color='Count',
                    color_continuous_scale=[[0, '#667eea'], [1, '#764ba2']]
                )
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Word Cloud")
            text = ' '.join(df_filtered['Text'].astype(str))
            
            if text.strip():
                wordcloud = WordCloud(width=800, height=400, background_color='white', 
                                     colormap='PuRd').generate(text)
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
        
        if 'Sentiment' in df_filtered.columns and 'Timestamp' in df_filtered.columns:
            st.markdown("###  Sentiment Trends Over Time")
            sentiment_time = df_filtered.groupby([df_filtered['Timestamp'].dt.date, 'Sentiment']).size().reset_index(name='Count')
            
            fig = px.line(
                sentiment_time,
                x='Timestamp',
                y='Count',
                color='Sentiment',
                title='Sentiment Distribution Over Time'
            )
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: Content Strategy
    with tab4:
        if 'Sentiment' in df_filtered.columns:
            best_sentiment = df_filtered.groupby('Sentiment')['Total_Engagement'].mean().idxmax()
            st.info(f" **Best Performing Sentiment:** {best_sentiment}")
        
        if 'Hour' in df_filtered.columns:
            best_hour = df_filtered.groupby('Hour')['Total_Engagement'].mean().idxmax()
            st.info(f" **Best Posting Time:** {best_hour}:00")
        
        if 'DayOfWeek' in df_filtered.columns:
            best_day = df_filtered.groupby('DayOfWeek')['Total_Engagement'].mean().idxmax()
            st.info(f" **Best Posting Day:** {best_day}")
        
        st.markdown("###  Content Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("####  Do More Of:")
            if 'Sentiment' in df_filtered.columns:
                top_sentiments = df_filtered.groupby('Sentiment')['Total_Engagement'].mean().nlargest(3)
                for sentiment, engagement in top_sentiments.items():
                    st.write(f"- **{sentiment}** posts (Avg engagement: {engagement:.1f})")
        
        with col2:
            st.markdown("####  Improve:")
            if 'Sentiment' in df_filtered.columns:
                bottom_sentiments = df_filtered.groupby('Sentiment')['Total_Engagement'].mean().nsmallest(3)
                for sentiment, engagement in bottom_sentiments.items():
                    st.write(f"- **{sentiment}** posts (Avg engagement: {engagement:.1f})")
        
        st.markdown("###  Optimal Content Length")
        df_filtered['Length_Category'] = pd.cut(
            df_filtered['Text_Length'],
            bins=[0, 50, 100, 200, 500, 1000],
            labels=['Very Short', 'Short', 'Medium', 'Long', 'Very Long']
        )
        
        length_performance = df_filtered.groupby('Length_Category')['Total_Engagement'].mean().reset_index()
        
        fig = px.bar(
            length_performance,
            x='Length_Category',
            y='Total_Engagement',
            title='Engagement by Content Length',
            color='Total_Engagement',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 5: Raw Data
    with tab5:
        st.markdown("###  Raw Data")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name='filtered_social_media_data.csv',
            mime='text/csv',
        )

