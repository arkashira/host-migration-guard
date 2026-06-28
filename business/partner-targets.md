# partner-targets.md

## Partner Integration Roadmap – Host‑Migration‑Guard

| # | Partner | Rationale | Free‑Tier Limits | Integration Effort | Value‑Add (User Job) | Revenue‑Share / Affiliate |
|---|---------|-----------|------------------|--------------------|----------------------|---------------------------|
| 1 | **Fly.io** | Rust‑centric, edge‑first hosting; ideal for low‑latency Rust apps. | $5/month, 1 GB RAM, 1 vCPU, 1 GB SSD, 1 GB outbound traffic. | **S** – API is lightweight, single‑auth token, simple migration scripts. | *“Keep my Rust app running everywhere”* – automated fail‑over & migration. | Affiliate program: 10 % recurring revenue. |
| 2 | **Railway.app** | One‑click deployment for Rust & PostgreSQL; free tier 5 GB DB, 1 GB storage. | 5 GB PostgreSQL, 1 GB storage, 1 GB outbound. | **S** – OAuth + REST API, minimal schema mapping. | *“Deploy & migrate with zero downtime”* – instant platform switch. | Revenue‑share: 12 % on paid plans. |
| 3 | **Supabase** | Managed PostgreSQL + auth; free tier 500 MB DB, 1 GB storage. | 500 MB DB, 1 GB storage, 1 GB outbound. | **S** – REST + JWT auth; data export/import scripts. | *“Move my database safely”* – automated DB migration & sync. | Affiliate: 15 % on paid tiers. |
| 4 | **Render.com** | Cloud‑native platform with free hobby tier; supports Rust via Docker. | $7/month hobby plan, 512 MB RAM, 1 GB SSD, 1 GB outbound. | **M** – Docker image handling, custom domain mapping. | *“Scale my app with minimal ops”* – automated container migration. | Revenue‑share: 10 % on paid plans. |
| 5 | **DigitalOcean** | Popular VPS & managed database; free $100 credit for new users. | $5/month Droplet, 1 GB RAM, 1 CPU, 25 GB SSD. | **M** – API for Droplet & Managed DB provisioning. | *“Keep my app alive even if a provider shuts down”* – rapid fail‑over. | Affiliate: 12 % on new Droplet sales. |
| 6 | **Cloudflare Pages / Workers** | Edge‑first static & serverless hosting; free tier unlimited sites. | Unlimited sites, 100 GB/month bandwidth. | **S** – API for site creation, DNS, KV store. | *“Deploy static assets globally with instant rollback”* – migration of front‑end assets. | No revenue‑share; low cost, high value. |
| 7 | **GitHub Actions** | CI/CD platform; free 2 GH‑hrs/month for public repos. | 2 GH‑hrs/month, 500 MB storage. | **S** – Webhooks + REST API; simple job triggers. | *“Trigger migration on CI failures”* – automated migration pipeline. | Marketplace revenue‑share: 15 % on paid plans. |
| 8 | **Sentry** | Error monitoring; free tier 5 k events/month. | 5 k events/month, 5 GB storage. | **M** – SDK integration, event enrichment. | *“Detect platform outages early”* – proactive alerts before migration. | Affiliate: 10 % on paid tiers. |

> **Note**: All partners are selected to cover the full migration workflow: monitoring, database, application, and infrastructure layers.  
> **Priority**: Partners with affiliate/revenue‑share are listed first; those without are still high value for user experience.

---

## Integration Phases

| Phase | Timeline | Partners | Key Deliverables | Success Metrics |
|-------|----------|----------|------------------|-----------------|
| **Phase 1 – Core Platform** | 0–3 mo | Fly.io, Railway.app, Supabase | • OAuth + API connectors<br>• Migration scripts (Docker, DB dump/restore)<br>• Dashboard widgets for health & migration status | • 3 k+ users onboarded<br>• 90 % migration success rate |
| **Phase 2 – Cloud & Edge** | 3–6 mo | Render.com, DigitalOcean, Cloudflare | • Container orchestration hooks<br>• DNS & CDN fail‑over<br>• Edge‑first asset migration | • 5 k+ users<br>• 95 % uptime during provider outage |
| **Phase 3 – Ops & Observability** | 6–9 mo | GitHub Actions, Sentry | • CI‑triggered migration pipelines<br>• Real‑time error alerts<br>• Automated rollback | • 10 k+ users<br>• 99.9 % SLA on migration events |

---

## Implementation Checklist

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Define data model for migration metadata | PM | ☐ | Must support multi‑platform mapping |
| Build Fly.io connector | Dev | ☐ | Use Fly API v1 |
| Build Railway connector | Dev | ☐ | OAuth + REST |
| Build Supabase connector | Dev | ☐ | Export/Import scripts |
| Build Render connector | Dev | ☐ | Docker image handling |
| Build DigitalOcean connector | Dev | ☐ | Droplet & Managed DB APIs |
| Build Cloudflare connector | Dev | ☐ | Pages & Workers APIs |
| Build GitHub Actions integration | Dev | ☐ | Webhook + Action template |
| Build Sentry integration | Dev | ☐ | SDK + event enrichment |
| Create affiliate tracking | PM | ☐ | Use UTM + partner IDs |
| Launch beta | PM | ☐ | Target 500 users |

---

## Revenue‑Share Outlook

| Partner | Share % | Expected Monthly Recurring Revenue (MRR) | Notes |
|---------|---------|----------------------------------------|-------|
| Fly.io | 10 % | $2 k | 200 new users @ $10/mo |
| Railway.app | 12 % | $3 k | 300 new users @ $10/mo |
| Supabase | 15 % | $4 k | 400 new users @ $10/mo |
| Render.com | 10 % | $1.5 k | 150 new users @ $10/mo |
| DigitalOcean | 12 % | $2.5 k | 250 new users @ $10/mo |
| GitHub Actions | 15 % | $3 k | 300 new users @ $10/mo |
| Sentry | 10 % | $1 k | 100 new users @ $10/mo |
| **Total** | | **$17.5 k** | **Projected first‑year revenue** |

> *Assumptions*: 10 % of new users on a paid plan, average $10/mo per user, 12 mo retention.

---

### Next Steps

1. **Finalize partner agreements** – secure affiliate contracts.  
2. **Kick off Phase 1 development** – start with Fly.io, Railway, Supabase.  
3. **Set up analytics** – track migration success, user churn, revenue share.  
4. **Prepare marketing assets** – partner logos, integration guides.  
5. **Launch beta** – invite early adopters, gather feedback.

---