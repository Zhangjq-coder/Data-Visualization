"""
YouTube数据集可视化分析应用主程序
================================

该应用基于Streamlit框架，对YouTube数据集进行深入分析和可视化展示。
主要功能包括：
1. 数据加载和预处理
2. 多维度数据分析（类别分布、相关性分析、互动指标等）
3. 丰富的可视化图表展示
4. 数据过滤和采样功能

作者：Junqing Zhang
学号：20252223
邮箱：junqing.zhang@efrei.net
GitHub：https://github.com/Zhangjq-coder/Data-Visualization
"""

import streamlit as st
import pandas as pd
# 导入各个功能模块
# intro: 项目介绍模块
# overview: 数据概览模块
# deep_dives: 深入分析模块
# conclusions: 结论模块
from sections import intro, overview, deep_dives, conclusions
# 导入数据处理工具
# load_data: 数据加载函数
# engineer_features: 特征工程函数
from utils.io import load_data
from utils.prep import engineer_features

# 应用程序标题和样式设置
# page_title: 浏览器标签页标题
# layout: 页面布局设置为"wide"以充分利用屏幕宽度
st.set_page_config(page_title="YouTube Dataset Visualization Analysis", layout="wide")

# 页面样式 - 定义CSS样式来美化应用界面
# 这些样式用于控制应用的整体外观和感觉
page_style = """
<style>
    /* 主标题样式 */
    .main-header {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
    }
    
    /* 指标卡样式 */
    .stMetric {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,1);
    }
    
    /* 选项卡内容样式 */
    .tab-content {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 洞察框样式 */
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    
    /* 下载按钮样式 */
    .download-button {
        background-color: #2ecc71;
        color: white;
        border-radius: 4px;
    }
    
    /* 侧边栏标题样式 */
    .sidebar-header {
        font-weight: bold;
        color: #333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* 选项卡列表样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    /* 单个选项卡样式 */
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #f0f0f0;
        border-radius: 4px 4px 0 0;
        padding: 8px 16px;
    }
    
    /* 选中选项卡样式 */
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

# 主标题 - 应用的主标题，使用HTML格式以便应用CSS样式
st.markdown("<h1 class='main-header'>YouTube数据集可视化分析 | YouTube Dataset Visualization Analysis</h1>", unsafe_allow_html=True)

# 侧边栏信息 - 在应用左侧显示相关信息
with st.sidebar:
    # 添加图片 - 显示WUT Logo和相关图片
    # use_container_width=True: 使图片适应容器宽度
    st.image("assets/WUT-Logo.png", caption="WUT Logo", use_container_width=True)
    st.image("assets/微信图片_20251121083856_98_172.png", caption="Related Image", use_container_width=True)
    
    # 课程信息 - 显示课程相关信息
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>课程信息 | Course Information</h3>", unsafe_allow_html=True)
    st.write("课程名称 | Course Name: Data Visualization")
    st.write("授课教师 | Instructor: Prof. Mano Mathew")
    st.write("学生姓名 | Student Name: Junqing Zhang")
    st.write("学号 | Student ID: 20252223")
    st.write("邮箱 | Email: junqing.zhang@efrei.net")
    st.markdown("[GitHub 项目地址 | GitHub Project](https://github.com/Zhangjq-coder/Data-Visualization)")
    
    # 数据集信息 - 显示数据集相关信息
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>关于数据集 | About Dataset</h3>", unsafe_allow_html=True)
    st.info("本数据集包含YouTube频道和视频的详细统计信息，包括观看次数、订阅者数量、点赞数等多种指标。 | This dataset contains detailed statistics on YouTube channels and videos, including views, subscriber counts, likes, and other metrics.")
    
    # 数据集链接 - 提供数据集的Kaggle链接
    st.markdown("[查看数据集 | View Dataset](https://www.kaggle.com/datasets/thedevastator/revealing-insights-from-youtube-video-and-channe/data)")
    
    # 界面设置 - 允许用户自定义界面主题
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>界面设置 | Interface Settings</h3>", unsafe_allow_html=True)
    # 主题选择下拉框
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
    
    # 数据过滤选项 - 控制是否显示基本数据信息
    st.markdown("---")
    st.markdown("<h3 class='sidebar-header'>数据过滤 | Data Filtering</h3>", unsafe_allow_html=True)
    # show_data_info: 控制是否显示数据基本信息统计的复选框
    show_data_info = st.checkbox("显示数据基本信息 | Show Basic Data Info", value=True, help="控制是否显示数据基本信息统计 | Control whether to display basic data information statistics")
    
    # 添加数据刷新按钮 - 允许用户重新加载数据
    # 使用session_state来跟踪刷新状态
    if 'refresh_data' not in st.session_state:
        st.session_state.refresh_data = False
    
    # 刷新数据按钮
    refresh_data = st.button("刷新数据 | Refresh Data", help="重新加载并处理数据集 | Reload and process the dataset")
    if refresh_data:
        st.session_state.refresh_data = True
        # experimental_rerun(): 重新运行应用以应用更改
        st.experimental_rerun()

# 主函数
def main():
    """
    主函数，处理数据加载和可视化展示
    
    功能：
    1. 加载YouTube数据集
    2. 应用数据预处理和特征工程
    3. 创建应用界面和选项卡
    4. 渲染各个分析部分
    
    异常处理：
    - 检查数据文件是否存在
    - 处理数据加载失败的情况
    - 处理空数据集的情况
    """
    # 定义数据文件路径
    file_path = "data/YouTubeDataset_withChannelElapsed.csv"
    
    # 检查文件是否存在
    import os
    if not os.path.exists(file_path):
        st.error(f"数据文件 '{file_path}' 不存在，请检查路径是否正确。 | Data file '{file_path}' does not exist, please check the path.")
        return
    
    # 加载数据（使用默认采样大小）
    # spinner: 显示加载状态的旋转指示器
    with st.spinner("正在加载数据，请稍候..."):
        # load_data: 从utils.io导入的数据加载函数
        df = load_data(file_path, sample_size=50000)
        if df is None:
            st.error("数据加载失败。 | Data loading failed.")
            return
        if df.empty:
            st.error("数据为空。 | Data is empty.")
            return
        # success: 显示成功消息
        st.success("数据加载成功！ | Data loaded successfully!")
    
    # 添加数据质量报告 - 显示数据集的基本统计信息
    st.subheader("数据质量报告 | Data Quality Report")
    # columns: 创建多列布局
    col1, col2, col3 = st.columns(3)
    with col1:
        # metric: 显示指标值
        st.metric("总记录数 | Total Records", f"{len(df):,}")
    with col2:
        st.metric("数据列数 | Number of Columns", f"{len(df.columns):,}")
    with col3:
        # 计算缺失数据比例
        missing_data_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("缺失数据比例 | Missing Data %", f"{missing_data_pct:.2f}%")
    
    # 在侧边栏添加数据采样和过滤选项
    with st.sidebar:
        st.markdown("---")
        st.markdown("<h3 class='sidebar-header'>数据采样设置 | Data Sampling Settings</h3>", unsafe_allow_html=True)
        # use_sampling: 是否使用数据采样的复选框
        use_sampling = st.checkbox("使用数据采样（对于大型数据集） | Use Data Sampling (For Large Datasets)", value=True)
        # sample_size: 采样大小滑块
        sample_size = st.slider(
            "采样数据量 | Sample Size", 
            min_value=1000, 
            max_value=100000, 
            value=50000, 
            step=1000,
            disabled=not use_sampling
        )
        
        # 添加随机种子设置 - 确保采样的可重复性
        if use_sampling:
            # random_seed: 随机种子数值输入框
            random_seed = st.number_input("随机种子 | Random Seed", min_value=0, value=42, help="设置随机种子以获得可重复的采样结果 | Set random seed for reproducible sampling results")
        
        # 数据质量过滤选项 - 允许用户过滤异常数据
        st.markdown("---")
        st.markdown("<h3 class='sidebar-header'>数据质量过滤 | Data Quality Filtering</h3>", unsafe_allow_html=True)
        
        # 添加高级过滤选项 - 提供更多过滤选项的展开面板
        with st.expander("高级过滤选项 | Advanced Filter Options", expanded=False):
            # filter_outliers: 过滤异常值的复选框
            filter_outliers = st.checkbox("过滤异常值 | Filter Outliers", value=True)
            
            # 视频观看量过滤选项
            if 'videoViewCount' in df.columns:
                # min_views: 最小观看量数值输入框
                min_views = st.number_input("最小观看量 | Minimum Views", min_value=0, value=0, step=1000, help="过滤掉观看量低于此值的视频 | Filter out videos with views below this value")
                # max_views: 最大观看量数值输入框
                max_views = st.number_input("最大观看量 | Maximum Views", min_value=0, value=int(df['videoViewCount'].max()) if 'videoViewCount' in df.columns else 1000000, step=1000)
            
            # 视频类别过滤选项
            if 'categoryName' in df.columns:
                # categories: 获取所有唯一类别
                categories = df['categoryName'].unique()
                # selected_categories: 多选框用于选择视频类别
                selected_categories = st.multiselect(
                    "选择视频类别 | Select Video Categories",
                    options=categories,
                    default=None,
                    help="选择要分析的视频类别，不选择表示全部 | Select video categories to analyze, leave empty for all"
                )
        
        # 重置按钮 - 允许用户重置所有设置
        if st.button("重置所有设置 | Reset All Settings", key="reset_filter"):
            # clear(): 清除所有session_state
            st.session_state.clear()
            st.experimental_rerun()
    
    # 加载数据 - 根据用户设置重新加载数据
    with st.spinner("正在加载数据..."):
        # 使用会话状态保存加载状态
        if 'data_loaded' not in st.session_state or st.session_state.get('refresh_data', False):
            st.session_state.data_loaded = False
            # 根据采样设置加载数据
            df = load_data(file_path, sample_size=sample_size if use_sampling else None)
            st.session_state.data_loaded = True
        else:
            # 如果数据已加载且不需要刷新，使用缓存的数据
            df = load_data(file_path, sample_size=sample_size if use_sampling else None)
    
    if df is not None:
        st.success(f"成功加载数据，共 {len(df):,} 条记录 | Successfully loaded data, total {len(df):,} records")
        
        # 应用高级过滤选项
        if 'min_views' in locals() and 'videoViewCount' in df.columns:
            # 验证输入值
            if min_views >= 0:
                # 过滤掉观看量低于最小值的视频
                df = df[df['videoViewCount'] >= min_views]
            else:
                st.warning("最小观看量不能为负数，已忽略此过滤条件。 | Minimum views cannot be negative, ignoring this filter.")
    
        if 'max_views' in locals() and 'videoViewCount' in df.columns:
            # 验证输入值
            if max_views >= 0 and max_views >= min_views:
                # 过滤掉观看量高于最大值的视频
                df = df[df['videoViewCount'] <= max_views]
            else:
                st.warning("最大观看量设置无效，已忽略此过滤条件。 | Maximum views setting is invalid, ignoring this filter.")
    
        if 'selected_categories' in locals() and selected_categories and 'categoryName' in df.columns:
            # 根据选择的类别过滤数据
            df = df[df['categoryName'].isin(selected_categories)]
            st.info(f"已应用类别过滤，显示 {len(df):,} 条记录 | Category filtering applied, showing {len(df):,} records")
        
        # 应用特征工程 - 对数据进行特征工程处理
        # engineer_features: 从utils.prep导入的特征工程函数
        df = engineer_features(df)
        
        # 创建选项卡 - 创建应用的主要功能选项卡
        # tabs: 创建多个选项卡用于组织不同功能
        tabs = st.tabs([
            "介绍 | Introduction",
            "数据概览 | Data Overview", 
            "深入分析 | Deep Dives",
            "结论 | Conclusions"
        ])
        
        # 渲染各部分 - 根据用户选择的选项卡渲染相应的内容
        with tabs[0]:
            # intro.render: 渲染项目介绍部分
            intro.render(df)
            
        with tabs[1]:
            # overview.render: 渲染数据概览部分
            overview.render(df, show_data_info)
            
        with tabs[2]:
            # deep_dives.render: 渲染深入分析部分
            deep_dives.render(df)
            
        with tabs[3]:
            # conclusions.render: 渲染结论部分
            conclusions.render(df)

# 程序入口点
# __name__ == "__main__": 确保只有直接运行此脚本时才执行main函数
if __name__ == "__main__":
    main()