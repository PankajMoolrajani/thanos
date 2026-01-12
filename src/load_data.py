import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from schema import (ComponentType, ControlsCollection, Control, ThreatModel, 
                    ThreatCategory, Threat, Component, ThreatModelComponent, init_db)
import argparse

def load_default_data(yaml_file_path):
    # Initialize DB
    init_db()
    engine = create_engine('sqlite:///thanos.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load YAML data
    with open(yaml_file_path, 'r') as f:
        data = yaml.safe_load(f)

    # Process each entry
    for item in data['nodes']:
        print(item)
        try:
            if item['kind'] == 'component_type':
                record = ComponentType(
                    id=item['id'],
                    name=item['name'],
                    category=item['category'],
                    provider=item['provider']
                )
                res = session.add(record)
                print(res)
                
            elif item['kind'] == 'controls_collection':
                record = ControlsCollection(
                    id=item['id'],
                    name=item['name'],
                    category=item['category'],
                    provider=item['provider']
                )
                session.add(record)
                
            elif item['kind'] == 'control':
                record = Control(
                    id=item['id'],
                    name=item['name'],
                    question=item.get('question', None)
                )
                session.add(record)
            
            elif item['kind'] == 'component':
                record = Component(
                    id=item['id'],
                    name=item['name'],
                    component_type_id=item['component_type_id']
                )
                session.add(record)
            
            elif item['kind'] == 'threat_model':
                record = ThreatModel(
                    id=item['id'],
                    name=item['name'],
                    description=item.get('description', '')
                )
                session.add(record)
            
            elif item['kind'] == 'threat_category':
                record = ThreatCategory(
                    id=item['id'],
                    name=item['name'],
                    description=item.get('description', '')
                )
                session.add(record)
            
            elif item['kind'] == 'threat':
                record = Threat(
                    id=item['id'],
                    name=item['name'],
                    description=item.get('description', ''),
                    threat_category_id=item.get('threat_category_id', None)
                )
                session.add(record)

            # Commit after each successful record
            session.commit()

        except IntegrityError:
            # Skip duplicate records
            session.rollback()
            continue
    
    # Second pass: link components to threat models
    # This must be done after all nodes are created
    for item in data['nodes']:
        if item['kind'] == 'component':
            try:
                # Find the first threat_model in the file (convention)
                threat_model_id = None
                for node in data['nodes']:
                    if node['kind'] == 'threat_model':
                        threat_model_id = node['id']
                        break
                
                if threat_model_id:
                    # Check if link already exists
                    existing = session.query(ThreatModelComponent).filter(
                        ThreatModelComponent.threat_model_id == threat_model_id,
                        ThreatModelComponent.component_id == item['id']
                    ).first()
                    
                    if not existing:
                        link = ThreatModelComponent(
                            threat_model_id=threat_model_id,
                            component_id=item['id']
                        )
                        session.add(link)
                        session.commit()
            except IntegrityError:
                session.rollback()
                continue

    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load data from YAML file')
    parser.add_argument('-f', '--file', required=True, help='Path to YAML file')
    args = parser.parse_args()
    load_default_data(args.file)
