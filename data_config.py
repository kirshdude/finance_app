import gspread
import pandas as pd
from credentials import spreadsheet
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import streamlit as st
import time


def get_categories(sheet_name):
    worksheet = spreadsheet.worksheet(sheet_name)
    categories = pd.DataFrame(worksheet.get_all_records())
    categories_dict = categories.to_dict(orient='list')

    return categories_dict

def get_data(sheet_name):
    # Read data from the worksheet
    worksheet = spreadsheet.worksheet(sheet_name)
    data = pd.DataFrame(worksheet.get_all_records())
    return data

def alter_dates(data):
    data['Month'] = pd.to_datetime(data['Month'], format='%b , %Y')
    data['Month fixed'] = data['Month'].dt.strftime('%B %y')
    return data


def filter_dates(data, months):
    end_date = data['Month'].max()
    start_date = end_date - relativedelta(months=months)
    # Filter the DataFrame based on the date range
    filtered_df = data[(data['Month'] >= start_date) & (data['Month'] <= end_date)]
    return filtered_df

def insert_data(sheet_name, new_data):
    worksheet = spreadsheet.worksheet(sheet_name)
    worksheet.append_row(new_data)  # Insert data starting at row 2


def insert_recurring_expenses(recurring_expenses,sheet_name,date):
    recurring_expenses['חודש']= [date for i in range(len(recurring_expenses['קטגוריה']))]
    print(recurring_expenses)
    for index, row in recurring_expenses.iterrows():
        # Simulate some task that takes time
        time.sleep(0.1)

        # Update the progress bar in session state
        st.session_state.progress_value = 100/(index + 1)
        insert_data(sheet_name,list(row))

def format_func(value):
    return "{:,.0f}₪".format(value)


recurring_expenses = pd.DataFrame({
    'קטגוריה': ['שכ״ד וחשבונות', 'שכ״ד וחשבונות', 'שכ״ד וחשבונות', 'שכ״ד וחשבונות', 'צ׳ילי'],
    'תת קטגוריה': ['שכ״ד', 'ועד בית', 'תמי 4', 'אינטרנט', 'וטרינר'],
    'סכום': [6300, 262, 67, 100, 70],
    'חודש': [1,1,1,1,1],
    'ניתן לוותר': ['לא','לא','לא','לא','לא']
})