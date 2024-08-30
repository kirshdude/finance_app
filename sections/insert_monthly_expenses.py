import streamlit as st
import design.buttons as design_buttons
def insert_monthly_expenses(categories_cached, all_months_cached, data_class, formatted_date):
    # Dropdown for Category
    selected_category = st.selectbox('Category:',list(categories_cached.keys()),index=0)

    # Now create the form for data entry and submission
    with st.form(key='insert_form'):
        # Dropdown for Month
        Month = st.selectbox("Month", all_months_cached, index=4)
        # Dropdown for Sub-category
        selected_sub_category = st.selectbox('Sub category:',categories_cached[selected_category],index=0)
        # Dropdown for Avoidable
        avoidable = st.selectbox("Avoidable", [True, False], index=0)
        # Text input for Amount
        Amount = st.text_input("Amount", "")

        design_buttons.save()
        # Save button logic
        save_button = st.form_submit_button("Save", use_container_width=True)
        if save_button:
            values = {
                'month': Month,
                'category': selected_category,
                'sub_category': selected_sub_category,
                'amount': int(Amount),
                'is_avoidable': avoidable,
                'date_updated': formatted_date,
                'expense_id': max(0,st.session_state.monthly_last_row) + 1
            }
            result = data_class.insert_data(data_class.monthly_expenses_table_name, values)
            st.success(result)
            return values