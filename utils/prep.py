import pandas as pd
import numpy as np

def clean_data(df):
    """
    清理数据，处理缺失值和异常值
    
    参数:
    df (pandas.DataFrame): 原始DataFrame
    
    返回:
    pandas.DataFrame: 清理后的DataFrame
    
    功能:
    1. 创建数据副本以避免修改原始数据
    2. 将特定标记值(-2.0, -1.0)替换为NaN
    3. 处理无穷大值
    4. 保持数据完整性
    
    注意:
    - 使用copy()方法创建副本以避免SettingWithCopyWarning
    - 仅处理数值类型的列
    """
    # 创建数据副本以避免修改原始数据
    # copy(): 创建DataFrame的副本，避免在清理过程中修改原始数据
    df_clean = df.copy()
    
    # 处理异常值和缺失值
    # select_dtypes: 选择数值类型的列
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    # 遍历所有数值列
    for col in numeric_cols:
        # 将-2.0和-1.0替换为NaN（这些可能是缺失值的标记）
        # replace: 替换指定值，-2.0和-1.0通常在数据集中表示缺失值
        df_clean[col] = df_clean[col].replace([-2.0, -1.0], np.nan)
        
        # 处理无穷大值
        # replace: 将正无穷大和负无穷大替换为NaN
        df_clean[col] = df_clean[col].replace([np.inf, -np.inf], np.nan)
    
    # 返回清理后的DataFrame
    return df_clean

def normalize_data(df):
    """
    标准化数据
    
    参数:
    df (pandas.DataFrame): DataFrame
    
    返回:
    pandas.DataFrame: 标准化后的DataFrame
    
    功能:
    1. 创建数据副本以避免修改原始数据
    2. 使用Z-score标准化方法
    3. 避免除以零的情况
    
    标准化方法:
    Z-score标准化: (x - μ) / σ
    其中μ是均值，σ是标准差
    
    注意:
    - 只对数值类型的列进行标准化
    - 当标准差为0时跳过标准化以避免除以零
    """
    # 创建数据副本以避免修改原始数据
    # copy(): 创建DataFrame的副本，避免在标准化过程中修改原始数据
    df_norm = df.copy()
    
    # 选择数值列进行标准化
    # select_dtypes: 选择数值类型的列
    numeric_cols = df_norm.select_dtypes(include=[np.number]).columns
    
    # 使用Z-score标准化
    # Z-score标准化公式: (x - μ) / σ
    # 遍历所有数值列
    for col in numeric_cols:
        # 检查标准差是否为零，避免除以零
        if df_norm[col].std() != 0:  # 避免除以零
            # 应用Z-score标准化公式
            # mean(): 计算均值
            # std(): 计算标准差
            df_norm[col] = (df_norm[col] - df_norm[col].mean()) / df_norm[col].std()
    
    # 返回标准化后的DataFrame
    return df_norm

def engineer_features(df):
    """
    特征工程，创建新的有用特征
    
    参数:
    df (pandas.DataFrame): DataFrame
    
    返回:
    pandas.DataFrame: 添加新特征后的DataFrame
    
    功能:
    1. 添加类别名称映射
    2. 计算衍生指标（观看/订阅者比率、互动率等）
    3. 创建综合评分
    4. 添加季节性特征
    5. 计算内容质量指标
    
    创建的新特征包括:
    - categoryName: 类别名称
    - views_per_subscriber: 每个订阅者的平均观看次数
    - like_rate: 点赞率
    - comment_rate: 评论率
    - engagement_score: 综合互动评分
    - dislike_rate: 不喜欢率
    - season: 季节特征
    - net_likes: 净喜欢数
    - like_to_dislike_ratio: 喜欢与不喜欢的比率
    """
    # 创建数据副本以避免修改原始数据
    # copy(): 创建DataFrame的副本，避免在特征工程过程中修改原始数据
    df_eng = df.copy()
    
    # 添加类别名称映射（基于YouTube标准类别ID）
    # 定义YouTube标准类别ID到类别名称的映射字典
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
    
    # 检查是否存在视频类别ID列
    if 'videoCategoryId' in df_eng.columns:
        # map: 使用映射字典将类别ID转换为类别名称
        df_eng['categoryName'] = df_eng['videoCategoryId'].map(category_mapping)
        # fillna: 将无法映射的值填充为'Unknown'
        df_eng['categoryName'] = df_eng['categoryName'].fillna('Unknown')
    
    # 计算一些有用的衍生指标
    # 检查观看数和订阅者数列是否存在
    if all(col in df_eng.columns for col in ['videoViewCount', 'subscriberCount']):
        # 计算每个订阅者的平均观看次数（排除异常值）
        # mask: 创建布尔掩码筛选有效数据（订阅者数和观看数都大于0）
        mask = (df_eng['subscriberCount'] > 0) & (df_eng['videoViewCount'] > 0)
        # loc: 使用位置索引安全地设置每订阅者观看数
        df_eng.loc[mask, 'views_per_subscriber'] = df_eng.loc[mask, 'videoViewCount'] / df_eng.loc[mask, 'subscriberCount']
    
    # 计算互动率
    # 检查点赞数和观看数列是否存在
    if all(col in df_eng.columns for col in ['videoLikeCount', 'videoViewCount']):
        # 计算点赞率并添加数据清洗
        # mask: 创建布尔掩码筛选观看数大于0的记录
        mask = df_eng['videoViewCount'] > 0
        # loc: 使用位置索引安全地设置点赞率
        df_eng.loc[mask, 'like_rate'] = df_eng.loc[mask, 'videoLikeCount'] / df_eng.loc[mask, 'videoViewCount']
        
        # 数据清洗 - 处理异常值
        # 点赞率理论上不应超过1（每个观看者最多点赞一次）
        # 超过1的值可能是数据收集错误
        # outlier_mask: 创建异常值掩码
        outlier_mask = df_eng['like_rate'] > 1
        # 将异常值设置为1.0（表示每个观看者都点赞）
        df_eng.loc[outlier_mask, 'like_rate'] = 1.0
    
    # 检查评论数和观看数列是否存在
    if all(col in df_eng.columns for col in ['VideoCommentCount', 'videoViewCount']):
        # mask: 创建布尔掩码筛选观看数大于0的记录
        mask = df_eng['videoViewCount'] > 0
        # loc: 使用位置索引安全地设置评论率
        df_eng.loc[mask, 'comment_rate'] = df_eng.loc[mask, 'VideoCommentCount'] / df_eng.loc[mask, 'videoViewCount']
    
    # 综合评分计算（简单示例）
    # 检查观看数、点赞数和评论数列是否存在
    if all(col in df_eng.columns for col in ['videoViewCount', 'videoLikeCount', 'VideoCommentCount']):
        # 过滤有效数据
        # valid_mask: 创建有效数据掩码（观看数大于0，点赞数和评论数非空）
        valid_mask = (df_eng['videoViewCount'] > 0) & (df_eng['videoLikeCount'].notna()) & (df_eng['VideoCommentCount'].notna())
        
        # 检查是否存在有效数据
        if valid_mask.any():
            # 计算综合评分（简化版）
            # 使用对数变换以减少极值的影响
            # np.log1p: 计算log(1+x)以处理零值
            df_eng.loc[valid_mask, 'engagement_score'] = (
                np.log1p(df_eng.loc[valid_mask, 'videoViewCount']) * 0.4 +
                np.log1p(df_eng.loc[valid_mask, 'videoLikeCount']) * 0.4 +
                np.log1p(df_eng.loc[valid_mask, 'VideoCommentCount']) * 0.2
            )
    
    # 计算更多的衍生指标
    # 检查观看数和评论数列是否存在
    if all(col in df_eng.columns for col in ['videoViewCount', 'VideoCommentCount']):
        # 计算评论率
        # mask: 创建布尔掩码筛选观看数大于0的记录
        mask = df_eng['videoViewCount'] > 0
        # loc: 使用位置索引安全地设置评论率
        df_eng.loc[mask, 'comment_rate'] = df_eng.loc[mask, 'VideoCommentCount'] / df_eng.loc[mask, 'videoViewCount']
    
    # 检查观看数和不喜欢数列是否存在
    if all(col in df_eng.columns for col in ['videoViewCount', 'videoDislikeCount']):
        # 计算不喜欢率
        # mask: 创建布尔掩码筛选观看数大于0的记录
        mask = df_eng['videoViewCount'] > 0
        # loc: 使用位置索引安全地设置不喜欢率
        df_eng.loc[mask, 'dislike_rate'] = df_eng.loc[mask, 'videoDislikeCount'] / df_eng.loc[mask, 'videoViewCount']
    
    # 添加基于时间段的特征
    # 检查发布月份列是否存在
    if 'publishMonth' in df_eng.columns:
        # 创建季节特征
        # 定义获取季节的函数
        def get_season(month):
            # 根据月份确定季节
            if month in [12, 1, 2]:
                return 'Winter'  # 冬季
            elif month in [3, 4, 5]:
                return 'Spring'  # 春季
            elif month in [6, 7, 8]:
                return 'Summer'  # 夏季
            else:
                return 'Fall'    # 秋季
        
        # apply: 对每个发布月份应用季节函数
        df_eng['season'] = df_eng['publishMonth'].apply(get_season)
    
    # 计算内容质量指标
    # 检查点赞数和不喜欢数列是否存在
    if all(col in df_eng.columns for col in ['videoLikeCount', 'videoDislikeCount']):
        # 计算净喜欢数（点赞数减去不喜欢数）
        df_eng['net_likes'] = df_eng['videoLikeCount'] - df_eng['videoDislikeCount']
        
        # 计算喜欢与不喜欢的比率
        # mask: 创建布尔掩码筛选不喜欢数大于0的记录
        mask = df_eng['videoDislikeCount'] > 0
        # loc: 使用位置索引安全地设置喜欢与不喜欢的比率
        df_eng.loc[mask, 'like_to_dislike_ratio'] = df_eng.loc[mask, 'videoLikeCount'] / df_eng.loc[mask, 'videoDislikeCount']
    
    # 返回添加新特征后的DataFrame
    return df_eng