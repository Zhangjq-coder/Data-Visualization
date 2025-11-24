import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def create_category_distribution_chart(df):
    """
    创建类别分布图表
    
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

def create_horizontal_bar_chart(df, x_col, y_col, title):
    """
    创建横向条形图
    
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

def create_correlation_heatmap(df, columns):
    """
    创建相关性热力图
    
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

def create_time_series_chart(df, x_col, y_col, title):
    """
    创建时间序列图表
    
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

def create_histogram_chart(df, column, title, bins=50):
    """
    创建直方图
    
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

def create_box_plot(df, x_col, y_col, title):
    """
    创建箱线图
    
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

def create_scatter_plot_matrix(df, columns, title):
    """
    创建散点图矩阵
    
    参数:
    df: DataFrame
    columns: 要分析的列名列表
    title: 图表标题
    
    返回:
    Plotly图表对象
    """
    sample_df = df[columns].dropna().sample(min(1000, len(df)), random_state=42)
    fig_scatter_matrix = px.scatter_matrix(
        sample_df,
        dimensions=columns[:4],  # 最多显示4个维度
        title=title,
        color=sample_df[columns[0]] if len(columns) > 0 else None,
        opacity=0.5
    )
    fig_scatter_matrix.update_layout(height=800)
    
    return fig_scatter_matrix