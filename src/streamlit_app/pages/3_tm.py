import streamlit as st
import sys
from pathlib import Path
sys.path.append('/app/src')

from libs.db import Database
from schema import ThreatModel

st.set_page_config(page_title="Threat Model")

# Get threat model ID from URL parameters
tm_id = st.query_params.get("tm")

if not tm_id:
    st.error("No threat model ID provided")
    st.stop()

# Get threat model from database
db = Database()
session = db.get_session()
threat_model = session.query(ThreatModel).filter(ThreatModel.id == tm_id).first()

if not threat_model:
    st.error(f"Threat model with ID {tm_id} not found")
    st.stop()

st.title(f"🔒 {threat_model.name}")

