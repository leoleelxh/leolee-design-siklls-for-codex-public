# Agent Design Process

Use this reference when the task is a new design, an ambiguous design brief, image-first work, Figma/HTML delivery, or asset-system preservation. Read [production-pipeline.md](production-pipeline.md) for mandatory gates and required artifacts.

## 1. Intake And Scope

First classify the user's input.

| User input | Agent response |
|---|---|
| Clear artifact and delivery | Proceed, state the design read. |
| Clear artifact, vague style | Ask one direction question with 3-5 professional choices. |
| Vague artifact, clear style | Ask one scope question: hero, page, product screen, deck, poster, system. |
| Vague everything | Ask one combined question with recommended default. |
| Existing project | Switch to redesign audit before visual exploration. |

Professional range choices:

- **Surface**: hero, landing page, product screen, dashboard, poster, deck, full brand/site kit.
- **Fidelity**: rough concept, high-fidelity visual comp, runnable HTML prototype, production UI, Figma library.
- **Design language**: restrained editorial, premium consumer, technical SaaS, experimental studio, trust-first public-sector, dense operational.
- **Delivery**: HTML/code, Figma, both, static image/PDF, reusable design assets.
- **Asset depth**: no new assets, generated hero/media only, full section imagery, component/icon set, token library.

Default recommendation when the user is unsure:

`HTML prototype first, image-first for new visual direction, then preserve tokens/assets if the direction lands.`

## 2. Design Brief

Before generating or implementing, write a compact brief:

```text
Design read: <artifact> for <audience>, using <design language>, optimized for <goal>.
Scope: <surface count and fidelity>.
Delivery: <HTML/Figma/both/static/system>.
Constraints: <brand, accessibility, platform, timeline, assets, existing stack>.
Risk: <what must not break or what is unknown>.
```

If the user has references, extract Design DNA first. If no references exist, select a coherent design world and name anti-references to avoid.

For ambiguous new visual work, read [style-exploration.md](style-exploration.md) and produce three style directions before choosing one.

## 3. Image Generation Loop

Use image generation when the project needs strong new visual direction.

For new visual design, this is a gate. Generate references before implementation unless the user opts out, no image tool is available, or the task is an existing-product redesign where preserving current UI is more important than exploration.

1. Create a section plan: section name, job, composition anchor, background mode, CTA, assets needed.
2. Generate one horizontal image per section for websites and apps. Never collapse the whole page into one tall image.
3. Keep the palette, type character, radius, material, and image treatment consistent across frames.
4. After each generation, critique as a designer:
   - Is the hierarchy obvious?
   - Does it avoid generic AI composition?
   - Can it be implemented from code?
   - Are images structural, not decorative filler?
   - Does the section support the funnel or task?
5. Iterate only the weak frames. Do not regenerate the whole set when one section fails.

When the platform can return files, save generated references under the target project's working output path, for example:

```text
output/<project-slug>/references/
  section-01-hero.png
  section-02-proof.png
```

Do not store project-specific generated images inside the skill folder.

## 4. Slicing And Assets

Treat section images as references, not automatically as final web assets.

"Slicing" means structured asset extraction: rebuild layout, text, spacing, states, and components in code; extract only semantic media or complex visuals as assets. Never treat slicing as cutting an entire generated page comp into image tiles for frontend assembly.

Create actual assets only for elements that should appear in the final deliverable:

- hero backgrounds,
- product/object/person/place imagery,
- portfolio thumbnails,
- logos and icons,
- textures and patterns,
- poster or card art,
- screenshots/mockups.

Asset workflow:

1. Identify every visual element needed by the implementation.
2. Classify each element as `code`, `token`, `component`, `asset`, or `omit`.
3. Reuse existing project assets first.
4. Generate or crop separate assets for semantic imagery. Avoid using the entire section comp as a background unless it is a static poster or intentional screenshot embed.
5. Place assets in the existing asset path:
   - Next.js/Vite static assets: `public/`
   - component imports: `src/assets/`
   - simple HTML prototype: adjacent `assets/`
   - Figma handoff: `output/<project-slug>/assets/`
6. Name assets by role, not by random prompt text: `hero-product-crop.webp`, `texture-paper-noise.png`, `case-study-dashboard.webp`.
7. Create an asset manifest for multi-asset work:

```json
{
  "assets": [
    {
      "file": "assets/hero-product-crop.webp",
      "role": "hero background",
      "source": "generated",
      "alt": "Close crop of the product interface on a calm green surface",
      "usage": "home hero"
    }
  ]
}
```

Always include alt text for meaningful images. Decorative textures may use empty alt text in HTML, but still document their visual role in the manifest.

Read [asset-pipeline.md](asset-pipeline.md) for the full asset taxonomy, manifest format, and export rules.
Read [ui-asset-generation-loop.md](ui-asset-generation-loop.md) when any element is classified as `generate`, `crop`, `export`, or `sprite`.

## 5. HTML Or Figma

Choose the output by job-to-be-done.

| Need | Output |
|---|---|
| Runnable, testable, deployable, or coding-agent-ready result | HTML/code |
| Visual stakeholder review, collaborative editing, design library, or Figma URL requested | Figma |
| High-fidelity design that must become production UI | Both: Figma/spec plus HTML implementation |
| Poster, cover, social image, or static campaign visual | Image/PDF plus source prompts/assets |
| Reusable brand/system work | Tokens, components, asset manifest, and optional Figma library |

HTML/code rules:

- Work inside the existing stack.
- If there is no existing stack and the output is a runnable demo, create a real project. Default to Vite + React + Tailwind CSS; use Next.js for multi-route or production-shaped demos.
- Do not deliver a single flat HTML file for runnable demos unless the user explicitly requests it or the artifact is static/no-build by nature.
- Use semantic structure and stable responsive constraints.
- Load assets from the target project's asset path.
- Verify in browser on desktop and mobile.
- Read [engineering-delivery.md](engineering-delivery.md) for the project structure, framework choice, and handoff checklist.

Figma rules:

- Use Figma tools/MCP only when available and requested or clearly useful.
- Build frames section by section.
- Prefer variables/tokens and reusable components over hardcoded one-off nodes.
- If no Figma tool is available, produce a Figma-ready handoff: frame sizes, layout grids, tokens, component list, asset manifest, and interaction notes.
- Read [figma-export.md](figma-export.md) for editable Figma paths and editability QA.

## 6. Implementation From Image

When converting an image reference to code:

1. Map the image into layout primitives: sections, grids, columns, layers, typography hierarchy, media blocks, and states.
2. Extract tokens: colors, font character, spacing, radius, shadows, borders, motion.
3. Identify actual assets and create/load them separately.
4. Implement the structure with code-native layout, not pixel-positioned imitation.
5. Compare implementation screenshot with the reference and fix hierarchy, spacing, scale, and crop differences.
6. Keep copy real and editable. Avoid baking text into images unless the artifact is a poster.
7. Split runnable demos into components, sections, data, assets, and design documentation. Avoid a monolithic one-file implementation.

Read [design-spec.md](design-spec.md) before coding from references, and [visual-alignment.md](visual-alignment.md) before final visual QA.

## 7. Asset Preservation

At the end, preserve design assets unless the user explicitly requested a throwaway prototype.

Preserve when:

- The user likes the direction.
- The project will reuse the style across multiple pages.
- New tokens, components, icons, images, prompts, or visual effects were created.
- The work can become a brand kit, design system, or future skill reference.

Preservation outputs can include:

```text
design/
  DESIGN.md
  tokens.json
  asset-manifest.json
  prompts/
  components/
  references/
```

Minimum for new runnable demos:

- `design/DESIGN.md` with design read, Design DNA, rationale, component inventory, and anti-references.
- `design/tokens.json` or project-native tokens (`src/data/design-tokens.ts`, CSS variables, Tailwind theme).
- `public/assets/asset-manifest.json` or equivalent even when the asset list is empty.
- Reusable primitives in `components/` and page-level sections in `sections/`.

For existing codebases, prefer the project's own convention: `src/styles/tokens.css`, `theme.ts`, `tailwind.config`, `components/ui`, or Figma variables.

Do not preserve weak first drafts as production assets. If the direction is not approved yet, preserve them as `draft` and label that status in `DESIGN.md` and the asset manifest.

Read [design-system-schema.md](design-system-schema.md) for token, mapping, and component inventory schema.

## 8. Final Handoff

Close with:

- design read,
- final output target,
- assets generated or reused,
- verification performed,
- whether reusable assets were saved,
- remaining design decisions for the user.
