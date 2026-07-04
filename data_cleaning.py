import json
import re
import pandas as pd
import numpy as np
from datetime import datetime

TEXT_COLUMNS = ('Text', 'text', 'full_text', 'tweet_text', 'content', 'body')
SENTIMENT_COLUMNS = ('Sentiment', 'sentiment', 'sentiment_label')
TIMESTAMP_COLUMNS = ('Timestamp', 'created_at', 'createdAt', 'timestamp', 'date')
USER_COLUMNS = ('User', 'author_username', 'username', 'screen_name', 'author')
LIKE_COLUMNS = ('Likes', 'like_count', 'favorite_count', 'likes', 'favorites')
RETWEET_COLUMNS = ('Retweets', 'retweet_count', 'share_count', 'retweets', 'shares')
HASHTAG_COLUMNS = ('Hashtags', 'hashtags', 'tags')
COUNTRY_COLUMNS = ('Country', 'country', 'location')
HASHTAG_PATTERN = re.compile(r'#\w+')


def first_existing_column(df, columns):
    for column in columns:
        if column in df.columns:
            return column
    return None


def extract_hashtags(text):
    tags = HASHTAG_PATTERN.findall(str(text))
    return ','.join(tags) if tags else 'none'


def read_social_media_upload(uploaded_file):
    name = getattr(uploaded_file, 'name', '').lower()
    uploaded_file.seek(0)

    if name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        raw = uploaded_file.getvalue()
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8-sig')

        if name.endswith(('.jsonl', '.ndjson')):
            rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
            df = pd.DataFrame(rows)
        else:
            payload = json.loads(raw)
            if isinstance(payload, dict):
                for key in ('data', 'items', 'posts', 'results', 'tweets'):
                    value = payload.get(key)
                    if isinstance(value, list):
                        payload = value
                        break
            df = pd.DataFrame(payload)

    return normalize_social_media_export(df)


def normalize_social_media_export(df):
    required_columns = {'Text', 'Sentiment', 'Timestamp', 'User', 'Platform', 'Hashtags', 'Likes', 'Retweets'}
    if required_columns.issubset(df.columns):
        return df

    text_column = first_existing_column(df, TEXT_COLUMNS)
    if text_column is None:
        return df

    sentiment_column = first_existing_column(df, SENTIMENT_COLUMNS)
    timestamp_column = first_existing_column(df, TIMESTAMP_COLUMNS)
    user_column = first_existing_column(df, USER_COLUMNS)
    like_column = first_existing_column(df, LIKE_COLUMNS)
    retweet_column = first_existing_column(df, RETWEET_COLUMNS)
    hashtag_column = first_existing_column(df, HASHTAG_COLUMNS)
    country_column = first_existing_column(df, COUNTRY_COLUMNS)

    normalized = pd.DataFrame()
    normalized['Text'] = df[text_column].fillna('').astype(str)
    normalized['Sentiment'] = df[sentiment_column] if sentiment_column else 'Neutral'
    normalized['Timestamp'] = df[timestamp_column] if timestamp_column else datetime.utcnow().isoformat()
    normalized['User'] = df[user_column] if user_column else 'xquik-export'
    normalized['Platform'] = df['Platform'] if 'Platform' in df.columns else 'Twitter'
    if hashtag_column:
        normalized['Hashtags'] = df[hashtag_column].fillna('none')
    else:
        normalized['Hashtags'] = normalized['Text'].apply(extract_hashtags)
    normalized['Likes'] = pd.to_numeric(df[like_column], errors='coerce').fillna(0) if like_column else 0
    normalized['Retweets'] = pd.to_numeric(df[retweet_column], errors='coerce').fillna(0) if retweet_column else 0
    normalized['Country'] = df[country_column] if country_column else 'Unknown'
    return normalized


def clean_social_media_data(df):
    print("Cleaning the data...")
    df_clean = df.copy()
    print(f"Missing values before cleaning:\n{df_clean.isnull().sum()}")
    df_clean['Text'] = df_clean['Text'].fillna('')
    df_clean['Hashtags'] = df_clean['Hashtags'].fillna('none')
    df_clean['Country'] = df_clean['Country'].fillna('Unknown')
    df_clean['Likes'] = df_clean['Likes'].fillna(0)
    df_clean['Retweets'] = df_clean['Retweets'].fillna(0)
    
   
    before_dup = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {before_dup - len(df_clean)} duplicate rows")
    
    df_clean['Text'] = df_clean['Text'].str.strip()
    df_clean['Text_Length'] = df_clean['Text'].str.len()
    
    df_clean['Likes'] = pd.to_numeric(df_clean['Likes'], errors='coerce').fillna(0).astype(int)
    df_clean['Retweets'] = pd.to_numeric(df_clean['Retweets'], errors='coerce').fillna(0).astype(int)
    
    if 'Timestamp' in df_clean.columns:
        df_clean['Timestamp'] = pd.to_datetime(df_clean['Timestamp'], errors='coerce')
    else:
        if all(col in df_clean.columns for col in ['Year', 'Month', 'Day']):
            df_clean['Hour'] = df_clean.get('Hour', 0)
            df_clean['Timestamp'] = pd.to_datetime(
                df_clean[['Year', 'Month', 'Day']].assign(Hour=df_clean['Hour'])
            )
    
    df_clean['Total_Engagement'] = df_clean['Likes'] + df_clean['Retweets']
    df_clean['Engagement_Rate'] = (df_clean['Total_Engagement'] / 
                                    (df_clean['Likes'] + df_clean['Retweets'] + 1)) * 100
    
    if 'Timestamp' in df_clean.columns:
        df_clean['Year'] = df_clean['Timestamp'].dt.year
        df_clean['Month'] = df_clean['Timestamp'].dt.month
        df_clean['Day'] = df_clean['Timestamp'].dt.day
        df_clean['Hour'] = df_clean['Timestamp'].dt.hour
        df_clean['DayOfWeek'] = df_clean['Timestamp'].dt.day_name()
        df_clean['Month_Name'] = df_clean['Timestamp'].dt.month_name()

    df_clean['Hashtags'] = df_clean['Hashtags'].str.lower().str.strip()
    df_clean['Hashtag_Count'] = df_clean['Hashtags'].apply(
        lambda x: len(str(x).split(',')) if x != 'none' else 0
    )
    
    df_clean = df_clean[df_clean['Text_Length'] > 0]
    df_clean = df_clean[df_clean['Likes'] >= 0]
    df_clean = df_clean[df_clean['Retweets'] >= 0]
    
    print(f"Cleaning complete! Final dataset: {len(df_clean)} rows")
    print(f"Missing values after cleaning:\n{df_clean.isnull().sum()}")
    
    return df_clean


def get_data_summary(df):
    """
    Get a summary of the cleaned data
    """
    summary = {
        'total_posts': len(df),
        'unique_users': df['User'].nunique() if 'User' in df.columns else 0,
        'unique_platforms': df['Platform'].nunique() if 'Platform' in df.columns else 0,
        'total_likes': df['Likes'].sum(),
        'total_retweets': df['Retweets'].sum(),
        'avg_engagement': df['Total_Engagement'].mean(),
        'date_range': f"{df['Timestamp'].min()} to {df['Timestamp'].max()}" if 'Timestamp' in df.columns else 'N/A'
    }
    return summary
