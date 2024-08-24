import streamlit as st
# Styling for Save button
def save():
    st.markdown("""
    <style>
    div.stButton > button:first-child {
          background-color: rgb(108, 133, 245);
          height:3em;
          width:50%;
          color:white;
          float: left;
    }
    </style>""", unsafe_allow_html=True)

def delete_last_row():
    st.markdown("""
        <style>
        div.stButton > button:second-child {
              background-color: red;
              height:3em;
              width:50%;
              color:white;
              float: left;
        }
        </style>""", unsafe_allow_html=True)

