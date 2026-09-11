# IAM Ticket & Provisioning Analytics

Analysis of IT support tickets and user provisioning/deprovisioning events in a hybrid
Active Directory / Microsoft Entra ID environment. Based on the kind of operational data
I worked with as a Support Engineer (IAM) - reframed here as a data analytics project
using **Python (pandas)** and **SQL (SQLite)**.

## Objective
Identify SLA compliance gaps and security risk patterns in identity lifecycle management -
specifically, how quickly accounts are provisioned/deprovisioned and where support tickets
breach service-level targets.

## Dataset
Synthetic dataset generated to reflect realistic patterns from a mid-size hybrid IAM environment:
- **1,050 support tickets** (Jul 2025 – Jun 2026): password resets, MFA issues, access requests,
  account lockouts, SSO failures, device enrollment, permission changes, group membership
- **780 provisioning/deprovisioning events** across 7 departments and 3 environments
  (Active Directory, Microsoft Entra ID, Hybrid)

*(Note: synthetic data, generated with realistic distributions — no real user/company data used.)*

## Tools
`Python` (pandas, matplotlib) · `SQL` (SQLite) · `sqlite3`

## Key Findings

1. **Deprovisioning is the biggest compliance risk.** SLA compliance for deprovisioning
   drops to 66.7% in Marketing and 70.2% in Legal — well below the 80%+ seen in Engineering
   and HR. Delayed deprovisioning is a direct security/audit exposure (ex-employees or
   role-changed users retaining access).

2. **Access Requests are the slowest ticket type**, meeting SLA only 80.6% of the time,
   compared to 98–100% for password resets and account lockouts — suggesting a manual
   approval bottleneck worth investigating.

3. **Ticket volume is stable month-to-month** (~85/month average), with no major seasonal
   spikes — useful for staffing/capacity planning.

4. **Agent performance is fairly consistent** (91–95% SLA compliance across the team), with
   ~3-4 percentage point spread — no major outliers.

## Files
| File | Description |
|---|---|
| `generate_data.py` | Generates the synthetic tickets & provisioning datasets |
| `tickets.csv` / `provisioning.csv` | Raw generated data |
| `sql_analysis.py` | Loads data into SQLite, runs analytical queries |
| `sql_queries.sql` | Standalone SQL queries (aggregation, grouping, SLA calculations) |
| `visualize.py` | Generates all charts |
| `chart_*.png` | Output visualizations |

## Charts
- `chart_monthly_volume.png` — ticket volume trend over 12 months
- `chart_sla_by_type.png` — SLA compliance rate by ticket type
- `chart_deprovisioning_sla.png` — deprovisioning SLA compliance by department (security risk view)
- `chart_provisioning_by_environment.png` — provisioning vs deprovisioning speed by environment

## Recommendation
Prioritize automating deprovisioning workflows for Marketing and Legal, and review the
Access Request approval chain to reduce manual bottlenecks — both would meaningfully lift
overall SLA compliance and reduce audit/security exposure.

---
*Author: Alena Palishchuk — Support Engineer (IAM) transitioning into Data Analytics.*
