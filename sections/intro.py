import streamlit as st

def render(df):
    """
    渲染介绍部分
    
    参数:
    df (pandas.DataFrame): 包含YouTube数据的DataFrame
    
    功能:
    1. 显示项目介绍和目标
    2. 描述数据集内容
    3. 说明分析目标
    4. 提供数据注意事项
    """
    # 项目介绍标题
    st.header("项目介绍 | Project Introduction")
    
    # 项目介绍内容 - 使用insight-box样式
    st.markdown("""
    <div class="insight-box">
    <p>本项目旨在通过对YouTube数据集的深入分析和可视化，揭示YouTube平台上内容创作者的表现、用户行为模式以及各类别视频的受欢迎程度。</p>
    <p>This project aims to provide in-depth analysis and visualization of YouTube dataset to reveal content creators' performance, user behavior patterns, and popularity of different video categories on the YouTube platform.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 数据集说明标题
    st.subheader("数据集说明 | Dataset Description")
    # 数据集说明内容
    st.write("""
    本数据集包含YouTube频道和视频的详细统计信息，包括但不限于：
    - 视频观看次数 (videoViewCount)
    - 订阅者数量 (subscriberCount)
    - 点赞数 (videoLikeCount)
    - 不喜欢数 (videoDislikeCount)
    - 评论数 (VideoCommentCount)
    - 发布时间 (videoPublished)
    - 视频类别 (videoCategoryId)
    
    The dataset contains detailed statistics on YouTube channels and videos, including but not limited to:
    - Video view counts
    - Subscriber counts
    - Like counts
    - Dislike counts
    - Comment counts
    - Publish time
    - Video categories
    """)
    
    # 分析目标标题
    st.subheader("分析目标 | Analysis Objectives")
    # 分析目标内容
    st.write("""
    1. 探索不同类别视频的分布情况
    2. 分析关键指标之间的相关性
    3. 研究用户互动模式（点赞、评论等）
    4. 识别热门内容和趋势
    5. 评估频道表现和内容质量
    
    1. Explore the distribution of videos across different categories
    2. Analyze correlations between key metrics
    3. Study user engagement patterns (likes, comments, etc.)
    4. Identify popular content and trends
    5. Evaluate channel performance and content quality
    """)
    
    # 数据注意事项标题
    st.subheader("数据注意事项 | Data Caveats")
    # 数据注意事项内容
    st.write("""
    <div class="insight-box">
    <ul>
    <li>数据可能存在缺失值和异常值，已在预处理阶段进行了处理</li>
    <li>部分视频的统计数据可能由于API限制而不完整</li>
    <li>数据仅代表特定时间段内的YouTube内容</li>
    <li>Data may contain missing values and outliers, which have been handled during preprocessing</li>
    <li>Some video statistics may be incomplete due to API limitations</li>
    <li>Data represents YouTube content only for a specific time period</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)