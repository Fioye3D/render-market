# Design decisions

All rationales below are design hypotheses unless explicitly described as source facts or measured QA.

| Decision | Rationale | Tradeoff / validation needed |
| --- | --- | --- |
| Dark charcoal rather than the guide's original navy | A quieter surround for terracotta, indigo and yellow artwork; selected dark premium direction | Dark UI is not universally preferred; test readability and a future light mode |
| `#5053CA` action background | Distinguishes primary actions while keeping off-white button labels above the selected 4.5:1 contrast target | Confirm every hover, disabled and focus use in Figma |
| Space Grotesk headings, Inter UI | Distinctive large titles with restrained interface text | Test small text, non-Latin scripts and localised content |
| Fold R working identity | Simple geometry relates to digital construction and survives small use | Owner refinement and small-size optical adjustment pending |
| Asset-led homepage | Shows the catalogue's subject before lengthy product claims | Test whether visitors understand what can be obtained |
| African catalogue majority | Fulfils the project's central audience/content goal | West Africa is the first collection, not a stand-in for all Africa |
| Place and cultural context on listings | Helps communicate an interpretation without implying authentication | Consult creators and cultural practitioners; verify naming |
| Three creator steps | Groups basics, files and licence decisions into a readable sequence | No usability study yet; step count may need revision |
| Fictional account entry | Demonstrates onboarding without collecting credentials | Secure production registration remains undesigned |
| Fixed NGN prices | Keeps this demonstration internally coherent | No exchange rates, payouts, tax or multicurrency implementation |

## Grid and rhythm

Desktop: 1440 px reference canvas; 56 px outer content margin; a 12-column reference grid; 24 px standard gutters. Studio uses a 256 px sidebar and content beginning at 304 px. Mobile: 390 px reference canvas, 20 px side margins and 4-column reference grid. Layouts use an 8 px rhythm with 4 px substeps. Main actions are 48 px high; the measured transparent hit targets are at least 24 px in both dimensions.

The shared scene source keeps exported artboards, browser visuals and Figma payload geometry aligned. Figma imports text as native editable text, previews as image fills and repeated buttons/cards as component instances. Screen-level layouts use explicit positions; responsive Auto Layout refinement remains part of the Figma handoff.

## Content decisions

No invented reviews, platform statistics, sales totals or verification. Fictional prices and creator identities are labelled. The catalogue uses original renders; museum reference images were not copied into the project. The technical format is BLEND where an actual Blender source exists. Production claims such as rigged, game-ready, scanned or historically authentic are avoided.

## Everyday Lagos iteration

The new collection follows everyday neighbourhood settings rather than adding unrelated generic assets. The canteen uses painted walls, a tiled splashback, stainless service surfaces and practical seating. The barbershop includes occupied chairs and a waiting area. Church, market, football, school, classroom and food-vendor scenes have separate listings so their contents and scope can be inspected independently.

The homepage keeps Sanctuary Temple as the featured user project and introduces the new collection below it. Library shortcuts find all ten Lagos studies or the five scenes with characters. Search includes descriptions and practical aliases such as “mama put”, “church”, “football field” and “akara woman”. Empty asset-type categories were removed.

Asset pages state character counts, static/non-rigged status, open-cutaway/exterior limits, exact file sizes and the actual included props. Sample prices are adjacent to the real download controls with a no-payment disclosure. This avoids suggesting a functioning checkout.

Shared 512px colour maps, restrained bevels and reusable human base geometry balance scene detail against transfer size. The ten new GLBs measure 0.86–5.57 MiB. This is a measured download-size result; browser frame rate and device performance have not been certified. Reference artboard titles now wrap, and Figma frame placement accounts for the tallest catalogue frame on each page.
