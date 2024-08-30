from design.headers import space_markdown
import streamlit as st

SIDE_BAR = {'menu_title': 'G&E Finances',
            'options': ['Home','Expenses Dashboard','Insert Expenses', 'Balance sheet', 'Pensions & Insurances'],
            'icons': ['house','bar-chart','database', 'database', 'file-earmark-person']
            }


INSERT_EXP_TABS = ["📥 Manual Insert", "⬆️ Upload from CVS", "♻️ Manage Entries"]

MANUAL_INSERT_TABS = ["☕️ Dynamic expenses", "🔄 Recurring expenses"]

def create_blank_line(num_of_lines):
    for line in range(num_of_lines):
        st.write(space_markdown, unsafe_allow_html=True)
