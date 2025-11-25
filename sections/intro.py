import streamlit as st
def render(df):
    st.header("Project Introduction")
    st.markdown("""<div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <p style='font-size: 16px;'>This project aims to analyze YouTube dataset using advanced visualization techniques to uncover insights about content performance, user engagement patterns, and channel characteristics. Through interactive visualizations, we seek to provide a comprehensive understanding of the YouTube ecosystem.</p>
</div>""", unsafe_allow_html=True)
    
    st.subheader("Dataset Description")
    st.markdown("""
    <div style='margin-bottom: 20px;'>
    <ul>
        <li>The dataset contains detailed information about YouTube videos and channels, including metrics such as views, likes, comments, and subscriber counts.</li>
        <li>Key fields include: videoViewCount, videoLikeCount, videoDislikeCount, VideoCommentCount, subscriberCount, and categoryName.</li>
        <li>The data provides a snapshot of YouTube content across various categories and publishing periods.</li>
        <li>After filtering and processing, we are analyzing a subset of the original data to focus on meaningful patterns.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Analysis Objectives")
    st.markdown("""
    <div style='margin-bottom: 20px;'>
    <ol>
        <li><strong>Content Performance Analysis</strong>: Identify which video categories perform best based on engagement metrics.</li>
        <li><strong>Engagement Pattern Recognition</strong>: Discover relationships between different engagement metrics (views, likes, comments).</li>
        <li><strong>Temporal Trends Exploration</strong>: Analyze how video publishing and performance have changed over time.</li>
        <li><strong>Channel Performance Comparison</strong>: Compare top-performing channels across different metrics.</li>
        <li><strong>Data Quality Assessment</strong>: Evaluate the completeness and reliability of the dataset.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Data Caveats")
    st.markdown("""
    <div style='background-color: #fff9e6; padding: 15px; border-left: 4px solid #ffcc00; border-radius: 4px;'>
    <p><strong>Important considerations when interpreting the results:</strong></p>
    <ul>
        <li>Outliers have been filtered to improve visualization clarity, which may affect extreme value analysis.</li>
        <li>Some data points may be missing, particularly for engagement metrics.</li>
        <li>The dataset represents a specific time period and may not reflect current YouTube trends.</li>
        <li>Correlation does not imply causation when interpreting relationships between metrics.</li>
        <li>Statistical significance should be considered when drawing conclusions from patterns.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)