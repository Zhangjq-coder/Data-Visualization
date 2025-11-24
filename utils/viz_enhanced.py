import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_enhanced_category_distribution_chart(df):
    """
    创建增强版类别分布图表
    
    参数:
    df: 包含categoryName列的DataFrame
    
    返回:
    Plotly图表对象
    """
    if 'categoryName' not in df.columns:
        return None
    
    # 类别数量统计
    category_counts = df['categoryName'].value_counts()
    
    # 创建饼图
    category_df = pd.DataFrame({
        'Category': category_counts.index,
        'Count': category_counts.values
    })
    
    fig_pie = px.pie(
        category_df,
        values='Count',
        names='Category',
        title="视频类别分布",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # 优化布局
    fig_pie.update_layout(
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        margin=dict(l=20, r=20, t=50, b=150)
    )
    
    # 优化标签
    fig_pie.update_traces(
        textposition='outside',
        textinfo='label+percent',
        texttemplate='%{label}<br>%{percent:.1%}',
        textfont=dict(size=10)
    )
    
    return fig_pie

def create_enhanced_horizontal_bar_chart(df, x_col, y_col, title):
    """
    创建增强版横向条形图
    
    参数:
    df: DataFrame
    x_col: x轴列名
    y_col: y轴列名
    title: 图表标题
    
    返回:
    Plotly图表对象
    """
    fig_bar = px.bar(
        x=df[x_col],
        y=df[y_col],
        orientation="h",
        title=title,
        color=df[x_col],
        color_continuous_scale="Viridis"
    )
    fig_bar.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        font=dict(size=12)
    )
    
    return fig_bar

def create_enhanced_correlation_heatmap(df, columns):
    """
    创建增强版相关性热力图
    
    参数:
    df: DataFrame
    columns: 要分析的列名列表
    
    返回:
    Plotly图表对象
    """
    # 创建相关性矩阵
    corr_df = df[columns].corr()
    
    # 热力图
    fig_heatmap = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="关键指标相关性矩阵"
    )
    fig_heatmap.update_layout(font=dict(size=12))
    
    return fig_heatmap

def create_enhanced_time_series_chart(df, x_col, y_col, title):
    """
    创建增强版时间序列图表
    
    参数:
    df: DataFrame
    x_col: x轴列名（时间）
    y_col: y轴列名
    title: 图表标题
    
    返回:
    Plotly图表对象
    """
    fig_line = px.line(
        df,
        x=x_col,
        y=y_col,
        markers=True,
        title=title,
        color_discrete_sequence=['#3274A1']
    )
    fig_line.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )
    
    return fig_line

def create_enhanced_histogram_chart(df, column, title, bins=50):
    """
    创建增强版直方图
    
    参数:
    df: DataFrame
    column: 要绘制的列名
    title: 图表标题
    bins: 箱数
    
    返回:
    Plotly图表对象
    """
    fig_hist = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title,
        color_discrete_sequence=['skyblue']
    )
    
    # 根据不同指标设置合适的x轴范围
    if column in ['like_rate', 'comment_rate']:
        fig_hist.update_layout(
            xaxis_title=f"{column.replace('_', ' ').title()} (%)",
            yaxis_title="频率",
            xaxis=dict(range=[0, 1])
        )
        # 添加百分比转换的提示
        st.markdown("<small>注：图表显示的是原始比率值，乘以100可转换为百分比</small>", unsafe_allow_html=True)
    else:
        fig_hist.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title="频率"
        )
    
    return fig_hist

def create_enhanced_box_plot(df, x_col, y_col, title):
    """
    创建增强版箱线图
    
    参数:
    df: DataFrame
    x_col: x轴列名
    y_col: y轴列名
    title: 图表标题
    
    返回:
    Plotly图表对象
    """
    fig_box = px.box(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color=x_col
    )
    fig_box.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        xaxis_tickangle=45,
        legend_title=x_col
    )
    
    return fig_box

def create_enhanced_scatter_plot_matrix(df, columns, title):
    """
    创建增强版散点图矩阵
    
    参数:
    df: DataFrame
    columns: 要分析的列名列表
    title: 图表标题
    
    返回:
    Plotly图表对象
    """
    sample_size = min(1000, len(df))
    sample_df = df[columns].dropna().sample(sample_size, random_state=42)
    fig_scatter_matrix = px.scatter_matrix(
        sample_df,
        dimensions=columns[:4],  # 最多显示4个维度
        title=title,
        color=sample_df[columns[0]] if len(columns) > 0 else None,
        opacity=0.5
    )
    fig_scatter_matrix.update_layout(height=800)
    
    return fig_scatter_matrix

def create_channel_performance_comparison_chart(df, top_n=10):
    """
    创建频道表现对比图表
    
    参数:
    df: DataFrame
    top_n: 显示前N个频道
    
    返回:
    Plotly图表对象
    """
    # 检查可用的频道标识字段
    available_channel_cols = []
    for col in ['channelName', 'channelId']:
        if col in df.columns:
            available_channel_cols.append(col)
            
    if not available_channel_cols:
        return None
        
    # 选择最合适的频道字段
    if 'channelName' in available_channel_cols:
        # 使用频道名称，但先检查是否有有效数据
        df_temp = df.copy()
        # 确保channelName是字符串类型
        df_temp['channelName'] = df_temp['channelName'].astype(str).fillna('')
        # 检查是否有非空的频道名称
        if df_temp['channelName'].str.strip().ne('').any():
            group_by_col = 'channelName'
            display_col = 'channelName'
            xaxis_title = "频道名称"
        else:
            # 如果channelName全为空，则使用channelId
            group_by_col = 'channelId'
            display_col = 'channelId'
            xaxis_title = "频道ID"
    else:
        # 只有channelId可用
        group_by_col = 'channelId'
        display_col = 'channelId'
        xaxis_title = "频道ID"
        
    # 计算每个频道的总观看量
    channel_performance = df.groupby(group_by_col)['videoViewCount'].sum().reset_index()
    channel_performance = channel_performance.sort_values('videoViewCount', ascending=False).head(top_n)
    
    # 针对频道ID的显示优化
    if group_by_col == 'channelId':
        # 创建更友好的显示ID，同时在悬停时显示完整ID
        channel_performance['displayId'] = channel_performance['channelId'].apply(
            lambda x: f"频道{hash(x) % 10000:04d}"  # 使用哈希生成简短频道编号
        )
        display_col = 'displayId'
    
    # 频道排名图
    fig_top_channels = px.bar(
        channel_performance,
        x=display_col,
        y='videoViewCount',
        title=f"Top {top_n} 频道观看量",
        color='videoViewCount',
        color_continuous_scale="YlOrRd",
        # 添加悬停信息，显示完整的频道标识
        hover_data={display_col: True, group_by_col: True, 'videoViewCount': True}
    )
    fig_top_channels.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title="总观看量",
        xaxis_tickangle=45,
        # 优化x轴标签显示
        xaxis=dict(
            tickfont=dict(size=10),
            automargin=True
        )
    )
    
    return fig_top_channels

def create_engagement_score_distribution_chart(df):
    """
    创建互动评分分布图表
    
    参数:
    df: DataFrame
    
    返回:
    Plotly图表对象
    """
    # 过滤有效数据
    valid_df = df[(df['videoViewCount'] > 0) & (df['videoLikeCount'].notna()) & (df['VideoCommentCount'].notna())].copy()
    
    if len(valid_df) > 0:
        # 计算综合评分（简化版）
        valid_df['engagement_score'] = (
            np.log1p(valid_df['videoViewCount']) * 0.4 +
            np.log1p(valid_df['videoLikeCount']) * 0.4 +
            np.log1p(valid_df['VideoCommentCount']) * 0.2
        )
        
        # 显示评分分布
        fig_score_dist = px.histogram(
            valid_df,
            x='engagement_score',
            nbins=30,
            title="内容质量综合评分分布",
            color_discrete_sequence=['#8884d8']
        )
        fig_score_dist.update_layout(
            xaxis_title="综合评分",
            yaxis_title="视频数量"
        )
        
        return fig_score_dist
    
    return None