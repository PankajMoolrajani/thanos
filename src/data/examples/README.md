# Example Threat Models

This directory contains example threat models demonstrating how to use Thanos for various scenarios.

## Available Examples

### E-Commerce Platform (`ecommerce_platform.tm.yaml`)

A comprehensive example of a modern e-commerce platform including:
- Web frontend (React SPA)
- API Gateway
- Microservices (Order Processing)
- Databases (User DB, Product Catalog)
- Third-party integrations (Stripe, SendGrid, Google Analytics)
- CDN and static asset storage

**To load this example:**
```bash
cd src
python load_data.py -f data/examples/ecommerce_platform.tm.yaml
```

Then access the web interface at `http://localhost:8501` to view and work with the threat model.

### Customer Call Recordings (`../customer_call_recordings_workflow.tm.yaml`)

A simpler example demonstrating a customer call recording workflow with SaaS integrations including Salesforce, SalesLoft, and Genesys.

## Creating Your Own Threat Models

Use these examples as templates. The basic structure is:

```yaml
nodes:
  # Define the threat model container
  - kind: threat_model
    id: your_system_id
    name: Your System Name
    description: Description of what you're modeling
  
  # Add components that make up your system
  - kind: component
    id: component_1
    name: Component Display Name
    component_type_id: webapp  # or saas, s3_bucket, etc.
  
  - kind: component
    id: component_2
    name: Another Component
    component_type_id: 3rd_party_api
```

## Available Component Types

- `webapp` - Web applications (custom)
- `ec2_instance` - AWS EC2 compute instances
- `s3_bucket` - AWS S3 storage buckets (also used for generic databases)
- `saas` - Third-party SaaS applications
- `3rd_party_api` - External APIs and services

## Best Practices

1. **Use descriptive IDs**: Make IDs readable and meaningful (e.g., `user_auth_api` not `api1`)
2. **Include context in names**: Help future users understand what the component does
3. **Write detailed descriptions**: Explain the purpose and security considerations
4. **Group related components**: Create separate threat models for distinct systems
5. **Start small**: Begin with critical paths and expand over time

## Next Steps

After loading a threat model:
1. View it in the web interface
2. Review applicable security controls for each component
3. Document which controls are implemented
4. Identify gaps and create action items
5. Export or share your findings with the team

For more details, see the main [USAGE.md](../../../USAGE.md) documentation.
