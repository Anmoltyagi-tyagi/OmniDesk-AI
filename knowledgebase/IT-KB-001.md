**Metadata**

| Field | Value |
|---|---|
| document_id | IT-KB-001 |
| domain | IT |
| document_title | IT Knowledge Base — Technology Services and Support |
| document_type | Knowledge Base / Policy Manual |
| version | 1.0 |
| effective_date | 2026-10-01 |
| owner_department | Information Technology |
| confidentiality | Internal — Employees and Contractors Only |
| intended_audience | All Contoso Enterprise employees and contractors |

> Synthetic document for the fictional organization Contoso Enterprise. Not a real corporate policy.

# IT Knowledge Base — Technology Services and Support

## 1. Purpose

This document describes how Information Technology (IT) at Contoso Enterprise provides, secures and supports the technology that employees and contractors use to work. It explains how to sign in, recover access, connect remotely, obtain and replace devices, request software, and get help when something breaks.

## 2. Scope

This document applies to all employees and contractors who use a Contoso Account or a Contoso-managed device. It covers the Contoso Account and password, multi-factor authentication (MFA), remote access through Contoso Secure Access (VPN), laptops and peripherals, software, meeting-room audio-visual equipment, network and Wi-Fi, and security incidents involving technology.

It does not cover physical building access (see FAC-KB-001), financial treatment of lost or damaged equipment and software chargebacks (see FIN-KB-001), or leave and remote-work eligibility (see HR-KB-001).

## 3. General Policy

### 3.1 Contoso Account and Managed Devices

Every employee receives one Contoso Account (first.last@contoso.example). Accounts are personal and must never be shared. IT never asks for a password by email, chat or phone. Work must be performed on Contoso-managed devices. Work files must be stored in company cloud storage and not only on the local disk, because local-only files may be lost when a device is replaced or wiped.

Password rules: minimum 14 characters, cannot reuse any of the last 10 passwords, and expires every 180 days. ServiceHub and email reminders are sent 14 days before expiry.

### 3.2 Acceptable Use

Company technology is for business use, with limited personal use that does not affect work or security. The following are prohibited: installing unlicensed or unapproved software, disabling security tools, connecting unapproved storage devices or remote-access tools, sharing credentials, and storing company data in personal cloud accounts.

### 3.3 Service Hours and Priorities

The IT Service Desk operates Monday–Friday 08:00–19:00. Outside these hours, only P1 incidents are handled, through ext. 4001 (critical after hours) or ext. 4002 (Information Security).

| Priority | IT examples | Initial response | Resolution target |
|---|---|---|---|
| P1 | Site-wide or company-wide outage, confirmed security incident, lost or stolen device, suspected account compromise | 30 minutes | 4 working hours |
| P2 | One person cannot work and has no workaround (broken laptop, locked out after self-service fails, VPN failure with no alternative) | 2 working hours | 1 working day |
| P3 | Degraded service with a workaround, software request from the catalog | 1 working day | 3 working days |
| P4 | How-to questions, minor issues, non-catalog requests | 2 working days | 5 working days |

Lost or stolen devices and suspected account compromise are always treated as P1.

## 4. Eligibility and Applicability

### 4.1 Remote Access (VPN)

All employees may use VPN from a Contoso-managed laptop. Contractors receive VPN access only when their sponsoring manager requests it in ServiceHub and the contract allows it. VPN is not available from personal devices. VPN is blocked by default from outside the country of the employee's office (see Section 6.3).

### 4.2 Device Entitlement

Each employee receives one standard laptop. Roles needing higher specifications (for example Engineering) receive an engineering laptop. Contractors receive a laptop only if their contract states it; otherwise they use a managed virtual desktop. Replacement is governed by the 4-year refresh cycle (Section 5.11), by faults and damage (Section 5.8), and by loss (Section 5.9).

### 4.3 Software Entitlement

Software in the Software Catalog (ServiceHub > IT > Software Catalog) is pre-approved. Anything else requires a request and review (Section 5.6). Persistent local administrator rights are not granted.

## 5. Procedures

### 5.1 Submitting an IT Ticket

1. Open ServiceHub, choose **IT**, and select the closest category (Account, Device, Software, Network, Access, Security, Other).
2. Describe the problem, when it started, what you tried, and the exact error message. Attach a screenshot.
3. Select priority. Choose P2 only if you cannot work and have no workaround.
4. Submit. You receive a ticket number beginning IT- and updates by email.

Emailing it-support@contoso.example creates a P3 ticket. Phone (ext. 4000) is for urgent issues and P1. If ServiceHub is unreachable, call ext. 4000.

### 5.2 Resetting a Forgotten Password

1. Go to the Account Recovery page from any device and enter your Contoso Account.
2. Verify your identity with Contoso Authenticator (MFA) or a registered recovery method.
3. Choose a new password that meets the rules in Section 3.1.
4. Connect your laptop to the office network or VPN, then lock and unlock the laptop so it picks up the new password.

If you cannot complete verification because you have no MFA method, follow Section 5.4 (MFA reset) or call the Service Desk at ext. 4000.

### 5.3 Unlocking a Locked Account

An account locks automatically after 5 failed sign-in attempts and unlocks by itself after 30 minutes. You can unlock immediately by completing a self-service password reset (Section 5.2).

After 10 failed attempts within 24 hours, the account is hard-locked and only the IT Service Desk can unlock it. The agent verifies identity using your Employee ID, a callback to your registered phone number, and, if the callback fails, confirmation from your manager. Once identity is verified, unlock is completed within 30 minutes.

### 5.4 Setting Up or Changing MFA

All Contoso Accounts require MFA using the Contoso Authenticator app on a phone. Sign-in prompts use number matching: type the number shown on the screen into the app.

- **First setup:** enroll on first sign-in. At enrollment, 10 single-use backup codes are generated; store them securely.
- **New phone, old phone still available:** before wiping the old phone, open Security Info in your account settings, add the new phone, then remove the old one.
- **Old phone lost, broken or wiped:** call the Service Desk (ext. 4000). After identity verification (Section 5.3), the agent issues a Temporary Access Code valid for 4 hours. Use it to sign in and enroll the new phone. MFA is never reset on the basis of an email request alone.
- **Hardware security keys** are issued to privileged IT administrator roles and are not available as a general alternative.

### 5.5 Connecting to VPN

VPN uses the Contoso Secure Access client, preinstalled on managed laptops.

1. Open Contoso Secure Access and select the profile **Contoso-Corporate**.
2. Sign in with your Contoso Account and approve the MFA prompt.
3. Wait for status "Connected".

VPN is needed outside Contoso offices for internal web applications, file shares, code repositories and internal databases. ServiceHub, email and chat are cloud-hosted and do not require VPN. VPN is not needed in the office. Sessions end after 10 hours, or after 60 minutes of inactivity.

### 5.6 Requesting Software

1. **Catalog software:** install it yourself from the Software Catalog. If it needs a license, submit a Software Request in ServiceHub. Your manager approves, and you must name the cost center that will pay the license. Target: 2 working days. License costs are charged to the department cost center (see FIN-KB-001 Section 5.11).
2. **Non-catalog software:** submit a Software Request with vendor, purpose, data it will handle and business justification. IT Security and licensing review takes 5–10 working days. Free or open-source software also requires review.
3. **Temporary admin rights** for approved development tools are granted through the elevation tool for up to 4 hours at a time.

Licenses unused for 90 days are reclaimed.

### 5.7 Requesting Access to Systems and Shared Resources

Submit an Access request in ServiceHub naming the system, role needed and business reason. Both your manager and the system owner must approve. Target: 3 working days. Access is reviewed within 5 working days of any role change.

### 5.8 Replacing a Faulty or Damaged Laptop

1. Submit a P2 ticket (category Device) or visit the IT Service Desk, HQ Building A ground floor.
2. IT diagnoses within 1 working day.
3. If the fault is a hardware defect, covered by warranty, or normal wear, the laptop is replaced at no cost.
4. A loaner laptop is available the same day at HQ. Regional offices receive a loaner by next-working-day courier.
5. IT restores work data synced to company cloud storage. Local-only data may not be recoverable.

For accidental damage (cracked screen, liquid spill, drop): the first incident in any 24-month period is replaced at no cost. A second or later incident within 24 months, or damage caused by negligence, is referred by IT to Finance for a cost-recovery assessment (see FIN-KB-001 Section 6.6). The employee is told before any charge is applied.

### 5.9 Reporting a Lost or Stolen Device

Report immediately, and within 1 hour of noticing the loss.

1. Call ext. 4000 (ext. 4001 after hours) or Information Security at ext. 4002.
2. If the device was lost inside a Contoso office, also tell the Security desk (ext. 4999) so it can be checked against found items (FAC-KB-001 Section 5.9).
3. If stolen, file a police report within 24 hours and add the reference number to the ticket.
4. IT locks the device and revokes sessions at once. If the device is not recovered within 24 hours, or if theft is confirmed, it is remotely wiped.
5. A loaner is issued within 1 working day. If your phone with Contoso Authenticator was also lost, follow Section 5.4.
6. When the incident is closed, IT sends the details to Finance to record the asset write-off and, where applicable, assess cost recovery (FIN-KB-001 Section 6.6).

**Lost abroad:** the IT Service Desk Lead may pre-approve an emergency local purchase of a replacement device up to USD 800. The employee must quote the IT ticket number when claiming it as "Emergency IT Equipment" (FIN-KB-001 Section 7.4).

### 5.10 Requesting Remote Work Equipment

Employees whose work-from-home arrangement has been approved by HR (HR-KB-001 Section 5.3) may request the Remote Work Equipment Kit: a 24-inch monitor, keyboard, mouse, headset and laptop stand.

1. Submit a ServiceHub request (IT > Remote Work Equipment) quoting the HR approval reference.
2. Confirm that your home address in your HR profile is current. The kit ships there within 5 working days.
3. Equipment remains Contoso property. Return it within 5 working days of the end of the arrangement or employment, using the prepaid courier label.

IT does not provide desks, chairs or printers for home use. Furniture is covered by the home office stipend (HR-KB-001 Section 3.4). IT-equipment purchased independently is not reimbursed. IT does not support home routers but can provide connectivity guidance.

### 5.11 Device Refresh (End-of-Life Replacement)

Laptops are refreshed after 4 years. IT notifies the employee 60 days before eligibility. IT migrates data, issues the new laptop at no cost to the employee, and the old device must be returned within 10 working days. Early refresh needs a documented performance problem or role change, approved by the manager and IT. A device above the standard specification requested for a role is charged to the department cost center after Finance confirms budget.

## 6. Common Scenarios

### 6.1 New Employee Setup

Once HR submits the onboarding request (at least 5 working days before the start date; see HR-KB-001 Section 5.9), IT creates the Contoso Account 3 working days before the start date and prepares the laptop. On day 1 the employee collects the laptop at the IT Service Desk at 11:00 (regional offices: shipped to the office 2 working days before). The employee signs in, sets a password and enrolls in MFA within 24 hours. If the laptop is not ready, IT issues a loaner. If the account does not work on day 1, call ext. 4000.

### 6.2 Changing Phone with MFA

Follow Section 5.4. Add the new phone while the old phone still works. If the old phone is gone, the Service Desk issues a 4-hour Temporary Access Code after identity verification.

### 6.3 Working While Traveling

Domestic business trips: VPN works as normal. International trips: VPN is blocked outside the home country by default. Submit a **Travel Access** request in ServiceHub at least 5 working days before departure with destination, dates and manager confirmation. For destinations on the Information Security high-risk list, IT issues a clean loaner laptop. Use VPN on public Wi-Fi. Working remotely abroad as a personal arrangement also needs HR approval (HR-KB-001 Section 7.2); submit the Travel Access request only after HR approval. If a device is lost abroad, see Section 5.9.

### 6.4 Role Change or Leaving the Company

On a role change, access is reviewed within 5 working days. On leaving, the Contoso Account is disabled at 18:00 on the last working day and the device must be returned within 5 working days (a prepaid courier label is provided). Badge return is handled by Facilities (FAC-KB-001 Section 6.6).

## 7. Exceptions

### 7.1 Unsupported Software

The following are not supported and may not be installed: unlicensed or cracked software, peer-to-peer file sharing, cryptocurrency miners, unapproved remote-access tools, consumer cloud storage clients, and software that disables security controls. A security exception can be requested through Information Security with business justification; approved exceptions last 6 months and are then reviewed.

### 7.2 Personal Devices (BYOD)

Personal phones may be used for Contoso Authenticator, chat and email through approved apps. Personal laptops and tablets may use only web-based applications and cannot connect to VPN or hold company data. A personal laptop cannot be used while your own laptop is being repaired; request a loaner instead (Section 5.8).

### 7.3 Contractors

Contractor accounts expire on the contract end date and are sponsored by a manager. Contractors may not request software or hardware directly unless the contract provides for it.

### 7.4 Urgent After-Hours Issues

Only P1 issues receive after-hours support. A single employee's laptop failure outside service hours is logged as P2 and handled the next working morning.

## 8. Troubleshooting

### 8.1 VPN Authentication Failure

Symptoms: "Authentication failed", "Credentials rejected", or no MFA prompt appears.

1. Sign in to ServiceHub in a browser with the same account. If that fails, the problem is the password or a lock; use Section 5.2 or 5.3.
2. Check whether your password was changed or has expired.
3. Confirm the laptop date and time are set automatically.
4. Open Contoso Authenticator manually and look for a pending prompt. If none appears, use a backup code.
5. Update the client from the Software Catalog, then restart it. Use "Reset sign-in" in the client menu to clear cached credentials.
6. If it still fails, raise a P2 ticket with the error text, time, location and network type.

### 8.2 VPN Connected but Internal Resources Unavailable

1. Confirm the client shows "Connected" with profile Contoso-Corporate.
2. Open https://intranet.contoso.example. If it loads, the problem is limited to one resource.
3. Use the full internal host name instead of a short name.
4. Disconnect other VPN or proxy software. Use "Refresh network settings" in the client menu, then restart the laptop.
5. Check the ServiceHub service status banner for a known outage.
6. If only one application fails, raise an Access ticket for the application owner (Section 5.7). If everything internal fails, raise a P2 ticket with the URL, time, a screenshot and the client's "Export Diagnostics" file.

### 8.3 Slow or Disconnecting VPN

Prefer a wired or 5 GHz Wi-Fi connection, avoid video streaming while on VPN, and use cloud-hosted tools without VPN when possible. Restart the client if disconnections continue and raise a P3 ticket with the times of disconnection.

### 8.4 MFA Prompt Not Arriving or Failing

Check the phone has internet and notifications enabled, open the app manually, and make sure phone time is automatic. Enter the number shown on screen exactly. Use a backup code if available. Three failed MFA attempts lock MFA for 15 minutes. If the phone is lost, follow Section 5.4. If you receive an MFA prompt you did not trigger, deny it and report it to Information Security (ext. 4002) as a possible compromise.

### 8.5 Laptop Does Not Start or Is Very Slow

Charge with the official charger for 30 minutes, then hold the power button for 15 seconds and restart. Restart weekly and apply pending updates. Security updates install automatically; restart prompts may be deferred up to 3 times before a forced restart within 24 hours. If the laptop still fails, follow Section 5.8.

### 8.6 Wi-Fi and Network Problems in the Office

Managed laptops connect to **Contoso-Secure** automatically. **Contoso-Guest** is for visitors and personal phones with limited access; guest credentials are printed on visitor badges. If Wi-Fi fails, forget and rejoin the network, then try another floor or the wired dock. Raise a P3 ticket with location, time and device.

### 8.7 Email and Calendar Not Syncing

Check the connection, sign out and in again, and confirm the password has not expired. Free mailbox space if full. Raise a P3 ticket if the issue lasts more than 1 hour.

### 8.8 Suspected Phishing or Compromised Account

Do not click links or open attachments. Use the Report Phishing button, or forward the email to phishing@contoso.example. Do not delete the email. If you clicked a link or entered a password, change your password immediately (Section 5.2) and call Information Security at ext. 4002. This is a P1 security incident.

### 8.9 Printing

Printers are named by building and floor. Add one from the Software Catalog (Printers). Queue and driver problems go to IT. Paper and toner are supplied by Facilities (FAC-KB-001 Section 5.7).

## 9. Escalation

### 9.1 Escalation Path

1. **IT Service Desk (Level 1):** initial triage and common fixes.
2. **IT Support Specialists (Level 2):** device, network and application support.
3. **IT Operations Manager (Level 3):** unresolved or repeated incidents and target breaches.
4. **Director of IT:** unresolved P1 or P2 issues with significant business impact.

### 9.2 When to Escalate

Use the Escalate action on your ServiceHub ticket after the initial response target has been missed, or when the issue returns after being closed. If there is no progress 2 working days past the resolution target, email the IT Operations Manager through it-support@contoso.example with the ticket number.

### 9.3 Security Incident Escalation

Suspected compromise, lost devices and phishing responses go directly to Information Security at ext. 4002 (24/7) or security@contoso.example. They are never held for normal queue handling.

## 10. Support Channels

| Channel | Use for |
|---|---|
| ServiceHub (IT category) | All non-urgent requests and incidents |
| it-support@contoso.example | Creates a P3 ticket |
| Phone ext. 4000 | Urgent issues; Mon–Fri 08:00–19:00 |
| Phone ext. 4001 | Critical (P1) after hours |
| Phone ext. 4002 | Information Security, 24/7 |
| IT Service Desk, HQ Building A ground floor | Walk-up help, loaners, laptop handover |

## 11. Frequently Needed Information

| Item | Value |
|---|---|
| Password | 14+ characters, expires every 180 days, last 10 not reusable |
| Account lock | 5 failed attempts = 30-minute lock; 10 in 24 h = hard lock (Service Desk only) |
| MFA app | Contoso Authenticator (number matching); 10 backup codes |
| Temporary Access Code | Valid 4 hours after identity verification |
| VPN | Contoso Secure Access, profile Contoso-Corporate; 10-hour session, 60-minute idle limit |
| Wi-Fi | Contoso-Secure (managed devices), Contoso-Guest (visitors) |
| Laptop refresh | Every 4 years |
| Lost device report | Within 1 hour; police report within 24 hours if stolen |
| Emergency device purchase abroad | Up to USD 800 with IT pre-approval |
| Software request (catalog license) | 2 working days |
| Software request (non-catalog) | 5–10 working days |
| Access request | 3 working days |
