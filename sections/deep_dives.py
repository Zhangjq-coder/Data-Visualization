import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.viz_enhanced import (
    create_enhanced_category_distribution_chart,
    create_enhanced_correlation_heatmap,
    create_enhanced_histogram_chart,
    create_enhanced_box_plot,
    create_enhanced_time_series_chart,
    create_enhanced_scatter_plot_matrix,
    create_channel_performance_comparison_chart,
    create_engagement_score_distribution_chart,
    create_enhanced_horizontal_bar_chart,
    create_enhanced_vertical_bar_chart
)
def render(df):
    st.header("Deep Dives")
    df_copy = df.copy()
    st.subheader("Data Visualization Analysis")
    layout_col = st.columns([1, 3], gap="medium")
    with layout_col[0]:
        chart_type = st.selectbox(
            "Chart Type Preference",
            ["Default Mix", "Prefer Pie Chart", "Prefer Bar Chart", "Prefer Line Chart"],
            index=0
        )
        show_annotations = st.checkbox("Show Data Labels", value=True)
        show_legend = st.checkbox("Show Legend", value=True)
    viz_tabs = st.tabs([
        "Category Distribution Analysis",
        "Correlation Analysis",
        "Engagement Metrics Analysis",
        "Time Trend Analysis",
        "Comprehensive Performance Analysis",
        "Seasonal Analysis"
    ])
    with viz_tabs[0]:
        st.header("Video Category Distribution")
        if 'categoryName' in df_copy.columns:
            fig_pie = create_enhanced_category_distribution_chart(df_copy)
            if fig_pie:
                st.plotly_chart(fig_pie, use_container_width=True)
            category_counts = df_copy['categoryName'].value_counts()
            category_df = pd.DataFrame({
                'Category': category_counts.index,
                'Count': category_counts.values
            })
            fig_bar = create_enhanced_horizontal_bar_chart(category_df, 'Count', 'Category', "Number of Videos by Category")
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Category data is not available")
    with viz_tabs[1]:
        st.header("Key Metrics Correlation Analysis")
        numeric_cols = ['videoViewCount', 'subscriberCount', 'videoLikeCount', 'videoDislikeCount', 'VideoCommentCount']
        available_cols = [col for col in numeric_cols if col in df_copy.columns]
        if len(available_cols) >= 2:
            fig_heatmap = create_enhanced_correlation_heatmap(df_copy, available_cols)
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
            st.subheader("Scatter Matrix Analysis")
            if len(available_cols) >= 3:
                fig_scatter_matrix = create_enhanced_scatter_plot_matrix(df_copy, available_cols, "Main Indicators Scatter Matrix")
                if fig_scatter_matrix:
                    st.plotly_chart(fig_scatter_matrix, use_container_width=True)
        else:
            st.warning("Insufficient numerical columns for correlation analysis")
    with viz_tabs[2]:
        st.header("User Engagement Metrics Analysis")
        engagement_cols = []
        if all(col in df_copy.columns for col in ['videoLikeCount', 'videoViewCount']):
            df_copy['like_rate'] = np.nan
            mask = df_copy['videoViewCount'] > 0
            df_copy.loc[mask, 'like_rate'] = df_copy.loc[mask, 'videoLikeCount'] / df_copy.loc[mask, 'videoViewCount']
            outlier_mask = df_copy['like_rate'] > 1
            if outlier_mask.any():
                st.info(f"Detected {outlier_mask.sum()} abnormal video data (likes > views), processed")
                df_copy.loc[outlier_mask, 'like_rate'] = 1.0
            engagement_cols.append('like_rate')
        if all(col in df_copy.columns for col in ['VideoCommentCount', 'videoViewCount']):
            df_copy['comment_rate'] = np.nan
            mask = df_copy['videoViewCount'] > 0
            df_copy.loc[mask, 'comment_rate'] = df_copy.loc[mask, 'VideoCommentCount'] / df_copy.loc[mask, 'videoViewCount']
            engagement_cols.append('comment_rate')
        if len(engagement_cols) > 0:
            for col in engagement_cols:
                fig_hist = create_enhanced_histogram_chart(df_copy[df_copy[col].notna()], col, f"{col.replace('_', ' ').title()} Distribution")
                if fig_hist:
                    st.plotly_chart(fig_hist, use_container_width=True)
            if 'categoryName' in df_copy.columns and len(engagement_cols) > 0:
                for col in engagement_cols:
                    valid_data = df_copy[df_copy[col].notna()]
                    if len(valid_data) > 0:
                        fig_box = create_enhanced_box_plot(valid_data, 'categoryName', col, f"{col.replace('_', ' ').title()} by Video Category")
                        if fig_box:
                            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("Insufficient engagement data for analysis")
    with viz_tabs[3]:
        st.header("Publishing Time Trend Analysis")
        if 'publishYear' in df_copy.columns:
            yearly_counts = df_copy.groupby('publishYear').size().reset_index()
            yearly_counts.columns = ['Year', 'Video Count']
            fig_yearly = create_enhanced_time_series_chart(yearly_counts, 'Year', 'Video Count', "Annual Video Publishing Trend")
            if fig_yearly:
                st.plotly_chart(fig_yearly, use_container_width=True)
            if 'publishMonth' in df_copy.columns:
                monthly_counts = df_copy.groupby('publishMonth').size().reset_index()
                monthly_counts.columns = ['Month', 'Video Count']
                fig_monthly = create_enhanced_vertical_bar_chart(monthly_counts, 'Month', 'Video Count', "Monthly Video Publishing Distribution")
                if fig_monthly:
                    st.plotly_chart(fig_monthly, use_container_width=True)
        elif 'publishDate' in df_copy.columns:
            try:
                if pd.api.types.is_datetime64_any_dtype(df_copy['publishDate']):
                    yearly_counts = df_copy.groupby(df_copy['publishDate'].dt.year).size().reset_index()
                else:
                    df_temp = df_copy.copy()
                    df_temp['year'] = pd.to_datetime(df_temp['publishDate'], errors='coerce').dt.year
                    yearly_counts = df_temp.groupby('year').size().reset_index()
                yearly_counts.columns = ['Year', 'Video Count']
                fig_yearly = create_enhanced_time_series_chart(yearly_counts, 'Year', 'Video Count', "Annual Video Publishing Trend")
                if fig_yearly:
                    st.plotly_chart(fig_yearly, use_container_width=True)
                if 'publishMonth' in df_copy.columns:
                    monthly_counts = df_copy.groupby('publishMonth').size().reset_index()
                    monthly_counts.columns = ['Month', 'Video Count']
                    fig_monthly = create_enhanced_vertical_bar_chart(monthly_counts, 'Month', 'Video Count', "Monthly Video Publishing Distribution")
                    if fig_monthly:
                        st.plotly_chart(fig_monthly, use_container_width=True)
            except Exception as e:
                st.warning(f"Error processing year data: {str(e)}")
        else:
            st.warning("Publishing time data not available")
    with viz_tabs[4]:
        st.header("Channel Comprehensive Performance Analysis")
        top_n = st.slider("Select Top N Channels to Display", 5, 20, 10)
        fig_channel_performance = create_channel_performance_comparison_chart(df_copy, top_n)
        if fig_channel_performance:
            st.plotly_chart(fig_channel_performance, use_container_width=True)
        st.subheader("Content Quality Comprehensive Score")
        fig_engagement_score = create_engagement_score_distribution_chart(df_copy)
        if fig_engagement_score:
            st.plotly_chart(fig_engagement_score, use_container_width=True)
        else:
            st.warning("Insufficient required data for comprehensive performance analysis")
    with viz_tabs[5]:
        st.header("Seasonal Analysis")
        if 'season' in df_copy.columns:
            season_counts = df_copy['season'].value_counts()
            season_df = pd.DataFrame({
                'Season': season_counts.index,
                'Count': season_counts.values
            })
            fig_season_bar = create_enhanced_horizontal_bar_chart(season_df, 'Count', 'Season', "Video Count Distribution by Season")
            if fig_season_bar:
                st.plotly_chart(fig_season_bar, use_container_width=True)
            if 'videoViewCount' in df_copy.columns:
                season_avg_views = df_copy.groupby('season')['videoViewCount'].mean().reset_index()
                season_avg_views.columns = ['Season', 'Average Views']
                fig_season_views = create_enhanced_horizontal_bar_chart(season_avg_views, 'Average Views', 'Season', "Average Views by Season")
                if fig_season_views:
                    st.plotly_chart(fig_season_views, use_container_width=True)
        else:
            st.warning("Seasonal data not available, please ensure the data contains publish month information")