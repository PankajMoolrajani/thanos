from schema import init_db, ThreatModel, Component
from libs.db import db

# create required tables in the db if not created
init_db()

def select_operation():
    print("Welcome to Threat Model Manager!")
    print("\nPlease select an option:")
    print("1. Create new threat model")
    print("2. Update existing threat model")
    
    choice = input("\nEnter your choice (1-2): ")

    if choice == "1":
        return "create_new_threat_model"
    elif choice == "2":
        return "update_existing_threat_model"
    else:
        return

def create_threat_model():
    print("\nCreating new threat model...")
        
    # Get threat model details from user
    tm_id = input("Enter threat model ID: ")
    tm_name = input("Enter threat model name: ")
    tm_desc = input("Enter threat model description: ")
    
    def create_threat_model(session):
        new_tm = ThreatModel(
            id=tm_id,
            name=tm_name,
            description=tm_desc
        )
        session.add(new_tm)
        # Remove commit here since execute_in_session handles it
        return new_tm.id # Return just the ID instead of the model instance
        
    result = db.execute_in_session(create_threat_model)
    if result:
        print("\nThreat model created successfully!")
        print(f"Threat Model ID: {result}")
    else:
        print("\nError creating threat model")
    
    return result

def select_add_component_op():
    print("\nWould you like to:")
    print("1. Add new component")
    print("2. Add existing component to threat model")
    
    choice = input("\nEnter your choice (1-2): ")

    if choice == "1":
        return "add_new_component"
    elif choice == "2":
        return "add_existing_component"
    else:
        return None

def add_new_component():
    print("\nAdding new component...")
    
    # Get component details from user
    comp_id = input("Enter component ID: ")
    comp_name = input("Enter component name: ")
    comp_type_id = input("Enter component type ID: ")
    
    def create_component(session):
        new_component = Component(
            id=comp_id,
            name=comp_name,
            component_type_id=comp_type_id
        )
        session.add(new_component)
        return new_component.id
        
    result = db.execute_in_session(create_component)
    if result:
        print("\nComponent created successfully!")
        print(f"Component ID: {result}")
    else:
        print("\nError creating component")
        
    return result

def main():
    operation = select_operation()
    if operation == "create_new_threat_model":
        threat_model_id = create_threat_model()
    elif operation == "update_existing_threat_model":
        print("\nUpdating existing threat model...")
    else:
        print("\nInvalid choice! Please select 1 or 2")

    add_component_op = select_add_component_op()
    if add_component_op == "add_new_component":
        component_id  = add_new_component()
    elif add_component_op == "add_existing_component":
        pass
        
if __name__ == '__main__':
    main()