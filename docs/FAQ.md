# Frequently Asked Questions (FAQ)

## General Questions

### What is Lamoda AI Recruiter?
Lamoda AI Recruiter is an intelligent, AI-powered recruitment platform designed to streamline the hiring process. It leverages advanced machine learning and natural language processing to automate resume screening, candidate evaluation, and interview question generation.

### Who should use Lamoda AI Recruiter?
Our platform is ideal for:
- Mid-size to large enterprises (500+ employees)
- Recruitment agencies and staffing companies
- Organizations with high-volume hiring needs
- Companies looking to reduce time-to-hire and improve hiring quality

### What problems does it solve?
- Reduces time-to-hire by 60%
- Decreases cost-per-hire by 40%
- Eliminates unconscious bias in screening
- Improves candidate experience
- Provides data-driven hiring insights

---

## Technical Questions

### What file formats do you support for resume parsing?
Currently, we support:
- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Text files (.txt)

We're working on support for additional formats.

### How accurate is the resume parsing?
Our resume parser achieves 95%+ accuracy on standard resumes. Accuracy may vary for:
- Non-standard formats
- Multiple languages (we're expanding language support)
- Heavily stylized resumes

### Is my data secure?
Yes. We implement:
- End-to-end encryption for data in transit (HTTPS/TLS)
- Encryption at rest for stored data
- Regular security audits
- GDPR and data privacy compliance
- SOC 2 compliance (in progress)

### Where is my data stored?
Data is stored in secure cloud infrastructure:
- Primary: Yandex Cloud (Russia/EU)
- Optional: AWS (for US-based customers)
- All data is encrypted and backed up

### What is your uptime SLA?
We guarantee:
- 99.9% uptime during business hours
- Automatic backups every 24 hours
- Disaster recovery plan in place
- Redundant infrastructure

### Do you support API integrations?
Yes! We offer:
- RESTful API
- Comprehensive API documentation
- Webhook support
- SDKs for Python, JavaScript, and Go
- Postman collection for testing

See [COMPREHENSIVE_API_REFERENCE.md](COMPREHENSIVE_API_REFERENCE.md) for details.

---

## Feature Questions

### How does the interview question generation work?
1. You provide job requirements and candidate profile
2. Our AI analyzes the data
3. It generates role-specific, personalized questions
4. You can review, edit, and customize questions
5. Questions are delivered to the interview panel

### Can I customize the scoring criteria?
Yes! You can:
- Set custom weights for different skills
- Define required vs. preferred qualifications
- Adjust scoring algorithms
- Create role-specific scoring profiles
- Compare candidates side-by-side

### Does the system reduce bias?
Our system helps reduce bias by:
- Focusing on objective criteria (skills, experience, education)
- Using consistent evaluation across all candidates
- Highlighting both strengths and gaps
- Providing explainable AI recommendations
- Tracking diversity metrics

Note: The system is a tool to assist human decision-making, not replace it.

### Can multiple recruiters collaborate?
(Coming in Q1 2025)
Upcoming features include:
- Team collaboration tools
- Shared candidate pools
- Comments and feedback
- Role-based permissions

---

## Deployment Questions

### How do I deploy the system?
Options:
1. **SaaS**: Cloud-hosted solution (recommended for most users)
2. **Self-hosted**: Deploy on your own infrastructure (enterprise option)
3. **Hybrid**: Combination of cloud and on-premise components

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### What are the system requirements for self-hosted deployment?
- 8GB RAM minimum (16GB recommended)
- 50GB storage (for database and logs)
- Python 3.9+
- PostgreSQL 12+
- Docker and Kubernetes support

### How long does setup take?
- SaaS: 15 minutes (with guided onboarding)
- Self-hosted: 2-4 hours (depending on infrastructure)
- Integration with existing systems: 1-2 days

### Do you provide training and support?
Yes! We offer:
- Onboarding sessions for new users
- Video tutorials and documentation
- Email support (response time: <4 hours)
- Knowledge base and FAQ
- Priority support for enterprise customers

---

## Pricing Questions

### What is your pricing model?
We offer three tiers:
- **Starter**: $499/month (50 candidates/year)
- **Professional**: $1,999/month (250 candidates/year)
- **Enterprise**: Custom pricing (unlimited)

Pricing includes:
- Platform access
- Resume parsing
- Candidate scoring
- Interview question generation
- Basic analytics
- Email support

### Is there a free trial?
Yes! We offer:
- 14-day free trial (no credit card required)
- Full access to all features
- 5 test candidates
- Support email: sales@lamoda-recruiter.com

### Are there any setup fees?
No setup fees for SaaS. Enterprise customers may have:
- One-time implementation fee
- Custom training sessions
- Integration development

These are quoted separately based on requirements.

### Can I cancel anytime?
Yes. You can cancel at any time:
- Month-to-month: Cancel immediately
- Annual plans: Prorated refund available
- No early termination fees

---

## Integration Questions

### What systems do you integrate with?
Current integrations:
- Slack (notifications)
- Email (candidate communications)
- Google Calendar (interview scheduling)

Upcoming integrations (Q1-Q2 2025):
- Workday
- SAP SuccessFactors
- ADP
- LinkedIn

### Do you have an API?
Yes! Complete API documentation available at [COMPREHENSIVE_API_REFERENCE.md](COMPREHENSIVE_API_REFERENCE.md)

Features:
- REST API with JSON
- Rate limiting: 1000 requests/hour
- Webhook support
- SDK libraries available

### Can I export data?
Yes! You can export:
- Candidate profiles (JSON, CSV)
- Scoring reports
- Interview questions
- Analytics data
- Audit logs

---

## Legal & Compliance Questions

### Is the system GDPR compliant?
Yes. We comply with:
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- LGPD (Brazil's data protection law)
- Local data protection regulations

We have:
- Data processing agreements (DPAs)
- Privacy policy documentation
- Data retention policies
- Right to deletion/export

### Can we use this in [specific country]?
We currently operate in:
- European Union
- United States
- Russia/CIS region
- With expansion planned for Asia-Pacific

Please contact us for region-specific compliance requirements.

### How long do you retain data?
Retention policies:
- Active candidates: Until end of hiring process
- Rejected candidates: 1 year (GDPR requirement)
- Custom retention periods available
- Full data deletion on request

### Do you comply with anti-discrimination laws?
Yes. Our system:
- Operates on objective, job-related criteria
- Does not use protected class information
- Helps identify and reduce unconscious bias
- Complies with EEOC guidelines
- Produces audit trails for compliance

---

## Support & Troubleshooting

### What if I have a technical issue?
1. Check our [documentation](./)
2. Search the knowledge base
3. Contact support: support@lamoda-recruiter.com
4. For urgent issues: Include "URGENT" in subject line

### How long is typical support response time?
- General questions: 4-8 hours
- Technical issues: 2-4 hours
- Urgent issues: 30 minutes
- Enterprise customers: Dedicated support team

### Do you offer customization?
Yes! We offer:
- Custom scoring algorithms
- Branded candidate portal
- Custom integrations
- White-label solutions
- API customization

Contactsales@lamoda-recruiter.com for custom solutions.

### Can I get training for my team?
Yes! Training options:
- Self-service video tutorials (free)
- Live webinar training (included)
- In-depth training sessions (enterprise)
- Certification program (coming soon)

---

## More Questions?

If you don't find the answer here:
- **Email**: support@lamoda-recruiter.com
- **Chat**: Available on our website (9 AM - 5 PM CET)
- **Phone**: +49-30-XXXX-XXXX (enterprise customers)
- **Community**: GitHub Discussions

---

*Last Updated: December 2024*
*FAQ Version: 1.0*
