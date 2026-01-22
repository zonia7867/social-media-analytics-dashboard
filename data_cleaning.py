import pandas as pd
import numpy as np
from datetime import datetime

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