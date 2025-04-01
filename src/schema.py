from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class ComponentType(Base):
    __tablename__ = 'component_types'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    provider = Column(String, nullable=False)

    components = relationship("Component", back_populates="component_type")

class Component(Base):
    __tablename__ = 'components'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    component_type_id = Column(String(36), ForeignKey('component_types.id'))

    component_type = relationship("ComponentType", back_populates="components")
    threat_model_components = relationship("ThreatModelComponent", back_populates="component")

class ControlsCollection(Base):
    __tablename__ = 'controls_collections'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    provider = Column(String, nullable=False)

    controls_collections_controls = relationship("ControlsCollectionsControls", back_populates="collection")

class ControlsCollectionsControls(Base):
    __tablename__ = 'controls_collections_controls'

    collection_id = Column(String(36), ForeignKey('controls_collections.id'), primary_key=True)
    control_id = Column(String(36), ForeignKey('controls.id'), primary_key=True)

    collection = relationship("ControlsCollection", back_populates="controls_collections_controls")
    control = relationship("Control", back_populates="controls_collections_controls")

class Control(Base):
    __tablename__ = 'controls'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

    controls_collections_controls = relationship("ControlsCollectionsControls", back_populates="control")
    rule_controls = relationship("ControlRuleControl", back_populates="control")

class ControlCondition(Base):
    __tablename__ = 'control_conditions'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    ob_type = Column(String, nullable=False)
    ob_key = Column(String, nullable=False)
    ob_value = Column(String, nullable=False)

    rule_conditions = relationship("ControlRuleCondition", back_populates="control_condition")

class ControlRule(Base):
    __tablename__ = 'control_rules'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

    rule_conditions = relationship("ControlRuleCondition", back_populates="control_rule")
    rule_controls = relationship("ControlRuleControl", back_populates="control_rule")

class ControlRuleCondition(Base):
    __tablename__ = 'control_rule_conditions'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    control_rule_id = Column(String(36), ForeignKey('control_rules.id'), nullable=False)
    control_condition_id = Column(String(36), ForeignKey('control_conditions.id'), nullable=False)

    control_rule = relationship("ControlRule", back_populates="rule_conditions")
    control_condition = relationship("ControlCondition", back_populates="rule_conditions")

class ControlRuleControl(Base):
    __tablename__ = 'control_rule_controls'

    control_rule_id = Column(String(36), ForeignKey('control_rules.id'), primary_key=True)
    control_id = Column(String(36), ForeignKey('controls.id'), primary_key=True)

    control_rule = relationship("ControlRule", back_populates="rule_controls")
    control = relationship("Control", back_populates="rule_controls")

class ThreatModel(Base):
    __tablename__ = 'threat_models'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)

    threat_model_components = relationship("ThreatModelComponent", back_populates="threat_model")

class ThreatModelComponent(Base):
    __tablename__ = 'threat_models_components'

    threat_model_id = Column(String(36), ForeignKey('threat_models.id'), primary_key=True)
    component_id = Column(String(36), ForeignKey('components.id'), primary_key=True)

    threat_model = relationship("ThreatModel", back_populates="threat_model_components")
    component = relationship("Component", back_populates="threat_model_components")

def init_db(db_url='sqlite:///thanos.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)