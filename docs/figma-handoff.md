# Figma handoff and publication

## What is ready locally

- Original SVG reference artboards and PNG design exports.
- Shared design tokens and scene geometry.
- A local development plugin that builds native editable text/shape layers, image fills, button/card components, colour variables, text styles and prototype navigation.
- `design/rendermarket.figmadraft.json`, containing the scenes and embedded original renders. This is **not** a `.fig` file.

## Current verification boundary

The plugin has been prepared against the [official Figma Plugin API](https://developers.figma.com/docs/plugins/api/figma/), including [reaction navigation](https://developers.figma.com/docs/plugins/api/Reaction/). It has not yet been run inside an authenticated Figma editor. Native import, exact typography and prototype behaviour remain unverified until that happens. No Figma file or public prototype is claimed to exist.

## Import into a new file

1. Sign in to Figma and open a new **Figma Design** file. Use the desktop app if the development-plugin import command is not available in the browser.
2. Make Inter and Space Grotesk available to Figma. Open-source font files and their licences are included in `assets/fonts/`. The importer falls back to Inter if a requested family/style is unavailable; verify typography afterward.
3. From Figma's plugin development menu, create a new Figma Design plugin with a custom UI and save its generated files in a new folder. Keep the real plugin `id` Figma assigns in its generated manifest; this project does not invent a Figma plugin identifier.
4. Copy this project's `design/figma-plugin/code.js` and `ui.html` into that generated folder. Merge the fields from `manifest.template.json` into the generated `manifest.json`, preserving Figma's real `id`. The `main`, `ui`, `editorType`, `documentAccess` and `networkAccess` values should match the template. Run **RenderMarket · Portfolio Builder** from development plugins. If needed, import the resulting generated manifest through Figma's development menu.
5. In its file picker, choose `design/rendermarket.figmadraft.json`, then **Build the design file**. The plugin creates new `RM v0.4` pages and preserves existing content. Re-running creates another set; use a new file for a clean import.
6. Inspect the cover, foundations, components, wireframes, screens/prototype and reusable-library pages.
7. On **Screens & prototype**, launch the Buyer or Creator flow. Use the Mobile starting point for the selected buyer adaptations.

## Review before sharing

- Confirm font families and inspect long titles for overlap or clipping.
- Inspect native component instances and edit the working logo.
- Refine screen-level responsive Auto Layout; this importer preserves explicit artboard geometry. Buttons use Auto Layout, while screens/cards retain authored positions.
- Check every primary route, overlays, back paths and flow starting points.
- Confirm culturally specific naming with relevant practitioners; these are digital interpretations.
- Keep “fictional”, “demo”, and “no transaction” disclosures.
- Search/filter/save are fixed Figma examples, with explanatory feedback. Use the browser preview for typed/filtering interactions.

## Publish and record the actual URL

After review, set the intended Figma audience, open the chosen prototype flow and copy its real view link. Test that link in a signed-out/private window as an application reviewer. Add the verified URL to the README. Never replace the status with a guessed Figma URL.

The project owner must review, refine and understand the work before presenting it as evidence of their individual skills. Preserve the assistance disclosure.


## Web viewer boundary

The browser now has responsive marketplace pages, real 3D inspection and actual file downloads. These require the supplied HTTP-served project and bundled Three.js. The Figma import remains a static UI/prototype representation; it does not execute WebGL or the download implementation. There are 108 prepared reference artboards, including asset variants.
