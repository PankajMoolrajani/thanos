import sys
from pathlib import Path
sys.path.append('/app/src')

from libs.db import Database
from schema import ThreatModel, Control, Component, ComponentType, ThreatModelComponent, ControlCondition

def get_control_conditions_by_component_type(component_type_id: str):
    db = Database()
    session = db.get_session()
    print (f"Getting control conditions for component type {component_type_id}")
    control_conditions = session.query(ControlCondition).filter(
        ControlCondition.ob_type == 'component_type',
        ControlCondition.ob_key == 'name',
        ControlCondition.ob_value == component_type_id
    ).all()
    return control_conditions

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
        print (component.name)
      
        control_conditions = get_control_conditions_by_component_type(component.component_type_id)
        print (control_conditions)
    



if __name__ == '__main__':
    main()