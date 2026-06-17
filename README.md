# Marketing Team Lead Management System

Internal Django dashboard for managers to track marketing team leads, assigned campaign work, and scored sales/marketing leads.

## Current Features

- Manager login with Django session authentication
- Team lead CRUD
- Assigned campaign work CRUD
- Work status and progress tracking
- Lead scoring based on engagement, behavior, industry fit, and revenue
- Automatic lead assignment to the best available team lead
- Search and filters
- Summary cards
- Dark mode
- Pie and bar charts
- Compact scrollable tables

## Demo Login

```text
Username: manager
Password: manager123
```

## Tech Stack

```text
Django
Django REST Framework
SQLite
HTML/CSS/JavaScript
Canvas charts
```

## Data Models

### TeamLead

Tracks marketing team leads.

```text
full_name
email
phone
department
designation
specialization
status
```

Statuses:

```text
active
inactive
on_leave
```

### AssignedWork

Tracks campaign/client/channel work assigned to a team lead.

```text
team_lead
title
client_name
campaign_name
campaign_type
channel
responsibility
priority
status
progress
start_date
due_date
notes
```

Statuses:

```text
not_started
in_progress
blocked
completed
cancelled
```

### Lead

Tracks scored leads/prospects and auto-routes them to team leads.

```text
full_name
email
phone
company_name
industry
annual_revenue
source
assigned_to
status
email_engagement
social_engagement
website_visits
form_submissions
lead_score
lead_grade
notes
```

Lead grades:

```text
hot
warm
cold
```

## Lead Scoring

The backend calculates `lead_score` automatically when a lead is saved.

Score inputs:

```text
email engagement
social engagement
website visits
form submissions
annual revenue
industry fit
```

Grade rules:

```text
75-100 -> hot
45-74  -> warm
0-44   -> cold
```

## Lead Distribution

If `assigned_to` is left blank, the backend auto-assigns the lead.

Rules:

```text
Hot leads -> active matching specialist first
Paid Ads source -> Paid Ads specialist
Social Media source -> Social Media specialist
Website source -> SEO specialist
Email Campaign source -> Email specialist
No match -> active team lead with the fewest scored leads
```

## API Endpoints

```text
/api/team-leads/
/api/assigned-work/
/api/leads/
```

Each endpoint supports:

```text
GET
POST
GET by id
PUT
PATCH
DELETE
```

## Dashboard Observability

Summary cards include:

```text
Total Team Leads
Active Team Leads
Total Assigned Work
In Progress Work
Blocked Work
Completed Work
Average Progress
High Priority Work
Scored Leads
Hot Leads
Warm Leads
Cold Leads
Unassigned Leads
Hot Unassigned Leads
Average Score
```

Charts include:

```text
Work Status Distribution
Workload By Team Lead
Average Progress By Team Lead
Lead Grade Distribution
Leads Per Team Lead
```

## Run Locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8001
```

Open:

```text
http://127.0.0.1:8001/
```

## Seeded Demo Data

Current local database includes:

```text
7 team leads
20 assigned work records
20 scored leads
```

