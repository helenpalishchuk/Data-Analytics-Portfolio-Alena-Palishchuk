# IAM Ticket & Provisioning Analytics

Analysis of IT support tickets and user provisioning/deprovisioning data in a hybrid
Active Directory / Microsoft Entra ID environment. This is based on the type of data I
worked with as a Support Engineer (IAM), rebuilt as a data analytics project using
Python and SQL.

# What this project does

I wanted to check how well SLA (service level agreement) targets were being met across
different ticket types and departments, and whether there were any patterns worth
flagging, especially around security risk.

# Dataset

The dataset is synthetic (generated with realistic patterns, not real company data):
- 1,050 support tickets from Jul 2025 to Jun 2026 (password resets, MFA issues, access
  requests, account lockouts, SSO failures, device enrollment, permission changes, group
  membership)
- 780 provisioning/deprovisioning events across 7 departments and 3 environments
  (Active Directory, Microsoft Entra ID, Hybrid)

# Tools used

Python (pandas, matplotlib), SQL (SQLite)

# What I found

1. Deprovisioning is the biggest risk area. SLA compliance drops to 66.7% in Marketing
   and 70.2% in Legal, compared to 80%+ in Engineering and HR. This matters because
   delayed deprovisioning means people can keep access after they've left or changed
   roles, which is a security/audit problem.

2. Access requests are the slowest ticket type overall, only meeting SLA 80.6% of the
   time, while password resets and account lockouts are almost always on time (98-100%).
   Could point to a manual approval bottleneck.

3. Ticket volume stayed pretty steady month to month, around 85 tickets on average, no
   big seasonal spikes.

4. Agent performance was fairly even across the team, 91-95% SLA compliance, no major
   outliers.

# Files

- generate_data.py: generates the synthetic datasets
- tickets.csv / provisioning.csv: the raw data
- sql_analysis.py: loads everything into SQLite and runs the analysis queries
- sql_queries.sql: the SQL queries on their own
- visualize.py: makes the charts
- chart_monthly_volume.png, chart_sla_by_type.png, chart_deprovisioning_sla.png,
  chart_provisioning_by_environment.png: the output charts

# What I'd recommend

Automating the deprovisioning process so it triggers as soon as HR records an employee's
end date, instead of relying on manual steps. That's where most of the delays and SLA
breaches were coming from.
