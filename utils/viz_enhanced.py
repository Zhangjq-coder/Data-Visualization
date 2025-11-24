import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import logging

# 设置日志记录
# basicConfig: 配置基础日志记录
logging.basicConfig(level=logging.INFO)
# getLogger: 获取日志记录器实例
logger = logging.getLogger(__name__)

def create_enhanced_category_distribution_chart(df):
    """
    创建增强版类别分布图表
    
    参数:
    df (pandas.DataFrame): 包含categoryName列的DataFrame
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式饼图显示类别分布
    2. 优化图表布局和标签显示
    3. 提供详细的数据标签和百分比信息
    4. 包含错误处理和日志记录
    
    图表特点:
    - 使用环形饼图（hole=0.3）提供更好的视觉效果
    - 自定义颜色方案（Pastel调色板）
    - 优化的标签位置和格式
    - 响应式布局适配不同屏幕尺寸
    """
    try:
        # 检查categoryName列是否存在于数据中
        if 'categoryName' not in df.columns:
            # 记录警告日志
            logger.warning("categoryName列不存在于数据中 | categoryName column does not exist in the data")
            # 返回None表示创建失败
            return None
        
        # 类别数量统计
        # value_counts(): 统计每个类别的视频数量
        category_counts = df['categoryName'].value_counts()
        
        # 创建饼图数据DataFrame
        category_df = pd.DataFrame({
            'Category': category_counts.index,  # 类别名称
            'Count': category_counts.values     # 视频数量
        })
        
        # 创建饼图
        # px.pie: 使用Plotly Express创建饼图
        fig_pie = px.pie(
            category_df,           # 数据源
            values='Count',        # 值列
            names='Category',      # 标签列
            title="视频类别分布",    # 图表标题
            hole=0.3,              # 环形饼图，0.3表示中心孔径比例
            color_discrete_sequence=px.colors.qualitative.Pastel  # 配色方案
        )
        
        # 优化布局
        # update_layout: 更新图表布局设置
        fig_pie.update_layout(
            font=dict(size=12),    # 字体大小
            legend=dict(
                orientation="h",   # 水平排列图例
                yanchor="bottom",  # 图例y轴锚点在底部
                y=-0.3,            # 图例y轴位置
                xanchor="center",  # 图例x轴锚点在中心
                x=0.5,             # 图例x轴位置
                font=dict(size=10) # 图例字体大小
            ),
            margin=dict(l=20, r=20, t=50, b=150)  # 图表边距
        )
        
        # 优化标签
        # update_traces: 更新图表轨迹设置
        fig_pie.update_traces(
            textposition='outside',           # 标签位置在饼图外部
            textinfo='label+percent',         # 显示标签和百分比
            texttemplate='%{label}<br>%{percent:.1%}',  # 标签模板格式
            textfont=dict(size=10)            # 标签字体大小
        )
        
        # 返回创建的饼图
        return fig_pie
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建类别分布图表时出错: {str(e)} | Error creating category distribution chart: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建类别分布图表时出错，请查看日志了解详细信息 | Error creating category distribution chart, please check logs for details")
        # 返回None表示创建失败
        return None

def create_enhanced_horizontal_bar_chart(df, x_col, y_col, title):
    """
    创建增强版横向条形图
    
    参数:
    df (pandas.DataFrame): DataFrame
    x_col (str): x轴列名
    y_col (str): y轴列名
    title (str): 图表标题
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式横向条形图
    2. 使用颜色渐变增强视觉效果
    3. 优化轴标签和图表标题
    4. 包含错误处理和日志记录
    
    图表特点:
    - 横向布局适合显示长标签
    - 颜色渐变反映数值大小
    - 响应式设计适配不同屏幕
    """
    try:
        # 检查指定的列是否存在于数据中
        if x_col not in df.columns or y_col not in df.columns:
            # 记录警告日志
            logger.warning(f"列 {x_col} 或 {y_col} 不存在于数据中 | Column {x_col} or {y_col} does not exist in the data")
            # 返回None表示创建失败
            return None
            
        # 创建横向条形图
        # px.bar: 使用Plotly Express创建条形图
        fig_bar = px.bar(
            df,                    # 数据源
            x=x_col,               # x轴列
            y=y_col,               # y轴列
            orientation="h",       # 横向条形图
            title=title,           # 图表标题
            color=x_col,           # 颜色映射列
            color_continuous_scale="Viridis"  # 颜色渐变方案
        )
        # 更新布局设置
        fig_bar.update_layout(
            xaxis_title=x_col,     # x轴标题
            yaxis_title=y_col,     # y轴标题
            font=dict(size=12)     # 字体大小
        )
        
        # 返回创建的横向条形图
        return fig_bar
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建横向条形图时出错: {str(e)} | Error creating horizontal bar chart: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建横向条形图时出错，请查看日志了解详细信息 | Error creating horizontal bar chart, please check logs for details")
        # 返回None表示创建失败
        return None

def create_enhanced_vertical_bar_chart(df, x_col, y_col, title):
    """
    创建增强版纵向条形图
    
    参数:
    df (pandas.DataFrame): DataFrame
    x_col (str): x轴列名
    y_col (str): y轴列名
    title (str): 图表标题
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式纵向条形图
    2. 使用蓝色渐变增强视觉效果
    3. 优化轴标签和图表标题
    4. 包含错误处理和日志记录
    
    图表特点:
    - 纵向布局适合显示分类数据
    - 蓝色渐变方案提供专业外观
    - 响应式设计适配不同屏幕
    """
    try:
        # 检查指定的列是否存在于数据中
        if x_col not in df.columns or y_col not in df.columns:
            # 记录警告日志
            logger.warning(f"列 {x_col} 或 {y_col} 不存在于数据中 | Column {x_col} or {y_col} does not exist in the data")
            # 返回None表示创建失败
            return None
            
        # 创建纵向条形图
        # px.bar: 使用Plotly Express创建条形图
        fig_bar = px.bar(
            df,                    # 数据源
            x=x_col,               # x轴列
            y=y_col,               # y轴列
            orientation="v",       # 纵向条形图
            title=title,           # 图表标题
            color=y_col,           # 颜色映射列
            color_continuous_scale="Blues"  # 蓝色渐变方案
        )
        # 更新布局设置
        fig_bar.update_layout(
            xaxis_title=x_col,     # x轴标题
            yaxis_title=y_col,     # y轴标题
            font=dict(size=12)     # 字体大小
        )
        
        # 返回创建的纵向条形图
        return fig_bar
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建纵向条形图时出错: {str(e)} | Error creating vertical bar chart: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建纵向条形图时出错，请查看日志了解详细信息 | Error creating vertical bar chart, please check logs for details")
        # 返回None表示创建失败
        return None

def create_enhanced_correlation_heatmap(df, columns):
    """
    创建增强版相关性热力图
    
    参数:
    df (pandas.DataFrame): DataFrame
    columns (list): 要分析的列名列表
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式相关性热力图
    2. 使用红蓝渐变色方案
    3. 自动显示相关系数值
    4. 包含错误处理和日志记录
    
    图表特点:
    - 红蓝渐变色方案（RdBu_r）突出正负相关
    - 自动显示相关系数值（text_auto=True）
    - 响应式设计适配不同屏幕
    """
    try:
        # 检查列是否存在
        # 列表推导式筛选出不存在的列
        missing_cols = [col for col in columns if col not in df.columns]
        # 如果存在缺失列，显示警告
        if missing_cols:
            # 显示警告信息给用户
            st.warning(f"以下列不存在于数据中: {missing_cols} | The following columns do not exist in the data: {missing_cols}")
            # 返回None表示创建失败
            return None
            
        # 创建相关性矩阵
        # corr(): 计算指定列之间的相关性矩阵
        corr_df = df[columns].corr()
        
        # 热力图
        # px.imshow: 使用Plotly Express创建热力图
        fig_heatmap = px.imshow(
            corr_df,                           # 相关性矩阵数据
            text_auto=True,                    # 自动显示相关系数值
            aspect="auto",                     # 自动调整纵横比
            color_continuous_scale="RdBu_r",   # 红蓝渐变色方案
            title="关键指标相关性矩阵"            # 图表标题
        )
        # 更新布局设置
        fig_heatmap.update_layout(font=dict(size=12))
        
        # 返回创建的相关性热力图
        return fig_heatmap
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建相关性热力图时出错: {str(e)} | Error creating correlation heatmap: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建相关性热力图时出错，请查看日志了解详细信息 | Error creating correlation heatmap, please check logs for details")
        # 返回None表示创建失败
        return None

def create_enhanced_time_series_chart(df, x_col, y_col, title):
    """
    创建增强版时间序列图表
    
    参数:
    df (pandas.DataFrame): DataFrame
    x_col (str): x轴列名（时间）
    y_col (str): y轴列名
    title (str): 图表标题
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式时间序列折线图
    2. 显示数据点标记
    3. 使用专业蓝色调色板
    4. 包含错误处理和日志记录
    
    图表特点:
    - 显示数据点标记增强可读性
    - 专业蓝色调色板提供清晰视觉
    - 响应式设计适配不同屏幕
    """
    try:
        # 检查指定的列是否存在于数据中
        if x_col not in df.columns or y_col not in df.columns:
            # 记录警告日志
            logger.warning(f"列 {x_col} 或 {y_col} 不存在于数据中 | Column {x_col} or {y_col} does not exist in the data")
            # 返回None表示创建失败
            return None
            
        # 创建时间序列折线图
        # px.line: 使用Plotly Express创建折线图
        fig_line = px.line(
            df,                              # 数据源
            x=x_col,                         # x轴列（时间）
            y=y_col,                         # y轴列
            markers=True,                    # 显示数据点标记
            title=title,                     # 图表标题
            color_discrete_sequence=['#3274A1']  # 自定义蓝色调色板
        )
        # 更新布局设置
        fig_line.update_layout(
            xaxis_title=x_col,               # x轴标题
            yaxis_title=y_col                # y轴标题
        )
        
        # 返回创建的时间序列图表
        return fig_line
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建时间序列图表时出错: {str(e)} | Error creating time series chart: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建时间序列图表时出错，请查看日志了解详细信息 | Error creating time series chart, please check logs for details")
        # 返回None表示创建失败
        return None

def create_enhanced_histogram_chart(df, column, title, bins=50):
    """
    创建增强版直方图
    
    参数:
    df (pandas.DataFrame): DataFrame
    column (str): 要绘制的列名
    title (str): 图表标题
    bins (int): 箱数，默认为50
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式直方图
    2. 支持自定义箱数
    3. 根据数据类型优化显示
    4. 包含错误处理和日志记录
    
    图表特点:
    - 支持自定义箱数以优化显示效果
    - 根据互动率数据特殊处理显示范围
    - 天空蓝配色方案提供清新视觉
    - 响应式设计适配不同屏幕
    """
    try:
        # 检查指定的列是否存在于数据中
        if column not in df.columns:
            # 记录警告日志
            logger.warning(f"列 {column} 不存在于数据中 | Column {column} does not exist in the data")
            # 返回None表示创建失败
            return None
            
        # 创建直方图
        # px.histogram: 使用Plotly Express创建直方图
        fig_hist = px.histogram(
            df,                              # 数据源
            x=column,                        # x轴列
            nbins=bins,                      # 箱数
            title=title,                     # 图表标题
            color_discrete_sequence=['skyblue']  # 天空蓝配色方案
        )
        
        # 根据不同指标设置合适的x轴范围
        # 特殊处理互动率数据
        if column in ['like_rate', 'comment_rate']:
            # 更新布局设置
            fig_hist.update_layout(
                xaxis_title=f"{column.replace('_', ' ').title()} (%)",  # x轴标题
                yaxis_title="频率",                                       # y轴标题
                xaxis=dict(range=[0, 1])                                 # x轴范围0-1
            )
            # 添加百分比转换的提示
            st.markdown("<small>注：图表显示的是原始比率值，乘以100可转换为百分比</small>", unsafe_allow_html=True)
        else:
            # 一般情况下的布局设置
            fig_hist.update_layout(
                xaxis_title=column.replace('_', ' ').title(),  # x轴标题
                yaxis_title="频率"                                # y轴标题
            )
        
        # 返回创建的直方图
        return fig_hist
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建直方图时出错: {str(e)} | Error creating histogram: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建直方图时出错，请查看日志了解详细信息 | Error creating histogram, please check logs for details")
        # 返回None表示创建失败
        return None

def create_enhanced_box_plot(df, x_col, y_col, title):
    """
    创建增强版箱线图
    
    参数:
    df (pandas.DataFrame): DataFrame
    x_col (str): x轴列名
    y_col (str): y轴列名
    title (str): 图表标题
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式箱线图
    2. 支持按类别分组显示
    3. 使用颜色区分不同组别
    4. 包含错误处理和日志记录
    
    图表特点:
    - 支持按类别分组显示数据分布
    - 使用颜色区分不同组别
    - 优化的标签角度提高可读性
    - 响应式设计适配不同屏幕
    """
    try:
        # 检查指定的列是否存在于数据中
        if x_col not in df.columns or y_col not in df.columns:
            # 记录警告日志
            logger.warning(f"列 {x_col} 或 {y_col} 不存在于数据中 | Column {x_col} or {y_col} does not exist in the data")
            # 返回None表示创建失败
            return None
            
        # 创建箱线图
        # px.box: 使用Plotly Express创建箱线图
        fig_box = px.box(
            df,                    # 数据源
            x=x_col,               # x轴列（分组列）
            y=y_col,               # y轴列（数值列）
            title=title,           # 图表标题
            color=x_col            # 颜色映射列
        )
        # 更新布局设置
        fig_box.update_layout(
            xaxis_title=x_col,     # x轴标题
            yaxis_title=y_col,     # y轴标题
            xaxis_tickangle=45,    # x轴标签角度
            legend_title=x_col     # 图例标题
        )
        
        # 返回创建的箱线图
        return fig_box
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建箱线图时出错: {str(e)} | Error creating box plot: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建箱线图时出错，请查看日志了解详细信息 | Error creating box plot, please check logs for details")
        # 返回None表示创建失败
        return None

def create_enhanced_scatter_plot_matrix(df, columns, title):
    """
    创建增强版散点图矩阵
    
    参数:
    df (pandas.DataFrame): DataFrame
    columns (list): 要分析的列名列表
    title (str): 图表标题
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建交互式散点图矩阵
    2. 支持多维度数据可视化
    3. 使用颜色映射第一个维度
    4. 包含错误处理和日志记录
    
    图表特点:
    - 支持多维度数据关系可视化
    - 使用颜色映射增强数据表达
    - 透明度设置提高重叠点可见性
    - 固定高度确保良好显示效果
    """
    try:
        # 检查列是否存在
        # 列表推导式筛选出不存在的列
        missing_cols = [col for col in columns if col not in df.columns]
        # 如果存在缺失列，记录警告日志
        if missing_cols:
            # 记录警告日志
            logger.warning(f"以下列不存在于数据中: {missing_cols} | The following columns do not exist in the data: {missing_cols}")
            # 返回None表示创建失败
            return None
            
        # 采样数据以提高性能
        # 确定采样大小（最多1000个点或数据总长度）
        sample_size = min(1000, len(df))
        # 删除缺失值并随机采样
        sample_df = df[columns].dropna().sample(sample_size, random_state=42)
        # 创建散点图矩阵
        # px.scatter_matrix: 使用Plotly Express创建散点图矩阵
        fig_scatter_matrix = px.scatter_matrix(
            sample_df,             # 采样数据
            dimensions=columns[:4],  # 最多显示4个维度
            title=title,           # 图表标题
            color=sample_df[columns[0]] if len(columns) > 0 else None,  # 颜色映射第一个维度
            opacity=0.5            # 透明度设置
        )
        # 更新布局设置
        fig_scatter_matrix.update_layout(height=800)
        
        # 返回创建的散点图矩阵
        return fig_scatter_matrix
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建散点图矩阵时出错: {str(e)} | Error creating scatter plot matrix: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建散点图矩阵时出错，请查看日志了解详细信息 | Error creating scatter plot matrix, please check logs for details")
        # 返回None表示创建失败
        return None

def create_channel_performance_comparison_chart(df, top_n=10):
    """
    创建频道表现对比图表
    
    参数:
    df (pandas.DataFrame): DataFrame
    top_n (int): 显示前N个频道，默认为10
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建频道表现对比条形图
    2. 支持频道名称和ID两种标识
    3. 使用热力颜色方案突出表现差异
    4. 包含错误处理和日志记录
    
    图表特点:
    - 支持频道名称和ID两种标识方式
    - 热力颜色方案（YlOrRd）突出表现差异
    - 优化的标签显示和悬停信息
    - 响应式设计适配不同屏幕
    """
    try:
        # 检查可用的频道标识字段
        # 初始化可用频道列列表
        available_channel_cols = []
        # 检查频道名称和ID列是否存在
        for col in ['channelName', 'channelId']:
            if col in df.columns:
                available_channel_cols.append(col)
                
        # 如果没有可用的频道标识字段，返回None
        if not available_channel_cols:
            return None
            
        # 选择最合适的频道字段
        # 优先使用频道名称
        if 'channelName' in available_channel_cols:
            # 使用频道名称，但先检查是否有有效数据
            df_temp = df.copy()
            # 确保channelName是字符串类型
            df_temp['channelName'] = df_temp['channelName'].astype(str).fillna('')
            # 检查是否有非空的频道名称
            if df_temp['channelName'].str.strip().ne('').any():
                group_by_col = 'channelName'   # 分组列
                display_col = 'channelName'    # 显示列
                xaxis_title = "频道名称"         # x轴标题
            else:
                # 如果channelName全为空，则使用channelId
                group_by_col = 'channelId'     # 分组列
                display_col = 'channelId'      # 显示列
                xaxis_title = "频道ID"          # x轴标题
        else:
            # 只有channelId可用
            group_by_col = 'channelId'         # 分组列
            display_col = 'channelId'          # 显示列
            xaxis_title = "频道ID"              # x轴标题
            
        # 计算每个频道的总观看量
        # groupby: 按频道分组
        # sum(): 计算总观看量
        # reset_index(): 重置索引
        channel_performance = df.groupby(group_by_col)['videoViewCount'].sum().reset_index()
        # sort_values: 按观看量降序排序
        # head: 取前N个频道
        channel_performance = channel_performance.sort_values('videoViewCount', ascending=False).head(top_n)
        
        # 针对频道ID的显示优化
        # 如果使用频道ID作为分组列
        if group_by_col == 'channelId':
            # 创建更友好的显示ID，同时在悬停时显示完整ID
            # apply: 对每个频道ID应用哈希函数生成简短频道编号
            channel_performance['displayId'] = channel_performance['channelId'].apply(
                lambda x: f"频道{hash(x) % 10000:04d}"  # 使用哈希生成简短频道编号
            )
            display_col = 'displayId'  # 更新显示列
        
        # 频道排名图
        # px.bar: 使用Plotly Express创建条形图
        fig_top_channels = px.bar(
            channel_performance,                             # 数据源
            x=display_col,                                   # x轴列
            y='videoViewCount',                              # y轴列
            title=f"Top {top_n} 频道观看量",                  # 图表标题
            color='videoViewCount',                          # 颜色映射列
            color_continuous_scale="YlOrRd",                 # 黄橙红渐变色方案
            # 添加悬停信息，显示完整的频道标识
            hover_data={display_col: True, group_by_col: True, 'videoViewCount': True}
        )
        # 更新布局设置
        fig_top_channels.update_layout(
            xaxis_title=xaxis_title,                         # x轴标题
            yaxis_title="总观看量",                            # y轴标题
            xaxis_tickangle=45,                              # x轴标签角度
            # 优化x轴标签显示
            xaxis=dict(
                tickfont=dict(size=10),                      # 标签字体大小
                automargin=True                              # 自动边距
            )
        )
        
        # 返回创建的频道表现对比图表
        return fig_top_channels
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建频道表现对比图表时出错: {str(e)} | Error creating channel performance comparison chart: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建频道表现对比图表时出错，请查看日志了解详细信息 | Error creating channel performance comparison chart, please check logs for details")
        # 返回None表示创建失败
        return None

def create_engagement_score_distribution_chart(df):
    """
    创建互动评分分布图表
    
    参数:
    df (pandas.DataFrame): DataFrame
    
    返回:
    plotly.graph_objects.Figure: Plotly图表对象
    
    功能:
    1. 创建互动评分分布直方图
    2. 使用对数变换处理极值
    3. 加权计算综合评分
    4. 包含错误处理和日志记录
    
    图表特点:
    - 使用紫色调色方案（#8884d8）提供专业外观
    30个箱数平衡细节和清晰度
    - 对数变换减少极值影响
    - 响应式设计适配不同屏幕
    """
    try:
        # 过滤有效数据
        # 筛选观看数大于0，点赞数和评论数非空的记录
        valid_df = df[(df['videoViewCount'] > 0) & (df['videoLikeCount'].notna()) & (df['VideoCommentCount'].notna())].copy()
        
        # 检查是否存在有效数据
        if len(valid_df) > 0:
            # 计算综合评分（简化版）
            # 使用对数变换以减少极值的影响
            # np.log1p: 计算log(1+x)以处理零值
            valid_df['engagement_score'] = (
                np.log1p(valid_df['videoViewCount']) * 0.4 +      # 观看量权重40%
                np.log1p(valid_df['videoLikeCount']) * 0.4 +      # 点赞数权重40%
                np.log1p(valid_df['VideoCommentCount']) * 0.2     # 评论数权重20%
            )
            
            # 显示评分分布
            # px.histogram: 使用Plotly Express创建直方图
            fig_score_dist = px.histogram(
                valid_df,                                        # 数据源
                x='engagement_score',                            # x轴列
                nbins=30,                                        # 箱数
                title="内容质量综合评分分布",                       # 图表标题
                color_discrete_sequence=['#8884d8']              # 紫色调色方案
            )
            # 更新布局设置
            fig_score_dist.update_layout(
                xaxis_title="综合评分",                           # x轴标题
                yaxis_title="视频数量"                            # y轴标题
            )
            
            # 返回创建的互动评分分布图表
            return fig_score_dist
        
        # 如果没有有效数据，返回None
        return None
    # 捕获所有异常
    except Exception as e:
        # 记录错误日志
        logger.error(f"创建互动评分分布图表时出错: {str(e)} | Error creating engagement score distribution chart: {str(e)}")
        # 显示错误信息给用户
        st.error(f"创建互动评分分布图表时出错，请查看日志了解详细信息 | Error creating engagement score distribution chart, please check logs for details")
        # 返回None表示创建失败
        return None