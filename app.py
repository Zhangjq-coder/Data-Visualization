import streamlit as st
import pandas as pd
from sections import intro, overview, deep_dives, conclusions
from utils.io import load_data
from utils.prep import engineer_features

# 应用程序标题和样式设置
st.set_page_config(page_title="YouTube Dataset Visualization Analysis", layout="wide")

# 页面样式
page_style = """
<style>
    .main-header {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .tab-content {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .download-button {
        background-color: #2ecc71;
        color: white;
        border-radius: 4px;
    }
    .sidebar-header {
        font-weight: bold;
        color: #333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #f0f0f0;
        border-radius: 4px 4px 0 0;
        padding: 8px 16px;
    }
    .stTabs [data-baseweb="tab"] [data-selected="true"] {
        background-color: #ffffff;
        box-shadow: 0 -2px 0 #3498db inset;
    }
    /* 响应式设计 - 移动端适配 */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .tab-content {
            padding: 10px;
        }
        .stMetric {
            margin-bottom: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px;
            font-size: 0.9rem;
        }
    }
</style>"""
st.markdown(page_style, unsafe_allow_html=True)

# 主标题
st.markdown("<h1 class='main-header'>YouTube数据集可视化分析 | YouTube Dataset Visualization Analysis</h1>", unsafe_allow_html=True)

# 侧边栏信息
with st.sidebar:
    # 添加图片
    st.image("assets/WUT-Logo.png", caption="WUT Logo", use_container_width=True)
    st.image("assets/微信图片_20251121083856_98_172.png", caption="Related Image", use_container_width=True)
    
    # 课程信息
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>课程信息 | Course Information</h3>", unsafe_allow_html=True)
    st.write("课程名称 | Course Name: Data Visualization")
    st.write("授课教师 | Instructor: Prof. Mano Mathew")
    st.write("学生姓名 | Student Name: Junqing Zhang")
    st.write("学号 | Student ID: 20252223")
    st.write("邮箱 | Email: junqing.zhang@efrei.bet")
    
    # 数据集信息
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>关于数据集 | About Dataset</h3>", unsafe_allow_html=True)
    st.info("本数据集包含YouTube频道和视频的详细统计信息，包括观看次数、订阅者数量、点赞数等多种指标。 | This dataset contains detailed statistics on YouTube channels and videos, including views, subscriber counts, likes, and other metrics.")
    
    # 数据集链接
    st.markdown("[查看数据集 | View Dataset](https://www.kaggle.com/datasets/thedevastator/revealing-insights-from-youtube-video-and-channe/data)")
    
    # 主题选择 (Theme Selection)
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>界面设置 | Interface Settings</h3>", unsafe_allow_html=True)
    theme = st.selectbox(
        "选择主题颜色 | Select Theme Color",
        ["默认蓝色 | Default Blue", "活力绿色 | Energetic Green", "温暖橙色 | Warm Orange", "优雅紫色 | Elegant Purple"],
        index=0,
        help="选择应用程序的主题颜色 | Select the theme color for the application"
    )
    
    # 根据选择的主题调整样式
    if theme == "活力绿色":
        st.markdown("""<style>
            .main-header { color: #27ae60; }
            .tab-content { border-left: 4px solid #27ae60; }
            .insight-box { border-left: 4px solid #27ae60; }
        </style>""", unsafe_allow_html=True)
    elif theme == "温暖橙色":
        st.markdown("""<style>
            .main-header { color: #e67e22; }
            .tab-content { border-left: 4px solid #e67e22; }
            .insight-box { border-left: 4px solid #e67e22; }
        </style>""", unsafe_allow_html=True)
    elif theme == "优雅紫色":
        st.markdown("""<style>
            .main-header { color: #9b59b6; }
            .tab-content { border-left: 4px solid #9b59b6; }
            .insight-box { border-left: 4px solid #9b59b6; }
        </style>""", unsafe_allow_html=True)
    
    # 过滤选项
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>数据过滤 | Data Filtering</h3>", unsafe_allow_html=True)
    show_data_info = st.checkbox("显示数据基本信息 | Show Basic Data Info", value=True, help="控制是否显示数据基本信息统计 | Control whether to display basic data information statistics")
    
    # 添加数据刷新按钮
    if 'refresh_data' not in st.session_state:
        st.session_state.refresh_data = False
    
    refresh_data = st.button("刷新数据 | Refresh Data", help="重新加载并处理数据集 | Reload and process the dataset")
    if refresh_data:
        st.session_state.refresh_data = True
        st.experimental_rerun()

# 主函数
def main():
    """
    主函数，处理数据加载和可视化展示
    """
    file_path = "data/YouTubeDataset_withChannelElapsed.csv"
    
    # 检查文件是否存在
    import os
    if not os.path.exists(file_path):
        st.error(f"数据文件 '{file_path}' 不存在，请检查路径是否正确。 | Data file '{file_path}' does not exist, please check the path.")
        return
    
    # 加载数据（使用默认采样大小）
    with st.spinner("正在加载数据，请稍候..."):
        df = load_data(file_path, sample_size=50000)
        if df is None or df.empty:
            st.error("数据加载失败或数据为空。 | Data loading failed or data is empty.")
            st.stop()
        st.success("数据加载成功！ | Data loaded successfully!")
    
    # 在侧边栏添加数据采样和过滤选项
    with st.sidebar:
        st.markdown("---")
        st.markdown("<h3 class='sidebar-header'>数据采样设置 | Data Sampling Settings</h3>", unsafe_allow_html=True)
        use_sampling = st.checkbox("使用数据采样（对于大型数据集） | Use Data Sampling (For Large Datasets)", value=True)
        sample_size = st.slider(
            "采样数据量 | Sample Size", 
            min_value=1000, 
            max_value=100000, 
            value=50000, 
            step=1000,
            disabled=not use_sampling
        )
        
        # 添加随机种子设置
        if use_sampling:
            random_seed = st.number_input("随机种子 | Random Seed", min_value=0, value=42, help="设置随机种子以获得可重复的采样结果 | Set random seed for reproducible sampling results")
        
        # 数据质量过滤选项
        st.markdown("---")
        st.markdown("<h3 class='sidebar-header'>数据质量过滤 | Data Quality Filtering</h3>", unsafe_allow_html=True)
        
        # 添加高级过滤选项
        with st.expander("高级过滤选项 | Advanced Filter Options", expanded=False):
            filter_outliers = st.checkbox("过滤异常值 | Filter Outliers", value=True)
            
            if 'videoViewCount' in df.columns:
                min_views = st.number_input("最小观看量 | Minimum Views", min_value=0, value=0, step=1000, help="过滤掉观看量低于此值的视频 | Filter out videos with views below this value")
                max_views = st.number_input("最大观看量 | Maximum Views", min_value=0, value=int(df['videoViewCount'].max()) if 'videoViewCount' in df.columns else 1000000, step=1000)
            
            if 'categoryName' in df.columns:
                categories = df['categoryName'].unique()
                selected_categories = st.multiselect(
                    "选择视频类别 | Select Video Categories",
                    options=categories,
                    default=None,
                    help="选择要分析的视频类别，不选择表示全部 | Select video categories to analyze, leave empty for all"
                )
        
        # 重置按钮
        if st.button("重置所有设置 | Reset All Settings", key="reset_filter"):
            st.session_state.clear()
            st.experimental_rerun()
    
    # 加载数据
    with st.spinner("正在加载数据..."):
        # 使用会话状态保存加载状态
        if 'data_loaded' not in st.session_state or st.session_state.get('refresh_data', False):
            st.session_state.data_loaded = False
            df = load_data(file_path, sample_size=sample_size if use_sampling else None)
            st.session_state.data_loaded = True
        else:
            # 如果数据已加载且不需要刷新，使用缓存的数据
            df = load_data(file_path, sample_size=sample_size if use_sampling else None)
    
    if df is not None:
        st.success(f"成功加载数据，共 {len(df):,} 条记录 | Successfully loaded data, total {len(df):,} records")
        
        # 应用高级过滤选项
        if 'min_views' in locals() and 'videoViewCount' in df.columns:
            df = df[df['videoViewCount'] >= min_views]
        
        if 'max_views' in locals() and 'videoViewCount' in df.columns:
            df = df[df['videoViewCount'] <= max_views]
        
        if 'selected_categories' in locals() and selected_categories and 'categoryName' in df.columns:
            df = df[df['categoryName'].isin(selected_categories)]
            st.info(f"已应用类别过滤，显示 {len(df):,} 条记录 | Category filtering applied, showing {len(df):,} records")
        
        # 应用特征工程
        df = engineer_features(df)
        
        # 创建选项卡
        tabs = st.tabs([
            "介绍 | Introduction",
            "数据概览 | Data Overview", 
            "深入分析 | Deep Dives",
            "结论 | Conclusions"
        ])
        
        # 渲染各部分
        with tabs[0]:
            intro.render(df)
            
        with tabs[1]:
            overview.render(df, show_data_info)
            
        with tabs[2]:
            deep_dives.render(df)
            
        with tabs[3]:
            conclusions.render(df)

if __name__ == "__main__":
    main()