import streamlit as st
import pandas as pd
from supabase import create_client
import random
from datetime import datetime

# 1. THE TOOLS
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 2. THE MEMORY
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steward_name' not in st.session_state:
    st.session_state.steward_name = ""
if 'steward_role' not in st.session_state:
    st.session_state.steward_role = ""

# 3. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    
    entrance_quotes = [
        "*O God, come to my assistance; O Lord, make haste to help me.*",
        "*Direct my steps according to Your word, and let no iniquity have dominion over me.*"
    ]
    st.info(random.choice(entrance_quotes))
    
    name_input = st.text_input("Identify yourself, Steward:")
    pin_input = st.text_input("Steward's PIN:", type="password")
    
    if st.button("Begin the Vigil"):
        user_query = supabase.table("users").select("*").eq("username", name_input).eq("pin", pin_input).execute()

        if len(user_query.data) > 0:
