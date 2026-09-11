import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams.update({"font.size": 10, "figure.dpi": 150})

tickets = pd.read_csv("tickets.csv", parse_dates=["created_date"])
provisioning = pd.read_csv("provisioning.csv", parse_dates=["request_date"])

# 1. Monthly ticket volume trend
fig, ax = plt.subplots(figsize=(9, 4.5))
monthly = tickets.groupby(tickets["created_date"].dt.to_period("M")).size()
monthly.index = monthly.index.astype(str)
ax.plot(monthly.index, monthly.values, marker="o", color="#2E5EAA", linewidth=2)
ax.set_title("Monthly IAM Support Ticket Volume (Jul 2025 - Jun 2026)")
ax.set_ylabel("Tickets")
ax.set_xlabel("Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_monthly_volume.png")
plt.close()

# 2. SLA compliance by ticket type
sla_by_type = tickets.groupby("ticket_type")["met_sla"].mean().sort_values() * 100
fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#D64545" if v < 90 else "#2E9E5B" for v in sla_by_type.values]
ax.barh(sla_by_type.index, sla_by_type.values, color=colors)
ax.set_title("SLA Compliance Rate by Ticket Type")
ax.set_xlabel("SLA Met (%)")
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
ax.axvline(90, color="gray", linestyle="--", linewidth=1, label="90% target")
ax.legend()
plt.tight_layout()
plt.savefig("chart_sla_by_type.png")
plt.close()

# 3. Deprovisioning SLA compliance by department (security risk)
deprov = provisioning[provisioning["event_type"] == "Deprovisioning"]
dep_sla = deprov.groupby("department")["met_sla"].mean().sort_values() * 100
fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#D64545" if v < 80 else "#2E9E5B" for v in dep_sla.values]
ax.barh(dep_sla.index, dep_sla.values, color=colors)
ax.set_title("Deprovisioning SLA Compliance by Department\n(Security Risk Indicator)")
ax.set_xlabel("SLA Met (%)")
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
plt.tight_layout()
plt.savefig("chart_deprovisioning_sla.png")
plt.close()

# 4. Provisioning vs deprovisioning completion time by environment
env_summary = provisioning.groupby(["environment", "event_type"])["completion_hours"].mean().unstack()
fig, ax = plt.subplots(figsize=(9, 5))
env_summary.plot(kind="bar", ax=ax, color=["#D64545", "#2E5EAA"])
ax.set_title("Avg Completion Time: Provisioning vs Deprovisioning by Environment")
ax.set_ylabel("Avg Hours")
ax.set_xlabel("")
plt.xticks(rotation=15)
plt.legend(title="")
plt.tight_layout()
plt.savefig("chart_provisioning_by_environment.png")
plt.close()

print("Saved 4 charts")
