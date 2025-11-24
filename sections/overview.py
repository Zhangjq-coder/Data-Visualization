import streamlit as st
import pandas as pd
import numpy as np

def render(df, show_data_info=True):
    """
    渲染数据概览部分
    
    参数:
    df (pandas.DataFrame): 包含YouTube数据的DataFrame
    show_data_info (bool): 控制是否显示数据基本信息的布尔值，默认为True
    
    功能:
    1. 显示数据基本信息（记录数、列数、类别数等）
    2. 展示数据结构、数值统计和数据预览
    3. 提供数据导出功能
    """
    # 数据概览标题
    st.header("数据概览 | Data Overview")
    
    # 显示数据基本信息
    if show_data_info:
        # 基本信息子标题
        st.subheader("数据基本信息 | Basic Data Information")
        
        # 创建数据概览统计 - 使用三列布局显示关键指标
        overview_cols = st.columns(3)
        with overview_cols[0]:
            # 总记录数指标
            st.metric("总记录数 | Total Records", f"{len(df):,}")
        with overview_cols[1]:
            # 数据列数指标
            st.metric("数据列数 | Number of Columns", f"{len(df.columns):,}")
        with overview_cols[2]:
            # 有效类别数计算和指标显示
            category_count = df['categoryName'].nunique() if 'categoryName' in df.columns else 0
            st.metric("有效类别数 | Number of Categories", category_count)
            
        # 使用tabs展示不同的数据信息 - 创建三个选项卡分别显示数据结构、数值统计和数据预览
        tab1, tab2, tab3 = st.tabs(["数据结构 | Data Structure", "数值统计 | Numerical Statistics", "数据预览 | Data Preview"])
        
        # 数据结构选项卡内容
        with tab1:
            # 显示各列的数据类型
            st.write("数据类型: | Data Types:")
            st.dataframe(df.dtypes.astype(str))
            
            # 显示缺失值统计信息
            st.write("\n缺失值统计: | Missing Value Statistics:")
            missing_data = df.isnull().sum()
            missing_percent = (missing_data / len(df) * 100).round(2)
            # 创建缺失值统计DataFrame
            missing_df = pd.DataFrame({
                '缺失值数量 | Missing Count': missing_data,
                '缺失值百分比 | Missing Percentage': missing_percent
            })
            # 只显示存在缺失值的列
            st.dataframe(missing_df[missing_df['缺失值数量 | Missing Count'] > 0])
            
        # 数值统计选项卡内容
        with tab2:
            # 显示数值列的统计摘要
            st.write("数值列统计摘要: | Numerical Columns Summary:")
            # 只选择数值列进行统计
            numeric_df = df.select_dtypes(include=[np.number])
            # 使用describe()方法显示统计信息，并格式化为两位小数
            st.dataframe(numeric_df.describe().style.format(precision=2))
          
        # 数据预览选项卡内容
        with tab3:
            # 显示数据前10行
            st.write("数据前10行: | First 10 Rows:")
            st.dataframe(df.head(10))
         
            # 显示数据后10行
            st.write("\n数据后10行: | Last 10 Rows:")
            st.dataframe(df.tail(10))
    
    # 添加数据导出功能 | 添加数据导出功能
    # 创建两列布局，只使用第一列用于导出控件
    export_col, spacer_col = st.columns([1, 4])
    with export_col:
        # 导出格式选择下拉框
        export_format = st.selectbox(
            "导出数据格式 | Export Data Format",
            ["CSV", "Excel", "JSON"],
            index=0,
            help="选择要导出的数据格式 | Select the data format to export"
        )
        
        # 导出数据按钮
        if st.button("导出当前数据 | Export Current Data", use_container_width=True, type="primary"):
            import io
            # 根据选择的格式导出数据
            if export_format == "CSV":
                # 将DataFrame转换为CSV格式
                csv = df.to_csv(index=False)
                # 创建下载按钮
                st.download_button(
                    label=f"下载CSV文件 | Download CSV File",
                    data=csv,
                    file_name='youtube_data.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            elif export_format == "Excel":
                # 将DataFrame转换为Excel格式
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='YouTube Data')
                processed_data = output.getvalue()
                # 创建下载按钮
                st.download_button(
                    label=f"下载Excel文件 | Download Excel File",
                    data=processed_data,
                    file_name='youtube_data.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    use_container_width=True
                )
            elif export_format == "JSON":
                # 将DataFrame转换为JSON格式
                json = df.to_json(orient='records')
                # 创建下载按钮
                st.download_button(
                    label=f"下载JSON文件 | Download JSON File",
                    data=json,
                    file_name='youtube_data.json',
                    mime='application/json',
                    use_container_width=True
                )