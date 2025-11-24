import pandas as pd
import numpy as np

def clean_data(df):
    """
    清理数据，处理缺失值和异常值
    
    参数:
    df: 原始DataFrame
    
    返回:
    清理后的DataFrame
    """
    # 创建数据副本以避免修改原始数据
    df_clean = df.copy()
    
    # 处理异常值和缺失值
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        # 将-2.0和-1.0替换为NaN（这些可能是缺失值的标记）
        df_clean[col] = df_clean[col].replace([-2.0, -1.0], np.nan)
        
        # 处理无穷大值
        df_clean[col] = df_clean[col].replace([np.inf, -np.inf], np.nan)
    
    return df_clean

def normalize_data(df):
    """
    标准化数据
    
    参数:
    df: DataFrame
    
    返回:
    标准化后的DataFrame
    """
    # 创建数据副本
    df_norm = df.copy()
    
    # 选择数值列进行标准化
    numeric_cols = df_norm.select_dtypes(include=[np.number]).columns
    
    # 使用Z-score标准化
    for col in numeric_cols:
        if df_norm[col].std() != 0:  # 避免除以零
            df_norm[col] = (df_norm[col] - df_norm[col].mean()) / df_norm[col].std()
    
    return df_norm

def engineer_features(df):
    """
    特征工程，创建新的有用特征
    
    参数:
    df: DataFrame
    
    返回:
    添加新特征后的DataFrame
    """
    # 创建数据副本
    df_eng = df.copy()
    
    # 添加类别名称映射（基于YouTube标准类别ID）
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
    
    # 计算一些有用的衍生指标
    if all(col in df_eng.columns for col in ['videoViewCount', 'subscriberCount']):
        # 计算每个订阅者的平均观看次数（排除异常值）
        mask = (df_eng['subscriberCount'] > 0) & (df_eng['videoViewCount'] > 0)
        df_eng.loc[mask, 'views_per_subscriber'] = df_eng.loc[mask, 'videoViewCount'] / df_eng.loc[mask, 'subscriberCount']
    
    # 计算互动率
    if all(col in df_eng.columns for col in ['videoLikeCount', 'videoViewCount']):
        # 计算点赞率并添加数据清洗
        mask = df_eng['videoViewCount'] > 0
        df_eng.loc[mask, 'like_rate'] = df_eng.loc[mask, 'videoLikeCount'] / df_eng.loc[mask, 'videoViewCount']
        
        # 数据清洗 - 处理异常值
        # 点赞率理论上不应超过1（每个观看者最多点赞一次）
        # 超过1的值可能是数据收集错误
        outlier_mask = df_eng['like_rate'] > 1
        # 将异常值设置为1.0
        df_eng.loc[outlier_mask, 'like_rate'] = 1.0
    
    if all(col in df_eng.columns for col in ['VideoCommentCount', 'videoViewCount']):
        mask = df_eng['videoViewCount'] > 0
        df_eng.loc[mask, 'comment_rate'] = df_eng.loc[mask, 'VideoCommentCount'] / df_eng.loc[mask, 'videoViewCount']
    
    # 综合评分计算（简单示例）
    if all(col in df_eng.columns for col in ['videoViewCount', 'videoLikeCount', 'VideoCommentCount']):
        # 过滤有效数据
        valid_mask = (df_eng['videoViewCount'] > 0) & (df_eng['videoLikeCount'].notna()) & (df_eng['VideoCommentCount'].notna())
        
        if valid_mask.any():
            # 计算综合评分（简化版）
            df_eng.loc[valid_mask, 'engagement_score'] = (
                np.log1p(df_eng.loc[valid_mask, 'videoViewCount']) * 0.4 +
                np.log1p(df_eng.loc[valid_mask, 'videoLikeCount']) * 0.4 +
                np.log1p(df_eng.loc[valid_mask, 'VideoCommentCount']) * 0.2
            )
    
    return df_eng