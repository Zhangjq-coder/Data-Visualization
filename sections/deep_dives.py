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
    create_engagement_score_distribution_chart
)

def render(df):
    """渲染深入分析部分"""
    st.header("深入分析 | Deep Dives")
    
    # 创建数据副本以避免修改原始数据
    df_copy = df.copy()
    
    # 数据可视化部分
    st.subheader("数据可视化分析 | Data Visualization Analysis")
    
    # 布局选择和控制选项
    layout_col = st.columns([1, 3], gap="medium")
    with layout_col[0]:
        chart_type = st.selectbox(
            "图表类型偏好 | Chart Type Preference",
            ["默认混合 | Default Mix", "优先饼图 | Prefer Pie Chart", "优先柱状图 | Prefer Bar Chart", "优先折线图 | Prefer Line Chart"],
            index=0
        )
        
        # 添加显示控制
        show_annotations = st.checkbox("显示数据标签 | Show Data Labels", value=True)
        show_legend = st.checkbox("显示图例 | Show Legend", value=True)
    
    # 创建可视化选项卡
    viz_tabs = st.tabs([
        "类别分布分析 | Category Distribution Analysis",
        "相关性分析 | Correlation Analysis",
        "互动指标分析 | Engagement Metrics Analysis",
        "时间趋势分析 | Time Trend Analysis",
        "综合表现分析 | Comprehensive Performance Analysis"
    ])
    
    # 1. 类别分布分析
    with viz_tabs[0]:
        st.header("视频类别分布 | Video Category Distribution")
        
        if 'categoryName' in df_copy.columns:
            # 使用增强版类别分布图表
            fig_pie = create_enhanced_category_distribution_chart(df_copy)
            if fig_pie:
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # 类别数量统计
            category_counts = df_copy['categoryName'].value_counts()
            
            # 创建条形图（横向）
            fig_bar = px.bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation="h",
                title="各类别视频数量 | Number of Videos by Category",
                color=category_counts.values,
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(
                xaxis_title="视频数量 | Number of Videos",
                yaxis_title="类别 | Category",
                font=dict(size=12)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("类别数据不可用 | Category data is not available")
    
    # 2. 相关性分析
    with viz_tabs[1]:
        st.header("关键指标相关性分析 | Key Metrics Correlation Analysis")
        
        # 选择要分析的数值列
        numeric_cols = ['videoViewCount', 'subscriberCount', 'videoLikeCount', 'videoDislikeCount', 'VideoCommentCount']
        available_cols = [col for col in numeric_cols if col in df_copy.columns]
        
        if len(available_cols) >= 2:
            # 使用增强版相关性热力图
            fig_heatmap = create_enhanced_correlation_heatmap(df_copy, available_cols)
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # 散点图矩阵
            st.subheader("散点图矩阵分析 | Scatter Matrix Analysis")
            if len(available_cols) >= 3:
                fig_scatter_matrix = create_enhanced_scatter_plot_matrix(df_copy, available_cols, "主要指标散点图矩阵 | Main Indicators Scatter Matrix")
                if fig_scatter_matrix:
                    st.plotly_chart(fig_scatter_matrix, use_container_width=True)
        else:
            st.warning("可用的数值列不足，无法进行相关性分析 | Insufficient numerical columns for correlation analysis")
    
    # 3. 互动指标分析
    with viz_tabs[2]:
        st.header("用户互动指标分析 | User Engagement Metrics Analysis")
        
        # 计算互动率
        engagement_cols = []
        
        # 安全地添加新列到副本DataFrame
        if all(col in df_copy.columns for col in ['videoLikeCount', 'videoViewCount']):
            # 初始化列以避免SettingWithCopyWarning
            df_copy['like_rate'] = np.nan
            # 计算点赞率并添加数据清洗
            mask = df_copy['videoViewCount'] > 0
            df_copy.loc[mask, 'like_rate'] = df_copy.loc[mask, 'videoLikeCount'] / df_copy.loc[mask, 'videoViewCount']
            
            # 数据清洗 - 处理异常值
            # 点赞率理论上不应超过1（每个观看者最多点赞一次）
            # 超过1的值可能是数据收集错误
            outlier_mask = df_copy['like_rate'] > 1
            if outlier_mask.any():
                # 记录异常数据数量
                st.info(f"检测到 {outlier_mask.sum()} 个异常视频数据（点赞数大于观看数），已进行处理 | Detected {outlier_mask.sum()} abnormal video data (likes > views), processed")
                # 可以选择将异常值设置为1或过滤掉
                df_copy.loc[outlier_mask, 'like_rate'] = 1.0  # 限制最大值为1.0
            
            engagement_cols.append('like_rate')
        
        if all(col in df_copy.columns for col in ['VideoCommentCount', 'videoViewCount']):
            # 初始化列以避免SettingWithCopyWarning
            df_copy['comment_rate'] = np.nan
            mask = df_copy['videoViewCount'] > 0
            df_copy.loc[mask, 'comment_rate'] = df_copy.loc[mask, 'VideoCommentCount'] / df_copy.loc[mask, 'videoViewCount']
            engagement_cols.append('comment_rate')
        
        if len(engagement_cols) > 0:
            # 使用增强版直方图显示互动率分布
            for col in engagement_cols:
                fig_hist = create_enhanced_histogram_chart(df_copy[df_copy[col].notna()], col, f"{col.replace('_', ' ').title()} 分布 | {col.replace('_', ' ').title()} Distribution")
                if fig_hist:
                    st.plotly_chart(fig_hist, use_container_width=True)
            
            # 使用增强版箱线图显示不同类别的互动率
            if 'categoryName' in df_copy.columns and len(engagement_cols) > 0:
                for col in engagement_cols:
                    valid_data = df_copy[df_copy[col].notna()]
                    if len(valid_data) > 0:
                        fig_box = create_enhanced_box_plot(valid_data, 'categoryName', col, f"不同类别视频的{col.replace('_', ' ').title()} | {col.replace('_', ' ').title()} by Video Category")
                        if fig_box:
                            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("互动数据不足，无法进行互动指标分析 | Insufficient engagement data for analysis")
    
    # 4. 时间趋势分析
    with viz_tabs[3]:
        st.header("发布时间趋势分析 | Publishing Time Trend Analysis")
        
        if 'publishYear' in df_copy.columns:
            # 使用预处理好的publishYear列进行按年统计
            yearly_counts = df_copy.groupby('publishYear').size().reset_index()
            yearly_counts.columns = ['Year', 'Video Count']
            
            # 使用增强版时间序列图表
            fig_yearly = create_enhanced_time_series_chart(yearly_counts, 'Year', 'Video Count', "视频发布数量年度趋势 | Annual Video Publishing Trend")
            if fig_yearly:
                st.plotly_chart(fig_yearly, use_container_width=True)
            
            # 按月统计
            if 'publishMonth' in df_copy.columns:
                monthly_counts = df_copy.groupby('publishMonth').size().reset_index()
                monthly_counts.columns = ['Month', 'Video Count']
                
                # 月度分布图
                fig_monthly = px.bar(
                    monthly_counts,
                    x='Month',
                    y='Video Count',
                    title="视频发布月度分布 | Monthly Video Publishing Distribution",
                    color='Video Count',
                    color_continuous_scale="Blues"
                )
                fig_monthly.update_layout(
                    xaxis_title="月份 | Month",
                    yaxis_title="视频数量 | Number of Videos"
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
        elif 'publishDate' in df_copy.columns:
            # 如果没有publishYear列但有publishDate，尝试安全地提取年份
            try:
                # 检查publishDate的类型
                if pd.api.types.is_datetime64_any_dtype(df_copy['publishDate']):
                    yearly_counts = df_copy.groupby(df_copy['publishDate'].dt.year).size().reset_index()
                else:
                    # 处理date类型或其他可转换为年份的类型
                    df_temp = df_copy.copy()
                    df_temp['year'] = pd.to_datetime(df_temp['publishDate'], errors='coerce').dt.year
                    yearly_counts = df_temp.groupby('year').size().reset_index()
                    
                yearly_counts.columns = ['Year', 'Video Count']
                
                # 使用增强版时间序列图表
                fig_yearly = create_enhanced_time_series_chart(yearly_counts, 'Year', 'Video Count', "视频发布数量年度趋势 | Annual Video Publishing Trend")
                if fig_yearly:
                    st.plotly_chart(fig_yearly, use_container_width=True)
                
                # 按月统计
                if 'publishMonth' in df_copy.columns:
                    monthly_counts = df_copy.groupby('publishMonth').size().reset_index()
                    monthly_counts.columns = ['Month', 'Video Count']
                    
                    # 月度分布图
                    fig_monthly = px.bar(
                        monthly_counts,
                        x='Month',
                        y='Video Count',
                        title="视频发布月度分布 | Monthly Video Publishing Distribution",
                        color='Video Count',
                        color_continuous_scale="Blues"
                    )
                    fig_monthly.update_layout(
                        xaxis_title="月份 | Month",
                        yaxis_title="视频数量 | Number of Videos"
                    )
                    st.plotly_chart(fig_monthly, use_container_width=True)
            except Exception as e:
                st.warning(f"处理年份数据时出错: {str(e)} | Error processing year data: {str(e)}")
        else:
            st.warning("发布时间数据不可用 | Publishing time data not available")
    
    # 5. 综合表现分析
    with viz_tabs[4]:
        st.header("频道综合表现分析 | Channel Comprehensive Performance Analysis")
        
        # 选择前N个表现最好的频道
        top_n = st.slider("选择显示的Top N频道 | Select Top N Channels to Display", 5, 20, 10)
        
        # 使用增强版频道表现对比图表
        fig_channel_performance = create_channel_performance_comparison_chart(df_copy, top_n)
        if fig_channel_performance:
            st.plotly_chart(fig_channel_performance, use_container_width=True)
        
        # 综合评分计算（简单示例）
        st.subheader("内容质量综合评分 | Content Quality Comprehensive Score")
        fig_engagement_score = create_engagement_score_distribution_chart(df_copy)
        if fig_engagement_score:
            st.plotly_chart(fig_engagement_score, use_container_width=True)
        else:
            st.warning("所需数据不足，无法进行综合表现分析 | Insufficient required data for comprehensive performance analysis")
