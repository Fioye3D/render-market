# QA log

**Date:** 29 October 2026. These are source/layout checks and a browser walkthrough performed during creation, not target-user research.

## Automated/source checks completed

- Initial draft: 44 artboards and 322 authored interaction targets inspected for valid destinations, supplied images and in-bounds target geometry. Iteration v0.2 retains 44 artboards and passes the same checks for 364 authored interaction targets.
- Reference hit targets checked at a 24 px minimum in both dimensions. This does not guarantee the same CSS size when desktop artboards scale down.
- All six selected normal-text contrast pairs pass 4.5:1: body/canvas 17.05; muted/canvas 9.39; muted/surface 8.58; primary-button label 5.52; accent/surface 9.55; error/canvas 10.41.
- Font-aware artboard export reports zero text extending beyond the right canvas boundary. This is a limited bound check, not a proof of zero overlaps or Figma font parity.
- Browser prototype and Figma importer JavaScript syntax checked.
- All six original artwork files are present, with editable Blender source.

Reports: [contrast pairs](../design/contrast-report.json) and [layout warnings](../design/layout-warnings.json). Re-run `tools/verify_design.py` and `tools/export_previews.py` after revisions.

## Browser walkthrough completed

- Opened the authored desktop homepage and visually inspected hierarchy and artwork.
- Navigated to Explore; typed `danfo`; verified one matching Lagos minibus result.
- Saved that sample, opened its asset detail, reviewed the example licence and reached the explicit no-transaction request acknowledgement.
- Entered the fictional creator studio and opened the listing workflow.
- Removed the title and verified continuation was blocked with a written message.
- Restored a valid title and moved to files/details.
- Attempted to continue without a sample attachment; verified the written requirement.
- Attached the supplied sample and moved to pricing.
- Entered `-20`; verified the price validation blocked preview.
- Entered `25000`; verified the preview displayed `₦25,000`.
- Reached the demo publication confirmation, which explicitly says no real upload or marketplace publication occurred.
- Opened the mobile buyer adaptation and filter dialog; selected Materials and verified the aṣọ òkè-inspired sample was the only visible asset.
- Searched for `no-such-asset` and verified written no-results feedback.

## Corrections made during review

- Revised the initial generic collection so five of six listings reference specific African subjects.
- Added cultural context/reference notes to the creator form and product details.
- Routed each fictional creator link to the matching profile rather than one shared identity.
- Moved the mobile library navigation below expanded result lists.
- Reduced an oversized mobile heading; latest export has no detected right-bound overflow.

## Still pending

Authenticated Figma import/run; native component/text inspection; prototype presentation checks in Figma; signed-out public URL checks; public GitHub creation and Pages deployment; complete mobile creator journey; keyboard-only and screen-reader audit; real creator/buyer usability testing and cultural review.

The Figma importer has not been executed in the actual editor. No native Figma validation or public publication is claimed.

## v0.4 Everyday Lagos and packaging

The catalogue contains 27 entries: Sanctuary Temple, sixteen earlier studies and ten new Lagos scene/prop listings. Five new scenes contain clothed adults in static poses. Character base geometry is credited to MakeHuman CC0. All new venues and characters are fictional.

Completed checks for this iteration:

- All 108 file paths and sizes, GLB headers and ZIP CRCs pass. The original Sanctuary BLEND remains byte-identical to the supplied source.
- The ten new GLBs have valid geometry payloads and embedded colour maps. OBJ archives include their referenced image maps; FBX binaries contain the expected embedded PNG payloads. The largest new GLB is approximately 5.6 MiB. See `design/lagos-asset-audit.json`.
- 108 reference artboards and 985 interaction targets pass destination, image-presence, target-bound and selected contrast checks. Six tested text/background pairs meet the selected 4.5:1 threshold. Font-aware right-canvas checks report zero overflows; this does not establish full text/overlap accessibility.
- Pure catalogue-logic checks cover 27 unique IDs, six named asset searches, discovery of all ten Lagos studies and all five occupied scenes, price sorting and price filtering. These tests do not control a browser.
- Authored scene previews were inspected and character pose/material assignment errors were corrected. Open scene framing was adjusted to keep scene boundaries visible.
- Code/documentation and complete-project archives are prepared separately. ZIP contents are checked for integrity. Large raw OBJ/MTL intermediate files are omitted from the complete archive because the downloadable OBJ ZIPs contain the complete package.

Browser access to the local preview was declined by the browser permission gate. No new browser, mobile GPU, keyboard or screen-reader pass is claimed. Native Figma import and public hosting remain pending. GitHub publication was not performed; the owner requested ZIP files for manual upload.

## v0.3 implementation record

The catalogue now contains 17 entries: one user-supplied Sanctuary Temple scene credited to Adefioye Favour (@fioye_3d), and 16 scripted sample studies. Fifteen entries reference African subjects or settings. No African origin is assigned to the fantasy temple.

Home and Explore are now responsive semantic pages. Asset pages use an actual Three.js GLB viewer and real file links; the creator demonstration and reference artboards remain a more limited design prototype.

Completed checks:

- All 68 download paths/sizes and GLB headers pass. All ZIP files pass CRC checks. The original Sanctuary BLEND copy matches the supplied file byte-for-byte.
- Sanctuary GLB loads in the browser. Overview camera selection and wireframe inspection change the actual viewer state.
- Jiko, a newly added asset, is found by homepage search; its product page exposes four actual file formats and loads an interactive GLB preview.
- Corrected unsupported procedural material colours in the Sanctuary web copy. Re-exported OBJ/FBX from that corrected copy; original BLEND was preserved.
- Baked base-colour textures for the three procedural textile studies into the portable exports.
- Responsive homepage visually inspected; corrected an SVG logo sizing conflict during testing.
- Viewer uses rendering on demand while static, instead of redrawing the scene continuously.

The current source has 78 artboards. Generated reports record the current interaction count and selected contrast/layout checks. Native responsive pages are separately implemented; the static Figma representations do not execute the WebGL viewer. Fullscreen behaviour, a comprehensive mobile GPU matrix, native Figma import, user research and public hosting remain unverified/pending.

## Reference-informed iteration v0.2

Implemented homepage and navigation search, keyword shortcuts, asset-category entry cards, six-item editorial collection, creator storefront highlights, creator/place/software metadata on cards, a place-reference filter, a native three-option sort menu and reorganised asset details with actual included source filenames. Mobile home and courtyard detail screens reflect the same priorities. The creator workflow remains the existing general three-step flow.

Browser checks completed on the changed controls: homepage search for `danfo` returns one matching asset; ascending-price sort puts the ₦6,000 textile first and the ₦24,000 courtyard last; selecting Ghana returns the Bolga basket; its creator link opens Nia Forms. The new source export reports zero right-canvas text overflows. No new user-research outcomes are claimed.
