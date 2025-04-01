import streamlit as st
import sys
from pathlib import Path
sys.path.append('/app/src')

from libs.db import Database
from schema import ThreatModel

st.set_page_config(page_title="Threat Models")

st.title("List Threat Models")


db = Database()
session = db.get_session()
# Query all threat models from the database
threat_models = session.query(ThreatModel).all()

# Display threat models in a table
if threat_models:
    for tm in threat_models:
        col1, col2 = st.columns([4,1])
        with col1:
            st.write(f"**{tm.name}**")
        with col2:
            st.link_button("View", f"view?id={tm.id}", use_container_width=True)
else:
    st.info("No threat models found. Create one to get started!")

