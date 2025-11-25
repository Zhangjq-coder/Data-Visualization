import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def create_enhanced_category_distribution_chart(df):
    """Create an enhanced pie chart showing the distribution of video categories."""
    try:
        if 'categoryName' not in df.columns:
            logger.warning("categoryName column does not exist in the data")
            return None
        category_counts = df['categoryName'].value_counts()
        category_df = pd.DataFrame({
            'Category': category_counts.index,
            'Count': category_counts.values
        })
        fig_pie = px.pie(
            category_df,
            values='Count',
            names='Category',
            title="Video Category Distribution",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(
            font=dict(size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            margin=dict(l=20, r=20, t=50, b=150)
        )
        fig_pie.update_traces(
            textposition='outside',
            textinfo='label+percent',
            texttemplate='%{label}<br>%{percent:.1%}',
            textfont=dict(size=10)
        )
        return fig_pie
    except Exception as e:
        logger.error(f"Error creating category distribution chart: {str(e)}")
        st.error("Error creating category distribution chart, please check logs for details")
        return None
def create_enhanced_horizontal_bar_chart(df, x_col, y_col, title):
    """Create an enhanced horizontal bar chart."""
    try:
        if x_col not in df.columns or y_col not in df.columns:
            logger.warning(f"Column {x_col} or {y_col} does not exist in the data")
            return None
        fig_bar = px.bar(
            df,
            x=x_col,
            y=y_col,
            orientation="h",
            title=title,
            color=x_col,
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            font=dict(size=12)
        )
        return fig_bar
    except Exception as e:
        logger.error(f"Error creating horizontal bar chart: {str(e)}")
        st.error("Error creating horizontal bar chart, please check logs for details")
        return None
def create_enhanced_vertical_bar_chart(df, x_col, y_col, title):
    """Create an enhanced vertical bar chart."""
    try:
        if x_col not in df.columns or y_col not in df.columns:
            logger.warning(f"Column {x_col} or {y_col} does not exist in the data")
            return None
        fig_bar = px.bar(
            df,
            x=x_col,
            y=y_col,
            orientation="v",
            title=title,
            color=y_col,
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            font=dict(size=12)
        )
        return fig_bar
    except Exception as e:
        logger.error(f"Error creating vertical bar chart: {str(e)}")
        st.error("Error creating vertical bar chart, please check logs for details")
        return None
def create_enhanced_correlation_heatmap(df, columns):
    """Create an enhanced correlation heatmap for the specified columns."""
    try:
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            st.warning(f"The following columns do not exist in the data: {missing_cols}")
            return None
        corr_df = df[columns].corr()
        fig_heatmap = px.imshow(
            corr_df,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Key Metrics Correlation Matrix"
        )
        fig_heatmap.update_layout(font=dict(size=12))
        return fig_heatmap
    except Exception as e:
        logger.error(f"Error creating correlation heatmap: {str(e)}")
        st.error("Error creating correlation heatmap, please check logs for details")
        return None
def create_enhanced_time_series_chart(df, x_col, y_col, title):
    """Create an enhanced time series line chart."""
    try:
        if x_col not in df.columns or y_col not in df.columns:
            logger.warning(f"Column {x_col} or {y_col} does not exist in the data")
            return None
        fig_line = px.line(
            df,
            x=x_col,
            y=y_col,
            markers=True,
            title=title,
            color_discrete_sequence=['#3274A1']
        )
        fig_line.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col
        )
        return fig_line
    except Exception as e:
        logger.error(f"Error creating time series chart: {str(e)}")
        st.error("Error creating time series chart, please check logs for details")
        return None
def create_enhanced_histogram_chart(df, column, title, bins=50):
    """Create an enhanced histogram chart for the specified column."""
    try:
        if column not in df.columns:
            logger.warning(f"Column {column} does not exist in the data")
            return None
        fig_hist = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=title,
            color_discrete_sequence=['skyblue']
        )
        if column in ['like_rate', 'comment_rate']:
            fig_hist.update_layout(
                xaxis_title=f"{column.replace('_', ' ').title()} (%)",
                yaxis_title="Frequency",
                xaxis=dict(range=[0, 1])
            )
            st.markdown("<small>Note: The chart shows raw ratio values, multiply by 100 to convert to percentage</small>", unsafe_allow_html=True)
        else:
            fig_hist.update_layout(
                xaxis_title=column.replace('_', ' ').title(),
                yaxis_title="Frequency"
            )
        return fig_hist
    except Exception as e:
        logger.error(f"Error creating histogram: {str(e)}")
        st.error("Error creating histogram, please check logs for details")
        return None
def create_enhanced_box_plot(df, x_col, y_col, title):
    """Create an enhanced box plot for the specified columns."""
    try:
        if x_col not in df.columns or y_col not in df.columns:
            logger.warning(f"Column {x_col} or {y_col} does not exist in the data")
            return None
        fig_box = px.box(
            df,
            x=x_col,
            y=y_col,
            title=title,
            color=x_col
        )
        fig_box.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            xaxis_tickangle=45,
            legend_title=x_col
        )
        return fig_box
    except Exception as e:
        logger.error(f"Error creating box plot: {str(e)}")
        st.error("Error creating box plot, please check logs for details")
        return None
def create_enhanced_scatter_plot_matrix(df, columns, title):
    """Create an enhanced scatter plot matrix for the specified columns."""
    try:
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"The following columns do not exist in the data: {missing_cols}")
            return None
        sample_size = min(1000, len(df))
        sample_df = df[columns].dropna().sample(sample_size, random_state=42)
        fig_scatter_matrix = px.scatter_matrix(
            sample_df,
            dimensions=columns[:4],
            title=title,
            color=sample_df[columns[0]] if len(columns) > 0 else None,
            opacity=0.5
        )
        fig_scatter_matrix.update_layout(height=800)
        return fig_scatter_matrix
    except Exception as e:
        logger.error(f"Error creating scatter plot matrix: {str(e)}")
        st.error("Error creating scatter plot matrix, please check logs for details")
        return None
def create_channel_performance_comparison_chart(df, top_n=10):
    """Create a chart comparing channel performance."""
    try:
        available_channel_cols = []
        for col in ['channelName', 'channelId']:
            if col in df.columns:
                available_channel_cols.append(col)
        if not available_channel_cols:
            return None
        if 'channelName' in available_channel_cols:
            df_temp = df.copy()
            df_temp['channelName'] = df_temp['channelName'].astype(str).fillna('')
            if df_temp['channelName'].str.strip().ne('').any():
                group_by_col = 'channelName'
                display_col = 'channelName'
                xaxis_title = "Channel Name"
            else:
                group_by_col = 'channelId'
                display_col = 'channelId'
                xaxis_title = "Channel ID"
        else:
            group_by_col = 'channelId'
            display_col = 'channelId'
            xaxis_title = "Channel ID"
        channel_performance = df.groupby(group_by_col)['videoViewCount'].sum().reset_index()
        channel_performance = channel_performance.sort_values('videoViewCount', ascending=False).head(top_n)
        if group_by_col == 'channelId':
            channel_performance['displayId'] = channel_performance['channelId'].apply(
                lambda x: f"Channel{hash(x) % 10000:04d}"
            )
            display_col = 'displayId'
        fig_top_channels = px.bar(
            channel_performance,
            x=display_col,
            y='videoViewCount',
            title=f"Top {top_n} Channel View Counts",
            color='videoViewCount',
            color_continuous_scale="YlOrRd",
            hover_data={display_col: True, group_by_col: True, 'videoViewCount': True}
        )
        fig_top_channels.update_layout(
            xaxis_title=xaxis_title,
            yaxis_title="Total Views",
            xaxis_tickangle=45,
            xaxis=dict(
                tickfont=dict(size=10),
                automargin=True
            )
        )
        return fig_top_channels
    except Exception as e:
        logger.error(f"Error creating channel performance comparison chart: {str(e)}")
        st.error("Error creating channel performance comparison chart, please check logs for details")
        return None
def create_engagement_score_distribution_chart(df):
    """Create a histogram chart showing the distribution of engagement scores."""
    try:
        valid_df = df[(df['videoViewCount'] > 0) & (df['videoLikeCount'].notna()) & (df['VideoCommentCount'].notna())].copy()
        if len(valid_df) > 0:
            valid_df['engagement_score'] = (
                np.log1p(valid_df['videoViewCount']) * 0.4 +
                np.log1p(valid_df['videoLikeCount']) * 0.4 +
                np.log1p(valid_df['VideoCommentCount']) * 0.2
            )
            fig_score_dist = px.histogram(
                valid_df,
                x='engagement_score',
                nbins=30,
                title="Content Quality Comprehensive Score Distribution",
                color_discrete_sequence=['#8884d8']
            )
            fig_score_dist.update_layout(
                xaxis_title="Comprehensive Score",
                yaxis_title="Number of Videos"
            )
            return fig_score_dist
        return None
    except Exception as e:
        logger.error(f"Error creating engagement score distribution chart: {str(e)}")
        st.error("Error creating engagement score distribution chart, please check logs for details")
        return None