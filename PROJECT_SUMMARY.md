# Project Summary: Thanos Threat Modeling Platform

## What is Thanos?

Thanos is an open-source threat modeling platform designed to help security teams and developers systematically identify and mitigate security risks in their systems. It implements the industry-standard STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) methodology for comprehensive threat analysis.

## Key Features

### 1. Component-Based Architecture Modeling
- Define system components with specific types (web apps, databases, APIs, SaaS services)
- Model relationships between components
- Group components into logical threat models

### 2. STRIDE Threat Framework
Built-in threat categories based on Microsoft's STRIDE methodology:
- **Spoofing**: Identity impersonation and authentication bypass
- **Tampering**: Data or request manipulation
- **Repudiation**: Inability to track or prove actions
- **Information Disclosure**: Unauthorized data access or exposure
- **Denial of Service**: Availability attacks and resource exhaustion
- **Elevation of Privilege**: Unauthorized access escalation

### 3. Security Controls Management
- Pre-configured security controls for common scenarios
- Control rules engine that automatically determines applicable controls
- Support for compliance frameworks (GDPR, Security Best Practices)
- Document control implementation status with detailed notes

### 4. Web-Based Interface
- Modern Streamlit-based UI
- Interactive threat model management
- Real-time control assessment
- Easy navigation between components and controls

### 5. Data-Driven Configuration
- YAML-based data initialization
- Easy to customize and extend
- Import/export capabilities
- Version control friendly

## Use Cases

### Security Teams
- Create and maintain threat models for critical systems
- Track security control implementation across infrastructure
- Generate compliance evidence (GDPR, SOC2, ISO27001)
- Identify security gaps and prioritize remediation

### Development Teams
- Integrate threat modeling into development lifecycle
- Document security considerations for new features
- Collaborate with security on risk assessment
- Track security requirements alongside functional requirements

### Compliance & Audit
- Document security posture for audits
- Demonstrate due diligence in security practices
- Track control implementation evidence
- Generate compliance reports

### Security Consultants
- Provide threat modeling services to clients
- Create reusable threat model templates
- Document security assessments
- Deliver actionable recommendations

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web user interface |
| **Backend** | Python 3.8+ | Application logic |
| **Database** | SQLite (dev), PostgreSQL-ready | Data persistence |
| **ORM** | SQLAlchemy | Database abstraction |
| **Data Format** | YAML | Configuration and initialization |
| **Deployment** | Docker, Docker Compose | Containerization |

## Architecture Highlights

### Layered Design
1. **Presentation Layer**: Streamlit web interface
2. **Business Logic**: Control rules engine, threat assessment
3. **Data Access**: SQLAlchemy ORM models
4. **Persistence**: Relational database

### Extensibility Points
- Custom component types
- Custom security controls
- Custom threat categories
- Custom compliance frameworks
- Pluggable data sources

### Data Model
- **Component Types**: Categories of infrastructure resources
- **Components**: Specific instances in your architecture
- **Threat Models**: Containers for related components
- **Controls**: Security requirements and best practices
- **Control Rules**: Logic for determining applicable controls
- **Threats**: Specific security threats mapped to STRIDE
- **Threat Categories**: STRIDE-based classification

## Getting Started

### Quick Start (< 5 minutes)
```bash
git clone https://github.com/PankajMoolrajani/thanos.git
cd thanos
chmod +x quickstart.sh
./quickstart.sh
```

### What You Get Out of the Box
- Pre-configured component types (AWS, generic services, SaaS)
- STRIDE threat taxonomy with common threats
- GDPR compliance controls
- Security best practices controls
- Example e-commerce threat model
- Ready-to-use web interface

## Example: Creating a Threat Model

### 1. Define Your System
Create a YAML file describing your system:
```yaml
nodes:
  - kind: threat_model
    id: my_app
    name: My Application
    description: User-facing web application
  
  - kind: component
    id: web_app
    name: Web Application
    component_type_id: webapp
  
  - kind: component
    id: database
    name: PostgreSQL Database
    component_type_id: s3_bucket
```

### 2. Load Into Thanos
```bash
cd src
python load_data.py -f my_app.yaml
```

### 3. Assess Controls
1. Open web interface at `http://localhost:8501`
2. Navigate to your threat model
3. For each component, review applicable controls
4. Document which controls are implemented and how

### 4. Identify Gaps
- Controls marked as not enforced represent security gaps
- Prioritize based on threat severity
- Create action items for remediation

## Documentation

- **[README.md](README.md)**: Overview and quick start
- **[USAGE.md](USAGE.md)**: Detailed usage instructions and examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Technical architecture and data model
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines
- **[LICENSE](LICENSE)**: MIT License

## Roadmap

### Near-Term Enhancements
- [ ] PDF/Word report generation
- [ ] Enhanced component visualizations
- [ ] PostgreSQL/MySQL production support
- [ ] User authentication and RBAC

### Medium-Term Features
- [ ] Cloud provider integrations (AWS, Azure, GCP)
- [ ] RESTful API
- [ ] Threat analytics dashboard
- [ ] Import from other tools (Microsoft Threat Modeling Tool, etc.)

### Long-Term Vision
- [ ] AI-powered threat identification
- [ ] Automated control recommendations
- [ ] Integration with SIEM and ticketing systems
- [ ] Real-time collaboration features
- [ ] Threat intelligence feed integration

## Community & Support

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community support
- **Pull Requests**: Code contributions welcome!

## License

MIT License - Free for commercial and personal use

## Acknowledgments

- STRIDE methodology by Microsoft
- Open-source security community
- Contributors and early adopters

---

**Ready to secure your systems? Get started with Thanos today!**

For questions or support: https://github.com/PankajMoolrajani/thanos/issues
