import streamlit as st
from streamlit_option_menu import option_menu
from person_info import person_page
from subject_rank import ranking_page
from landing_analyze import analyze_page

if __name__ == '__main__':
    st.set_page_config(layout='wide')
    st.title('DSS Final Project')
    # Using "with" notation
    with st.sidebar:
        selected = option_menu("分類",
                               ["個人資料", "各科級距", "落點分析"],
                               icons=["person-vcard", "sort-down", "bezier"],
                               menu_icon="funnel")
    
    if selected == '個人資料':
        person_page()
    
    if selected == '各科級距':
        ranking_page()
    
    if selected == '落點分析':
        analyze_page()
