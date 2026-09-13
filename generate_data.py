"""
Synthetic IAM support ticket + provisioning/deprovisioning data,
modeled on a hybrid AD / Microsoft Entra ID environment.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N_TICKETS = 1050          # ~20/week - 1 year
N_PROVISIONING = 780      # ~15/week - 1 year

departments = ["Finance", "Sales", "Engineering", "HR", "Operations", "Marketing", "Legal"]
ticket_types = ["Password Reset", "MFA Issue", "Access Request", "Account Lockout",
                 "SSO Login Failure", "Device Enrollment", "Permission Change", "Group Membership"]
priority_levels = ["Low", "Medium", "High"]
agents = ["A. Palishchuk", "J. Nguyen", "R. Costa", "M. Singh", "T. O'Brien"]

start_date = datetime(2025, 7, 1)
end_date = datetime(2026, 7, 1)
date_range_days = (end_date - start_date).days

# Support Tickets
ticket_rows = []
for i in range(N_TICKETS):
    created = start_date + timedelta(days=np.random.randint(0, date_range_days),
                                       hours=np.random.randint(8, 18))
    ttype = np.random.choice(ticket_types, p=[0.22, 0.16, 0.18, 0.12, 0.10, 0.08, 0.09, 0.05])
    priority = np.random.choice(priority_levels, p=[0.5, 0.35, 0.15])

    # Resolution time varies by type and priority (in hours)
    base_time = {
        "Password Reset": 0.5, "MFA Issue": 1.5, "Access Request": 6,
        "Account Lockout": 0.75, "SSO Login Failure": 2, "Device Enrollment": 5,
        "Permission Change": 4, "Group Membership": 3
    }[ttype]
    priority_mult = {"Low": 1.3, "Medium": 1.0, "High": 0.6}[priority]
    resolution_hours = max(0.1, np.random.exponential(base_time * priority_mult))

    resolved = created + timedelta(hours=resolution_hours)
    sla_target = {"Low": 24, "Medium": 8, "High": 2}[priority]
    met_sla = resolution_hours <= sla_target

    ticket_rows.append({
        "ticket_id": f"TKT-{10000+i}",
        "created_date": created,
        "resolved_date": resolved,
        "department": np.random.choice(departments),
        "ticket_type": ttype,
        "priority": priority,
        "assigned_agent": np.random.choice(agents, p=[0.28, 0.18, 0.18, 0.18, 0.18]),
        "resolution_hours": round(resolution_hours, 2),
        "sla_target_hours": sla_target,
        "met_sla": met_sla
    })

tickets_df = pd.DataFrame(ticket_rows)

# Provisioning/Deprovisioning Events
prov_rows = []
for i in range(N_PROVISIONING):
    event_type = np.random.choice(["Provisioning", "Deprovisioning"], p=[0.55, 0.45])
    request_date = start_date + timedelta(days=np.random.randint(0, date_range_days))

    if event_type == "Provisioning":
        # time to fully provision a new hire (hours)
        completion_hours = max(0.5, np.random.exponential(4))
        sla_target = 8
    else:
        # deprovisioning should be fast for security/compliance (hours)
        completion_hours = max(0.2, np.random.exponential(3))
        sla_target = 4

    completed_date = request_date + timedelta(hours=completion_hours)
    met_sla = completion_hours <= sla_target

    prov_rows.append({
        "event_id": f"PRV-{5000+i}",
        "event_type": event_type,
        "department": np.random.choice(departments),
        "environment": np.random.choice(["Active Directory", "Microsoft Entra ID", "Hybrid (AD + Entra ID)"],
                                          p=[0.25, 0.35, 0.40]),
        "request_date": request_date,
        "completed_date": completed_date,
        "completion_hours": round(completion_hours, 2),
        "sla_target_hours": sla_target,
        "met_sla": met_sla
    })

provisioning_df = pd.DataFrame(prov_rows)

tickets_df.to_csv("tickets.csv", index=False)
provisioning_df.to_csv("provisioning.csv", index=False)

print(f"Generated {len(tickets_df)} tickets and {len(provisioning_df)} provisioning events")
print(tickets_df.head())
print(provisioning_df.head())
