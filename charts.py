# from credentials import data
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np




def general_monthly_expenses_chart(data):
    # Group by month and calculate total amount
    monthly_total = data.groupby("Month")["Amount"].sum()

    # Convert the index to a list for plotting
    months = data['Month'].unique()

    # Create the Plotly line chart
    line_chart = px.line(data, x=months, y=monthly_total.values, labels={'Month': 'חודש', 'Amount': 'סך הכל הוצאות'},
                         width=900, height=600)

    # Add annotations for monthly totals
    for i in range(len(monthly_total.values)):
        line_chart.add_annotation(
            x=months[i],
            y=monthly_total.values[i],
            text=str(monthly_total.values[i]),
            showarrow=True,
            arrowhead=0,
            ax=0,
            ay=-30
        )

    # Calculate the average of all monthly totals
    average_total = np.mean(monthly_total.values)

    # Add a trend line representing the average
    line_chart.add_shape(type="line",
                         x0=min(months),
                         y0=average_total,
                         x1=max(months),
                         y1=average_total,
                         line=dict(color="red", width=2, dash="dash"),
                         name="Average Trend")

    # Add data label for the average
    line_chart.add_annotation(
        x=max(months),
        y=average_total,
        text=f'Average: {average_total:.2f}',
        showarrow=True,
        arrowhead=0,
        ax=-50,
        ay=30,
        bgcolor="white"
    )

    # Display Plotly chart
    st.plotly_chart(line_chart)


def breakdown(data):

    st.title('Bar Chart with Breakdown')
    columns = data.columns.unique().tolist()

    st.sidebar.write("Select breakdown options:")
    main_breakdown_options = st.sidebar.multiselect("Select main breakdown:", columns, default=["Month"])
    print(["None"] + columns)
    sub_breakdown_options = st.sidebar.multiselect("Select sub breakdown:", ["None"] + columns, default="None")

    st.sidebar.write("Select filters:")

    category_filter = st.sidebar.selectbox("Select Category:", ["All"] + data["Category"].unique().tolist())
    sub_category_filter = st.sidebar.selectbox("Select Subcategory:", ["All"] + data["Sub Category"].unique().tolist())
    avoidable_filter = st.sidebar.selectbox("Is Avoidable:", ["All"] + data["Is Avoidable"].unique().tolist())

    # Filter data based on user selection
    filtered_data = data.copy()
    if category_filter != "All":
        filtered_data = filtered_data[filtered_data["Category"] == category_filter]
    if sub_category_filter != "All":
        filtered_data = filtered_data[filtered_data["Sub Category"] == sub_category_filter]
    if avoidable_filter != "All":
        filtered_data = filtered_data[filtered_data["Is Avoidable"] == avoidable_filter]

    # Function to generate breakdown data based on user selection
    def generate_breakdown_data(main_breakdown_options, sub_breakdown_options):
        if "None" in sub_breakdown_options or main_breakdown_options == sub_breakdown_options:
            breakdown_data = filtered_data.groupby(main_breakdown_options)["Amount"].sum().reset_index()
        else:
            breakdown_data = filtered_data.groupby(main_breakdown_options + sub_breakdown_options)["Amount"].sum().reset_index()

            # Calculate percentage for each sub-category within its corresponding main category
            breakdown_data['Percentage'] = breakdown_data.groupby(main_breakdown_options)['Amount'].transform(
                lambda x: (x / x.sum()) * 100)

        return breakdown_data

    # Generate breakdown data based on user selection
    breakdown_data = generate_breakdown_data(main_breakdown_options, sub_breakdown_options)

    # Create bar chart
    if "None" in sub_breakdown_options or main_breakdown_options == sub_breakdown_options:
        x_label = main_breakdown_options[0]
        bar_chart = px.bar(breakdown_data, x=x_label, y="Amount", labels={'Amount': 'Total Amount'})
        title = f"Total Amount Breakdown by {x_label}"
    else:
        x_label = " - ".join(main_breakdown_options + sub_breakdown_options)
        bar_chart = px.bar(breakdown_data, x=", ".join(main_breakdown_options), y="Percentage", color=", ".join(sub_breakdown_options),
                           labels={'Percentage': 'Percentage of Total', 'Amount': 'Total Amount'})

        title = f"Total Amount Breakdown by {', '.join(main_breakdown_options)} with Sub Breakdown by {', '.join(sub_breakdown_options)}"

    # Add data labels showing percentage from the total main breakdown category
    if "None" not in sub_breakdown_options:
        bar_chart.update_traces(texttemplate='%{y:.1f}%', textposition='outside')

    bar_chart.update_layout(title=title, xaxis_title=x_label, yaxis_title="Percentage")
    bar_chart.update_layout(height=600, width=900)
    # Display the bar chart
    st.plotly_chart(bar_chart)


