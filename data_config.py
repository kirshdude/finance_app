import streamlit as st
import pandas as pd
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta

from connectors.connection_manager import ConnectionManager
connection_manager = ConnectionManager()
bq_connection = connection_manager.bigquery_connection
bq_client = bq_connection.client


class DataConfig:
    def __init__(self):
        # self.categories_sheet = 'הגדרת שמות'
        # self.monthly_expenses_sheet = 'הוצאות שוטפות'
        # self.recurring_expenses_sheet = 'הוצאות קבועות'
        
        self.project_id = 'personal-finance-401213'
        self.dataset_id = 'expenses_test'

        self.categories_table = 'expenses_categories'
        self.monthly_expenses_table = 'monthly_expenses_final'
        self.recurring_expenses_sheet = 'recurring_expenses'

        self.monthly_expenses = self.get_monthly_expenses()
        self.categories_dict = self.get_categories()
        self.recurring_expenses = self.get_recurring_expenses()

    def get_data(self, table_name):
        # Read data from the worksheet
        table_ref = bq_client.dataset(self.dataset_id).table(table_name)
        table = bq_client.get_table(table_ref)
        columns = [schema_field.name for schema_field in table.schema]

        # Construct the dynamic SQL query
        column_checks = " OR ".join([f"{col} IS NOT NULL" for col in columns])
        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset_id}.{table_name}`
            WHERE {column_checks}
            """
        # Run the query
        query_job = bq_client.query(query)
        df = query_job.to_dataframe()
        return df

    def get_categories(self):
        categories = self.get_data(self.categories_table)
        categories.columns = categories.iloc[0]
        categories = categories.drop(0)
        categories_dict = categories.to_dict(orient='list')
        return categories_dict

    def get_recurring_expenses(self):
        recurring_expenses = self.get_data(self.recurring_expenses_sheet)
        recurring_expenses['Month'] = [datetime.now() for i in range(len(recurring_expenses))]
        recurring_expenses = self.alter_dates(recurring_expenses, 'Month')
        return recurring_expenses

    def get_monthly_expenses(self):
        date_column = 'Month'
        monthly_expenses = self.get_data(self.monthly_expenses_table)
        # monthly_expenses = self.alter_dates(monthly_expenses, date_column)
        # monthly_expenses[date_column] = pd.to_datetime(monthly_expenses[date_column], format='%b , %Y')
        return monthly_expenses

    @staticmethod
    def alter_dates(data, date_column='Month'):
        data[date_column] = pd.to_datetime(data[date_column])
        data[date_column] = data[date_column].dt.strftime('%B %y')
        return data

    @staticmethod
    def filter_dates(data, months):
        end_date = data['Month'].max()
        start_date = end_date - relativedelta(months=months)
        # Filter the DataFrame based on the date range
        filtered_df = data[(data['Month'] >= start_date) & (data['Month'] <= end_date)]
        return filtered_df

    def insert_data(self, spread_sheet, new_data):
        worksheet = spreadsheet.worksheet(spread_sheet)
        worksheet.append_row(new_data)  # Insert data starting at row 2

    def insert_recurring_expenses(self, recurrent_expenses):
        for index, row in recurrent_expenses.iterrows():
            # Simulate some task that takes time
            time.sleep(0.1)
            # Update the progress bar in session state
            st.session_state.progress_value = 100/(index + 1)
            self.insert_data(self.monthly_expenses_sheet, list(row))

def format_func(value):
    return "{:,.0f}₪".format(value)

def csv_uploader():
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file is not None:
        # Read the uploaded file with pandas
        csv_file = pd.read_csv(file, header=0)
        return csv_file
    else:
        return file

def process_credit_card_sheet(csv_file):
    index_start_data = csv_file[csv_file.iloc[:, 1].notna()].index.min()
    # If index_start_data is not found, set it to 0
    if pd.isna(index_start_data):
        index_start_data = 0

    df = csv_file.iloc[index_start_data:, :]
    new_columns = df.iloc[0]
    # Rename the columns of the DataFrame
    df.rename(columns=new_columns, inplace=True)
    # Drop the first row as it's now redundant
    df.drop(df.index[0], inplace=True)
    # Drop the rows with NaN values in the second column
    df = df[df.iloc[:, 1].notnull()]
    # Reset the index of the DataFrame
    df.reset_index(drop=True, inplace=True)

    return df



