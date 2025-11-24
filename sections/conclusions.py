import streamlit as st
import pandas as pd
import numpy as np

def render(df):
    """
    渲染结论部分
    
    参数:
    df (pandas.DataFrame): 包含YouTube数据的DataFrame
    
    功能:
    1. 生成基于数据的自动洞察
    2. 提供内容创作者、数据分析和技术改进建议
    3. 展示综合评分和相关性分析结果
    
    生成的洞察包括:
    - 最受欢迎的视频类别
    - 平均观看量
    - 平均点赞率
    - 最新视频发布年份
    - 表现最好的视频特征
    - 点赞率和评论率的相关性
    """
    # 结论与洞察标题
    st.header("结论与洞察 | Conclusions & Insights")
    
    # 添加数据洞察总结标题
    st.subheader("数据洞察总结 | Data Insights Summary")
    # 说明文本
    st.write("基于可视化分析，我们可以得出以下洞察： | Based on visualization analysis, we can draw the following insights:")
    
    # 初始化洞察列表
    insights = []
    
    # 生成一些自动洞察
    # 检查类别名称列是否存在
    if 'categoryName' in df.columns:
        # idxmax(): 获取数量最多的类别
        top_category = df['categoryName'].value_counts().idxmax()
        # 添加最受欢迎类别洞察
        insights.append(f"1. 最受欢迎的视频类别是 **{top_category}**，拥有最多的视频数量。 | The most popular video category is **{top_category}** with the highest number of videos.")
    
    # 检查观看数列是否存在
    if 'videoViewCount' in df.columns:
        # mean(): 计算平均观看量
        avg_views = df['videoViewCount'].mean()
        # 添加平均观看量洞察
        insights.append(f"2. 数据集视频的平均观看量约为 **{avg_views:,.0f}** 次。 | The average views per video in the dataset is approximately **{avg_views:,.0f}**.")
    
    # 检查点赞数和观看数列是否存在
    if all(col in df.columns for col in ['videoLikeCount', 'videoViewCount']):
        # 筛选有效数据（观看数大于0且点赞数非空）
        valid_likes = df[(df['videoViewCount'] > 0) & (df['videoLikeCount'].notna())]
        # 检查是否存在有效数据
        if len(valid_likes) > 0:
            # 计算平均点赞率
            avg_like_rate = (valid_likes['videoLikeCount'] / valid_likes['videoViewCount']).mean() * 100
            # 添加平均点赞率洞察
            insights.append(f"3. 平均点赞率约为 **{avg_like_rate:.2f}%**。 | The average like rate is approximately **{avg_like_rate:.2f}%**.")
    
    # 检查发布年份列是否存在
    if 'publishYear' in df.columns:
        # max(): 获取最新年份
        recent_year = df['publishYear'].max()
        # 添加最新视频发布年份洞察
        insights.append(f"4. 最新的视频发布于 **{recent_year}** 年。 | The most recent videos were published in **{recent_year}**.")
    
    # 添加更多深入洞察
    # 检查综合评分列是否存在
    if 'engagement_score' in df.columns:
        # nlargest(): 获取综合评分最高的5个视频
        top_videos = df.nlargest(5, 'engagement_score')
        # 检查是否存在评分最高的视频
        if not top_videos.empty:
            # 添加表现最好视频洞察
            insights.append(f"5. 根据综合评分，表现最好的视频具有较高的互动性。 | Based on comprehensive scoring, the best performing videos have high engagement.")
    
    # 检查点赞率和评论率列是否存在
    if 'like_rate' in df.columns and 'comment_rate' in df.columns:
        # corr(): 计算相关性
        correlation = df['like_rate'].corr(df['comment_rate'])
        # 检查相关性是否为有效数值
        if not np.isnan(correlation):
            # 添加相关性洞察
            insights.append(f"6. 点赞率和评论率之间的相关性为 **{correlation:.2f}**，表明用户互动行为之间存在{'强' if abs(correlation) > 0.5 else '弱'}相关性。 | The correlation between like rate and comment rate is **{correlation:.2f}**, indicating a {'strong' if abs(correlation) > 0.5 else 'weak'} correlation between user engagement behaviors.")
    
    # 显示所有洞察
    for insight in insights:
        st.write(insight)
    
    # 总结说明文本
    st.write("\n通过这些可视化分析，我们可以更好地了解YouTube平台上的内容表现和用户行为模式。 | Through these visualization analyses, we can better understand content performance and user behavior patterns on the YouTube platform.")
    
    # 建议标题
    st.subheader("建议 | Recommendations")
    # 建议内容 - 使用HTML格式和insight-box样式
    st.write("""
    <div class="insight-box">
    <h4>内容创作者建议 | Content Creator Recommendations:</h4>
    <ul>
    <li>关注热门类别：根据分析结果，了解哪些类别更受欢迎 | Pay attention to popular categories: Understand which categories are more popular based on analysis results</li>
    <li>优化发布时间：分析最佳发布时间以获得更高的观看量 | Optimize publishing time: Analyze the best publishing time to achieve higher views</li>
    <li>提高互动率：通过内容优化提高点赞和评论率 | Improve engagement rate: Enhance likes and comments through content optimization</li>
    </ul>
    
    <h4>数据分析建议 | Data Analysis Recommendations:</h4>
    <ul>
    <li>深入分析特定类别的成功因素 | In-depth analysis of success factors for specific categories</li>
    <li>研究频道增长模式和策略 | Study channel growth patterns and strategies</li>
    <li>探索更多维度的数据关联性 | Explore data correlations across more dimensions</li>
    <li>进行时间序列分析以识别趋势 | Conduct time series analysis to identify trends</li>
    </ul>
    
    <h4>技术改进建议 | Technical Improvement Recommendations:</h4>
    <ul>
    <li>增加更多高级可视化图表 | Add more advanced visualization charts</li>
    <li>实现更复杂的数据过滤和查询功能 | Implement more complex data filtering and query functions</li>
    <li>添加预测分析功能 | Add predictive analysis capabilities</li>
    <li>优化性能以处理更大的数据集 | Optimize performance to handle larger datasets</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)