import streamlit as st
import pandas as pd
import numpy as np
def render(df):
    st.header("Conclusions & Insights")
    st.subheader("Data Insights Summary")
    st.write("Based on visualization analysis, we can draw the following insights:")
    insights = []
    if 'categoryName' in df.columns:
        top_category = df['categoryName'].value_counts().idxmax()
        insights.append(f"1. The most popular video category is **{top_category}** with the highest number of videos.")
    if 'videoViewCount' in df.columns:
        avg_views = df['videoViewCount'].mean()
        insights.append(f"2. The average views per video in the dataset is approximately **{avg_views:,.0f}**.")
    if all(col in df.columns for col in ['videoLikeCount', 'videoViewCount']):
        valid_likes = df[(df['videoViewCount'] > 0) & (df['videoLikeCount'].notna())]
        if len(valid_likes) > 0:
            avg_like_rate = (valid_likes['videoLikeCount'] / valid_likes['videoViewCount']).mean() * 100
            insights.append(f"3. The average like rate is approximately **{avg_like_rate:.2f}%**.")
    if 'publishYear' in df.columns:
        recent_year = df['publishYear'].max()
        insights.append(f"4. The most recent videos were published in **{recent_year}**.")
    if 'engagement_score' in df.columns:
        top_videos = df.nlargest(5, 'engagement_score')
        if not top_videos.empty:
            insights.append(f"5. Based on comprehensive scoring, the best performing videos have high engagement.")
    if 'like_rate' in df.columns and 'comment_rate' in df.columns:
        correlation = df['like_rate'].corr(df['comment_rate'])
        if not np.isnan(correlation):
            insights.append(f"6. The correlation between like rate and comment rate is **{correlation:.2f}**, indicating a {'strong' if abs(correlation) > 0.5 else 'weak'} correlation between user engagement behaviors.")
    for insight in insights:
        st.write(insight)
    st.write("\nThrough these visualization analyses, we can better understand content performance and user behavior patterns on the YouTube platform.")
    st.subheader("In-depth Chart Analysis & Reasoning")
    st.write("Based on the charts in the deep dive section, we can further interpret the reasons behind these phenomena:")
    chart_analysis_tabs = st.tabs([
        "Category Distribution Analysis",
        "Correlation Analysis",
        "Engagement Metrics Analysis",
        "Time Trend Analysis",
        "Seasonal Analysis"
    ])
    with chart_analysis_tabs[0]:
        st.markdown("""
        <div style='margin-bottom: 20px;'>
        <p>The category distribution charts reveal important patterns about content preferences on YouTube:</p>
        <ul>
            <li><strong>Dominance of Specific Categories</strong>: The prevalence of certain categories (such as Entertainment or Music) suggests these genres have broader appeal and potentially lower barriers to content creation.</li>
            <li><strong>Market Saturation</strong>: Highly populated categories may indicate market saturation, making it more difficult for new creators to gain visibility.</li>
            <li><strong>Content Gap Opportunities</strong>: Less represented categories might offer untapped opportunities for niche content creators.</li>
            <li><strong>Audience Diversification</strong>: The diversity of categories shows YouTube's ability to cater to varied audience interests.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with chart_analysis_tabs[1]:
        st.markdown("""
        <div style='margin-bottom: 20px;'>
        <p>The correlation analysis provides insights into relationships between different engagement metrics:</p>
        <ul>
            <li><strong>Views-Likes Relationship</strong>: The positive correlation between views and likes indicates content that attracts more viewers tends to also receive more positive feedback.</li>
            <li><strong>Comment Engagement Drivers</strong>: The strength of correlation between comments and other metrics reveals which factors most strongly drive discussion.</li>
            <li><strong>Subscriber Impact</strong>: The relationship between subscriber count and engagement metrics helps understand the value of a loyal audience.</li>
            <li><strong>Independent Metrics</strong>: Metrics with weak correlations suggest they measure different aspects of content performance and audience behavior.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with chart_analysis_tabs[2]:
        st.markdown("""
        <div style='margin-bottom: 20px;'>
        <p>The engagement metrics analysis reveals patterns in how users interact with content:</p>
        <ul>
            <li><strong>Like Rate Distribution</strong>: The spread of like rates across videos indicates varying content quality and audience satisfaction levels.</li>
            <li><strong>Comment Rate Insights</strong>: Variations in comment rates highlight differences in content's ability to spark conversation.</li>
            <li><strong>Category-Specific Engagement</strong>: Different categories show distinct engagement patterns, suggesting tailored content strategies may be more effective.</li>
            <li><strong>Outlier Analysis</strong>: Videos with exceptionally high or low engagement rates provide case studies for what works or doesn't work.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with chart_analysis_tabs[3]:
        st.markdown("""
        <div style='margin-bottom: 20px;'>
        <p>The time trend analysis illustrates how YouTube content has evolved over time:</p>
        <ul>
            <li><strong>Publishing Volume Trends</strong>: Changes in annual publishing volume reflect platform growth and content creation democratization.</li>
            <li><strong>Content Evolution</strong>: Shifts in category popularity over time show changing audience interests and platform dynamics.</li>
            <li><strong>Growth Patterns</strong>: Acceleration in video creation suggests increasing competition and opportunities.</li>
            <li><strong>Consistency in Publishing</strong>: Monthly distribution patterns reveal whether content creation follows seasonal trends.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with chart_analysis_tabs[4]:
        st.markdown("""
        <div style='margin-bottom: 20px;'>
        <p>The seasonal analysis provides insights into how timing affects content performance:</p>
        <ul>
            <li><strong>Seasonal Publishing Patterns</strong>: Variations in video counts by season may reflect content creator behavior and audience availability.</li>
            <li><strong>Viewership Seasonality</strong>: Changes in average views across seasons suggest optimal timing for content release.</li>
            <li><strong>Holiday Effects</strong>: Specific seasons may show increased engagement due to holidays or changes in viewer routines.</li>
            <li><strong>Strategic Timing Opportunities</strong>: Identifying peak seasons can inform content planning and release strategies.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Recommendations")
    st.markdown("""
    <div style='margin-bottom: 30px;'>
    <h4 style='color: #2c3e50; margin-bottom: 15px;'>Content Strategy Recommendations</h4>
    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <ul>
            <li><strong>Focus on High-Engagement Categories</strong>: Prioritize content in categories that show strong engagement metrics, but be mindful of competition levels.</li>
            <li><strong>Optimize for Key Metrics</strong>: Based on correlation analysis, focus on improving metrics that have the strongest relationship with overall performance.</li>
            <li><strong>Consider Seasonal Timing</strong>: Align content release schedules with identified seasonal trends to maximize visibility.</li>
            <li><strong>Encourage Comment Interaction</strong>: Implement strategies to increase comment rates, as engagement appears to be a key differentiator.</li>
        </ul>
    </div>
    
    <h4 style='color: #2c3e50; margin-bottom: 15px;'>Data Collection and Analysis Improvements</h4>
    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <ul>
            <li><strong>Enhanced Data Tracking</strong>: Collect additional metadata such as video tags, description length, and thumbnail characteristics.</li>
            <li><strong>Temporal Analysis Refinement</strong>: Implement more granular time-based analysis, including day-of-week and time-of-day patterns.</li>
            <li><strong>Geographic Analysis</strong>: Incorporate regional data to understand geographic variations in content preferences.</li>
            <li><strong>Longitudinal Studies</strong>: Implement tracking of individual videos over time to understand performance trajectories.</li>
        </ul>
    </div>
    
    <h4 style='color: #2c3e50; margin-bottom: 15px;'>Platform and Business Implications</h4>
    <div style='background-color: #fff3e0; padding: 15px; border-radius: 8px;'>
        <ul>
            <li><strong>Creator Opportunities</strong>: Identify underserved niches with growing demand but limited supply.</li>
            <li><strong>Monetization Strategy</strong>: Focus on content types with both high viewership and strong engagement metrics.</li>
            <li><strong>Audience Development</strong>: Develop strategies to convert viewers into subscribers based on identified engagement patterns.</li>
            <li><strong>Content Differentiation</strong>: In saturated categories, emphasize unique angles or formats to stand out.</li>
        </ul>
    </div>
    </div>
    """, unsafe_allow_html=True)