-- 1. SLA compliance rate by ticket type
SELECT
        ticket_type,
        COUNT(*) AS total_tickets,
        SUM(CASE WHEN met_sla THEN 1 ELSE 0 END) AS sla_met,
        ROUND(100.0 * SUM(CASE WHEN met_sla THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_pct
    FROM tickets
    GROUP BY ticket_type
    ORDER BY sla_pct ASC;

-- 2. Monthly ticket volume trend
SELECT
        strftime('%Y-%m', created_date) AS month,
        COUNT(*) AS ticket_count,
        ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
    FROM tickets
    GROUP BY month
    ORDER BY month;

-- 3. Agent performance (avg resolution time, SLA rate)
SELECT
        assigned_agent,
        COUNT(*) AS tickets_handled,
        ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours,
        ROUND(100.0 * SUM(CASE WHEN met_sla THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_pct
    FROM tickets
    GROUP BY assigned_agent
    ORDER BY sla_pct DESC;

-- 4. Deprovisioning SLA compliance by department (security risk indicator)
SELECT
        department,
        COUNT(*) AS deprovisioning_events,
        ROUND(AVG(completion_hours), 2) AS avg_completion_hours,
        ROUND(100.0 * SUM(CASE WHEN met_sla THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_pct,
        SUM(CASE WHEN NOT met_sla THEN 1 ELSE 0 END) AS breaches
    FROM provisioning
    WHERE event_type = 'Deprovisioning'
    GROUP BY department
    ORDER BY sla_pct ASC;

-- 5. High priority tickets that breached SLA (detail)
SELECT ticket_id, department, ticket_type, resolution_hours, sla_target_hours
    FROM tickets
    WHERE priority = 'High' AND met_sla = 0
    ORDER BY resolution_hours DESC
    LIMIT 10;

-- 6. Provisioning vs Deprovisioning avg completion time by environment
SELECT
        environment,
        event_type,
        COUNT(*) AS events,
        ROUND(AVG(completion_hours), 2) AS avg_hours
    FROM provisioning
    GROUP BY environment, event_type
    ORDER BY environment, event_type;

