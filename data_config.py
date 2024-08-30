import streamlit as st
import pandas as pd
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
import config

from connectors.connection_manager import ConnectionManager
connection_manager = ConnectionManager()
bq_connection = connection_manager.bigquery_connection
bq_client = bq_connection.client

def update_session_state(key, value):
    st.session_state[key] = value

class DataConfig:
    def __init__(self):
        
        self.project_id = config.project_id 
        self.dataset_id = config.dataset_id 

        self.monthly_expenses_table_name = config.monthly_expenses_table_name 
        self.recurring_expenses_table_name = config.recurring_expenses_table_name 
        self.date_column = config.date_colum 

        if 'monthly_expenses_table' not in st.session_state:
            st.session_state.monthly_expenses_table = self.get_monthly_expenses()
        
        if 'recurring_expenses_table' not in st.session_state:
            st.session_state.recurring_expenses_table = self.get_recurring_expenses()
            
        if 'monthly_last_row' not in st.session_state:
            st.session_state.monthly_last_row = st.session_state.monthly_expenses_table['expense_id'].max()

        if 'added_rows' not in st.session_state:
            st.session_state.added_rows = pd.DataFrame(columns=st.session_state.monthly_expenses_table.columns)

        self.categories_dict = self.get_categories()

    def get_data(self, table_name):
        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset_id}.{table_name}`
            """
        # Run the query
        query_output, query_error = self.query_database(query)
        if query_error is None:
            df = query_output.to_dataframe()
        return df

    @staticmethod
    def get_categories():
        data = st.session_state.monthly_expenses_table
        categories_dict = data.groupby('category')['sub_category'].apply(lambda x: list(set(x))).to_dict()
        return categories_dict

    def get_recurring_expenses(self):
        recurring_expenses = self.get_data(self.recurring_expenses_table_name)
        recurring_expenses[self.date_column] = [datetime.now() for i in range(len(recurring_expenses))]
        recurring_expenses = self.alter_dates(data=recurring_expenses, date_column=self.date_column)
        return recurring_expenses

    def get_monthly_expenses(self):
        monthly_expenses = self.get_data(self.monthly_expenses_table_name)
        if self.date_column in monthly_expenses.columns:
            monthly_expenses[self.date_column] = pd.to_datetime(monthly_expenses[self.date_column], format='%b , %Y')
        return monthly_expenses

    @staticmethod
    def alter_dates(data, date_column):
        data[date_column] = pd.to_datetime(data[date_column])
        data[date_column] = data[date_column].dt.strftime('%B %y')
        return data

    def filter_dates(self, data, months):
        end_date = data[self.date_column].max()
        start_date = end_date - relativedelta(months=months)
        # Filter the DataFrame based on the date range
        filtered_df = data[(data[self.date_column] >= start_date) & (data[self.date_column] <= end_date)]
        return filtered_df

    def query_database(self, query):
        result = None
        query_result = bq_client.query(query)
        try:
            results = query_result.result()
            user_error_message = None
            return  results, user_error_message

        except Exception as error:
            error_message = str(error)
            sorry = 'We are so sorry!'
            user_error_message =  sorry + error_message
            print(user_error_message)
            return result, user_error_message


    def insert_data(self, table_name, data_dict):
        columns = ', '.join(data_dict.keys())
        values = ', '.join(f"'{value}'" if isinstance(value, str) else str(value) for value in data_dict.values())

        # Constructing the insert query
        insert_query = f"""
            INSERT INTO {self.project_id}.{self.dataset_id}.{table_name} ({columns}) 
            VALUES ({values})
        """
        #TODO: add here an exception of error and update last row only if no error
        query_output, query_error = self.query_database(insert_query)

        if query_error is None:
            # Convert the dictionary to a DataFrame
            new_row_df = pd.DataFrame([data_dict])
            # Concatenate the new row to the existing DataFrame
            st.session_state.added_rows = pd.concat([st.session_state.added_rows, new_row_df], ignore_index=True)
            self.update_last_row(table_name, up=True)
            self.update_table(table_name=table_name, add=True, row=new_row_df)
            success_message = 'Data successfully inserted!'
            print(success_message)
            return success_message


    def insert_recurring_expenses(self, recurrent_expenses):
        # Initialize the progress bar
        progress_bar = st.progress(0)

        columns = recurrent_expenses.columns
        total_rows = len(recurrent_expenses)
        for index, row in recurrent_expenses.iterrows():
            # Simulate some task that takes time
            time.sleep(0.1)
            data_dict = dict(zip(columns, row))
            data_dict['expense_id'] = max(0,st.session_state.monthly_last_row) + 1
            self.insert_data(self.monthly_expenses_table_name, data_dict)
            # Update the progress bar in session state
            progress = (index + 1) / total_rows
            progress_bar.progress(progress)

        st.success("All recurring expenses have been inserted.")
        time.sleep(2)  # Display the message for 2 seconds
        st.rerun()

    @staticmethod
    def update_last_row(table_name, up:bool):
        if table_name == 'monthly_expenses_final':
            if up:
                st.session_state.monthly_last_row += 1
            else:
                st.session_state.monthly_last_row -= 1
        else:
            if up:
                st.session_state.recurring_last_row += 1
            else:
                st.session_state.recurring_last_row -= 1

    def delete_row(self, table_name, conditions, last:bool):
        if last:
            if table_name == 'monthly_expenses_final':
                delete_query = f"""
                                   DELETE FROM {self.project_id}.{self.dataset_id}.{table_name}
                                   WHERE expense_id = {st.session_state.monthly_last_row};
                                """
                st.session_state.added_rows = st.session_state.added_rows.iloc[:-1]

            else:
                delete_query = f"""
                                   DELETE FROM {self.project_id}.{self.dataset_id}.{table_name}
                                   WHERE expense_id = {st.session_state.recurring_last_row};
                                                """
        else:
            delete_query = f"""
                            DELETE FROM {self.project_id}.{self.dataset_id}.{table_name}
                            WHERE expense_id = {conditions};
                          """
        self.query_database(delete_query)
        self.update_last_row(table_name, up=False)


    def update_table(self, table_name, add:bool, row=None, index=None):
        if table_name == self.monthly_expenses_table_name:
            if add:
                st.session_state.monthly_expenses_table = pd.concat([st.session_state.monthly_expenses_table, row], ignore_index=True)
            else:
                st.session_state.monthly_expenses_table = st.session_state.monthly_expenses_table[st.session_state.monthly_expenses_table['expense_id'] != index]
        else:
            if add:
                st.session_state.recurring_expenses_table = pd.concat([st.session_state.recurring_expenses_table_name, row], ignore_index=True)
            else:
                st.session_state.recurring_expenses_table = st.session_state.recurring_expenses_table.drop(index=index)

    @staticmethod
    def show_df(table: pd.DataFrame, order_by: list, ascending: bool):
        table = table.sort_values(by=order_by, ascending=ascending)
        st.dataframe(table)


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

#Todo: add an index column to the recurring expenses table in order to delete and add rows
# Add the option to add row to recurring expenses
# add option to remove row from recurring expenses

