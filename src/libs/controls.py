import sys
from pathlib import Path
sys.path.append('/app/src')

from libs.db import Database
from schema import *

def get_controls_by_component_type_old(component_type_id: str):
    db = Database()
    session = db.get_session()
    print (f"Getting control conditions for component type {component_type_id}")
    control_conditions = session.query(ControlCondition).filter(
        ControlCondition.ob_type == 'component_type',
        ControlCondition.ob_key == 'name',
        ControlCondition.ob_value == component_type_id
    ).all()
    return control_conditions

def get_controls_by_component_type(component_type_id: str):
    print (f"Getting control conditions for component type {component_type_id}")
    db = Database()
    session = db.get_session()
        # Get control rules that use these conditions
    control_rules = session.query(ControlRule)\
        .join(ControlRuleCondition)\
        .join(ControlCondition)\
        .filter(
            ControlCondition.ob_type == 'component_type',
            ControlCondition.ob_key == 'id',
            ControlCondition.ob_value == component_type_id
        ).distinct().all()
    print (f"Found {len(control_rules)} control rules")
    # Get all controls associated with these control rules
    controls = []
    for rule in control_rules:
        rule_controls = session.query(Control)\
            .join(ControlRuleControl)\
            .filter(ControlRuleControl.control_rule_id == rule.id)\
            .all()
        controls.extend(rule_controls)
    print (f"Found {len(controls)} controls")
    return controls

def get_component_controls(component_id: str):
    db = Database()
    session = db.get_session()
    component = session.query(Component).filter(Component.id == component_id).first()
    controls = get_controls_by_component_type(component.component_type_id)
    return controls

def update_component_control_status(component_id: str, control_id: str, is_enforced: bool, details: str):
    db = Database()
    session = db.get_session()
    component = session.query(Component).filter(Component.id == component_id).first()
    control = session.query(Control).filter(Control.id == control_id).first()
    component.control_values.append(ComponentControlValue(control=control, is_enforced=is_enforced, details=details))
    session.commit()

def get_control_value(component_id: str, control_id: str):
    print (f"Getting control value for component {component_id} and control {control_id}")
    db = Database()
    session = db.get_session()
    try: 
        control_value = session.query(ComponentControlValue).first()
        if not control_value:
            print ("No control value found")
        else:
            return control_value
    except Exception as e:
        print (f"Error getting control value: {e}")
    
    

def main():
    print ("Get list of controls")
    db = Database()
    session = db.get_session()
    tm_id = 'customer_call_recordings'
    tm = session.query(ThreatModel).filter(ThreatModel.id == tm_id).first()
    tm_components = session.query(ThreatModelComponent).filter(ThreatModelComponent.threat_model_id == tm_id).all()

    for tm_component in tm_components:
        print (tm_component.component_id)
        component = session.query(Component).filter(Component.id == tm_component.component_id).first()
      
        control_rules, controls = get_controls_by_component_type(component.component_type_id)
        print (controls)
        for control in controls:
            print (control.name)
    



if __name__ == '__main__':
    main()