# INITIAL EVALUATION DATASET

Section numbers refer to the knowledge-base documents (IT-KB-001, HR-KB-001, FIN-KB-001, FAC-KB-001, all v1.0).

## A. Single-Domain Queries

### A1. IT (10)

| # | query | expected_domain | expected_section | expected_answer_summary |
|---|---|---|---|---|
| IT-01 | I got a new phone last night and now I can't approve my sign-in prompts. What do I do? | IT | IT-KB-001 §5.4 Setting Up or Changing MFA | Call the Service Desk (ext. 4000). After identity verification you get a 4-hour Temporary Access Code to sign in and enroll the new phone. Reset is not done by email alone. |
| IT-02 | VPN keeps saying authentication failed, but I can open my email fine. | IT | IT-KB-001 §8.1 VPN Authentication Failure | Check ServiceHub sign-in, password expiry, device time, pending MFA prompt or backup code, update client and use "Reset sign-in". If unresolved, raise a P2 ticket with the error text, time and network. |
| IT-03 | I'm on VPN but can't open the shared drive, though the intranet loads. | IT | IT-KB-001 §8.2 VPN Connected but Internal Resources Unavailable | Problem is limited to one resource. Use the full host name, refresh network settings, check the service status banner, and raise an Access ticket or a P2 ticket with diagnostics. |
| IT-04 | How many wrong passwords before I get locked out, and when does it unlock? | IT | IT-KB-001 §5.3 Unlocking a Locked Account | 5 failed attempts lock the account for 30 minutes (or reset your password for immediate unlock). 10 failures in 24 hours is a hard lock needing the Service Desk. |
| IT-05 | I dropped my laptop and the screen cracked. Will I be charged? | IT | IT-KB-001 §5.8 Replacing a Faulty or Damaged Laptop | The first accidental damage in 24 months is replaced at no cost. A repeat or negligent damage is referred to Finance for cost-recovery assessment, and the employee is told before any charge. |
| IT-06 | I left my bag with my laptop on the train. What's the first thing I should do? | IT | IT-KB-001 §5.9 Reporting a Lost or Stolen Device | Call ext. 4000 or 4001 (or 4002) immediately and within 1 hour. File a police report within 24 hours if stolen. IT locks the device, and a loaner is issued within 1 working day. |
| IT-07 | Can I install a free PDF converter I found online? | IT | IT-KB-001 §5.6 / §7.1 | Not without review. Use the Software Catalog; non-catalog software, including free or open-source, needs a Security and licensing review of 5–10 working days. Unapproved software is not allowed. |
| IT-08 | Can I use my own laptop to connect to VPN while mine is being repaired? | IT | IT-KB-001 §7.2 Personal Devices (BYOD) | No. Personal laptops cannot connect to VPN or hold company data. Request a loaner laptop instead. |
| IT-09 | My laptop is four years old and crawling. Can I get a new one? | IT | IT-KB-001 §5.11 Device Refresh | Laptops are refreshed after 4 years at no cost; IT notifies 60 days before. Data is migrated and the old device returned within 10 working days. |
| IT-10 | I got an email asking me to confirm payroll details and I clicked the link. | IT | IT-KB-001 §8.8 Suspected Phishing or Compromised Account | Change password immediately and call Information Security (ext. 4002). Treated as P1. Do not delete the email; use Report Phishing. |

### A2. HR (10)

| # | query | expected_domain | expected_section | expected_answer_summary |
|---|---|---|---|---|
| HR-01 | How many days of annual leave will I get after four years here? | HR | HR-KB-001 §3.1 Annual Leave | 22 working days per year (3 to under 7 years of service). |
| HR-02 | Can I carry unused leave into next year? | HR | HR-KB-001 §3.1 Annual Leave | Up to 5 days carry over and must be used by 31 March; the rest is forfeited. |
| HR-03 | I'm sick today. Who do I tell, and what do I need to log? | HR | HR-KB-001 §5.2 Reporting Sick Leave | Tell the manager before 10:00, log in ServiceHub within 2 working days, upload a certificate for 3+ consecutive days. |
| HR-04 | Do I need a doctor's note for two days off sick? | HR | HR-KB-001 §3.2 Sick Leave | No. A certificate is needed from 3 consecutive working days. |
| HR-05 | I'm still in probation. Can I work from home? | HR | HR-KB-001 §3.4 / §4.2 | Up to 1 day per week with manager approval; 2 days per week after probation. |
| HR-06 | How do I change the bank account my salary goes to? | HR | HR-KB-001 §5.5 Updating Personal and Employment Information | Enter in ServiceHub with bank proof; HR verifies in 3 working days; effective next payroll if verified by the 20th. |
| HR-07 | My partner is expecting in March. What leave can I take and when do I have to tell HR? | HR | HR-KB-001 §3.3 / §5.4 | Secondary caregiver: 4 weeks at full pay (in up to two blocks) if you have 6 months of service. Notify HR at least 8 weeks before. |
| HR-08 | I got sick during my annual leave. Do I get the days back? | HR | HR-KB-001 §6.2 Illness During Annual Leave | Yes, if sick for 3+ consecutive working days with a certificate; notify manager and HR. 1–2 sick days are not converted. |
| HR-09 | When do I have to enroll for health insurance after joining? | HR | HR-KB-001 §5.6 / §3.6 | Within 30 days of joining; a qualifying life event opens a new 30-day window. |
| HR-10 | I forgot to check in last Tuesday when I worked from home. Can it be fixed? | HR | HR-KB-001 §5.7 Correcting Attendance Records | Submit an Attendance Correction within 3 working days of the date; manager approves. Later corrections after the 20th cutoff apply next month. |

### A3. Finance (10)

| # | query | expected_domain | expected_section | expected_answer_summary |
|---|---|---|---|---|
| FIN-01 | I stayed at a hotel during a business trip. How do I claim it? | Finance | FIN-KB-001 §5.2 Claiming a Hotel Expense | Get an itemized folio, create a Lodging claim with dates and rate, attach the folio, reference the Travel Request, remove disallowed items. |
| FIN-02 | What happens if I lost the receipt for my taxi? | Finance | FIN-KB-001 §6.1 Lost Receipt | Submit a Missing Receipt Declaration with substitute evidence. Up to USD 100 per item needs manager approval; limited to 3 declarations per year. |
| FIN-03 | Who approves my expense claim of $1,800? | Finance | FIN-KB-001 §5.6 Approval Workflow | Direct manager, then department head (USD 501–2,500), followed by Finance policy review. |
| FIN-04 | My reimbursement was rejected with code R03. What now? | Finance | FIN-KB-001 §8.1 / §8.2 | R03 means submitted late. Provide justification per deadlines and resubmit within 10 working days; can appeal within 15 working days. |
| FIN-05 | After my claim is approved, how long until the money arrives? | Finance | FIN-KB-001 §5.7 Reimbursement Timeline | Paid in the weekly Thursday run if approved by Tuesday 17:00; funds in about 2 working days; typical total 10 working days. |
| FIN-06 | What's the most I can spend per night on a hotel in a smaller city? | Finance | FIN-KB-001 §4.3 Travel Expense Limits | USD 160 (Tier 2) or USD 120 (Tier 3) per night including taxes, depending on the Travel Desk City Tier List. |
| FIN-07 | My company card was stolen at the airport. | Finance | FIN-KB-001 §5.9 Lost or Stolen Corporate Card | Call the issuer's 24-hour line to block it, tell Finance within 4 hours, review transactions, replacement in 3 working days (2 abroad). |
| FIN-08 | Do I need receipts for meals on a business trip? | Finance | FIN-KB-001 §4.3 / §5.5 | No. Meals are paid by per diem (USD 60 domestic / USD 75 international per full day) without receipts. |
| FIN-09 | I submitted my expenses 45 days after I got back. Will they still be paid? | Finance | FIN-KB-001 §3.5 Submission Deadlines | Possibly. 31–60 days late needs written manager justification and is flagged. |
| FIN-10 | Can I claim a standing desk I bought for working from home? | Finance | FIN-KB-001 §5.11 Other Reimbursable Categories | Yes, under Home Office Setup (USD 300 one-time) with an HR approval reference, receipts, and within 60 days of approval. |

### A4. Facilities (10)

| # | query | expected_domain | expected_section | expected_answer_summary |
|---|---|---|---|---|
| FAC-01 | I lost my access badge this morning. What now? | Facilities | FAC-KB-001 §5.2 Lost, Damaged or Forgotten Badge | Report to Security (ext. 4999). Badge is deactivated; temporary badge for 3 days; replacement within 2 working days; free first time in 12 months. |
| FAC-02 | Can I bring a client to the office tomorrow? What do I need to do? | Facilities | FAC-KB-001 §5.4 Registering a Visitor | Register the visitor in ServiceHub at least 1 working day ahead; visitor brings photo ID; escort at all times; hours 09:00–17:00. |
| FAC-03 | Why did my meeting room booking vanish 15 minutes after the start? | Facilities | FAC-KB-001 §5.5 Booking a Meeting Room | Rooms are released when no check-in occurs within 15 minutes. |
| FAC-04 | The AC on the 3rd floor is freezing cold. Who do I tell? | Facilities | FAC-KB-001 §8.4 HVAC and Temperature | Report in ServiceHub with location and time; the comfort range is 22–24 °C; below 20 °C is P2. Do not adjust thermostats. |
| FAC-05 | I found a wallet in the lobby. | Facilities | FAC-KB-001 §5.9 Lost and Found | Hand it to the Security desk or reception within 1 working day; it is logged and held 90 days as a valuable. |
| FAC-06 | The fire alarm just went off. What should I do? | Facilities | FAC-KB-001 §9.1 Fire Alarm and Evacuation | Leave belongings, use stairs not elevators, go to the assembly point, wait for roll call and the all-clear from Security. |
| FAC-07 | How do I get weekend access to the office? | Facilities | FAC-KB-001 §5.3 Requesting Restricted-Area or After-Hours Access | Manager requests after-hours access in ServiceHub; valid up to 90 days and renewable. |
| FAC-08 | There's water dripping from the ceiling next to my desk. | Facilities | FAC-KB-001 §8.3 Plumbing Issues | Active ceiling leak is P2 (P1 if water is spreading; call ext. 4911). Move equipment away and report in ServiceHub. |
| FAC-09 | I'm hybrid. How do I get a desk? | Facilities | FAC-KB-001 §5.6 Booking a Desk | Book a hot desk in ServiceHub up to 5 working days ahead; check in by badge; released at 10:30 if unused. |
| FAC-10 | Can I plug a small heater in under my desk? | Facilities | FAC-KB-001 §9.6 Basic Safety Rules | No. Personal heaters, kettles and multi-socket extensions are not permitted. |

---

## B. Ambiguous Queries (10)

| # | query | possible_domains | reason_for_ambiguity | expected_behavior |
|---|---|---|---|---|
| AMB-01 | My access isn't working. | IT, Facilities | Could mean system or VPN access (IT) or door and badge access (Facilities) | Ask whether it is a system/VPN access problem or a building badge problem before routing. |
| AMB-02 | I need a new one, mine is broken. | IT, Facilities | "One" could be a laptop, a badge or a chair | Ask what item is broken. |
| AMB-03 | I lost my card. | Finance, Facilities | Could be a corporate card or an access badge | Ask which card; if corporate card treat as urgent after clarification. |
| AMB-04 | How do I get approval for this? | HR, Finance, IT | No object: leave, expense, software or travel | Ask what needs approval. |
| AMB-05 | I need to book something for next week. | Facilities, Finance, HR | Could be a room, desk, travel or leave | Ask what they want to book. |
| AMB-06 | Where is my payment? | Finance, HR | Could be expense reimbursement or payroll | Ask whether it is a reimbursement or salary. |
| AMB-07 | I need equipment for home. | IT, HR, Finance | IT equipment kit, furniture stipend, or approval | Ask whether it is a monitor/peripherals or furniture, and whether a hybrid arrangement is approved. |
| AMB-08 | Something is wrong with my account. | IT, HR, Finance | Contoso Account, HR profile or card/expense account | Ask which account and what is happening. |
| AMB-09 | I'm moving next month. What do I need to do? | HR, Facilities | Personal home move vs transfer to a different office | Ask whether it is a home address change or an office transfer. |
| AMB-10 | The system rejected my request. | IT, HR, Finance, Facilities | No system or request named | Ask what the request was and what message was shown. |

---

## C. Multi-Domain Queries (10)

| # | query | expected_domains | expected_intents | expected_behavior |
|---|---|---|---|---|
| MD-01 | My laptop was stolen on my business trip. What do I do, and will I have to pay for it? | IT, Finance | Report stolen device; understand cost recovery and emergency purchase | Dispatch to IT (§5.9: call within 1 hour, police report, loaner, wipe) and Finance (§6.6 net book value, negligence charges; §7.4 emergency purchase up to USD 800). Combine. |
| MD-02 | I'm starting hybrid work next month. What equipment can I get and how do I claim a chair? | HR, IT, Finance | Hybrid eligibility; equipment kit; stipend claim | HR §3.4 (eligibility, stipend), IT §5.10 (kit), Finance §5.11 (Home Office Setup claim, 60 days). |
| MD-03 | I'm being transferred to Regional Office East. What happens to my badge, laptop and relocation money? | HR, Facilities, IT, Finance | Transfer process; badge update; device delivery; allowance | HR §5.8 (approval and triggers), Facilities §6.2 (badge, desk), IT §5.10 (address update/shipping), Finance §5.11 (USD 3,000 if company-initiated). |
| MD-04 | I'm traveling to another country for work. Do I need approval for VPN, and how do I book the trip? | IT, Finance | Travel Access for VPN; Travel Request and booking | IT §6.3 (Travel Access 5 working days ahead, VPN blocked abroad); Finance §3.2 and §5.1 (Travel Request, Travel Desk, department head for international). |
| MD-05 | A new hire starts Monday. What needs to be arranged? | HR, IT, Facilities | Onboarding tasks for account, laptop, badge and desk | HR §5.9 (onboarding request 5 working days before), IT §6.1 (account, laptop 11:00), Facilities §6.1 (badge 09:30, desk, locker). |
| MD-06 | I'm leaving the company next Friday. What do I need to return and what about my unpaid expenses? | HR, IT, Facilities, Finance | Offboarding returns; final claims | HR §5.10, IT §6.4 (device within 5 working days), Facilities §6.6 (badge on last day), Finance §5.8 / HR §5.10 (final claims by last day, card reconciled). |
| MD-07 | I lost my phone and my corporate card was in the same bag. | IT, Finance | MFA reset; block card | IT §5.4 (Temporary Access Code, MFA re-enroll); Finance §5.9 (block card immediately, tell Finance within 4 hours). Urgent. |
| MD-08 | I'm hosting an external workshop next month: how do I register guests, book a large room and charge the catering? | Facilities, Finance, IT | Visitor registration; large room and event; catering cost center; AV | Facilities §5.4, §5.5, §5.10, §7.3 (over 30 attendees needs 10 working days' notice); Finance §5.11 (cost center); IT for AV equipment. |
| MD-09 | I need to work from my parents' home in another country for two weeks. Is that allowed, and do I need anything for my laptop? | HR, IT | Remote work abroad approval; VPN/Travel Access | HR §7.2 (limit 10 working days per year, 15 working days' notice, manager+HR approval, tax and legal review; two weeks exceeds the limit); IT §6.3 (Travel Access after HR approval). |
| MD-10 | I need a more powerful workstation for my new role. Who pays and how do I get it? | IT, Finance | Early device replacement; cost center | IT §5.11 (early refresh, role-based specification, manager and IT approval); Finance §5.11 context via cost center; charged to department cost center after budget confirmation. |

---

## D. Out-of-Domain Queries (5)

| # | query | expected_behavior |
|---|---|---|
| OOD-01 | What's the weather going to be like in Delhi this weekend? | Say this is outside the supported IT, HR, Finance and Facilities areas; do not use enterprise documents; may suggest a weather service. |
| OOD-02 | Can you write a Python script that sorts a list of numbers? | Decline as out of scope for the employee-request assistant; do not route to IT support. |
| OOD-03 | What's our company's revenue for last quarter? | Not in the knowledge base. Do not invent figures; state no source is available and suggest asking the investor relations or finance leadership. |
| OOD-04 | Can you recommend a good restaurant near the office? | Outside scope; do not fabricate. Optionally mention Facilities provides catering only for approved meetings. |
| OOD-05 | I'm in a dispute with my landlord. Can you advise me legally? | Outside scope; no legal advice. Do not route to HR or Legal; may mention the Ethics and Conduct Line is for workplace misconduct only. |

---

# RAG PREPARATION NOTES

## Recommended Chunking Boundaries

- **Primary unit: the third-level heading (`###`, for example 5.2 or 8.1)**. Each is written to stand alone, repeats key nouns, and mostly runs 80–350 words.
- Keep each **table** with its parent subsection. Tables such as Travel Expense Limits (FIN §4.3), Approval Workflow (FIN §5.6), Annual Leave entitlement (HR §3.1) and Access Zones (FAC §4.1) should not be split from their heading.
- Short sibling sections that belong together (IT §8.3, §8.6, §8.7) can be merged, or kept separate if they are retrieved independently.
- Do not chunk across `##` boundaries. Section 11 (Frequently Needed Information) is a compact lookup chunk and should be indexed whole.
- Prepend each chunk with a breadcrumb: document title, section number, section title, so text like "5.2" and "Claiming a Hotel Expense" travels with the content.
- Optionally index the metadata block as a separate low-weight chunk, or only as fields.

## Fields to Store

Per chunk: chunk_id; document_id; domain; document_title; document_type; version; effective_date; owner_department; confidentiality; intended_audience; section_number; section_title; parent_section_title; content; content_vector; source_file; word_count.

## Fields to Make Filterable

domain, document_id, version, effective_date, owner_department, confidentiality, section_number, document_type. The router should apply `domain` as a filter per downstream call. `version` and `effective_date` support future document updates and rollback.

Searchable (text) fields: content, section_title, document_title. Retrievable: all fields, so answers can cite document_id and section_number.

## High-Value Retrieval Targets

- **IT:** §5.2–5.4 (password, lock, MFA), §5.5 and §8.1–8.2 (VPN), §5.8–5.9 (device damage and loss), §5.6 and §7.1 (software), §5.11 (refresh).
- **HR:** §3.1 (annual leave), §3.2 (sick leave), §3.3 (parental leave), §3.4 (work from home and stipend), §5.5 (profile changes), §5.8–5.9 (relocation and onboarding), §6.2–6.3 (scenarios).
- **Finance:** §4.3 (limits), §5.2 (hotel), §5.6 (approvals), §5.7 (timeline), §5.9 (lost card), §6.1 (lost receipt), §6.6 (company device loss), §8.1 (reason codes), §5.11 (home office, relocation).
- **Facilities:** §5.1–5.2 (badges), §5.4 (visitors), §5.5–5.6 (rooms and desks), §5.7 and §8.1–8.4 (maintenance), §5.9 (lost and found), §9.1–9.2 (emergencies).

## Cross-Domain Chunk Pairs (for router and retrieval testing)

These pairs share subject matter and are what multi-domain queries should retrieve from separate domain indexes:

- Lost device: IT §5.9 with FIN §6.6 and §7.4.
- Home-working equipment: HR §3.4 with IT §5.10 and FIN §5.11.
- Relocation or transfer: HR §5.8 with FAC §6.2, IT §5.10 and FIN §5.11.
- Onboarding: HR §5.9 with IT §6.1 and FAC §6.1.
- Offboarding: HR §5.10 with IT §6.4, FAC §6.6 and FIN §5.8.
- Business travel: FIN §3.2 and §5.1 with HR §6.3 and IT §6.3.
- Remote work abroad: HR §7.2 with IT §6.3.
- Event hosting: FAC §5.4, §5.5, §5.10 with FIN §5.11 and IT §5.5.

## Maintenance Notes

- Keep numbers (limits, deadlines, extensions) consistent across files. The shared values are in `00_context_and_index.md` and the "Frequently Needed Information" sections.
- When adding sections, keep section numbers stable or update the cross-references and `expected_section` values in this evaluation set.
- Add new scenarios inside existing sections where possible rather than creating duplicate policy statements.
