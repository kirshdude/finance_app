import streamlit as st

# Set the page configuration
st.set_page_config(layout='wide', page_icon='$', page_title='G&EFinanace')

from streamlit_option_menu import option_menu
import numpy as np
from charts import general_monthly_expenses_chart, breakdown
from data_config import DataConfig, csv_uploader, process_credit_card_sheet
from datetime import datetime
from dateutil.relativedelta import relativedelta
from design.headers import main_dashboard_title, general_expenses_graph_title, slide_bar_exp, space_markdown, \
    adding_recurring_expense, home_page_title
from design.structure import side_bar, TABS
import design.buttons as deisgn_buttons
from sections.insert_monthly_expenses import insert_monthly_expenses as insert_monthly_expenses_form

# Initialize the data class
data_class = DataConfig()

# Caching data processing functions
@st.cache_data
def load_monthly_expenses():
    return data_class.monthly_expenses

@st.cache_data
def filter_dates(data, months):
    return data_class.filter_dates(data, months)

@st.cache_data
def load_categories():
    return data_class.categories_dict

categories_cached = load_categories()

@st.cache_data
def load_recurring_expenses():
    return data_class.recurring_expenses

current_date = datetime.now()
@st.cache_data
def load_current_date():
    formatted_date = current_date.strftime('%Y-%m-%d')
    return formatted_date

formatted_date = load_current_date()

@st.cache_data
def get_all_months():
    last_six_months = [(current_date - relativedelta(months=i)).strftime('%b , %Y') for i in range(6)][::-1]
    next_six_months = [(current_date + relativedelta(months=i)).strftime('%b , %Y') for i in range(1, 7)]
    all_months = last_six_months + next_six_months
    return [str(date) for date in all_months]

# Load categories and months using memoization
all_months_cached = get_all_months()


def update_session_state(key, value):
    if st.session_state.get(key) != value:
        st.session_state[key] = value


def main():

    with st.sidebar:
        selected = option_menu(menu_title=side_bar['menu_title'],
                               options=side_bar['options'],
                               icons=side_bar['icons'])



########################################################################################################################
############################################  EXPENSES DASHBOARD  ######################################################
########################################################################################################################
#Todo:
# Make sure all the charts work
# Add the chart for specific category over time
# Add the % for the amounts in the charts
    if selected == 'Home':
        st.write(home_page_title, unsafe_allow_html=True, color="white")

    if selected == 'Expenses Dashboard':
        st.write(main_dashboard_title, unsafe_allow_html=True, color="white")
        st.write(space_markdown, unsafe_allow_html=True)
        st.write(general_expenses_graph_title, unsafe_allow_html=True)

        months = st.slider('Choose the # of months back', min_value=1, max_value=24, value=12, step=1)
        monthly_expenses = load_monthly_expenses()
        filtered_data = filter_dates(monthly_expenses, months)

        general_monthly_expenses_chart(filtered_data)
        st.write(space_markdown, unsafe_allow_html=True)
        breakdown(monthly_expenses)

########################################################################################################################
############################################  INSERT EXPENSES  #########################################################
########################################################################################################################

    if selected == 'Insert Expenses':
        tab1, tab2, tab3 = st.tabs(TABS)

###################################################  TAB 1  ############################################################

        with tab1:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown('Insert expenses', unsafe_allow_html=True)
                added_rows = insert_monthly_expenses_form(categories_cached, all_months_cached, data_class, formatted_date)

            with col2:
                for i in range(6):
                    st.write(space_markdown, unsafe_allow_html=True)

                if len(st.session_state.added_rows)>=1:
                    st.write('Added expenses', unsafe_allow_html=True)
                    st.dataframe(st.session_state.added_rows)

                    deisgn_buttons.delete_last_row()
                    delete_last_button = st.button("Delete Last Row", key="delete_button", use_container_width=True)
                    if delete_last_button:
                        data_class.delete_row(table_name=data_class.monthly_expenses_table, conditions=None, last=True)
                        st.experimental_rerun()
                        st.write(f'deleted {st.session_state.recurring_last_row}', unsafe_allow_html=True)

            with col2:
                pass
                # if insert is not None:
                #     st.markdown(insert)


###################################################  TAB 2  ############################################################
        with tab2:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                recurring_expenses = load_recurring_expenses()
                month_for_recurrent = st.selectbox("Month", [str(date) for date in all_months_cached[1:]], 3)
                recurring_expenses['month'] = np.array([month_for_recurrent for i in range(recurring_expenses.shape[0])])
                recurring_expenses['date_updated'] = formatted_date

            st.dataframe(recurring_expenses)

            add_button = st.button('Insert recurring expenses', use_container_width=True)
            if add_button:
                data_class.insert_recurring_expenses(recurring_expenses)

            st.write(space_markdown, unsafe_allow_html=True)
            st.write(space_markdown, unsafe_allow_html=True)
            st.write(adding_recurring_expense, unsafe_allow_html=True)
            st.write(space_markdown, unsafe_allow_html=True)

            #TODO: add the ability to add recurring expenses
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                Main_Category = st.selectbox("Category", [cat for cat in categories_cached.keys()], 0)
            with col2:
                Sub_Category = st.selectbox("Sub Category", categories_cached[Main_Category], 0)
            with col3:
                avoidable = st.selectbox("Avoidable", [True, False], 0)
            with col4:
                Amount = st.text_input("Amount:", "")

            new_row_data = {
                'Category': Main_Category,
                'Sub Category': Sub_Category,
                'Amount': Amount,
                'Avoidable': avoidable
            }
###################################################  TAB 3  ############################################################
        with tab3:
            file = csv_uploader()
            if file is not None:
                df = process_credit_card_sheet(file)
                st.dataframe(df)


if __name__ == '__main__':
    main()
