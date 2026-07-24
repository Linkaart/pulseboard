# PulseBoard

Dashboard analytics SaaS - Projet CDA (Django + React) avec KPIs, filtres, graphiques, export et gestion des roles.

## Presentation

PulseBoard est une application web de type SaaS permettant a une entreprise de centraliser ses indicateurs cles, d'analyser sa performance via des graphiques interactifs, d'appliquer des filtres metier, d'exporter les resultats et de securiser l'acces aux donnees selon les roles utilisateur.

## Objectifs

- Authentifier les utilisateurs et securiser l'acces aux donnees via RBAC et JWT.
- Presenter des KPIs orientes decision, avec filtres temporels et metier.
- Afficher des visualisations lisibles et adaptees au besoin utilisateur.
- Permettre l'export CSV et PDF de vues ou d'insights.
- Journaliser certaines actions pour assurer la tracabilite.

## Profils utilisateurs

- **Administrateur** : gere les utilisateurs, les roles, les parametres globaux et l'acces aux exports.
- **Manager** : consulte les KPI globaux, applique des filtres d'equipe ou de periode, exporte des rapports.
- **Analyste** : explore les donnees detaillees, enregistre des filtres et consulte les vues analytiques autorisees.

## Fonctionnalites (MVP)

- Connexion securisee (JWT)
- Tableau de bord avec cartes KPI
- Graphiques interactifs (MRR, nouveaux clients, churn)
- Filtres par date, equipe, canal, produit
- Tableau de donnees paginee
- Export CSV et PDF
- Gestion des roles (RBAC)
- Historique d'activite

## KPI suivis

- MRR (Monthly Recurring Revenue)
- Nouveaux clients
- Churn rate
- Taux de conversion
- ARPU (revenu moyen par client)
- Tickets support ouverts/fermes

## Stack technique

| Couche | Technologie |
|---|---|
| Front-end | React + TypeScript |
| Back-end | Django + Django REST Framework |
| Auth | JWT |
| Autorisation | Groupes + permissions Django (RBAC) |
| Base de donnees | PostgreSQL |
| Charts | Chart.js / Recharts |
| Export | CSV + PDF |
| Deploiement | Docker + Render/Railway |

## Architecture

Le frontend React consomme une API REST Django. L'API gere l'authentification, les roles, les calculs de KPI, les filtres et les exports. PostgreSQL stocke les donnees metier et analytics.

### Modele de donnees (entites principales)

- Company, Team, User
- Customer, Subscription, Invoice
- MetricSnapshot, SavedFilter
- ActivityLog

## Arborescence Backend (Django)

```
pulseboard-backend/
apps/
  accounts/      -> User, Role, permissions
  companies/     -> Company, Team
  customers/     -> Customer, Subscription, Invoice
  analytics/     -> MetricSnapshot, SavedFilter, calculs KPI
  exports/       -> export CSV / PDF
  audit/         -> ActivityLog
config/
  settings/
  urls.py
manage.py
```

## Arborescence Frontend (React + TS)

```
pulseboard-frontend/
src/
  pages/         -> Login, Dashboard, AnalyticsDetail, UsersAdmin, ActivityLog
  components/    -> KpiCard, ChartLine, ChartBar, FilterBar, DataTable, Sidebar
  features/      -> auth, dashboard, users (slices)
  services/      -> api.ts (axios + JWT)
  types/
  routes/        -> ProtectedRoute
```

## API principale

| Endpoint | Methode | Role requis |
|---|---|---|
| /api/auth/login/ | POST | public |
| /api/auth/refresh/ | POST | public |
| /api/auth/me/ | GET | connecte |
| /api/dashboard/summary/ | GET | view_kpi |
| /api/dashboard/charts/ | GET | view_kpi |
| /api/dashboard/table/ | GET | view_reports |
| /api/filters/ | GET/POST | connecte |
| /api/exports/csv/ | GET | export_data |
| /api/exports/pdf/ | GET | export_data |
| /api/users/ | GET/POST | manage_users |
| /api/users/{id}/role/ | PATCH | manage_users |

## Roles et permissions (RBAC)

| Action | Admin | Manager | Analyste |
|---|---|---|---|
| Voir dashboard | Oui | Oui | Oui |
| Voir tous les KPI | Oui | Oui | Selon droits |
| Export CSV/PDF | Oui | Oui | Optionnel |
| Gerer utilisateurs | Oui | Non | Non |
| Modifier parametres | Oui | Non | Non |

## Tests prevus

- Authentification et permissions
- Endpoints KPI et calculs de metriques
- Exports CSV/PDF
- Composants front cles (KpiCard, FilterBar, DataTable)

## Planning (sprints)

1. Cadrage, MCD/MLD, initialisation back/front, auth JWT
2. Modeles metier, permissions RBAC, endpoints dashboard
3. UI dashboard, graphiques, filtres
4. Exports CSV/PDF, admin utilisateurs, logs d'activite
5. Tests, seed de donnees, deploiement, documentation

## Auteur

Projet realise dans le cadre d'une formation Concepteur Developpeur d'Applications (CDA).
