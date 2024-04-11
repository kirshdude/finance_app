import streamlit as st
import time
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np

import plotly.express as px
from charts import general_monthly_expenses_chart, breakdown
from data_config import get_data, alter_dates, insert_data, filter_dates, get_categories, recurring_expenses, \
     insert_recurring_expenses
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from design import main_dashboard_title, general_expenses_graph_title, side_bar_exp, space_markdown,\
                    adding_recurring_expense, inserting_recurring_expenses




def main():

    st.set_page_config(layout='wide', page_icon='$',
                   page_title='G&EFinanace')

    with st.sidebar:
        selected = option_menu(menu_title='G&E Finances',
                               options=['Expenses Dashboard','Insert Expenses', 'Balance sheet' , 'Pensions & Insurances'],
                               icons=['house', 'database', 'database', 'file-earmark-person']
                               )

    # Option to select different view of the app

    if selected == 'Expenses Dashboard':
        st.write(main_dashboard_title, unsafe_allow_html=True, color="blue")
        monthly_expenses = 'הוצאות שוטפות'
        st.write(general_expenses_graph_title, unsafe_allow_html=True)

        st.write(side_bar_exp, unsafe_allow_html=True )
        months = st.slider('', min_value=1, max_value=24, value=12, step=1)

        sheet_name = monthly_expenses
        data = get_data(sheet_name)
        data = alter_dates(data)
        filtered_data = filter_dates(data, months)

        general_monthly_expenses_chart(filtered_data)
        # st.pyplot(general_monthly_expenses_chart(data))

        ############################################################
        breakdown(data)
        print('got here')

    if selected == 'Insert Expenses':
        TABS = ["🗃הכנסת נתונים", "📈 הוצאות קבועות ", "🔤 משהו מגניב"]
        values= {'Month': datetime.now(), 'Main Category': '', 'Sub Category': '', 'Description': '', 'Amount': 0 ,'avoidable': ''}

        #get the category names
        categories = get_categories('הגדרת שמות')
        # Month input Box
        current_date = datetime.now()
        last_six_months = [(current_date - relativedelta(months=i)).strftime('%b , %Y') for i in range(6)][::-1]
        # Generate dates for the next 6 months
        next_six_months = [(current_date + relativedelta(months=i)).strftime('%b , %Y') for i in range(1, 7)]
        # Combine the lists
        all_months = last_six_months + next_six_months

        tab1, tab2, tab3 = st.tabs(TABS)

        #create the drop downs
        with tab1:
            col1, col2, col3, col4 = st.columns(4)

            with col4:
                Month = st.selectbox(
                    "חודש", [str(date) for date in all_months], 4)

                avoidable = st.selectbox(
                    "ניתן לוותר", ["כן", "לא"], 0)

            with col3:
                #Main Category Box
                Main_Category = st.selectbox(
                    "קטגוריה", [cat for cat in categories.keys()], 0)
                Amount = st.text_input("סכום:", "")

            with col2:
                relevent_sub_categories = categories[Main_Category]

                Sub_Category = st.selectbox(
                    "תת קטגוריה", [cat for cat in relevent_sub_categories], 0)


            m = st.markdown("""
                                            <style>
                                            div.stButton > button:first-child {
                                                  background-color: rgb(108, 133, 245);
                                                  height:3em; width:20%;
                                                  color:white;
                                            }
                                            </style>""", unsafe_allow_html=True)

            save_button = st.button("שמור")
            if save_button:
                # Save or perform any action with the user's input
                values['Month'] = Month
                values['Main Category'] = Main_Category
                values['Sub Category'] = Sub_Category
                values['Amount'] = Amount
                values['avoidable'] = avoidable
                st.write("Saved:", Month)
                insert_data('הוצאות שוטפות', [Main_Category, Sub_Category, Amount, Month, avoidable])

            one_month_ago = current_date - timedelta(days=30)
            one_month_ago = one_month_ago

        with tab2:

            st.dataframe(recurring_expenses)
            month_for_recurrent = st.selectbox(
                "חודש", [str(date) for date in all_months[1:]], 3)
            add_button = st.button('הכנסת הוצאות קבועות', use_container_width=True)


            if add_button:
                if 'progress_value' not in st.session_state:
                    # Initialize progress value in session state
                    st.session_state.progress_value = 0

                # Create the progress bar
                progress_bar = st.progress(st.session_state.progress_value)
                # Save or perform any action with the user's input
                insert_recurring_expenses(recurring_expenses, 'הוצאות שוטפות', month_for_recurrent)
                st.markdown("מושלם")
                # recurring_expenses = recurring_expenses.append(new_row_data, ignore_index=True)

            st.write(space_markdown, unsafe_allow_html=True)
            st.write(space_markdown, unsafe_allow_html=True)
            st.write(adding_recurring_expense, unsafe_allow_html=True)
            st.write(space_markdown, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                # Getting user input
                Main_Category = st.selectbox(" קטגוריה", [cat for cat in categories.keys()], 0)
            with col2:
                Sub_Category = st.selectbox(" תת קטגוריה", [cat for cat in relevent_sub_categories], 0)
            with col3:
                avoidable = st.selectbox("ניתן לוותר", ['לא','כן'], 0)

            with col4:
                Amount = st.text_input(" סכום:", "")

            new_row_data = {
                'קטגוריה': Main_Category,
                'תת קטגוריה': Sub_Category,
                'סכום': Amount,
                'ניתן לוותר':avoidable
            }


    # if selected == 'Balance sheet':



if __name__ == '__main__':
    main()