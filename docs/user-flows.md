# User flows

## Buyer

```mermaid
flowchart LR
 H[Home] --> E[Explore]
 E --> S[Search and filter]
 S --> D[Asset detail]
 D --> C[Creator profile]
 C --> D
 D --> L[Review example licence]
 L --> R[Demo request acknowledgement]
 R --> E
 D --> V[Save in session]
```

The browser search matches titles, creators, categories and asset tags. Category filtering and a price filter combine with the query. No-match states suggest changing the query or resetting filters. Save/unsave uses current-session memory. Example licence content clearly precedes the demo request; no purchase occurs.

## Creator

```mermaid
flowchart LR
 A[Demo creator entry] --> B[Dashboard]
 B --> U[Asset basics]
 U --> F[Attach supplied sample and metadata]
 F --> P[Price and example licence]
 P --> V[Preview listing]
 V --> X[Demo publication confirmation]
 X --> B
 F --> U
 P --> F
 V --> P
```

Title must be non-empty. The sample attachment must be selected before the pricing step. Price must be zero or greater. Back routes preserve entered values within the active browser session. The browser preview uses the edited title and price; the confirmation and catalogue are fixed sample data rather than a real listing database.

## Prototype differences

Figma prepares fixed examples and feedback overlays for typed search, sorting, attachment and saves. The local browser preview is the richer interaction demonstration. Three dedicated mobile buyer artboards adapt home, explore and the courtyard detail. Remaining destinations open desktop reference artboards; they are not completed mobile journeys.
