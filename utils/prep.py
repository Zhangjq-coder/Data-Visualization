import pandas as pd
import numpy as np
def clean_data(df):
    """Clean the data by replacing invalid values with NaN."""
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df_clean[col] = df_clean[col].replace([-2.0, -1.0], np.nan)
        df_clean[col] = df_clean[col].replace([np.inf, -np.inf], np.nan)
    return df_clean
def normalize_data(df):
    """Normalize numeric columns in the dataframe."""
    df_norm = df.copy()
    numeric_cols = df_norm.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_norm[col].std() != 0:
            df_norm[col] = (df_norm[col] - df_norm[col].mean()) / df_norm[col].std()
    return df_norm
def engineer_features(df):
    """Engineer new features from the raw data."""
    df_eng = df.copy()
    category_mapping = {
        1: 'Film & Animation',
        2: 'Autos & Vehicles',
        10: 'Music',
        15: 'Pets & Animals',
        17: 'Sports',
        18: 'Short Movies',
        19: 'Travel & Events',
        20: 'Gaming',
        21: 'Videoblogging',
        22: 'People & Blogs',
        23: 'Comedy',
        24: 'Entertainment',
        25: 'News & Politics',
        26: 'Howto & Style',
        27: 'Education',
        28: 'Science & Technology',
        29: 'Nonprofits & Activism',
        30: 'Movies',
        31: 'Anime/Animation',
        32: 'Action/Adventure',
        33: 'Classics',
        34: 'Comedy',
        35: 'Documentary',
        36: 'Drama',
        37: 'Family',
        38: 'Foreign',
        39: 'Horror',
        40: 'Sci-Fi/Fantasy',
        41: 'Thriller',
        42: 'Shorts',
        43: 'Shows',
        44: 'Trailers'
    }
    if 'videoCategoryId' in df_eng.columns:
        df_eng['categoryName'] = df_eng['videoCategoryId'].map(category_mapping)
        df_eng['categoryName'] = df_eng['categoryName'].fillna('Unknown')
    if all(col in df_eng.columns for col in ['videoViewCount', 'subscriberCount']):
        mask = (df_eng['subscriberCount'] > 0) & (df_eng['videoViewCount'] > 0)
        df_eng.loc[mask, 'views_per_subscriber'] = df_eng.loc[mask, 'videoViewCount'] / df_eng.loc[mask, 'subscriberCount']
    if all(col in df_eng.columns for col in ['videoLikeCount', 'videoViewCount']):
        mask = df_eng['videoViewCount'] > 0
        df_eng.loc[mask, 'like_rate'] = df_eng.loc[mask, 'videoLikeCount'] / df_eng.loc[mask, 'videoViewCount']
        outlier_mask = df_eng['like_rate'] > 1
        df_eng.loc[outlier_mask, 'like_rate'] = 1.0
    if all(col in df_eng.columns for col in ['VideoCommentCount', 'videoViewCount']):
        mask = df_eng['videoViewCount'] > 0
        df_eng.loc[mask, 'comment_rate'] = df_eng.loc[mask, 'VideoCommentCount'] / df_eng.loc[mask, 'videoViewCount']
    if all(col in df_eng.columns for col in ['videoViewCount', 'videoLikeCount', 'VideoCommentCount']):
        valid_mask = (df_eng['videoViewCount'] > 0) & (df_eng['videoLikeCount'].notna()) & (df_eng['VideoCommentCount'].notna())
        if valid_mask.any():
            df_eng.loc[valid_mask, 'engagement_score'] = (
                np.log1p(df_eng.loc[valid_mask, 'videoViewCount']) * 0.4 +
                np.log1p(df_eng.loc[valid_mask, 'videoLikeCount']) * 0.4 +
                np.log1p(df_eng.loc[valid_mask, 'VideoCommentCount']) * 0.2
            )
    if all(col in df_eng.columns for col in ['videoViewCount', 'VideoCommentCount']):
        mask = df_eng['videoViewCount'] > 0
        df_eng.loc[mask, 'comment_rate'] = df_eng.loc[mask, 'VideoCommentCount'] / df_eng.loc[mask, 'videoViewCount']
    if all(col in df_eng.columns for col in ['videoViewCount', 'videoDislikeCount']):
        mask = df_eng['videoViewCount'] > 0
        df_eng.loc[mask, 'dislike_rate'] = df_eng.loc[mask, 'videoDislikeCount'] / df_eng.loc[mask, 'videoViewCount']
    if 'publishMonth' in df_eng.columns:
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Fall'
        df_eng['season'] = df_eng['publishMonth'].apply(get_season)
    if all(col in df_eng.columns for col in ['videoLikeCount', 'videoDislikeCount']):
        df_eng['net_likes'] = df_eng['videoLikeCount'] - df_eng['videoDislikeCount']
        mask = df_eng['videoDislikeCount'] > 0
        df_eng.loc[mask, 'like_to_dislike_ratio'] = df_eng.loc[mask, 'videoLikeCount'] / df_eng.loc[mask, 'videoDislikeCount']
    return df_eng