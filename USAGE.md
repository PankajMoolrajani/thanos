# Thanos Usage Guide

This guide provides detailed instructions on how to use Thanos for threat modeling.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Understanding the Data Model](#understanding-the-data-model)
3. [Creating a Threat Model](#creating-a-threat-model)
4. [Working with the Web Interface](#working-with-the-web-interface)
5. [Advanced Usage](#advanced-usage)

## Getting Started

### Initial Setup

After installing Thanos, you need to initialize the database with baseline data:

```bash
cd src

# Load default component types and controls
python load_data.py -f data/default.yaml

# Load comprehensive control rules and STRIDE threats
python load_data.py -f data/init/controls.yaml
```

This will populate your database with:
- Component types (EC2 instances, S3 buckets, SaaS applications, etc.)
- Security control definitions
- Control rules and conditions
- STRIDE threat categories
- Common threats for each category

### Starting the Application

**Local Installation:**
```bash
cd src
streamlit run streamlit_app/app.py
```

**Docker Installation:**
```bash
docker-compose up -d
# Access the shell if needed
docker exec -it thanos bash
```

Access the web interface at `http://localhost:8501`

## Understanding the Data Model

### Component Types

Component types define categories of infrastructure and application resources. Built-in types include:

- **ec2_instance**: AWS EC2 compute instances
- **s3_bucket**: AWS S3 storage buckets
- **saas**: Third-party SaaS applications
- **webapp**: Custom web applications
- **3rd_party_api**: External APIs
- **generic_api_service**: Generic API services
- **generic_database**: Database systems
- **generic_secret_store**: Secret management systems

Each component type has associated security controls that should be considered.

### Components

Components are specific instances in your architecture:
- Example: "Customer Database" (type: generic_database)
- Example: "User Authentication API" (type: generic_api_service)
- Example: "Salesforce" (type: saas)

### Controls

Security controls are specific requirements or best practices. Examples:

- **S3 Bucket Encryption**: Is the S3 bucket encrypted?
- **Data Localization**: Is data stored in specific geographic regions?
- **Access Logging**: Are access logs enabled and monitored?
- **Audit Logging**: Are audit logs available for compliance?

### Control Rules and Conditions

Control rules determine which controls apply to which components based on conditions:

```
IF component_type == "generic_api_service" AND is_publicly_accessible == true
THEN require controls: ["authentication", "rate_limiting", "input_validation"]
```

### STRIDE Threat Categories

The platform organizes threats using STRIDE:

1. **Spoofing**: Impersonation attacks
   - Credential theft
   - Session hijacking
   - Service identity spoofing

2. **Tampering**: Data manipulation
   - Request parameter tampering
   - Data tampering at rest
   - Man-in-the-middle attacks

3. **Repudiation**: Lack of accountability
   - Insufficient logging
   - Log tampering
   - Missing audit trails

4. **Information Disclosure**: Unauthorized data access
   - Sensitive data exposure
   - Unencrypted communications
   - Excessive permissions

5. **Denial of Service**: Availability attacks
   - Resource exhaustion
   - Service flooding
   - Amplification attacks

6. **Elevation of Privilege**: Unauthorized access
   - Privilege escalation
   - Missing authorization checks
   - Insecure default configurations

## Creating a Threat Model

### Method 1: Using the Command-Line Interface

1. **Start the CLI tool:**
```bash
cd src
python main.py
```

2. **Create a new threat model:**
```
Select option: 1 (Create new threat model)
Enter threat model ID: my_system_tm
Enter threat model name: My System
Enter threat model description: Threat model for my application
```

3. **Add components:**
```
Select option: 1 (Add new component)
Enter component ID: auth_api
Enter component name: Authentication API
Enter component type ID: generic_api_service
```

4. **Repeat** to add all components in your system

### Method 2: Using YAML Configuration

Create a YAML file describing your threat model:

```yaml
# my_system.tm.yaml
nodes:
  - kind: threat_model
    id: my_system_tm
    name: My System
    description: Threat model for my e-commerce application
    
  - kind: component
    id: web_frontend
    name: Web Frontend
    component_type_id: webapp
    
  - kind: component
    id: api_gateway
    name: API Gateway
    component_type_id: generic_api_service
    
  - kind: component
    id: user_database
    name: User Database
    component_type_id: generic_database
    
  - kind: component
    id: payment_processor
    name: Stripe Payment API
    component_type_id: 3rd_party_api
```

Load it into the database:
```bash
python load_data.py -f my_system.tm.yaml
```

### Method 3: Using the Web Interface

1. Navigate to the "Create Threat Model" page
2. Follow the wizard to:
   - Select or define your system
   - Identify assets and components
   - Define threats for each component
   - Determine security controls
   - Generate a report

## Working with the Web Interface

### Home Page

The home page provides navigation to:
- List all threat models
- Create new threat models
- View and edit existing threat models

### List Threat Models Page

- View all threat models in your database
- Click "View" to access a specific threat model
- See basic information (name, description)

### View Threat Model Page

The threat model view shows:

**Left Panel (30% width):**
- List of all components in the threat model
- Click any component to view its details

**Right Panel (70% width):**
- Component details
- Security controls applicable to the selected component
- For each control:
  - Control name and description
  - Checkbox: "Is this control enforced?"
  - Text area: "Implementation details"
  - Submit button to save changes

### Documenting Control Implementation

For each component in your threat model:

1. **Select the component** from the left panel
2. **Review applicable controls** - these are automatically determined based on the component type
3. **For each control:**
   - Check the box if the control is currently enforced
   - Document how it's implemented in the details field
   
Example:
```
Control: Access Logging
☑ Is this control enforced?
Details: CloudWatch logs enabled with 90-day retention. 
         Logs are sent to our SIEM for analysis.
         Alert rules configured for suspicious access patterns.
```

4. **Click "Update Control Status"** to save

### Best Practices for Documentation

**Be Specific:**
```
❌ Bad: "Encryption is enabled"
✓ Good: "TLS 1.3 for data in transit. AES-256 encryption at rest using AWS KMS with customer-managed keys rotated every 90 days."
```

**Include Evidence:**
```
❌ Bad: "We have logging"
✓ Good: "Application logs to CloudWatch (log group: /app/prod). Retention: 365 days. Monitored via DataDog with alerts for error rates >1%."
```

**Document Compensating Controls:**
```
Control: Data Localization
☐ Is this control enforced?
Details: Data is stored in US-EAST-1 (not EU-specific). 
         However, we maintain GDPR compliance through:
         - Data processing agreements with AWS
         - Strong encryption (meets EU standards)
         - Right to deletion implemented
         - Data access logging
```

## Advanced Usage

### Custom Component Types

Add your own component types by creating a YAML file:

```yaml
nodes:
  - kind: component_type
    id: kubernetes_pod
    name: Kubernetes Pod
    category: container
    provider: kubernetes
```

Load it:
```bash
python load_data.py -f my_component_types.yaml
```

### Custom Controls

Define organization-specific controls:

```yaml
nodes:
  - kind: control
    id: soc2_access_review
    name: SOC2 Access Review
    question: Are access rights reviewed quarterly per SOC2 requirements?
```

### Creating Control Rules

Define when controls should apply:

```yaml
nodes:
  - kind: control_condition
    id: publicly_accessible_api
    name: Publicly Accessible API
    ob_type: component_type
    ob_key: id
    ob_value: generic_api_service
    
  - kind: control_rule
    id: public_api_security
    name: Public API Security Requirements
    
  # Link conditions to rules and rules to controls
  # (via control_rule_conditions and control_rule_controls tables)
```

### Exporting Threat Models

Currently, threat models are stored in SQLite database. To export:

```bash
# Backup entire database
cp src/thanos.db backups/thanos_$(date +%Y%m%d).db

# Export specific tables
sqlite3 src/thanos.db ".dump threat_models" > threat_models_backup.sql
```

### Programmatic Access

Access the data model programmatically:

```python
from libs.db import Database
from schema import ThreatModel, Component

db = Database()
session = db.get_session()

# Query threat models
threat_models = session.query(ThreatModel).all()
for tm in threat_models:
    print(f"Threat Model: {tm.name}")
    for tmc in tm.threat_model_components:
        print(f"  - Component: {tmc.component.name}")

# Get components of specific type
from schema import Component, ComponentType
api_type = session.query(ComponentType).filter(
    ComponentType.id == 'generic_api_service'
).first()
apis = session.query(Component).filter(
    Component.component_type_id == api_type.id
).all()
```

### Bulk Operations

Process multiple threat models:

```python
import os
import glob

# Load all threat model YAML files from a directory
yaml_files = glob.glob('threat_models/*.tm.yaml')
for yaml_file in yaml_files:
    os.system(f'python load_data.py -f {yaml_file}')
```

## Tips and Tricks

1. **Start Small**: Begin with a single critical system or workflow
2. **Iterate**: Create an initial threat model, then refine over time
3. **Collaborate**: Share the web interface link with your team for collaborative documentation
4. **Regular Reviews**: Update control implementations during sprint planning or quarterly reviews
5. **Use Templates**: Copy and modify existing threat model YAML files for similar systems
6. **Version Control**: Store your threat model YAML files in Git alongside your application code

## Troubleshooting

### Database Locked Error
If you see "database is locked":
- Close other connections to the database
- Only one process should write at a time
- Use the web interface OR CLI, not both simultaneously

### Controls Not Appearing
If controls don't show for a component:
- Verify the component type is correct
- Check that control rules exist for that component type
- Review `src/data/init/controls.yaml` for rule definitions

### Changes Not Saving
- Ensure you click "Update Control Status" after making changes
- Check for error messages in the Streamlit interface
- View logs in the terminal where Streamlit is running

## Next Steps

- Explore [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute improvements
- Check the [GitHub repository](https://github.com/PankajMoolrajani/thanos) for updates
