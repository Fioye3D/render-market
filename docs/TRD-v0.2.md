# RenderMarket: Technical Requirements Document

Version 0.2 | 22 November 2026 | Draft for owner review
Owner: Adefioye Favour / Fioye Studios

## 1. Purpose and current state
RenderMarket, by Fioye Studios, is a digital asset marketplace for African creative work. The current public site is a static portfolio prototype. Accounts, verified payments and protected delivery are not implemented. This document specifies the proposed production release; it does not claim these capabilities exist.

## 2. Release boundary
Recommended MVP: one merchant, Fioye Studios, with admin-managed listings and registered buyers. This scope requires owner agreement before implementation. Include responsive browsing, search/filter/sort, actual 3D previews, email and Google authentication, checkout in NGN, purchase library, private downloads and administration. Exclude third-party seller onboarding, split payouts, commissions, subscriptions, reviews, chat, mobile applications and automated 3D conversion. Creator marketplace features remain a later phase.

## 3. Roles
Visitor: view published listings and public previews. Buyer: manage own profile, saved assets, orders and purchased downloads. Admin: manage listings, source files, prices, publication and support/refund operations. Role changes must require privileged server authorization; a user cannot edit their own role.

## 4. Functional requirements and acceptance
| ID | Requirement | Acceptance condition |
|---|---|---|
| AUTH-01 | Email/password, verification, reset and Google OAuth | Successful verified account can sign in/out; invalid/expired callbacks fail safely; no password or token logged |
| AUTH-02 | Server-side session authorization | Unauthenticated protected request returns 401; another buyer's resource returns 403 or 404 |
| CAT-01 | Paginated catalogue with search, category and sort | Shared URLs reproduce filters; empty/error states work; unpublished assets are inaccessible |
| CAT-02 | Accurate listing details | Price, creator, licence version, included files, sizes and preview limitations shown before checkout |
| VIEW-01 | Load optimized GLB only on explicit request | Initial listing fetches no GLB; progress, cancellation/failure and static fallback available |
| SAVE-01 | Buyer saved assets | Unique user/asset pair; persisted across sessions; accessible only to owner |
| ADM-01 | Admin drafts, versions and publication | Publication blocked until approved licence, rights confirmation, clean files, preview and price exist |
| UP-01 | Private resumable source uploads | Server validates admin, size and allowed formats; hash/size confirmed; rejected files never published |
| PAY-01 | Server-created hosted checkout | Client-supplied prices ignored; server records immutable NGN amount and licence snapshot |
| PAY-02 | Verified payment fulfilment | Signed webhook and provider verification match reference, successful status, amount, currency and environment before entitlement |
| PAY-03 | Idempotency and recovery | Duplicate/concurrent events produce one fulfilment; abandoned/late payments reconciled without duplicate charging |
| LIB-01 | Purchase library and receipt | Only fulfilled items appear; pending/failed/refunded states explained |
| DL-01 | Entitlement-controlled download | Server checks session, item, entitlement and approved version; grants a 60-second signed URL; no public source URL |
| REF-01 | Refund/dispute processing | Admin action audited; provider result reconciled; confirmed refund revokes future download grants under approved policy |
| LEG-01 | Versioned terms, privacy and licences | Acceptance version/time recorded at checkout; receipt retains purchased rights snapshot |

Sanctuary Temple owner-set list price: NGN 300,000 (30,000,000 kobo). Other existing prices are proposed, not approved production prices. No generated study becomes sale-ready solely because it appears in the prototype.

## 5. Non-functional requirements
Targets, not measured results: WCAG 2.2 AA; keyboard-accessible menus/forms/viewer fallback; 44px primary touch targets. At mobile p75 target LCP <=2.5s, INP <=200ms and CLS <=0.1, measured with real-user telemetry when sufficient traffic exists. Before launch use repeatable cold-cache mobile lab checks on home, search and listing pages. Server-render useful HTML; no full-page skeleton gate. Responsive image sizes, compressed WebP/AVIF, reserved dimensions, long cache lifetimes for versioned public media. Initial route compressed first-party JS budget <=200KB excluding on-demand viewer. Catalogue API p95 <=500ms under 50 concurrent browsing clients in a documented staging load test. Availability objective 99.5% monthly excluding provider outages; monitor external dependency health separately.

Security: TLS, secure HttpOnly session cookies, CSRF/origin checks for mutations, RLS, schema validation, parameterized queries, rate limits, admin MFA, no secret/service-role key in frontend. Hosted payment UI; never store card data. Scan uploaded archives/files and enforce decompressed size/path limits. Logs redact secrets, signed URLs and payment payload PII. Session expiration must block new grants. Signed URLs are bearer links until expiry; downloaded files cannot be recalled.

## 6. Data requirements
PostgreSQL stores identities/references, catalogue metadata, prices, immutable order snapshots, payment attempts, entitlements and audit history. Object storage holds media and binaries. All money is integer minor units with explicit currency. UTC timestamps; presentation localized. UUID internal IDs, unique asset slugs and provider references. Retention/deletion rules for personal data, financial records and audit logs must be approved before launch; do not assume deleting an auth account deletes statutory records.

## 7. Validation and release gates
Integration tests: two-buyer isolation, admin access denial, unpublished asset denial, source bucket anonymous denial, expired/revoked download denial, duplicate/out-of-order webhook, forged signature, altered amount/currency, provider timeout, successful delayed payment and refund reconciliation. End-to-end staging journey: signup, sign-in, browse, test checkout, purchase library, all included formats. Test responsive layout at 390px and 1440px. Restore database and one asset from backup in staging. No live launch until merchant approval, rights/licences/prices, domain/email, private storage, alerts and restore verification pass.

## 8. Decisions and dependencies
Proposed: Next.js/TypeScript, Supabase Postgres/Auth/Storage, Paystack hosted checkout, managed Next.js deployment and transactional email provider. Hosting/storage tiers must be selected against maximum file sizes, egress and budget. Google Pay is not promised: available channels depend on approved provider, merchant and buyer context. Outstanding: legal merchant identity, domain, monthly budget, refund policy, licence text, tax handling, support address, maximum upload size and production catalogue. No merchant accounts or infrastructure created by this document.

## 9. Implementation sequence
1. Inventory public files and rights; approve MVP and data model.
2. Build responsive server-rendered frontend, database migrations and auth/RLS.
3. Build private admin upload/publication and preview pipeline.
4. Integrate test payments, fulfilment, purchase library and downloads.
5. Complete security/accessibility/performance/restore checks, then controlled live launch.

## References
- https://paystack.com/docs/payments/verify-payments/
- https://paystack.com/docs/payments/webhooks/
- https://supabase.com/docs/guides/storage/security/access-control
- https://supabase.com/docs/guides/storage/buckets/fundamentals

## Revision 0.2: narrative, positioning and evidence
RenderMarket is by Fioye Studios. It began as an independently initiated portfolio project and is transitioning toward a commercial product. The proposed initial niche is Blender-ready Nigerian environments and everyday scene kits; this positioning is a hypothesis pending owner approval and buyer research. African creative work remains the broader direction. Existing competitors mean no first/only/largest claims are permitted. No competitor narrative, research findings or operating metrics may be presented as RenderMarket evidence.

Discovery gate before commercial launch: interview at least five prospective buyers across animation, games and visualization; record consent, workflow, missing assets, format requirements and willingness-to-pay evidence. Do not treat the interview count as proof of demand. Summarize actual findings and update priorities. Review launch catalogue quality and licences separately from research.

MVP remains single merchant, with Fioye Studios managing publication. Third-party creator selling and payouts remain deferred. Sanctuary Temple remains NGN300000; all other proposed prices require approval. UI/UX specification: UIUX-v0.2.md. Project narrative: project-story.md.
