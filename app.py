import streamlit as st
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sections import intro, overview, deep_dives, conclusions
from utils.io import load_data
from utils.prep import engineer_features
st.set_page_config(page_title="YouTube Dataset Visualization Analysis", layout="wide")
page_style = """<style>
    .main-header {
        color: #333;
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
        border-bottom: 2px solid #eee;
    }
    .sidebar-header {
        color: #333;
        margin-bottom: 0.5rem;
    }
</style>"""
st.markdown(page_style, unsafe_allow_html=True)
st.markdown("<h1 class='main-header'>YouTube Dataset Visualization Analysis</h1>", unsafe_allow_html=True)
with st.sidebar:
    st.image("assets/WUT-Logo.png", caption="WUT Logo", use_container_width=True)
    st.image("assets/微信图片_20251121083856_98_172.png", caption="Related Image", use_container_width=True)
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>Course Information</h3>", unsafe_allow_html=True)
    st.write("Course Name: Data Visualization")
    st.write("Instructor: Prof. Mano Mathew")
    st.write("Student Name: Junqing Zhang")
    st.write("Student ID: 20252223")
    st.write("Email: junqing.zhang@efrei.net")
    st.markdown("[GitHub Project](https://github.com/Zhangjq-coder/Data-Visualization)")
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>About Dataset</h3>", unsafe_allow_html=True)
    st.info("This dataset contains detailed statistics on YouTube channels and videos, including views, subscriber counts, likes, and other metrics.")
    st.markdown("[View Dataset](https://www.kaggle.com/datasets/thedevastator/revealing-insights-from-youtube-video-and-channe/data)")
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>Interface Settings</h3>", unsafe_allow_html=True)
    theme = st.selectbox(
        "Select Theme Color",
        ["Default Blue", "Energetic Green", "Warm Orange", "Elegant Purple"],
        index=0,
        help="Select the theme color for the application"
    )
    if theme == "Energetic Green":
        st.markdown("""<style>:root{--primary-color:#4CAF50;--secondary-color:#81C784;}</style>""", unsafe_allow_html=True)
    elif theme == "Warm Orange":
        st.markdown("""<style>:root{--primary-color:#FF9800;--secondary-color:#FFB74D;}</style>""", unsafe_allow_html=True)
    elif theme == "Elegant Purple":
        st.markdown("""<style>:root{--primary-color:#9C27B0;--secondary-color:#BA68C8;}</style>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>Data Filtering</h3>", unsafe_allow_html=True)
    show_data_info = st.checkbox("Show Basic Data Info", value=True, help="Control whether to display basic data information statistics")
    if 'refresh_data' not in st.session_state:
        st.session_state.refresh_data = False
    refresh_data = st.button("Refresh Data", help="Reload and process the dataset")
    if refresh_data:
        st.session_state.refresh_data = True
        st.rerun()
def main():
    file_path = "data/YouTubeDataset_withChannelElapsed.csv"
    import os
    if not os.path.exists(file_path):
        st.error(f"Data file '{file_path}' does not exist, please check the path.")
        return
    with st.sidebar:
        st.markdown("---")
        st.markdown("<h3 class='sidebar-header'>Data Sampling Settings</h3>", unsafe_allow_html=True)
        use_sampling = st.checkbox("Use Data Sampling (For Large Datasets)", value=True)
        sample_size = st.slider(
            "Sample Size",
            min_value=1000,
            max_value=100000,
            value=50000,
            step=1000,
            disabled=not use_sampling
        )
        if use_sampling:
            random_seed = st.number_input("Random Seed", min_value=0, value=42, help="Set random seed for reproducible sampling results")
        st.markdown("---")
        st.markdown("<h3 class='sidebar-header'>Data Quality Filtering</h3>", unsafe_allow_html=True)
        min_views_default = st.session_state.get('min_views_default', 0)
        max_views_default = st.session_state.get('max_views_default', 1000000)
        selected_categories_default = st.session_state.get('selected_categories_default', [])
        available_categories = st.session_state.get('available_categories', [])
        st.markdown("### # View Count Filtering")
        col1, col2 = st.columns(2)
        with col1:
            min_views = st.number_input(
                "Minimum Views",
                min_value=0,
                value=min_views_default,
                step=1000,
                help="Filter out videos with views below this value",
                key="min_views"
            )
        with col2:
            max_views = st.number_input(
                "Maximum Views",
                min_value=0,
                value=max_views_default,
                step=1000,
                help="Filter out videos with views above this value",
                key="max_views"
            )
        st.markdown("### # Category Filtering")
        if 'available_categories' not in st.session_state:
            st.session_state['available_categories'] = []
        if 'selected_categories_default' not in st.session_state:
            st.session_state['selected_categories_default'] = []
        available_categories = st.session_state.get('available_categories', [])
        display_categories = available_categories if available_categories else ["Entertainment", "Music", "Education", "Gaming", "Science & Technology"]
        previous_selected = st.session_state.get('selected_categories_cache', [])
        valid_defaults = [cat for cat in previous_selected if cat in display_categories]
        if not valid_defaults and previous_selected:
            valid_defaults = st.session_state['selected_categories_default']
        selected_categories = st.multiselect(
            "Select Video Categories",
            options=display_categories,
            default=valid_defaults,
            key="selected_categories",
            help="Select video categories to analyze, leave empty for all",
            disabled=False
        )
        st.session_state['selected_categories_cache'] = selected_categories
        if st.session_state.get('loading_in_progress', False):
            progress_info = st.session_state.get('loading_progress', {})
            if progress_info.get('processed_rows', 0) > 0:
                progress_container = st.empty()
                total_rows = progress_info.get('total_rows', 100000)
                progress = min(progress_info['processed_rows'] / total_rows, 1.0)
                with progress_container.container():
                    st.progress(progress)
                    st.info(f"Loading data, processed {progress_info['processed_rows']:,} rows, " \
                           f"found {len(available_categories)} categories...")
            else:
                st.info("Data loading, category list will update in real time...")
        elif 'prev_category_count' in st.session_state and \
             st.session_state['prev_category_count'] < len(available_categories):
            st.info(f"Category list updated, now {len(available_categories)} categories available")
        st.session_state['prev_category_count'] = len(available_categories)
        with st.expander("Advanced Filter Options", expanded=False):
            st.markdown("#### # Outlier Handling")
            filter_outliers = st.checkbox(
                "Filter Outliers",
                value=True,
                help="Enable this option to filter out outliers in the data for more accurate analysis results"
            )
            st.session_state['filter_outliers'] = filter_outliers
            st.markdown("#### # Other Options")
            st.info("More filter options will be available after data loading")
        st.markdown("---")
        if st.button("🔄 Reset All Settings", key="reset_filter", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        if 'available_categories' not in st.session_state:
            st.session_state['available_categories'] = []
        if 'loading_in_progress' not in st.session_state:
            st.session_state['loading_in_progress'] = False
        if 'progress_message' not in st.session_state:
            st.session_state['progress_message'] = ""
        def progress_callback(progress_info):
            st.session_state['loading_progress'] = progress_info
            if 'categories' in progress_info:
                new_categories = set(st.session_state.get('available_categories', []))
                new_categories.update(progress_info['categories'])
                st.session_state['available_categories'] = sorted(list(new_categories))
            if 'error' in progress_info:
                st.session_state['loading_error'] = progress_info['error']
                st.session_state['loading_in_progress'] = False
                st.session_state['progress_message'] = f"Error loading data: {progress_info['error']}"
            elif progress_info.get('is_complete', False):
                st.session_state['progress_message'] = "Data loading complete!"
                st.session_state['loading_in_progress'] = False
            else:
                st.session_state['progress_message'] = f"Processed {progress_info.get('processed_rows', 0)} rows, found {len(st.session_state.get('available_categories', []))} categories..."
        progress_container = st.empty()
        if st.session_state.get('loading_in_progress', False):
            progress_info = st.session_state.get('loading_progress', {})
            processed_rows = progress_info.get('processed_rows', 0)
            total_rows = progress_info.get('total_rows', 100000)
            current_categories = st.session_state.get('available_categories', [])
            progress = min(processed_rows / total_rows, 1.0) if total_rows else 0
            with progress_container.container():
                st.progress(progress)
                st.info(f"Loading data: {int(progress * 100)}% | Processed {processed_rows:,} rows | Found {len(current_categories)} categories")
        elif st.session_state['progress_message']:
            progress_container.info(st.session_state['progress_message'])
        if 'prev_sampling_settings' in st.session_state and (\
           st.session_state['prev_sampling_settings']['use_sampling'] != use_sampling or \
           st.session_state['prev_sampling_settings']['sample_size'] != sample_size):
            st.session_state['prev_sampling_settings'] = {
                'use_sampling': use_sampling,
                'sample_size': sample_size
            }
            st.session_state.refresh_data = True
            st.rerun()
        if 'prev_sampling_settings' not in st.session_state:
            st.session_state['prev_sampling_settings'] = {
                'use_sampling': use_sampling,
                'sample_size': sample_size
            }
        if 'data_loaded' not in st.session_state or st.session_state.get('refresh_data', False):
            st.session_state.loading_in_progress = True
            st.session_state.progress_message = "Starting to load data..."
            df = load_data(
                file_path,
                sample_size=sample_size if use_sampling else None,
                progress_callback=progress_callback
            )
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.session_state.loading_in_progress = False
            st.session_state.refresh_data = False
            if df is not None:
                progress_container.success(f"✅ Data loading complete! Loaded {len(df):,} records")
            else:
                progress_container.error("❌ Data loading failed, please check the data file and format")
        elif 'df' in st.session_state:
            df = st.session_state.df
            if df is not None:
                progress_container.info(f"✅ Using cached data, {len(df):,} records")
            else:
                progress_container.error("❌ Cached data is invalid, please reload data")
        else:
            st.session_state.loading_in_progress = True
            st.session_state.progress_message = "Starting to load data..."
            df = load_data(
                file_path,
                sample_size=sample_size if use_sampling else None,
                progress_callback=progress_callback
            )
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.session_state.loading_in_progress = False
    if df is not None:
        st.success(f"Successfully loaded data, total {len(df):,} records")
        if 'videoViewCount' in df.columns:
            max_views_val = int(df['videoViewCount'].max()) if len(df) > 0 else 1000000
            st.session_state['max_views_default'] = max_views_val
        if 'categoryName' in df.columns:
            try:
                categories = df['categoryName'].dropna().unique().tolist()
                if categories:
                    categories.sort()
                    st.session_state['available_categories'] = categories
                else:
                    st.warning("No valid category information found in the data")
                    st.session_state['available_categories'] = []
            except Exception as e:
                st.error(f"Error processing category data: {str(e)}")
                st.session_state['available_categories'] = []
        if 'selected_categories_default' not in st.session_state:
            st.session_state['selected_categories_default'] = []
        needs_rerun = False
        if 'videoViewCount' in df.columns and 'max_views_default' in st.session_state:
            if 'prev_max_views_default' not in st.session_state or st.session_state['max_views_default'] != st.session_state['prev_max_views_default']:
                st.session_state['prev_max_views_default'] = st.session_state['max_views_default']
                needs_rerun = True
        if needs_rerun:
            st.rerun()
        min_views_val = st.session_state.get('min_views', 0)
        max_views_val = st.session_state.get('max_views', st.session_state.get('max_views_default', 1000000))
        selected_categories_val = st.session_state.get('selected_categories', [])
        filter_info = []
        if min_views_val > 0:
            filter_info.append(f"Min views: {min_views_val:,}")
        if max_views_val < 1000000:
            filter_info.append(f"Max views: {max_views_val:,}")
        if selected_categories_val and selected_categories_val != ["Please wait for data loading to complete..."]:
            filter_info.append(f"Selected categories: {', '.join(selected_categories_val)}")
        if filter_info:
            st.info(f"Current filters: {', '.join(filter_info)}")
        original_df = df.copy()
        if 'videoViewCount' in df.columns:
            if min_views_val >= 0:
                original_count = len(df)
                df = df[df['videoViewCount'] >= min_views_val]
                if len(df) < original_count:
                    st.info(f"Filtered out {original_count - len(df):,} videos with views less than {min_views_val:,}")
            else:
                st.warning("Minimum views cannot be negative, ignoring this filter.")
        if 'videoViewCount' in df.columns:
            if max_views_val >= 0 and max_views_val >= min_views_val:
                original_count = len(df)
                df = df[df['videoViewCount'] <= max_views_val]
                if len(df) < original_count:
                    st.info(f"Filtered out {original_count - len(df):,} videos with views greater than {max_views_val:,}")
            else:
                st.warning("Maximum views setting is invalid, ignoring this filter.")
        categories_to_filter = st.session_state.get('selected_categories_cache', selected_categories_val)
        if categories_to_filter and categories_to_filter != ["Please wait for data loading to complete..."] and 'categoryName' in df.columns:
            original_count = len(df)
            df = df[df['categoryName'].isin(categories_to_filter)]
            if len(df) < original_count:
                st.info(f"Category filtering applied, showing {len(df):,} records (filtered out {original_count - len(df):,} records)")
        elif categories_to_filter and categories_to_filter != ["Please wait for data loading to complete..."]:
            st.warning("CategoryName column does not exist in the data, cannot apply category filtering.")
        filter_outliers_val = st.session_state.get('filter_outliers', True)
        if filter_outliers_val:
            original_count = len(df)
            cols_to_process = ['videoViewCount', 'videoLikeCount', 'VideoCommentCount', 'subscriberCount']
            cols_to_process = [col for col in cols_to_process if col in df.columns]
            if cols_to_process:
                valid_mask = pd.Series(True, index=df.index)
                for col in cols_to_process:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        Q1 = df[col].quantile(0.25)
                        Q3 = df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        valid_mask = valid_mask & (df[col] >= lower_bound) & (df[col] <= upper_bound)
                df = df[valid_mask]
                filtered_count = len(df)
                if filtered_count < original_count:
                    st.info(f"Filtered out {original_count - filtered_count:,} outlier records")
                else:
                    st.info("No outliers detected")
            else:
                st.info("No numeric columns found for outlier filtering, skipping")
        else:
            st.info("Outlier filtering not applied")
        df = engineer_features(df)
        if len(df) == 0:
            st.warning("⚠️ No data after filtering! Please adjust filter criteria.")
            st.warning("⚠️ No data after filtering! Please adjust filter criteria.")
            df = original_df
            st.info("Restored to original data state.")
        st.subheader("Data Quality Report")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Number of Columns", f"{len(df.columns):,}")
        with col3:
            if len(df) > 0 and len(df.columns) > 0:
                missing_data_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                st.metric("Missing Data %", f"{missing_data_pct:.2f}%")
            else:
                st.metric("Missing Data %", "N/A")
        tabs = st.tabs([
            "Introduction",
            "Data Overview",
            "Deep Dives",
            "Conclusions"
        ])
        with tabs[0]:
            intro.render(df)
        with tabs[1]:
            overview.render(df, show_data_info)
        with tabs[2]:
            deep_dives.render(df)
        with tabs[3]:
            conclusions.render(df)
if __name__ == "__main__":
    main()