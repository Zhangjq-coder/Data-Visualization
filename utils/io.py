import streamlit as st
import pandas as pd
import numpy as np
import os

@st.cache_data
def load_data(file_path, sample_size=None):
    """
    加载并预处理YouTube数据集
    
    参数:
    file_path: 数据集文件路径
    sample_size: 采样大小，如果为None则加载全部数据
    
    返回:
    预处理后的DataFrame
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            st.error(f"错误：找不到文件 '{file_path}'")
            # 返回一个空的DataFrame作为备用
            return pd.DataFrame()
        
        st.write("开始加载数据... | Starting to load data...")
        
        # 使用chunksize分块读取大数据集
        chunks = []
        chunk_size = 100000
        
        try:
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                chunks.append(chunk)
                st.write(f"已加载 {len(chunks) * chunk_size:,} 行数据... | Loaded {len(chunks) * chunk_size:,} rows of data...")
                
                # 如果指定了采样大小且已达到，则停止加载
                if sample_size and len(chunks) * chunk_size >= sample_size:
                    break
        except pd.errors.EmptyDataError:
            st.error("错误：文件为空或格式不正确")
            return pd.DataFrame()
        except pd.errors.ParserError as e:
            st.error(f"错误：解析CSV文件时出错 - {str(e)}")
            return pd.DataFrame()
        
        # 合并所有块
        df = pd.concat(chunks, ignore_index=True)
        
        # 如果指定了采样大小，随机采样
        if sample_size and len(df) > sample_size:
            df = df.sample(sample_size, random_state=42)
        
        st.write(f"数据加载完成，共 {len(df):,} 行 | Data loading completed, total {len(df):,} rows")
        
        # 数据类型转换和预处理
        if 'videoPublished' in df.columns:
            # 安全地转换日期时间并处理错误
            try:
                df['videoPublished'] = pd.to_datetime(df['videoPublished'], errors='coerce')
                # 检查是否成功转换为日期时间类型
                if pd.api.types.is_datetime64_any_dtype(df['videoPublished']):
                    df['publishYear'] = df['videoPublished'].dt.year
                    df['publishMonth'] = df['videoPublished'].dt.month
                    df['publishDate'] = df['videoPublished'].dt.date
                else:
                    st.warning("无法将videoPublished列转换为日期时间类型")
            except Exception as e:
                st.warning(f"处理日期时间时出错: {str(e)}")
        
        # 处理异常值和缺失值
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            # 将-2.0和-1.0替换为NaN（这些可能是缺失值的标记）
            df[col] = df[col].replace([-2.0, -1.0], np.nan)
            
            # 处理无穷大值
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        
        st.write("数据预处理完成 | Data preprocessing completed")
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        import traceback
        st.exception(traceback.format_exc())
        return None