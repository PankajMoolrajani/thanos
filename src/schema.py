from sqlalchemy import create_engine, Column, String, ForeignKey, Boolean
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
    control_values = relationship("ComponentControlValue", back_populates="component")

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
    question = Column(String)

    controls_collections_controls = relationship("ControlsCollectionsControls", back_populates="control")
    rule_controls = relationship("ControlRuleControl", back_populates="control")
    control_values = relationship("ComponentControlValue", back_populates="control")
    threat_mitigations = relationship("ThreatControlMitigation", back_populates="control")

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

class ComponentControlValue(Base):
    __tablename__ = 'component_control_values'

    id = Column(String(36), primary_key=True)
    component_id = Column(String(36), ForeignKey('components.id'), nullable=False)
    control_id = Column(String(36), ForeignKey('controls.id'), nullable=False)
    is_enforced = Column(Boolean, nullable=False, default=False)
    details = Column(String, nullable=False)

    component = relationship("Component", back_populates="control_values")
    control = relationship("Control", back_populates="control_values")

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

class ThreatCategory(Base):
    __tablename__ = 'threat_categories'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)

    threats = relationship("Threat", back_populates="threat_category")

class Threat(Base):
    __tablename__ = 'threats'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)
    threat_category_id = Column(String(36), ForeignKey('threat_categories.id'))

    threat_category = relationship("ThreatCategory", back_populates="threats")
    control_mitigations = relationship("ThreatControlMitigation", back_populates="threat")

class ThreatControlMitigation(Base):
    __tablename__ = 'threat_control_mitigations'

    threat_id = Column(String(36), ForeignKey('threats.id'), primary_key=True)
    control_id = Column(String(36), ForeignKey('controls.id'), primary_key=True)

    threat = relationship("Threat", back_populates="control_mitigations")
    control = relationship("Control", back_populates="threat_mitigations")

def init_db(db_url='sqlite:///thanos.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)