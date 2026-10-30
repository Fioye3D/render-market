# Accessibility review

## Basis

The design uses [WCAG 2.2 contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) as a target: 4.5:1 for normal text and 3:1 for qualifying large text. [Target-size guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) describes a 24 by 24 CSS-pixel minimum with exceptions; the reference-artboard geometry is checked against that minimum, with 48 px primary actions.

Actual computed pairs are recorded in [contrast-report.json](../design/contrast-report.json). Passing these pairs is not a full WCAG conformance claim.

## Implemented in the browser review prototype

- Semantic links/buttons over the visual artboards, with accessible labels.
- Keyboard focus styling, a skip link and labelled text inputs.
- Text equivalents for visual artboard content in a screen-reader section.
- Written error/success messages rather than colour alone.
- Demo navigation dialog with a close control; Escape uses native dialog behaviour.
- Reduced-motion styling.
- Typed search and a written no-results state.
- No real credentials, payment information or file selection.

## Remaining limitations and checks

The browser preview uses reference artboards, not a fully responsive production DOM. At intermediate widths the desktop artboard scales down; nominal design targets are not guaranteed to stay 24 CSS pixels after scaling. Three mobile artboards are provided, but the complete creator flow has not been designed for mobile. A production build should use reflowing semantic HTML instead.

The screen-reader text equivalent preserves information but is verbose. Real screen-reader testing, reading order refinement, 200% zoom/reflow testing, forced-colours testing and disabled/loading-state coverage are pending. Text inside authored SVG exports is not a substitute for an accessible production website.

Figma requires an account import followed by checks of text bounds, fonts, focus annotations and interaction links. Do not claim that the Figma prototype has passed testing until those checks happen.

## Preview descriptions

Courtyard: an original ochre earthen architectural study with an indigo seat. Danfo: a stylised yellow Lagos minibus. Basket: a woven grass-coloured digital basket with a dark handle. Textile: an indigo, cream and gold striped fabric study. Drum: an hourglass drum with tension cords and a curved beater. Lamp: an orange enamel desk-light study.

## v0.3 responsive implementation

The homepage, asset library and asset viewer now use responsive semantic HTML rather than scaled reference artboards. Search/filter/sort/download controls use native elements. The creator flow and supporting reference screens retain the earlier artboard implementation and its stated limits. The 3D viewer includes render fallback, written status, camera presets, reset and wireframe controls. Comprehensive keyboard, screen-reader, mobile GPU and WCAG testing remain pending.

## v0.4 catalogue changes

Catalogue titles and metadata have larger native CSS type sizes. At widths up to 760px, save buttons, discovery chips, filter labels and the sort selector have at least 44px control height. Asset posters have descriptive alt text; the 3D view remains optional. Download sizes, scene contents and static-character limits appear as text, rather than being communicated through imagery alone.

The current iteration was checked through authored render inspection, JavaScript syntax checks, pure catalogue-logic tests and file/format checks. Browser access to the local preview was declined by the browser permission gate during this iteration, so no new browser, keyboard, reflow or screen-reader pass is claimed.
