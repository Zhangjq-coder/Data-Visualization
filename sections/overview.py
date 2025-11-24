import streamlit as st
import pandas as pd
import numpy as np

def render(df, show_data_info=True):
    """渲染数据概览部分"""
    st.header("数据概览 | Data Overview")
    
    # 显示数据基本信息
    if show_data_info:
        st.subheader("数据基本信息 | Basic Data Information")
        
        # 创建数据概览统计
        overview_cols = st.columns(3)
        with overview_cols[0]:
            st.metric("总记录数 | Total Records", f"{len(df):,}")
        with overview_cols[1]:
            st.metric("数据列数 | Number of Columns", f"{len(df.columns):,}")
        with overview_cols[2]:
            # 计算有效类别的数量
            category_count = df['categoryName'].nunique() if 'categoryName' in df.columns else 0
            st.metric("有效类别数 | Number of Categories", category_count)
            
        # 使用tabs展示不同的数据信息
        tab1, tab2, tab3 = st.tabs(["数据结构 | Data Structure", "数值统计 | Numerical Statistics", "数据预览 | Data Preview"])
        
        with tab1:
            st.write("数据类型: | Data Types:")
            st.dataframe(df.dtypes.astype(str))
            
            st.write("\n缺失值统计: | Missing Value Statistics:")
            missing_data = df.isnull().sum()
            missing_percent = (missing_data / len(df) * 100).round(2)
            missing_df = pd.DataFrame({
                '缺失值数量 | Missing Count': missing_data,
                '缺失值百分比 | Missing Percentage': missing_percent
            })
            st.dataframe(missing_df[missing_df['缺失值数量 | Missing Count'] > 0])
            
        with tab2:
            st.write("数值列统计摘要: | Numerical Columns Summary:")
            # 只选择数值列进行统计
            numeric_df = df.select_dtypes(include=[np.number])
            st.dataframe(numeric_df.describe().style.format(precision=2))
          
        with tab3:
            st.write("数据前10行: | First 10 Rows:")
            st.dataframe(df.head(10))
         
            st.write("\n数据后10行: | Last 10 Rows:")
            st.dataframe(df.tail(10))
    
    # Add data export functionality | 添加数据导出功能
    export_col, spacer_col = st.columns([1, 4])
    with export_col:
        export_format = st.selectbox(
            "导出数据格式 | Export Data Format",
            ["CSV", "Excel", "JSON"],
            index=0,
            help="选择要导出的数据格式 | Select the data format to export"
        )
        
        if st.button("导出当前数据 | Export Current Data", use_container_width=True, type="primary"):
            import io
            if export_format == "CSV":
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"下载CSV文件 | Download CSV File",
                    data=csv,
                    file_name='youtube_data.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            elif export_format == "Excel":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='YouTube Data')
                processed_data = output.getvalue()
                st.download_button(
                    label=f"下载Excel文件 | Download Excel File",
                    data=processed_data,
                    file_name='youtube_data.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    use_container_width=True
                )
            elif export_format == "JSON":
                json = df.to_json(orient='records')
                st.download_button(
                    label=f"下载JSON文件 | Download JSON File",
                    data=json,
                    file_name='youtube_data.json',
                    mime='application/json',
                    use_container_width=True
                )