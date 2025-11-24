import streamlit as st
import pandas as pd
import numpy as np

def render(df):
    """渲染结论部分"""
    st.header("结论与洞察 | Conclusions & Insights")
    
    # 添加数据洞察总结
    st.subheader("数据洞察总结 | Data Insights Summary")
    st.write("基于可视化分析，我们可以得出以下洞察： | Based on visualization analysis, we can draw the following insights:")
    
    insights = []
    
    # 生成一些自动洞察
    if 'categoryName' in df.columns:
        top_category = df['categoryName'].value_counts().idxmax()
        insights.append(f"1. 最受欢迎的视频类别是 **{top_category}**，拥有最多的视频数量。 | The most popular video category is **{top_category}** with the highest number of videos.")
    
    if 'videoViewCount' in df.columns:
        avg_views = df['videoViewCount'].mean()
        insights.append(f"2. 数据集视频的平均观看量约为 **{avg_views:,.0f}** 次。 | The average views per video in the dataset is approximately **{avg_views:,.0f}**.")
    
    if all(col in df.columns for col in ['videoLikeCount', 'videoViewCount']):
        valid_likes = df[(df['videoViewCount'] > 0) & (df['videoLikeCount'].notna())]
        if len(valid_likes) > 0:
            avg_like_rate = (valid_likes['videoLikeCount'] / valid_likes['videoViewCount']).mean() * 100
            insights.append(f"3. 平均点赞率约为 **{avg_like_rate:.2f}%**。 | The average like rate is approximately **{avg_like_rate:.2f}%**.")
    
    if 'publishYear' in df.columns:
        recent_year = df['publishYear'].max()
        insights.append(f"4. 最新的视频发布于 **{recent_year}** 年。 | The most recent videos were published in **{recent_year}**.")
    
    # 添加更多深入洞察
    if 'engagement_score' in df.columns:
        top_videos = df.nlargest(5, 'engagement_score')
        if not top_videos.empty:
            insights.append(f"5. 根据综合评分，表现最好的视频具有较高的互动性。 | Based on comprehensive scoring, the best performing videos have high engagement.")
    
    if 'like_rate' in df.columns and 'comment_rate' in df.columns:
        # 计算相关性
        correlation = df['like_rate'].corr(df['comment_rate'])
        if not np.isnan(correlation):
            insights.append(f"6. 点赞率和评论率之间的相关性为 **{correlation:.2f}**，表明用户互动行为之间存在{'强' if abs(correlation) > 0.5 else '弱'}相关性。 | The correlation between like rate and comment rate is **{correlation:.2f}**, indicating a {'strong' if abs(correlation) > 0.5 else 'weak'} correlation between user engagement behaviors.")
    
    for insight in insights:
        st.write(insight)
    
    st.write("\n通过这些可视化分析，我们可以更好地了解YouTube平台上的内容表现和用户行为模式。 | Through these visualization analyses, we can better understand content performance and user behavior patterns on the YouTube platform.")
    
    st.subheader("建议与后续步骤 | Recommendations & Next Steps")
    st.write("""
    <div class="insight-box">
    <h4>内容创作者建议 | Content Creator Recommendations:</h4>
    <ul>
    <li>关注热门类别：根据分析结果，了解哪些类别更受欢迎</li>
    <li>优化发布时间：分析最佳发布时间以获得更高的观看量</li>
    <li>提高互动率：通过内容优化提高点赞和评论率</li>
    </ul>
    
    <h4>数据分析建议 | Data Analysis Recommendations:</h4>
    <ul>
    <li>深入分析特定类别的成功因素</li>
    <li>研究频道增长模式和策略</li>
    <li>探索更多维度的数据关联性</li>
    <li>进行时间序列分析以识别趋势</li>
    </ul>
    
    <h4>技术改进建议 | Technical Improvement Recommendations:</h4>
    <ul>
    <li>增加更多高级可视化图表</li>
    <li>实现更复杂的数据过滤和查询功能</li>
    <li>添加预测分析功能</li>
    <li>优化性能以处理更大的数据集</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)