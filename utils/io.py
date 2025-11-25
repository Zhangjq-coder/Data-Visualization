import streamlit as st
import pandas as pd
import numpy as np
import os
import time
from utils.prep import engineer_features
def load_data(file_path, sample_size=None, progress_callback=None):
    try:
        if not os.path.exists(file_path):
            st.error(f"Error: File '{file_path}' not found")
            return pd.DataFrame()
        found_categories = set()
        st.write("Starting to load data...")
        total_rows = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for _ in f:
                    total_rows += 1
            total_rows -= 1
            st.write(f"Detected {total_rows:,} total rows in file")
        except Exception:
            total_rows = 100000
            st.write("Unable to calculate total rows, using default estimate")
        chunks = []
        chunk_size = min(100000, sample_size) if sample_size else 100000
        total_processed_rows = 0
        try:
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                chunk = chunk.dropna(subset=['categoryName']) if 'categoryName' in chunk.columns else chunk
                if 'categoryName' in chunk.columns:
                    current_categories = set(chunk['categoryName'].dropna().astype(str).unique())
                else:
                    chunk = chunk.dropna(subset=['videoCategoryId'])
                    current_categories = set(chunk['videoCategoryId'].dropna().astype(str).unique())
                found_categories.update(current_categories)
                sorted_categories = sorted(list(found_categories))
                if progress_callback:
                    current_processed = total_processed_rows + len(chunk)
                    display_total = min(sample_size, total_rows) if sample_size else total_rows
                    progress_percentage = (current_processed / display_total * 100) if display_total > 0 else 0
                    progress_percentage = min(progress_percentage, 100)
                    print(f"Debug - 回调进度: {current_processed}/{display_total} 行, 进度: {progress_percentage:.2f}%")
                    progress_callback({
                        'categories': sorted_categories,
                        'processed_rows': current_processed,
                        'total_rows': display_total,
                        'is_complete': False
                    })
                chunks.append(chunk)
                total_processed_rows += len(chunk)
                print(f"Debug - Chunk added, current processed rows: {total_processed_rows}, chunk size: {len(chunk)}")
                st.write(f"Loaded {total_processed_rows:,} rows of data...")
                st.write(f"Categories found so far: {len(found_categories)}")
                if sample_size and total_processed_rows >= sample_size:
                    print(f"Debug - Sample size {sample_size} reached, stopping loading")
                    break
                time.sleep(0.1)
        except pd.errors.EmptyDataError:
            st.error("Error: File is empty or incorrectly formatted")
            return pd.DataFrame()
        except pd.errors.ParserError as e:
            st.error(f"Error: Failed to parse CSV file - {str(e)}")
            return pd.DataFrame()
        df = pd.concat(chunks, ignore_index=True)
        if sample_size and len(df) > sample_size:
            df = df.sample(sample_size, random_state=42)
            st.write(f"Data sampling completed, total {len(df):,} rows")
        else:
            st.write(f"Data loading completed, total {len(df):,} rows")
        st.write("Performing data quality checks...")
        required_columns = ['videoViewCount', 'subscriberCount', 'videoLikeCount', 'VideoCommentCount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.warning(f"Missing key columns: {missing_columns}")
        numeric_columns = ['videoViewCount', 'subscriberCount', 'videoLikeCount', 'VideoCommentCount', 'videoDislikeCount']
        for col in numeric_columns:
            if col in df.columns:
                non_numeric_count = df[col].apply(lambda x: not isinstance(x, (int, float)) and not pd.isna(x)).sum()
                if non_numeric_count > 0:
                    st.warning(f"Column '{col}' contains {non_numeric_count} non-numeric values")
        if 'videoPublished' in df.columns:
            try:
                df['videoPublished'] = pd.to_datetime(df['videoPublished'], errors='coerce')
                if pd.api.types.is_datetime64_any_dtype(df['videoPublished']):
                    df['publishYear'] = df['videoPublished'].dt.year
                    df['publishMonth'] = df['videoPublished'].dt.month
                    df['publishDate'] = df['videoPublished'].dt.date
                else:
                    st.warning("Unable to convert videoPublished column to datetime type")
            except Exception as e:
                st.warning(f"Error processing datetime: {str(e)}")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df[col].replace([-2.0, -1.0], np.nan)
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        if 'categoryName' in df.columns:
            final_categories = sorted(list(df['categoryName'].dropna().astype(str).unique()))
        else:
            final_categories = sorted(list(df['videoCategoryId'].dropna().astype(str).unique()))
        if progress_callback:
            final_processed = len(df)
            display_total = min(sample_size, total_rows) if sample_size else total_rows
            print(f"Debug - 最终进度: {final_processed}/{display_total} 行, 进度: {100.0:.2f}%")
            progress_callback({
                'categories': final_categories,
                'processed_rows': final_processed,
                'total_rows': display_total,
                'is_complete': True
            })
        st.write("Data preprocessing completed")
        st.write(f"Final categories count: {len(final_categories)}")
        df = engineer_features(df)
        return df
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        import traceback
        st.exception(traceback.format_exc())
        if 'progress_callback' in locals() and progress_callback:
            progress_callback({
                'categories': [],
                'processed_rows': 0,
                'total_rows': total_rows if 'total_rows' in locals() else 0,
                'is_complete': True,
                'error': str(e)
            })
        return None