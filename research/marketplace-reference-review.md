# Marketplace reference review

**Reviewed:** 29 October 2026. **Method:** read-only review of three public homepages, Blendkit's upload guidance and one Superhive product page. No accounts, purchases, downloads or seller workflows were tested. This is a limited reference review, not a usability study or comprehensive competitive audit.

## Observed patterns and proposed applications

| Reference | Observation on the reviewed pages | RenderMarket design hypothesis |
| --- | --- | --- |
| [CGTrader](https://www.cgtrader.com/) | Prominent model search; hierarchical subject categories; asset-type and budget routes; format-based discovery; seller resources. | Make search and catalogue browsing the primary entry points. Distinguish subject, asset type and file compatibility. |
| [Blendkit](https://www.blendkit.com/) | Asset classes include models, materials, HDRIs and scenes. The homepage describes integration into Blender. [Creator guidance](https://www.blendkit.com/docs/upload-tutorials/) separates preparation by asset type. | Expose software/version information, then use asset-type-specific upload prompts. Treat a future Blender integration as a separate product idea, not an implemented feature. |
| [Superhive](https://superhivemarket.com/) | Product cards identify creators and categories; homepage sections organise discovery around new products, bundles and creators. The reviewed [Modeling Toolkit listing](https://superhivemarket.com/products/modeling-toolkit) includes a gallery, descriptions, licence options and a Blender-version detail. | Connect every listing to its creator. Make previews, included files, version requirements and licence differences legible before a demo request. |

These observations show available interface patterns. They do not establish that those patterns improve conversion or that people prefer them.

## Recommended next RenderMarket iteration

1. **Search-led discovery:** add a compact labelled search field to the homepage and keep search available throughout browsing. The current prototype's full search field is on Explore.
2. **Separate filtering dimensions:** keep asset type, software, format and price distinct. Add an optional place/cultural-context filter as the catalogue grows; do not equate artist location with an asset's cultural reference.
3. **More useful catalogue cards:** retain preview, title, creator and price; prioritise relevant format/compatibility and concise place context. Avoid crowding every field onto the card.
4. **Evaluation-focused detail page:** organise original previews, description, actual included files, software requirements, cultural reference and example licence into a clear hierarchy. Additional views should be original rendered views, not duplicate images presented as different angles.
5. **Asset-specific creator guidance:** models need geometry/scale notes; materials need procedural/PBR and texture information; future animation packs need rig/version and clip information. Ask only for fields relevant to the selected type.
6. **Editorial collections with an African focus:** examples include Lagos everyday life, West African textiles, basketry and earthen environments. These are proposed collections rather than user-validated demand or claims of comprehensive regional coverage.

## Scope decisions

The existing six-item sample does not justify a large mega-menu or popularity rankings. Expand navigation only when there is enough genuine sample content to demonstrate it clearly. Keep the approved dark premium identity, desktop plus selected mobile scope and majority African-referenced catalogue. Subscriptions, add-on integration, dynamic pricing, seller analytics and real verification remain outside this prototype.

No third-party listing images, product descriptions, ratings, sales figures or badges were copied into RenderMarket. The owner subsequently authorised combining these patterns in iteration v0.2. The homepage, browsing controls, card metadata and asset-detail structure have now been revised. See the [before-and-after review](../prototype/changes.html). Asset-specific upload guidance remains a future improvement; the general three-step creator flow is retained.

## Questions for later testing

- Do buyers search by object name, place, material, culture, software or intended scene?
- Which metadata belongs on a card and which can wait until the detail page?
- Can buyers distinguish an original interpretation from a documented scan or reconstruction?
- Can creators accurately provide technical requirements and cultural-reference notes?

These questions require real creator and buyer evidence.
