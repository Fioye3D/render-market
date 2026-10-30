# Component specification / v0.1

## Foundations

Use `design-tokens.json` as the working source. Canvas `#101112`, surface `#191B1E`, raised `#202327`, border `#3D424A`, text `#F5F3EE`, muted `#B2B7C1`, action `#5053CA`, accent `#B9BBFF`. Heading: Space Grotesk. Body/UI: Inter. Work on an 8 px rhythm with 4 px substeps.

## Core components

| Component | Anatomy | States / notes |
| --- | --- | --- |
| Button | 48 px high; 18 px horizontal padding; 8 px radius; 14 px semibold label | Primary, secondary, keyboard focus, disabled reference; loading/hover native variants need Figma refinement |
| Asset card | 0.7×width preview; title, sample creator, format and price; 44 px save target | Native importer creates reusable masters per content/width; saved state works in browser |
| Text field | Visible label; 27 px label-to-field offset; 52 px field; 8 px radius | Default, focused browser control, written validation feedback; multiline 130 px |
| Filter chip | 32 px visual height; 44 px interaction area; label plus selected treatment | Category and price examples; full multi-select controls are future work |
| Creator header | Fictional identity, clear speciality and catalogue | No ratings, fake testimonials or verification badges |
| Licence summary | Explicit allowed/example usage and redistribution boundary before request | Design content only; not a binding transaction |
| Feedback | Written heading, explanation and a return/close path | Empty, error, sample save, draft, attachment and demo completion |

## Figma implementation boundary

The prepared importer makes native editable text/shapes, image fills, colour variables, text styles, button components with editable label properties, repeated asset-card components and click reactions. Buttons use Auto Layout. It preserves exact screen/card geometry with explicit positioning, rather than claiming a fully responsive Auto Layout system. It must be run and inspected in Figma before it can be called a completed Figma library.

## Naming

Frames use journey/screen names; layers use the actual content or role; interaction regions use `Interaction / action label`. Components and tokens are prefixed with `RM v0.1` or their control type to remain distinct from existing file content.
