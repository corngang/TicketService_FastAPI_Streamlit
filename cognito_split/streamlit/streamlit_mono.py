import streamlit as st
import authenticate as authenticate


pg = st.navigation([
    st.Page("streamlit_main.py", title="Main"),
    st.Page("streamlit_reserve.py", title="Reservation")], position="hidden")


pg.run()

# print(st.session_state.logged_in)
