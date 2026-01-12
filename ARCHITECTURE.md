# Thanos Architecture

This document describes the technical architecture of the Thanos threat modeling platform.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Data Model](#data-model)
4. [Application Layers](#application-layers)
5. [Key Components](#key-components)
6. [Data Flow](#data-flow)
7. [Deployment Architecture](#deployment-architecture)

## Overview

Thanos is built as a Python web application using modern frameworks and follows a layered architecture pattern. The system is designed to be:

- **Modular**: Clear separation between data, business logic, and presentation
- **Extensible**: Easy to add new component types, controls, and threat categories
- **Portable**: Runs locally or in containers with minimal configuration
- **Data-Driven**: Configuration and initialization through YAML files

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│                  (Streamlit Web UI)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │   Home   │  │   List   │  │   View   │             │
│  │   Page   │  │ Threat   │  │ Threat   │             │
│  │          │  │  Models  │  │  Model   │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                   Business Logic Layer                   │
│  ┌────────────────────┐  ┌─────────────────────┐       │
│  │  Control Rules     │  │  Threat Assessment  │       │
│  │  Engine            │  │  Logic              │       │
│  │  (libs/controls.py)│  │                     │       │
│  └────────────────────┘  └─────────────────────┘       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    Data Access Layer                     │
│  ┌──────────────────────────────────────────┐           │
│  │         SQLAlchemy ORM Models            │           │
│  │              (schema.py)                 │           │
│  │  ┌────────────┐  ┌─────────────┐        │           │
│  │  │ Database   │  │ Session     │        │           │
│  │  │ Connection │  │ Management  │        │           │
│  │  │ (libs/db.py)  │            │        │           │
│  │  └────────────┘  └─────────────┘        │           │
│  └──────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    Persistence Layer                     │
│                  SQLite Database                         │
│                   (thanos.db)                            │
└─────────────────────────────────────────────────────────┘
```

## Data Model

### Entity-Relationship Diagram

```
ComponentType ──┐
                │
                ├── Component ──┐
                                │
                                ├── ThreatModelComponent ── ThreatModel
                                │
                                └── ComponentControlValue ── Control
                                                              │
                                                              ├── ControlsCollectionsControls ── ControlsCollection
                                                              │
                                                              └── ControlRuleControl ── ControlRule
                                                                                         │
                                                                                         └── ControlRuleCondition ── ControlCondition

ThreatCategory ── Threat ── ThreatControlMitigation ── Control
```

### Core Entities

#### Component Type
Defines categories of infrastructure/application resources.

```python
class ComponentType:
    id: String (Primary Key)
    name: String
    category: String
    provider: String
    components: List[Component]
```

**Examples**: ec2_instance, s3_bucket, generic_api_service, saas

#### Component
Specific instances in the architecture being modeled.

```python
class Component:
    id: String (Primary Key)
    name: String
    component_type_id: ForeignKey(ComponentType)
    component_type: ComponentType
    threat_model_components: List[ThreatModelComponent]
    control_values: List[ComponentControlValue]
```

**Examples**: "Authentication API", "Customer Database", "Salesforce"

#### Threat Model
Container for a related set of components representing a system.

```python
class ThreatModel:
    id: String (Primary Key)
    name: String
    description: String
    threat_model_components: List[ThreatModelComponent]
```

**Examples**: "E-commerce Platform", "Payment Processing Workflow"

#### Control
Security control or compliance requirement.

```python
class Control:
    id: String (Primary Key)
    name: String
    controls_collections_controls: List[ControlsCollectionsControls]
    rule_controls: List[ControlRuleControl]
    control_values: List[ComponentControlValue]
```

**Examples**: "Access Logging", "Data Encryption", "GDPR Right to be Forgotten"

#### Control Rule & Condition
Logic for determining which controls apply to which components.

```python
class ControlRule:
    id: String (Primary Key)
    name: String
    rule_conditions: List[ControlRuleCondition]
    rule_controls: List[ControlRuleControl]

class ControlCondition:
    id: String (Primary Key)
    name: String
    ob_type: String  # e.g., "component_type"
    ob_key: String   # e.g., "id"
    ob_value: String # e.g., "generic_api_service"
    rule_conditions: List[ControlRuleCondition]
```

**Example Rule**: 
- Condition: component_type == "generic_api_service"
- Required Controls: ["authentication", "rate_limiting", "input_validation"]

#### Component Control Value
Tracks implementation status of controls for components.

```python
class ComponentControlValue:
    id: String (Primary Key)
    component_id: ForeignKey(Component)
    control_id: ForeignKey(Control)
    is_enforced: Boolean
    details: String
    component: Component
    control: Control
```

**Example**:
- Component: "User API"
- Control: "TLS Encryption"
- is_enforced: True
- details: "TLS 1.3 enforced via AWS ALB with strict cipher suites"

#### Threat Category & Threat
STRIDE-based threat classification.

```python
class ThreatCategory:
    id: String (Primary Key)
    name: String
    description: String
    threats: List[Threat]

class Threat:
    id: String (Primary Key)
    name: String
    description: String
    threat_category_id: ForeignKey(ThreatCategory)
    threat_category: ThreatCategory
    control_mitigations: List[ThreatControlMitigation]
```

**Examples**:
- Category: "Spoofing" → Threats: "Credential Theft", "Session Hijacking"
- Category: "Information Disclosure" → Threats: "Sensitive Data Exposure", "Unencrypted Communications"

## Application Layers

### 1. Presentation Layer (Streamlit)

**Location**: `src/streamlit_app/`

**Purpose**: Web-based user interface for threat modeling

**Key Files**:
- `app.py`: Main application entry point and navigation
- `pages/list.py`: List all threat models
- `pages/1_create.py`: Wizard for creating threat models
- `pages/2_view.py`: View and edit threat model details
- `pages/3_tm.py`: Additional threat model views

**Features**:
- Responsive web interface
- Component selection and detail views
- Control assessment forms
- Real-time updates

### 2. Business Logic Layer

**Location**: `src/libs/`

**Purpose**: Core threat modeling logic and control assessment

**Key Files**:
- `controls.py`: Control rule evaluation and assessment logic
- `db.py`: Database connection and session management

**Key Functions**:

```python
# Get controls applicable to a component based on its type
def get_controls_by_component_type(component_type_id: str) -> List[Control]

# Get controls for a specific component
def get_component_controls(component_id: str) -> List[Control]

# Update control implementation status
def update_component_control_status(
    component_id: str, 
    control_id: str, 
    is_enforced: bool, 
    details: str
)

# Get current control value for a component
def get_control_value(component_id: str, control_id: str) -> ComponentControlValue
```

### 3. Data Access Layer (SQLAlchemy)

**Location**: `src/schema.py`, `src/libs/db.py`

**Purpose**: ORM models and database operations

**Key Components**:
- **ORM Models**: Python classes mapping to database tables
- **Database Connection**: Singleton pattern for connection management
- **Session Management**: Thread-safe database sessions

**Database Class**:
```python
class Database:
    def __init__(self, db_url='sqlite:///thanos.db'):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
```

### 4. Data Initialization Layer

**Location**: `src/load_data.py`, `src/data/`

**Purpose**: Bootstrap and configure the system with baseline data

**Process**:
1. Read YAML configuration files
2. Parse node definitions (component types, controls, threats, etc.)
3. Create ORM objects
4. Persist to database with duplicate handling

**Supported Node Types**:
- `component_type`: Infrastructure/app categories
- `controls_collection`: Grouped controls (e.g., GDPR, Security Best Practices)
- `control`: Individual security controls
- `threat_model`: Threat model containers
- `threat_category`: STRIDE categories
- `threat`: Specific threats
- `component`: Specific component instances

## Key Components

### Control Rules Engine

**Purpose**: Determine which controls apply to which components

**Algorithm**:
1. Given a component, identify its component_type
2. Query ControlConditions matching component_type
3. Find ControlRules using those conditions
4. Retrieve all Controls linked to those rules
5. Return applicable controls

**Example Flow**:
```
Component: "User API" (type: generic_api_service)
    ↓
Condition: component_type.id == "generic_api_service"
    ↓
Rule: "Public API Security Requirements"
    ↓
Controls: ["Authentication", "Rate Limiting", "Input Validation"]
```

### Threat Assessment

**Purpose**: Map threats to components and track mitigations

**Approach**:
1. **Threat Identification**: Each component type has associated threat categories
2. **Control Mapping**: Controls are mapped to threats they mitigate
3. **Gap Analysis**: Identify threats without enforced mitigations
4. **Documentation**: Track mitigation details

### Session Management

**Pattern**: Session-per-request

**Implementation**:
```python
db = Database()
session = db.get_session()
try:
    # Perform database operations
    results = session.query(ThreatModel).all()
    session.commit()
except Exception as e:
    session.rollback()
    raise e
finally:
    session.close()
```

## Data Flow

### Creating a Threat Model

```
User Input (CLI/Web) 
    → Create ThreatModel object
    → Add Components to ThreatModel
    → Link via ThreatModelComponent relationships
    → Persist to Database
```

### Assessing Controls

```
User selects Component
    → Identify ComponentType
    → Query ControlRules matching type
    → Retrieve applicable Controls
    → Display Controls to User
    → User documents implementation
    → Create/Update ComponentControlValue
    → Persist to Database
```

### Loading Data from YAML

```
YAML File
    → Parse with PyYAML
    → Iterate through nodes
    → Determine node kind
    → Create appropriate ORM object
    → Handle IntegrityError (duplicates)
    → Commit to Database
```

## Deployment Architecture

### Local Development

```
Developer Machine
    ├── Python 3.8+ Runtime
    ├── SQLite Database (file-based)
    ├── Streamlit Server (port 8501)
    └── Browser (localhost:8501)
```

### Docker Deployment

```
Docker Host
    └── thanos Container
        ├── Ubuntu Base Image
        ├── Python 3 + pip
        ├── Application Code (/app)
        ├── SQLite Database (/app/src/thanos.db)
        └── Streamlit Server (port 8501 exposed)
```

**Docker Compose Configuration**:
```yaml
services:
  thanos:
    build: .
    volumes:
      - .:/app  # Live code updates
    ports:
      - "8501:8501"
    restart: unless-stopped
```

### Production Considerations

For production deployment, consider:

1. **Database**: Migrate from SQLite to PostgreSQL or MySQL
   ```python
   # In schema.py and db.py
   db_url = 'postgresql://user:pass@host:5432/thanos'
   ```

2. **Authentication**: Add user authentication (Streamlit Auth, OAuth)

3. **Multi-tenancy**: Extend schema to support multiple organizations

4. **Scalability**: 
   - Run multiple Streamlit instances behind a load balancer
   - Use connection pooling for database
   - Consider caching frequently accessed data

5. **Backup**: Automated database backups

6. **Monitoring**: Application and database monitoring

7. **Security**:
   - Use environment variables for sensitive configuration
   - Enable HTTPS/TLS
   - Regular security updates
   - Rate limiting and CSRF protection

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Web UI framework |
| **Backend** | Python 3.8+ | Application logic |
| **ORM** | SQLAlchemy | Database abstraction |
| **Database** | SQLite (dev), PostgreSQL (prod) | Data persistence |
| **Data Format** | YAML | Configuration and initialization |
| **Container** | Docker | Deployment packaging |
| **Orchestration** | Docker Compose | Multi-container management |

## Extensibility Points

### Adding Custom Component Types

1. Create YAML definition:
```yaml
nodes:
  - kind: component_type
    id: azure_function
    name: Azure Function
    category: serverless
    provider: azure
```

2. Load into database:
```bash
python load_data.py -f custom_types.yaml
```

### Adding Custom Controls

1. Define control in YAML:
```yaml
nodes:
  - kind: control
    id: hipaa_encryption
    name: HIPAA Encryption Standard
    question: Is data encrypted per HIPAA requirements?
```

2. Create control rule linking it to component types

### Adding Custom Threats

1. Define in YAML:
```yaml
nodes:
  - kind: threat
    id: supply_chain_attack
    name: Supply Chain Attack
    description: Compromise via third-party dependencies
    threat_category_id: tampering
```

### Extending the UI

Add new Streamlit pages in `src/streamlit_app/pages/`:
- `4_reports.py`: Generate PDF reports
- `5_analytics.py`: Threat analytics dashboard
- `6_integrations.py`: Third-party integrations

## Performance Considerations

1. **Database Queries**: 
   - Use eager loading for relationships: `session.query(ThreatModel).options(joinedload(ThreatModel.threat_model_components))`
   - Index frequently queried columns

2. **Caching**:
   - Use Streamlit's `@st.cache_data` for expensive operations
   - Cache control rules evaluation results

3. **Pagination**:
   - Implement pagination for large threat model lists
   - Limit components displayed per page

## Future Architecture Enhancements

1. **API Layer**: RESTful API for programmatic access
2. **Event Sourcing**: Track all changes to threat models
3. **Real-time Collaboration**: WebSocket-based multi-user editing
4. **Graph Database**: Neo4j for complex relationship queries
5. **Microservices**: Separate control engine, threat assessment, and UI
6. **ML Integration**: AI-powered threat identification and control recommendations

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [STRIDE Threat Modeling](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
