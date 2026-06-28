# Customer Journey – **host‑migration‑guard**

| Phase | Trigger Event | Friction Points | User Emotions | Opportunities to Delight | Success Metric |
|-------|---------------|----------------|---------------|--------------------------|----------------|
| **Aware** | • News article or tweet about a major hosting provider outage (e.g., “Platform X shuts down”). <br>• Reddit / Hacker News thread titled *“My Rust + Postgres app went down because my host vanished”*. | • Information overload – many unrelated alerts. <br>• No clear “what can I do?” guidance. | **Anxiety → Curiosity** – developers feel vulnerable but start looking for a safety net. | • Publish a **“Hosting‑Disruption Playbook”** (1‑page PDF) that references the tool. <br>• Run a **Twitter‑Spaces** with a Rust community leader discussing “Never lose a host again”. <br>• Offer a **free “Disruption‑Alert” email subscription** (no sign‑up required). | **Awareness Reach** – % of target devs (Rust + Postgres) who view the playbook or attend the Space. <br>*Target*: 5 % of the estimated 30 k Rust‑Postgres devs per month. |
| **Consider** | • Developer receives the first “Potential host disruption” email from the free alert service. <br>• Searches “how to migrate Rust app from Platform X”. | • Uncertainty about tool credibility (no known brand). <br>• Perceived integration effort with existing CI/CD pipelines. | **Skepticism → Hope** – “Will this actually protect my app?” | • Provide a **one‑page ROI calculator** (downtime cost vs. guard subscription). <br>• Offer a **30‑day free trial** with **zero‑config** onboarding (detects host via `Cargo.toml` & `DATABASE_URL`). <br>• Publish **case‑study videos** of a migration from a real‑world outage. | **Consideration Conversion** – % of alerted users who click “Learn More” → trial sign‑up. <br>*Target*: 20 % (≈ 200 / 1 000 alerts). |
| **Try** | • User signs up for the free trial and runs the **“Detect My Host”** wizard. | • False‑positive alerts (e.g., flagging a dev‑only sandbox). <br>• Limited documentation for edge‑case setups (multiple DB hosts). | **Cautious Optimism → Frustration (if bugs)** | • **Live onboarding chat** with a migration engineer (first 30 min free). <br>• **Auto‑generated migration plan** (step‑by‑step, with `docker-compose` & `sqlx` scripts). <br>• **In‑app “sandbox”** to simulate a migration without touching production. | **Trial Activation Rate** – % of sign‑ups that complete the “Detect & Plan” flow. <br>*Target*: 70 % (≈ 140 / 200). |
| **Adopt** | • Successful dry‑run migration and a real‑world migration triggered by a host‑deprecation notice. | • Subscription pricing perceived as high for solo developers. <br>• Need for ongoing monitoring beyond the trial period. | **Confidence → Commitment** – “I can finally sleep at night.” | • Offer **tiered pricing** (Solo $9/mo, Team $29/mo, Enterprise $99/mo) with **annual discount 20 %**. <br>• Include **“always‑on health dashboard”** and **Slack/Discord webhook alerts**. <br>• Provide **“migration‑as‑a‑service”** add‑on for teams lacking ops expertise. | **Adoption Rate** – % of trial users who convert to paid plan within 30 days. <br>*Target*: 15 % (≈ 21 / 140). |
| **Expand** | • Customer adds a second service (e.g., a Rust micro‑service) to the same guard account. <br>• Receives a “New platform recommendation” based on usage patterns. | • Feature fatigue – too many alerts or suggestions. <br>• Lack of clear upgrade path for larger orgs. | **Empowerment → Advocacy** – “This tool is now part of my DevOps stack.” | • Introduce **“Guard‑Plus”** – automated multi‑cloud fail‑over and blue‑green deployments. <br>• Offer **partner integrations** (GitHub Actions, GitLab CI, Terraform). <br>• Run a **customer‑success webinar** each quarter showcasing advanced use‑cases; give early‑access beta features. | **Expansion Revenue** – % of paying customers who upgrade to a higher tier or purchase add‑ons within 6 months. <br>*Target*: 30 % (≈ 6 / 21). |

---

## Narrative Flow (Quick Reference)

1. **Aware** – A hosting‑outage news story pushes developers to look for protection.  
2. **Consider** – They receive a free alert, evaluate ROI, and are nudged by a low‑friction trial offer.  
3. **Try** – Guided wizard + sandbox simulation turns curiosity into a concrete migration plan.  
4. **Adopt** – Successful migration triggers a paid subscription; pricing tiers match solo vs. team needs.  
5. **Expand** – Ongoing health monitoring and advanced fail‑over features encourage upsell and advocacy.

---

### Key KPI Dashboard (Monthly)

| KPI | Definition | Goal |
|-----|------------|------|
| **Awareness Reach** | Unique devs who view playbook / attend Space | 1,500 |
| **Consideration Click‑Through** | Alerts → “Learn More” clicks | 20 % |
| **Trial Activation** | Completed “Detect & Plan” flow | 70 % |
| **Paid Conversion** | Trial → paid within 30 d | 15 % |
| **Expansion Upsell** | Paid → higher tier/add‑on in 6 mo | 30 % |
| **NPS (post‑adopt)** | Net Promoter Score after 90 d | > 55 |

---

### Quick Wins for the First 90 Days

| Action | Owner | Timeline |
|--------|-------|----------|
| Publish “Hosting‑Disruption Playbook” + embed in Reddit threads | Marketing | Week 1 |
| Build “Detect My Host” wizard (auto‑parse `Cargo.toml` & `DATABASE_URL`) | Engineering | Week 2‑4 |
| Launch free alert email service (SMTP + simple webhook) | DevOps | Week 3 |
| Record 2‑minute case‑study video (real outage → migration) | Product | Week 4 |
| Set up live onboarding chat (first‑hour free) | Customer Success | Week 5 |
| Release tiered pricing page + annual discount calculator | Business Ops | Week 6 |
| Run first “Guard‑Plus” webinar (beta preview) | Marketing / Eng | Week 8 |

--- 

*Prepared for the host‑migration‑guard product synthesis.*