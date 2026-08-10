# Public Attack Surface & OSINT Assessment Report

> **Audit Provenance**: Timestamp: `2026-08-02T23:21:39.354832` | Git SHA: `d934836309da0bb4450ff2ef5da90714054e9b05` | Branch: `release/2027.1` | Tool: `v2.0.0`

### Impersonation Risk Level: **Moderate-High (Standard for Public Educator Portfolios)**

### Summary
The repository exposes detailed career history, academic qualifications, and public contact information. Because this is a public digital portfolio designed for recruiters, identity attributes (name, education, career timeline) are intentionally exposed. However, strict defense-in-depth measures (zero private key leaks, zero session cookies, zero home addresses or passport numbers) ensure that credential compromise or unauthorized access is impossible.

### Exposed Portfolio Attributes
- **Full Name**: Mohammed Shehzad Khan
- **Email**: mshehzadkhan@hotmail.com
- **Education**: B.Ed. Education (UCL / University of London)
- **Career History**: EAL & STEM Teacher, International School Educator
- **Location**: Hong Kong / International
- **Public Portfolio**: CV Master & Tailored HTML Outputs
- **Certifications**: QTS, Teaching Credentials

### Governance Recommendations
- Maintain separation between public professional profile and private personal identification.
- Never commit raw passport scans or national identification numbers into evidence directories.
- Use signed verification hashes for documentary certificates where possible.
