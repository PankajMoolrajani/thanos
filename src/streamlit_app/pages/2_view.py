import sys
from pathlib import Path
import streamlit as st

sys.path.append('/app/src')

from libs.db import Database
from libs.controls import get_component_controls, get_control_value
from schema import ThreatModel

st.set_page_config(page_title="Threat Model", layout="wide")

# Get threat model ID from URL parameters
tm_id = st.query_params.get("id")

if not tm_id:
    st.error("No threat model ID provided")
    st.stop()

st.title(f"Threat Model ID: {tm_id}")

# Create two columns with 30-70 split
col1, col2 = st.columns([30, 70])

# Left sidebar (30%) - Component List
with col1:
    st.header("Components")
    
    # Get threat model from database
    db = Database()
    session = db.get_session()
    threat_model = session.query(ThreatModel).filter(ThreatModel.id == tm_id).first()
    components = [tmc.component for tmc in threat_model.threat_model_components]

    # Create clickable links for each component
    for component in components:
        if st.button(component.name, key=f"component_btn_{component.id}"):
            st.session_state.selected_component_id = component.id

# Main content area (70%) - Component Details  
with col2:
    st.header("Component Details")
    print(st.session_state)
    st.write(f"Selected component: {st.session_state.selected_component_id}")
    controls = get_component_controls(st.session_state.selected_component_id)
    for control in controls:
        st.write(control.name)
        st.write(control.id)
        component_control_value = get_control_value(st.session_state.selected_component_id, control.id)
        # Create a form for each control
        with st.form(key=f"control_{control.id}_{component.id}"):
            st.write("---")
            is_enforced = st.checkbox("Is this control enforced?", key=f"enforced_{control.id}_{component.id}", value=component_control_value.is_enforced)
            details = st.text_area("Implementation details:", key=f"details_{control.id}_{component.id}", value=component_control_value.details)
            
            if st.form_submit_button("Update Control Status"):
                from libs.controls import update_component_control_status
                update_component_control_status(
                    component_id=st.session_state.selected_component_id,
                    control_id=control.id, 
                    is_enforced=is_enforced,
                    details=details
                )
                st.success("Control status updated successfully!")


# Get threat model from database
db = Database()
session = db.get_session()
threat_model = session.query(ThreatModel).filter(ThreatModel.id == tm_id).first()
components = [tmc.component for tmc in threat_model.threat_model_components]
for component in components:
    st.write(component.name)
    controls = get_component_controls(component.id)
    for control in controls:
        st.write(control.name)
        st.write(control.id)
        component_control_value = get_control_value(component.id, control.id)
        # Create a form for each control
        with st.form(key=f"control_{control.id}_{component.id}"):
            st.write("---")
            is_enforced = st.checkbox("Is this control enforced?", key=f"enforced_{control.id}_{component.id}", value=component_control_value.is_enforced)
            details = st.text_area("Implementation details:", key=f"details_{control.id}_{component.id}", value=component_control_value.details)
            
            if st.form_submit_button("Update Control Status"):
                from libs.controls import update_component_control_status
                update_component_control_status(
                    component_id=component.id,
                    control_id=control.id, 
                    is_enforced=is_enforced,
                    details=details
                )
                st.success("Control status updated successfully!")

if not threat_model:
    st.error(f"Threat model with ID {tm_id} not found")
    st.stop()


