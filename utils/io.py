import streamlit as st
import pandas as pd
import numpy as np
import os

@st.cache_data
def load_data(file_path, sample_size=None):
    """
    加载并预处理YouTube数据集
    
    参数:
    file_path (str): 数据集文件路径
    sample_size (int, optional): 采样大小，如果为None则加载全部数据
    
    返回:
    pandas.DataFrame: 预处理后的DataFrame
    
    功能:
    1. 分块读取大型CSV文件以节省内存
    2. 支持数据采样以提高性能
    3. 执行数据质量检查
    4. 处理日期时间列
    5. 清理异常值和缺失值
    6. 提供详细的加载进度和错误处理
    
    异常处理:
    - 文件不存在
    - 空文件或格式错误
    - CSV解析错误
    - 通用异常捕获
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            st.error(f"错误：找不到文件 '{file_path}'")
            # 返回一个空的DataFrame作为备用
            return pd.DataFrame()
        
        # 显示开始加载数据的消息
        st.write("开始加载数据... | Starting to load data...")
        
        # 使用chunksize分块读取大数据集
        # 这样可以避免一次性将整个大文件加载到内存中
        chunks = []
        chunk_size = 100000
        
        try:
            # pd.read_csv: 使用chunksize参数分块读取CSV文件
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                # 将每个块添加到chunks列表中
                chunks.append(chunk)
                # 显示加载进度
                st.write(f"已加载 {len(chunks) * chunk_size:,} 行数据... | Loaded {len(chunks) * chunk_size:,} rows of data...")
                
                # 如果指定了采样大小且已达到，则停止加载
                # 这样可以提前停止读取，提高性能
                if sample_size and len(chunks) * chunk_size >= sample_size:
                    break
        # 处理空数据文件异常
        except pd.errors.EmptyDataError:
            st.error("错误：文件为空或格式不正确")
            return pd.DataFrame()
        # 处理CSV解析异常
        except pd.errors.ParserError as e:
            st.error(f"错误：解析CSV文件时出错 - {str(e)}")
            return pd.DataFrame()
        
        # 合并所有块
        # pd.concat: 将所有数据块合并成一个DataFrame
        df = pd.concat(chunks, ignore_index=True)
        
        # 如果指定了采样大小，随机采样
        # sample: 随机采样指定数量的记录
        if sample_size and len(df) > sample_size:
            # random_state: 设置随机种子以确保结果可重现
            df = df.sample(sample_size, random_state=42)
        
        # 显示数据加载完成的消息
        st.write(f"数据加载完成，共 {len(df):,} 行 | Data loading completed, total {len(df):,} rows")
        
        # 数据质量检查
        st.write("正在进行数据质量检查... | Performing data quality checks...")
        
        # 检查关键字段是否存在
        # 定义关键字段列表
        required_columns = ['videoViewCount', 'subscriberCount', 'videoLikeCount', 'VideoCommentCount']
        # 检查缺失的列
        missing_columns = [col for col in required_columns if col not in df.columns]
        # 如果存在缺失列，显示警告
        if missing_columns:
            st.warning(f"以下关键字段缺失: {missing_columns} | Missing key columns: {missing_columns}")
        
        # 检查数据类型
        # 定义数值列列表
        numeric_columns = ['videoViewCount', 'subscriberCount', 'videoLikeCount', 'VideoCommentCount', 'videoDislikeCount']
        # 遍历数值列
        for col in numeric_columns:
            # 检查列是否存在于数据中
            if col in df.columns:
                # 检查是否包含非数值数据
                # apply: 对每个元素应用检查函数
                # isinstance: 检查数据类型
                # pd.isna: 检查是否为NaN
                non_numeric_count = df[col].apply(lambda x: not isinstance(x, (int, float)) and not pd.isna(x)).sum()
                # 如果存在非数值数据，显示警告
                if non_numeric_count > 0:
                    st.warning(f"列 '{col}' 包含 {non_numeric_count} 个非数值数据 | Column '{col}' contains {non_numeric_count} non-numeric values")
        
        # 数据类型转换和预处理
        # 检查是否存在视频发布日期列
        if 'videoPublished' in df.columns:
            # 安全地转换日期时间并处理错误
            try:
                # pd.to_datetime: 转换为日期时间类型
                # errors='coerce': 无法转换的值设为NaT
                df['videoPublished'] = pd.to_datetime(df['videoPublished'], errors='coerce')
                # 检查是否成功转换为日期时间类型
                # pd.api.types.is_datetime64_any_dtype: 检查是否为日期时间类型
                if pd.api.types.is_datetime64_any_dtype(df['videoPublished']):
                    # 提取年份、月份和日期
                    df['publishYear'] = df['videoPublished'].dt.year
                    df['publishMonth'] = df['videoPublished'].dt.month
                    df['publishDate'] = df['videoPublished'].dt.date
                else:
                    # 如果转换失败，显示警告
                    st.warning("无法将videoPublished列转换为日期时间类型")
            # 捕获处理日期时间时的异常
            except Exception as e:
                st.warning(f"处理日期时间时出错: {str(e)}")
        
        # 处理异常值和缺失值
        # select_dtypes: 选择数值类型的列
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        # 遍历数值列
        for col in numeric_cols:
            # 将-2.0和-1.0替换为NaN（这些可能是缺失值的标记）
            # replace: 替换指定值
            df[col] = df[col].replace([-2.0, -1.0], np.nan)
            
            # 处理无穷大值
            # replace: 替换无穷大值为NaN
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        
        # 显示数据预处理完成的消息
        st.write("数据预处理完成 | Data preprocessing completed")
        # 返回预处理后的DataFrame
        return df
    # 捕获通用异常
    except Exception as e:
        # 显示错误信息
        st.error(f"数据加载失败: {e}")
        # 显示详细异常信息
        import traceback
        st.exception(traceback.format_exc())
        # 返回None表示加载失败
        return None