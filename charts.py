# from credentials import data
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import streamlit as st
from design.headers import break_down_charts, space_markdown, choose_graph_header
import plotly.express as px
import numpy as np
import plotly.express as px
import altair as alt
import seaborn as sns



def general_monthly_expenses_chart(data):
    # Ensure the 'month' column is in datetime format
    data['month'] = pd.to_datetime(data['month'])

    # Group by month and calculate total amount, then reset the index
    monthly_total = data.groupby('month')['amount'].sum().reset_index()

    # Sort by 'month' to ensure chronological order
    monthly_total = monthly_total.sort_values('month')

    # Create the Plotly line chart
    line_chart = px.line(monthly_total, x='month', y='amount',
                         labels={'month': 'month', 'amount': 'Total Expenses'},
                         width=1000, height=600)

    # Add annotations for monthly totals
    for i in range(len(monthly_total)):
        line_chart.add_annotation(
            x=monthly_total['month'].iloc[i],
            y=monthly_total['amount'].iloc[i],
            text=f"{monthly_total['amount'].iloc[i]:,.0f}", #str(monthly_total['amount'].iloc[i]),
            showarrow=True,
            arrowhead=0,
            ax=0,
            ay=-30
        )

    #Todo: make the average trend lind red if over % from income and green if under

    # Calculate the average of all monthly totals
    average_total = monthly_total['amount'].mean()

    # Add a trend line representing the average
    line_chart.add_shape(type="line",
                         x0=monthly_total['month'].min(),
                         y0=average_total,
                         x1=monthly_total['month'].max(),
                         y1=average_total,
                         line=dict(color="red", width=2, dash="dash"),
                         name="Average Trend")

    # Add data label for the average
    line_chart.add_annotation(
        x=monthly_total['month'].max(),
        y=average_total,
        text=f'Average: {average_total:,.0f}',
        showarrow=True,
        arrowhead=0,
        ax=0,
        ay=00,
        bgcolor="red"
    )

    # Display Plotly chart
    st.plotly_chart(line_chart)
    # return line_chart


def update_session_state(key, value):
    # if key not in st.session_state:
    if st.session_state.get(key) != value:
        st.session_state[key] = value

def breakdown(df):
    insight_list = ["Total Expenses Over Time by Category",
                    "Percentage of Sub Category by Category",
                    "Total Percentage of Each Category of Expenses",
                    "Total Breakdown of Avoidable vs Not Avoidable",
                    "Breakdown of Category Types and Sub Category Types for a Specific Month",
                    "Total Expenses Over Time by Avoidability"
                    ]

    st.write(choose_graph_header, unsafe_allow_html=True)
    st.write(space_markdown, unsafe_allow_html=True)
    insight = st.selectbox(
            "Choose a chart ",
            insight_list,
            key='insight_selectbox'
        )

    # Function to format and sort months
    def format_months(df):
        months = df['month'].dropna().unique()
        months = pd.to_datetime(months, format='%Y-%m').strftime('%B %Y')
        months = sorted(months, key=lambda x: pd.to_datetime(x, format='%B %Y'))
        return months

    # Function to apply month filters
    def filter_months(df, excluded_months):
        if excluded_months:
            excluded_months = [pd.to_datetime(month, format='%B %Y').strftime('%Y-%m') for month in excluded_months]
            df = df[~df['month'].isin(excluded_months)]
        return df

    # Initialize excluded_months
    excluded_months = st.multiselect(
        "Select Months to Exclude",
        format_months(df),
        default=[],
        key='month_filter_multiselect'
    )

    # Function to plot percentage of subcategory by category
    def plot_percentage_subcategory_by_category(df, excluded_months=None):
        df = filter_months(df, excluded_months)
        df_category_sum = df.groupby(['category', 'sub_category'])['amount'].sum().reset_index()
        df_category_sum['Percentage'] = df_category_sum.groupby('category')['amount'].transform(
            lambda x: 100 * x / x.sum())

        fig = px.bar(df_category_sum, x='category', y='Percentage', color='sub_category',
                     labels={'Percentage': 'Percentage'},
                     # title="Percentage of Sub Category by Category",
                     height=700, width=1000)
        return fig

    # Function to plot total percentage of each category of expenses
    def plot_total_percentage_of_each_category(df, excluded_months=None):
        df = filter_months(df, excluded_months)
        df_category_sum = df.groupby('category')['amount'].sum().reset_index()
        df_category_sum['Percentage'] = 100 * df_category_sum['amount'] / df_category_sum['amount'].sum()

        fig = px.pie(df_category_sum, names='category', values='Percentage',
                     # title="Total Percentage of Each Category of Expenses",
                     height=700, width=1000)
        return fig

    # Function to plot total breakdown of avoidable vs not avoidable
    def plot_total_breakdown_of_avoidable(df, excluded_months=None):
        df = filter_months(df, excluded_months)
        df_avoidable_sum = df.groupby('is_avoidable')['amount'].sum().reset_index()

        fig = px.pie(df_avoidable_sum, names='is_avoidable', values='amount',
                     # title="Total Breakdown of Avoidable vs Not Avoidable Expenses",
                     height=700, width=1000)
        return fig

    # Function to plot breakdown of category and subcategory types for a specific month
    def plot_breakdown_for_specific_month(df, selected_month):
        df_filtered = df[df['month'] == selected_month]
        df_category_sum = df_filtered.groupby(['category', 'sub_category'])['amount'].sum().reset_index()

        fig = px.bar(df_category_sum, x='category', y='amount', color='sub_category',
                     labels={'amount': 'amount'},
                     title=f"Breakdown of Categories and Sub Categories for {selected_month}",
                     height=700, width=1000)
        return fig

    # Function to plot total expenses over time broken down by category
    def plot_total_expenses_over_time_by_category(df, selected_categories, excluded_months=None):
        df = filter_months(df, excluded_months)

        # Filter the DataFrame by the selected categories
        if selected_categories:
            df = df[df['category'].isin(selected_categories)]

        df_monthly_category_sum = df.groupby(['month', 'category'])['amount'].sum().reset_index()
        df_monthly_category_sum['month'] = pd.to_datetime(df_monthly_category_sum['month'], format='%Y-%m')
        df_monthly_category_sum = df_monthly_category_sum.pivot(index='month', columns='category',
                                                                values='amount').fillna(0)
        df_monthly_category_sum = df_monthly_category_sum.reset_index()
        df_monthly_category_sum = pd.melt(df_monthly_category_sum, id_vars='month', var_name='category',
                                          value_name='amount')

        fig = px.bar(df_monthly_category_sum, x='month', y='amount', color='category',
                     labels={'amount': 'amount'},
                     # title="Total Expenses Over Time by Category",
                     height=700, width=1000)
        return fig

    # Function to plot total expenses over time broken down by avoidability
    def plot_total_expenses_over_time_by_avoidability(df, excluded_months=None):
        df = filter_months(df, excluded_months)
        df_monthly_avoidable_sum = df.groupby(['month', 'is_avoidable'])['amount'].sum().reset_index()
        df_monthly_avoidable_sum['month'] = pd.to_datetime(df_monthly_avoidable_sum['month'], format='%Y-%m')
        df_monthly_avoidable_sum = df_monthly_avoidable_sum.pivot(index='month', columns='is_avoidable', values='amount').fillna(0)
        df_monthly_avoidable_sum = df_monthly_avoidable_sum.reset_index()
        df_monthly_avoidable_sum = pd.melt(df_monthly_avoidable_sum, id_vars='month', var_name='is_avoidable', value_name='amount')

        fig = px.bar(df_monthly_avoidable_sum, x='month', y='amount', color='is_avoidable',
                     labels={'amount': 'amount'},
                     # title="Total Expenses Over Time by Avoidability",
                     height=700, width=1000)
        return fig

    # Display the corresponding graph based on the selected insight
    if insight == "Breakdown of Category Types and Sub Category Types for a Specific Month":
        selected_month = st.selectbox("Select Month", format_months(df), key='month_selectbox')
        selected_month = pd.to_datetime(selected_month, format='%B %Y').strftime('%Y-%m')

    # Layout: Single column with graph and dropdown below
    if insight == "Percentage of Sub Category by Category":
        fig = plot_percentage_subcategory_by_category(df, excluded_months)

    elif insight == "Total Percentage of Each Category of Expenses":
        fig = plot_total_percentage_of_each_category(df, excluded_months)

    elif insight == "Total Breakdown of Avoidable vs Not Avoidable":
        fig = plot_total_breakdown_of_avoidable(df, excluded_months)

    elif insight == "Breakdown of Category Types and Sub Category Types for a Specific Month":
        fig = plot_breakdown_for_specific_month(df, selected_month)

    elif insight == "Total Expenses Over Time by Category":
        categories = df['category'].unique()
        selected_categories = st.multiselect('Select Categories', categories, default=categories)
        fig = plot_total_expenses_over_time_by_category(df, selected_categories, excluded_months)

    elif insight == "Total Expenses Over Time by Avoidability":
        fig = plot_total_expenses_over_time_by_avoidability(df, excluded_months)

    st.write(break_down_charts.format(insight), unsafe_allow_html=True)
    st.plotly_chart(fig)