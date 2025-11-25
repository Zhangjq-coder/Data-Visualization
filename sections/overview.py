import streamlit as st
import pandas as pd
import numpy as np
def render(df, show_data_info=True):
    st.header("Data Overview")
    if show_data_info:
        st.subheader("Basic Data Information")
        overview_cols = st.columns(3)
        with overview_cols[0]:
            st.metric("Total Records", f"{len(df):,}")
        with overview_cols[1]:
            st.metric("Number of Columns", f"{len(df.columns):,}")
        with overview_cols[2]:
            category_count = df['categoryName'].nunique() if 'categoryName' in df.columns else 0
            st.metric("Number of Categories", category_count)
        tab1, tab2, tab3 = st.tabs(["Data Structure", "Numerical Statistics", "Data Preview"])
        with tab1:
            st.write("Data Types:")
            st.dataframe(df.dtypes.astype(str))
            st.write("\nMissing Value Statistics:")
            missing_data = df.isnull().sum()
            missing_percent = (missing_data / len(df) * 100).round(2)
            missing_df = pd.DataFrame({
                'Missing Count': missing_data,
                'Missing Percentage': missing_percent
            })
            st.dataframe(missing_df[missing_df['Missing Count'] > 0])
        with tab2:
            st.write("Numerical Columns Summary:")
            numeric_df = df.select_dtypes(include=[np.number])
            st.dataframe(numeric_df.describe().style.format(precision=2))
        with tab3:
            st.write("First 10 Rows:")
            st.dataframe(df.head(10))
            st.write("\nLast 10 Rows:")
            st.dataframe(df.tail(10))
    export_col, spacer_col = st.columns([1, 4])
    with export_col:
        export_format = st.selectbox(
            "Export Data Format",
            ["CSV", "Excel", "JSON"],
            index=0,
            help="Select the data format to export"
        )
        if st.button("Export Current Data", use_container_width=True, type="primary"):
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