import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def create_category_distribution_chart(df):
    """Create a pie chart showing the distribution of video categories."""
    if 'categoryName' not in df.columns:
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
def create_horizontal_bar_chart(df, x_col, y_col, title):
    """Create a horizontal bar chart."""
    fig_bar = px.bar(
        x=df[x_col],
        y=df[y_col],
        orientation="h",
        title=title,
        color=df[x_col],
        color_continuous_scale="Viridis"
    )
    fig_bar.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        font=dict(size=12)
    )
    return fig_bar
def create_correlation_heatmap(df, columns):
    """Create a correlation heatmap for the specified columns."""
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
def create_time_series_chart(df, x_col, y_col, title):
    """Create a time series line chart."""
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
def create_histogram_chart(df, column, title, bins=50):
    """Create a histogram chart for the specified column."""
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
def create_box_plot(df, x_col, y_col, title):
    """Create a box plot for the specified columns."""
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
def create_scatter_plot_matrix(df, columns, title):
    """Create a scatter plot matrix for the specified columns."""
    sample_df = df[columns].dropna().sample(min(1000, len(df)), random_state=42)
    fig_scatter_matrix = px.scatter_matrix(
        sample_df,
        dimensions=columns[:4],
        title=title,
        color=sample_df[columns[0]] if len(columns) > 0 else None,
        opacity=0.5
    )
    fig_scatter_matrix.update_layout(height=800)
    return fig_scatter_matrix