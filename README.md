# Thanos - AI-Powered Threat Modeling Platform

**Thanos** is a comprehensive threat modeling platform that helps security teams systematically identify, assess, and mitigate security threats in their systems. Built on the industry-standard STRIDE methodology, Thanos provides an intuitive interface for creating and managing threat models across your infrastructure.

## 🎯 Overview

Thanos enables security professionals and development teams to:
- Create detailed threat models for systems and applications
- Map components and their relationships
- Apply security controls based on component types
- Track compliance with frameworks like GDPR
- Assess threats using the STRIDE methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
- Generate actionable insights for risk mitigation

## ✨ Features

### Core Capabilities
- **Component-Based Modeling**: Define system components with specific types (EC2, S3, SaaS, APIs, etc.)
- **STRIDE Threat Analysis**: Comprehensive threat categorization based on industry standards
- **Security Controls**: Pre-configured controls for various component types and compliance frameworks
- **Control Enforcement Tracking**: Document which controls are implemented and how
- **Multi-Framework Support**: Built-in support for GDPR compliance and security best practices
- **Data-Driven Approach**: YAML-based configuration for easy customization and extension

### Web Interface
- **Streamlit-based UI**: Modern, responsive web interface
- **Interactive Threat Model Management**: Create, view, and edit threat models
- **Component Visualization**: Organized views of threat model components
- **Control Assessment**: Document control implementation status with detailed notes

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

#### Option 1: Local Installation

#### Quick Start (Recommended)

Use the automated setup script:

```bash
git clone https://github.com/PankajMoolrajani/thanos.git
cd thanos
chmod +x quickstart.sh
./quickstart.sh
```

This will:
- Initialize the database
- Load default component types and controls
- Load STRIDE threat categories
- Load example threat models
- Start the web interface at `http://localhost:8501`

#### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/PankajMoolrajani/thanos.git
cd thanos
```

2. Install dependencies:
```bash
cd src
pip install -r requirements.txt
```

3. Initialize the database with default data:
```bash
python load_data.py -f data/default.yaml
python load_data.py -f data/init/controls.yaml
python load_data.py -f data/examples/ecommerce_platform.tm.yaml  # Optional
```

4. Run the Streamlit application:
```bash
streamlit run streamlit_app/app.py
```

5. Access the application at `http://localhost:8501`

#### Option 2: Docker Deployment

1. Clone the repository:
```bash
git clone https://github.com/PankajMoolrajani/thanos.git
cd thanos
```

2. Build and start the container:
```bash
docker-compose up -d
```

3. Access the application at `http://localhost:8501`

4. Initialize the database (inside the container):
```bash
docker exec -it thanos bash
cd src
python load_data.py -f data/default.yaml
python load_data.py -f data/init/controls.yaml
```

## 📖 Usage

### Creating Your First Threat Model

1. **Define Component Types**: Start by defining the types of components in your system (e.g., databases, APIs, web applications)

2. **Create Components**: Add specific components based on the types (e.g., "User Authentication API", "Customer Database")

3. **Build Threat Model**: Group related components into a threat model representing a system or workflow

4. **Apply Controls**: Review and document which security controls are enforced for each component

5. **Assess Threats**: Identify applicable threats from the STRIDE categories

6. **Document Mitigations**: Record how each threat is mitigated by security controls

For detailed step-by-step instructions, see [USAGE.md](USAGE.md)

## 🏗️ Architecture

Thanos is built with a clean, modular architecture:

- **Database Layer**: SQLAlchemy ORM with SQLite (easily adaptable to PostgreSQL/MySQL)
- **Data Model**: Comprehensive schema supporting components, controls, threats, and relationships
- **Business Logic**: Python modules for control assessment and threat analysis
- **Presentation Layer**: Streamlit-based web interface
- **Data Initialization**: YAML-based configuration for easy customization

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md)

## 📊 Data Model

The platform supports:
- **Component Types**: Categorize infrastructure and application components
- **Components**: Specific instances in your architecture
- **Controls**: Security controls and compliance requirements
- **Control Rules & Conditions**: Logic for determining which controls apply
- **Threat Categories**: STRIDE-based threat classification
- **Threats**: Specific security threats mapped to categories
- **Threat Models**: Containers for related components and their security posture

## 🎓 STRIDE Methodology

Thanos implements the STRIDE threat modeling methodology:

- **S**poofing: Identity spoofing and authentication bypass
- **T**ampering: Data or request manipulation
- **R**epudiation: Inability to track actions
- **I**nformation Disclosure: Unauthorized data access
- **D**enial of Service: Availability attacks
- **E**levation of Privilege: Unauthorized access escalation

## �� Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Code style and standards

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

For security concerns or to report vulnerabilities, please see our security policy or contact the maintainers directly.

## 📬 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/PankajMoolrajani/thanos/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/PankajMoolrajani/thanos/discussions)

## 🗺️ Roadmap

Future enhancements planned:
- [ ] Enhanced visualization with component diagrams
- [ ] Export threat models to PDF/Word reports
- [ ] Integration with cloud provider APIs for automated component discovery
- [ ] Threat intelligence feed integration
- [ ] Multi-user support with role-based access control
- [ ] RESTful API for programmatic access
- [ ] Integration with JIRA and other ticketing systems

## 🙏 Acknowledgments

- Built on the STRIDE methodology developed by Microsoft
- Inspired by open-source threat modeling tools
- Uses Streamlit for rapid web application development

---

**Made with ❤️ for the security community**
