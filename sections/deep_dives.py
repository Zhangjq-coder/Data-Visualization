import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# 导入增强版可视化函数
# 这些函数提供了更丰富的图表功能和错误处理
from utils.viz_enhanced import (
    create_enhanced_category_distribution_chart,     # 增强版类别分布图表
    create_enhanced_correlation_heatmap,             # 增强版相关性热力图
    create_enhanced_histogram_chart,                 # 增强版直方图
    create_enhanced_box_plot,                        # 增强版箱线图
    create_enhanced_time_series_chart,               # 增强版时间序列图表
    create_enhanced_scatter_plot_matrix,             # 增强版散点图矩阵
    create_channel_performance_comparison_chart,     # 频道表现对比图表
    create_engagement_score_distribution_chart,      # 互动评分分布图表
    create_enhanced_horizontal_bar_chart,            # 增强版横向条形图
    create_enhanced_vertical_bar_chart               # 增强版纵向条形图
)

def render(df):
    """
    渲染深入分析部分
    
    参数:
    df (pandas.DataFrame): 包含YouTube数据的DataFrame
    
    功能:
    1. 创建多个选项卡用于不同维度的深入分析
    2. 使用增强版可视化函数生成图表
    3. 提供交互式控件让用户自定义图表显示
    4. 处理各种数据异常情况
    
    分析维度包括:
    - 类别分布分析
    - 相关性分析
    - 互动指标分析
    - 时间趋势分析
    - 综合表现分析
    - 季节性分析
    """
    # 深入分析标题
    st.header("深入分析 | Deep Dives")
    
    # 创建数据副本以避免修改原始数据
    # copy(): 创建DataFrame的副本，避免在分析过程中修改原始数据
    df_copy = df.copy()
    
    # 数据可视化部分标题
    st.subheader("数据可视化分析 | Data Visualization Analysis")
    
    # 布局选择和控制选项 - 创建两列布局用于放置控件
    # 第一列宽度较小用于放置控件，第二列宽度较大用于显示内容
    layout_col = st.columns([1, 3], gap="medium")
    with layout_col[0]:
        # 图表类型偏好选择下拉框
        chart_type = st.selectbox(
            "图表类型偏好 | Chart Type Preference",
            ["默认混合 | Default Mix", "优先饼图 | Prefer Pie Chart", "优先柱状图 | Prefer Bar Chart", "优先折线图 | Prefer Line Chart"],
            index=0
        )
        
        # 添加显示控制选项
        # show_annotations: 控制是否显示数据标签的复选框
        show_annotations = st.checkbox("显示数据标签 | Show Data Labels", value=True)
        # show_legend: 控制是否显示图例的复选框
        show_legend = st.checkbox("显示图例 | Show Legend", value=True)
    
    # 创建可视化选项卡
    # tabs: 创建六个选项卡分别用于不同维度的分析
    viz_tabs = st.tabs([
        "类别分布分析 | Category Distribution Analysis",
        "相关性分析 | Correlation Analysis",
        "互动指标分析 | Engagement Metrics Analysis",
        "时间趋势分析 | Time Trend Analysis",
        "综合表现分析 | Comprehensive Performance Analysis",
        "季节性分析 | Seasonal Analysis"
    ])
    
    # 1. 类别分布分析选项卡
    with viz_tabs[0]:
        # 类别分布分析标题
        st.header("视频类别分布 | Video Category Distribution")
        
        # 检查数据中是否存在类别名称列
        if 'categoryName' in df_copy.columns:
            # 使用增强版类别分布图表
            # create_enhanced_category_distribution_chart: 从utils.viz_enhanced导入的函数
            fig_pie = create_enhanced_category_distribution_chart(df_copy)
            # 检查图表是否成功创建
            if fig_pie:
                # plotly_chart: 显示Plotly图表
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # 类别数量统计
            # value_counts(): 统计每个类别的视频数量
            category_counts = df_copy['categoryName'].value_counts()
            
            # 使用增强版横向条形图显示类别数量
            # 创建包含类别和数量的DataFrame
            category_df = pd.DataFrame({
                'Category': category_counts.index,
                'Count': category_counts.values
            })
            # create_enhanced_horizontal_bar_chart: 创建横向条形图
            fig_bar = create_enhanced_horizontal_bar_chart(category_df, 'Count', 'Category', "各类别视频数量 | Number of Videos by Category")
            # 检查图表是否成功创建
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            # 如果类别数据不可用，显示警告信息
            st.warning("类别数据不可用 | Category data is not available")
    
    # 2. 相关性分析选项卡
    with viz_tabs[1]:
        # 相关性分析标题
        st.header("关键指标相关性分析 | Key Metrics Correlation Analysis")
        
        # 选择要分析的数值列
        # 定义关键数值指标列
        numeric_cols = ['videoViewCount', 'subscriberCount', 'videoLikeCount', 'videoDislikeCount', 'VideoCommentCount']
        # 检查这些列是否存在于数据中
        available_cols = [col for col in numeric_cols if col in df_copy.columns]
        
        # 确保至少有两个可用列才能进行相关性分析
        if len(available_cols) >= 2:
            # 使用增强版相关性热力图
            # create_enhanced_correlation_heatmap: 创建相关性热力图
            fig_heatmap = create_enhanced_correlation_heatmap(df_copy, available_cols)
            # 检查图表是否成功创建
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # 散点图矩阵分析子标题
            st.subheader("散点图矩阵分析 | Scatter Matrix Analysis")
            # 确保至少有三个可用列才能创建散点图矩阵
            if len(available_cols) >= 3:
                # create_enhanced_scatter_plot_matrix: 创建散点图矩阵
                fig_scatter_matrix = create_enhanced_scatter_plot_matrix(df_copy, available_cols, "主要指标散点图矩阵 | Main Indicators Scatter Matrix")
                # 检查图表是否成功创建
                if fig_scatter_matrix:
                    st.plotly_chart(fig_scatter_matrix, use_container_width=True)
        else:
            # 如果可用数值列不足，显示警告信息
            st.warning("可用的数值列不足，无法进行相关性分析 | Insufficient numerical columns for correlation analysis")
    
    # 3. 互动指标分析选项卡
    with viz_tabs[2]:
        # 用户互动指标分析标题
        st.header("用户互动指标分析 | User Engagement Metrics Analysis")
        
        # 计算互动率
        # 初始化互动指标列列表
        engagement_cols = []
        
        # 安全地添加新列到副本DataFrame
        # 检查点赞数和观看数列是否存在
        if all(col in df_copy.columns for col in ['videoLikeCount', 'videoViewCount']):
            # 初始化点赞率列以避免SettingWithCopyWarning
            df_copy['like_rate'] = np.nan
            # 计算点赞率并添加数据清洗
            # mask: 创建布尔掩码用于筛选观看数大于0的记录
            mask = df_copy['videoViewCount'] > 0
            # loc: 使用位置索引安全地设置点赞率
            df_copy.loc[mask, 'like_rate'] = df_copy.loc[mask, 'videoLikeCount'] / df_copy.loc[mask, 'videoViewCount']
            
            # 数据清洗 - 处理异常值
            # 点赞率理论上不应超过1（每个观看者最多点赞一次）
            # 超过1的值可能是数据收集错误
            # outlier_mask: 创建异常值掩码
            outlier_mask = df_copy['like_rate'] > 1
            # any(): 检查是否存在异常值
            if outlier_mask.any():
                # 记录异常数据数量
                st.info(f"检测到 {outlier_mask.sum()} 个异常视频数据（点赞数大于观看数），已进行处理 | Detected {outlier_mask.sum()} abnormal video data (likes > views), processed")
                # 可以选择将异常值设置为1或过滤掉
                # 将异常值设置为1.0（表示每个观看者都点赞）
                df_copy.loc[outlier_mask, 'like_rate'] = 1.0  # 限制最大值为1.0
            
            # 将点赞率列添加到互动指标列列表
            engagement_cols.append('like_rate')
        
        # 检查评论数和观看数列是否存在
        if all(col in df_copy.columns for col in ['VideoCommentCount', 'videoViewCount']):
            # 初始化评论率列以避免SettingWithCopyWarning
            df_copy['comment_rate'] = np.nan
            # mask: 创建布尔掩码用于筛选观看数大于0的记录
            mask = df_copy['videoViewCount'] > 0
            # loc: 使用位置索引安全地设置评论率
            df_copy.loc[mask, 'comment_rate'] = df_copy.loc[mask, 'VideoCommentCount'] / df_copy.loc[mask, 'videoViewCount']
            # 将评论率列添加到互动指标列列表
            engagement_cols.append('comment_rate')
        
        # 检查是否存在互动指标列
        if len(engagement_cols) > 0:
            # 使用增强版直方图显示互动率分布
            # 遍历所有互动指标列
            for col in engagement_cols:
                # notna(): 筛选非空值
                fig_hist = create_enhanced_histogram_chart(df_copy[df_copy[col].notna()], col, f"{col.replace('_', ' ').title()} 分布 | {col.replace('_', ' ').title()} Distribution")
                # 检查图表是否成功创建
                if fig_hist:
                    st.plotly_chart(fig_hist, use_container_width=True)
            
            # 使用增强版箱线图显示不同类别的互动率
            # 检查类别名称列是否存在且存在互动指标列
            if 'categoryName' in df_copy.columns and len(engagement_cols) > 0:
                # 遍历所有互动指标列
                for col in engagement_cols:
                    # 筛选非空值数据
                    valid_data = df_copy[df_copy[col].notna()]
                    # 检查是否存在有效数据
                    if len(valid_data) > 0:
                        # create_enhanced_box_plot: 创建箱线图
                        fig_box = create_enhanced_box_plot(valid_data, 'categoryName', col, f"不同类别视频的{col.replace('_', ' ').title()} | {col.replace('_', ' ').title()} by Video Category")
                        # 检查图表是否成功创建
                        if fig_box:
                            st.plotly_chart(fig_box, use_container_width=True)
        else:
            # 如果互动数据不足，显示警告信息
            st.warning("互动数据不足，无法进行互动指标分析 | Insufficient engagement data for analysis")
    
    # 4. 时间趋势分析选项卡
    with viz_tabs[3]:
        # 发布时间趋势分析标题
        st.header("发布时间趋势分析 | Publishing Time Trend Analysis")
        
        # 检查是否存在发布年份列
        if 'publishYear' in df_copy.columns:
            # 使用预处理好的publishYear列进行按年统计
            # groupby: 按年份分组统计视频数量
            yearly_counts = df_copy.groupby('publishYear').size().reset_index()
            # 重命名列名
            yearly_counts.columns = ['Year', 'Video Count']
            
            # 使用增强版时间序列图表
            # create_enhanced_time_series_chart: 创建时间序列图表
            fig_yearly = create_enhanced_time_series_chart(yearly_counts, 'Year', 'Video Count', "视频发布数量年度趋势 | Annual Video Publishing Trend")
            # 检查图表是否成功创建
            if fig_yearly:
                st.plotly_chart(fig_yearly, use_container_width=True)
            
            # 按月统计
            # 检查是否存在发布月份列
            if 'publishMonth' in df_copy.columns:
                # groupby: 按月份分组统计视频数量
                monthly_counts = df_copy.groupby('publishMonth').size().reset_index()
                # 重命名列名
                monthly_counts.columns = ['Month', 'Video Count']
                
                # 使用增强版纵向条形图显示月度分布
                # create_enhanced_vertical_bar_chart: 创建纵向条形图
                fig_monthly = create_enhanced_vertical_bar_chart(monthly_counts, 'Month', 'Video Count', "视频发布月度分布 | Monthly Video Publishing Distribution")
                # 检查图表是否成功创建
                if fig_monthly:
                    st.plotly_chart(fig_monthly, use_container_width=True)
        # 如果没有publishYear列但有publishDate，尝试安全地提取年份
        elif 'publishDate' in df_copy.columns:
            # try-except: 处理可能的异常
            try:
                # 检查publishDate的类型
                # is_datetime64_any_dtype: 检查是否为日期时间类型
                if pd.api.types.is_datetime64_any_dtype(df_copy['publishDate']):
                    # 按年份分组统计
                    yearly_counts = df_copy.groupby(df_copy['publishDate'].dt.year).size().reset_index()
                else:
                    # 处理date类型或其他可转换为年份的类型
                    # copy(): 创建临时副本
                    df_temp = df_copy.copy()
                    # to_datetime: 转换为日期时间类型，errors='coerce'处理无法转换的值
                    df_temp['year'] = pd.to_datetime(df_temp['publishDate'], errors='coerce').dt.year
                    # 按年份分组统计
                    yearly_counts = df_temp.groupby('year').size().reset_index()
                    
                # 重命名列名
                yearly_counts.columns = ['Year', 'Video Count']
                
                # 使用增强版时间序列图表
                fig_yearly = create_enhanced_time_series_chart(yearly_counts, 'Year', 'Video Count', "视频发布数量年度趋势 | Annual Video Publishing Trend")
                # 检查图表是否成功创建
                if fig_yearly:
                    st.plotly_chart(fig_yearly, use_container_width=True)
                
                # 按月统计
                if 'publishMonth' in df_copy.columns:
                    # groupby: 按月份分组统计
                    monthly_counts = df_copy.groupby('publishMonth').size().reset_index()
                    # 重命名列名
                    monthly_counts.columns = ['Month', 'Video Count']
                    
                    # 使用增强版纵向条形图显示月度分布
                    fig_monthly = create_enhanced_vertical_bar_chart(monthly_counts, 'Month', 'Video Count', "视频发布月度分布 | Monthly Video Publishing Distribution")
                    # 检查图表是否成功创建
                    if fig_monthly:
                        st.plotly_chart(fig_monthly, use_container_width=True)
            # 捕获处理年份数据时的异常
            except Exception as e:
                # 显示错误信息
                st.warning(f"处理年份数据时出错: {str(e)} | Error processing year data: {str(e)}")
        else:
            # 如果发布时间数据不可用，显示警告信息
            st.warning("发布时间数据不可用 | Publishing time data not available")
    
    # 5. 综合表现分析选项卡
    with viz_tabs[4]:
        # 频道综合表现分析标题
        st.header("频道综合表现分析 | Channel Comprehensive Performance Analysis")
        
        # 选择前N个表现最好的频道
        # slider: 创建滑块用于选择显示的频道数量
        top_n = st.slider("选择显示的Top N频道 | Select Top N Channels to Display", 5, 20, 10)
        
        # 使用增强版频道表现对比图表
        # create_channel_performance_comparison_chart: 创建频道表现对比图表
        fig_channel_performance = create_channel_performance_comparison_chart(df_copy, top_n)
        # 检查图表是否成功创建
        if fig_channel_performance:
            st.plotly_chart(fig_channel_performance, use_container_width=True)
        
        # 综合评分计算（简单示例）
        # 内容质量综合评分子标题
        st.subheader("内容质量综合评分 | Content Quality Comprehensive Score")
        # create_engagement_score_distribution_chart: 创建互动评分分布图表
        fig_engagement_score = create_engagement_score_distribution_chart(df_copy)
        # 检查图表是否成功创建
        if fig_engagement_score:
            st.plotly_chart(fig_engagement_score, use_container_width=True)
        else:
            # 如果所需数据不足，显示警告信息
            st.warning("所需数据不足，无法进行综合表现分析 | Insufficient required data for comprehensive performance analysis")
    
    # 6. 季节性分析选项卡
    with viz_tabs[5]:
        # 季节性分析标题
        st.header("季节性分析 | Seasonal Analysis")
        
        # 检查是否存在季节列
        if 'season' in df_copy.columns:
            # 季节性视频数量分布
            # value_counts(): 统计每个季节的视频数量
            season_counts = df_copy['season'].value_counts()
            # 创建包含季节和数量的DataFrame
            season_df = pd.DataFrame({
                'Season': season_counts.index,
                'Count': season_counts.values
            })
            
            # create_enhanced_horizontal_bar_chart: 创建横向条形图显示季节分布
            fig_season_bar = create_enhanced_horizontal_bar_chart(season_df, 'Count', 'Season', "各季节视频数量分布 | Video Count Distribution by Season")
            # 检查图表是否成功创建
            if fig_season_bar:
                st.plotly_chart(fig_season_bar, use_container_width=True)
            
            # 季节性平均观看量分析
            # 检查是否存在观看数列
            if 'videoViewCount' in df_copy.columns:
                # groupby: 按季节分组计算平均观看量
                season_avg_views = df_copy.groupby('season')['videoViewCount'].mean().reset_index()
                # 重命名列名
                season_avg_views.columns = ['Season', 'Average Views']
                
                # create_enhanced_horizontal_bar_chart: 创建横向条形图显示季节平均观看量
                fig_season_views = create_enhanced_horizontal_bar_chart(season_avg_views, 'Average Views', 'Season', "各季节平均观看量 | Average Views by Season")
                # 检查图表是否成功创建
                if fig_season_views:
                    st.plotly_chart(fig_season_views, use_container_width=True)
        else:
            # 如果季节性数据不可用，显示警告信息
            st.warning("季节性数据不可用，请确保数据包含发布月份信息 | Seasonal data not available, please ensure the data contains publish month information")