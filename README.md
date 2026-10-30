# RenderMarket

**A digital asset marketplace concept for African creatives.**

RenderMarket explores how 3D artists, animators and digital designers can showcase their work, help buyers inspect assets and share creative resources. The catalogue centres African objects and contemporary settings, from a Lagos canteen and barbershop to textile studies, market props and food scenes.

Created by **Adefioye Favour** · [GitHub](https://github.com/Fioye3D) · [Instagram](https://www.instagram.com/fioye_3d/)

> **Local project scope:** The complete media and model files have been restored to this Desktop folder. It now includes rendered images, fonts, editable Blender scenes and downloads. Any earlier code-only archive or GitHub commit requires these restored resources to show the complete prototype.

## Why this project exists

RenderMarket connects my interest in Blender and 3D creation with UI/UX design. It explores a marketplace where African creatives can present culturally relevant work with clear previews, understandable technical information and straightforward navigation.

This is a self-initiated portfolio project started in October 2026. It is separate from my Access Youth Tech Forge competition proposal.

## Experience and visual direction

The interface uses charcoal surfaces, off-white typography, blue controls and large asset previews. Desktop layouts and selected mobile screens share reusable colours, spacing, typography and components.

| Area | Implementation |
| --- | --- |
| Discovery | Responsive homepage, catalogue, search, filters and price sorting |
| Asset review | Product details, creator attribution, sample pricing and licensing information |
| 3D inspection | Three.js viewer with orbit, zoom, camera presets and wireframe controls; model files required |
| File delivery | Links for BLEND, GLB, OBJ and FBX; downloadable files supplied separately |
| Creator journey | Registration, dashboard, upload, pricing and demo publication screens |
| Design system | Tokens, component specifications, reference artboards and Figma import source |

The catalogue data describes **27 listings**, including an **Everyday Lagos** collection of ten scenes and props. Artwork and model files are included in this complete local folder.

## Featured work: Sanctuary Temple

Sanctuary Temple is my supplied Blender scene and the featured portfolio listing. The complete project includes its original Blender file and separate optimized exports for browser inspection and other workflows.

The scene is credited independently from the scripted catalogue studies. Its ownership and usage terms are separate from the source-code licence. No commercial-use licence has been specified for it.

## Main journeys

**Buyer:** Homepage → Explore → Search and filter → Asset details → Review preview, formats and licensing → Download available portfolio files.

**Creator:** Register → Dashboard → Upload → Add previews and metadata → Set sample pricing and licensing → Preview → Demo publication.

Payments, authentication, seller payouts and persistent publishing are not implemented. Prices and the fictional sample creator identities are demonstration content.

## Run locally

You need Python 3 and a modern browser. No npm installation is required to serve the interface; Three.js is bundled locally.

```bash
git clone https://github.com/Fioye3D/render-market.git
cd render-market
python -m http.server 8765
```

Open **http://localhost:8765/prototype/**. On Windows, `py -m http.server 8765` is an alternative.

On Windows, double-click **Start-Prototype.cmd** to start the preview after it has stopped. Keep its window open. The viewer requires an HTTP server; opening the HTML directly from disk is insufficient.

For a phone on the same Wi-Fi, replace `localhost` with the computer's Wi-Fi IPv4 address, such as `http://10.4.9.145:8765/prototype/`. That address can change. The server binds to all interfaces; Windows Firewall and Wi-Fi isolation may affect access from other devices. A public hosted link is still pending.

## Repository guide

```text
render-market/
├── prototype/       HTML, CSS, JavaScript and bundled viewer dependencies
├── design/          Design tokens, catalogue data, reference scenes and Figma plugin source
├── docs/            User flows, design decisions, accessibility, credits and handoff notes
├── research/        Desk research and cultural-reference notes
├── assets/          Included logos, dependency notices and licence files
├── tools/           Python/Blender generation, export, packaging and verification scripts
├── LICENSE
└── README.md
```

Blender tooling targets Blender 4.2. Individual scripts may also require Pillow or other dependencies indicated in their source. Running asset-generation tools is optional for reviewing the interface.

## Design process and documentation

The project moves from a problem statement and user journeys through wireframes, design tokens, high-fidelity reference screens and a browser prototype. Marketplace references informed browsing patterns, asset presentation and technical detail placement.

- [Problem statement](docs/problem-statement.md)
- [User flows](docs/user-flows.md)
- [Design decisions](docs/design-decisions.md)
- [Marketplace reference review](research/marketplace-reference-review.md)
- [Accessibility notes](docs/accessibility.md)
- [Everyday Lagos scope and provenance](docs/lagos-life-collection.md)
- [Design tokens](design/design-tokens.json)
- [Component specification](design/component-specification.md)
- [Figma handoff](docs/figma-handoff.md)
- [QA log](docs/qa-log.md)

The design source describes 108 reference artboards, including foundations and screen variants. This is not a count of distinct product features. Figma import source is prepared; import into the actual editor and a public prototype link remain pending. No user interviews or usability studies have been conducted.

## Status and limitations

This is an ongoing portfolio prototype. Creator workflows include artboard-based demonstrations, and the site has no production backend or payment processing. A hosted demo and a published Figma prototype are not yet available.

The complete-project verification reports are retained as development records. After restoring media, all 108 download checks pass in this local folder. Accessibility documentation records selected checks and outstanding work, rather than full WCAG certification.

The Lagos assets are semi-realistic environment studies. Included character designs are static, and their garment fitting and silhouettes need further manual refinement before production use.

## Authorship and acknowledgements

I supplied Sanctuary Temple and selected the audience, concept, visual direction and scope. Codex provided substantial assistance with implementation, documentation, procedural sample scenes and export tooling. This project is presented as assisted work, not wholly unaided manual work.

Third-party resources include Three.js (MIT), Inter and Space Grotesk (SIL Open Font License), and MakeHuman CC0 human geometry used in selected complete-project scenes. See [credits](docs/credits.md) and the included notices for sources and attribution.

## Licence

See [LICENSE](LICENSE) for the source-code terms and exclusions. Sanctuary Temple and third-party resources retain their separate ownership and licence conditions. Sample marketplace prices do not establish a purchase agreement or grant commercial asset rights.
