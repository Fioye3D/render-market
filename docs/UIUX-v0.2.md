# RenderMarket: UI/UX Specification

Version 0.2 | 22 November 2026 | Draft for owner review
Related: TRD-v0.2.md, SAD-v0.2.md, project-story.md

## Product and evidence
RenderMarket by Fioye Studios connects African creative perspectives with reusable digital assets. Proposed initial niche: Blender-ready Nigerian environments and everyday scenes. This is a positioning hypothesis, not validated demand. The current site is a portfolio prototype; working production accounts, checkout and protected delivery are planned. Keep the existing logo. Use the original narrative in project-story.md; never import another designer's personal story or research.

## Users and research plan
Primary hypotheses: Blender artists seeking editable local scenes; game/animation teams seeking optimized environments; Fioye Studios admin publishing owned assets. Interview prospective buyers about their last actual asset purchase, discovery steps, compatibility failures, licence questions and missing local subjects. Avoid leading questions such as whether they like RenderMarket. Record observations separately from interpretations. Test tasks with five representative users per early iteration when feasible; report actual participants and results only. No interview or usability result exists merely because this specification requests it.

## Information architecture
Public: Discover, Explore, Collections, Asset detail, Creator profile, About, Terms, Privacy, Licence information and Help. Account: Sign in, Sign up, Google callback, Email verification, Reset password, Saved assets, Purchase library, Order detail and Profile. Admin: Catalogue, Draft editor, Uploads, Publication review, Orders and Support/refunds. Do not show seller earnings or payout controls in the single-merchant MVP.

## Screen specification
| Screen | Required content and behavior |
|---|---|
| Discover | Prominent search, original Sanctuary feature, real collection rows, asset type navigation, studio endorsement; no invented sales or ratings |
| Explore | URL-persisted query/category/sort, result count, clear filters, pagination; desktop sidebar and accessible mobile filter sheet |
| Collection | Scope/introduction, matching assets, breadcrumbs and return-to-results context |
| Asset detail | Large preview, explicit load-3D control, technical data, creator, included formats/sizes, limitations, price and versioned licence before checkout |
| Creator | Actual creator name/bio and genuine work; label fictional sample creators in prototype; no unearned verification badges |
| Authentication | Labelled email/password fields, Google option, validation, reset, verification and pending/error states; never imply demo login is live |
| Checkout | Server-priced order summary, licence/terms version acknowledgement, hosted-provider handoff; no locally trusted payment success |
| Return/order | Pending verification, confirmed, failed or delayed status; refresh status and support path; no premature download button |
| Library | Purchased items, purchased version/licence, receipt and available formats; expired sessions request sign-in |
| Download | Request access from server; handle unavailable/revoked entitlement, expired grant, network error and retry without repurchase |
| Admin editor | Draft metadata, source upload progress/retry, preview, pricing/licence, rights confirmation, scan status and publish validation |
| About | Original project story, current stage, creator contribution and honest scope |

## Main journeys
Buyer: Discover -> query/filter -> asset -> inspect preview -> review licence -> sign in -> order -> hosted payment -> verification -> library -> authorized download. Preserve intended asset after login; avoid external redirect injection. Payment failure returns to the same order and clearly explains retry.
Admin: Sign in with MFA -> draft -> private upload -> validation/scan -> preview/metadata -> approved price/licence -> publication review -> publish. Failed upload retains safe draft fields. Replacing files creates a new version, not a silent rewrite of purchased files.

## Visual system
Use the current RenderMarket symbol and a restrained by Fioye Studios endorsement. Dark neutral surfaces (#0a0a0a, #171717), off-white text (#fafafa), muted text with verified contrast, blue action accent (#2563eb). These are proposed implementation tokens; verify contrast in actual combinations. Spacing scale: 4,8,12,16,24,32,48,64px. Body 16px/24px; labels 14px/20px; page headings 32px/40px desktop and 28px/36px mobile. Reuse local font assets, with system fallback and swap. Search pill retained; controls use consistent 8px radius and cards 12px. Existing earlier exclusion list was superseded by the user's explicit design reset; retain subsequent user choices: no header dropdown arrows, exclusive dropdown expansion, no intrusive square loading patterns.

Components: header, exclusive text-labelled disclosure menus, breadcrumbs, search, filter group, sort, asset card, collection row, pagination, viewer controls, price/licence panel, form field, status message, upload item, order status and confirmation dialog. Define default/focus/disabled/pending/error states. Save action exposes pressed state and meaningful accessible name. Critical actions must not depend on hover.

## Loading and perceived performance
Server-render useful route-specific content. No full-page grey block startup gate. Preserve dimensions while images load; plain neutral media surface only, no patterned overlay hiding loaded images. Prioritize the first visible previews; lazy-load below-fold media. Keep listing thumbnails small and responsive; defer viewer code/GLB until requested. Inline field/action progress rather than blanking the entire page. Provide a recoverable error message when a real request fails. Measure cold-cache mobile and desktop performance rather than claiming instant loading.

## Responsive and accessibility requirements
Design and verify at 390,768,1024 and1440px plus 320px reflow. Desktop result grid adapts to available width; mobile uses readable cards and filter drawer. Collection shelves support touch and keyboard with visible focus and clear browse-all alternatives. Header navigation remains reachable on mobile. WCAG2.2AA target: semantic landmarks/headings, labelled inputs, text contrast >=4.5:1 for normal text, meaningful alt text, keyboard operation, announced errors/status and reduced-motion preference. Target44px primary controls. Viewer has static image and technical text fallback. Dialogs trap focus, close with Escape and restore focus. Dropdown state must expose expanded/collapsed semantics.

## Content and trust
No fabricated research, reviews, counts, sales, scarcity, compatibility or authenticity claims. Counts derive from published database entries. Prices and licences must be approved; Sanctuary300000NGN. Rural studies remain labelled procedural interpretations. Do not portray generic models as authenticated cultural replicas. Include technical quality limitations and compatible tested software versions. Clearly distinguish preview GLB from paid source. Demo material must never be sold without rights/quality review.

## Usability acceptance and handoff
Tasks: find a Lagos scene, narrow by category, inspect technical details, understand licence, sign in, complete test payment and download a purchased format. Test keyboard-only access, slow connection, failed payment, delayed webhook, expired session and unavailable file. Record task completion, errors and participant feedback; set improvement targets after baseline. Before launch all critical purchase/access tasks must complete without unresolved blocking defects. Handoff includes editable design source, component/state inventory, annotated desktop/mobile screens, flow diagrams, content, tokens, API-state mapping and accessibility notes. These artifacts are deliverables to create; this document does not claim Figma screens exist.

## Requirement mapping
Discovery/detail -> CAT-01/02 and VIEW-01. Account -> AUTH-01/02. Saved -> SAVE-01. Admin -> ADM-01/UP-01. Checkout/status -> PAY-01/02/03. Library/download -> LIB-01/DL-01. Policies -> LEG-01. Refund support -> REF-01.
