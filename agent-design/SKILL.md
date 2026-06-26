---
name: agent-design
description: Codex-first end-to-end design production pipeline, art-direction, design-to-code, Figma editable export, asset handoff, and visual QA skill for creating, redesigning, and polishing interfaces, landing pages, portfolios, brand surfaces, product UI, posters, slides, and other visual artifacts. Use when the user asks for premium UI/UX design, image-first design exploration, vague-to-specific design scoping, image-to-code workflows, HTML/Figma delivery decisions, anti-generic redesigns, design system extraction, visual polish, screenshot/browser QA, or designer-grade self-testing. Optimized for Codex and other agents with image generation plus browser verification.
---

# Agent Design

Use this skill to turn vague visual intent into a designed artifact that survives implementation. Treat design as a production pipeline, not a style checklist: scope the brief, explore visually, produce a design spec, extract assets/tokens, implement or export to Figma, verify, and preserve the result as reusable design assets.

## Core Workflow

1. Read the brief and existing project before designing.
2. If the brief is vague, ask one concise scoping question with professional range choices. Include a recommended option.
3. State one line: `Design read: <artifact type> for <audience>, <design language>, <risk/constraint>.`
4. Choose the mode:
   - `image-first`: new landing page, brand page, portfolio, poster, hero, campaign, product concept.
   - `redesign`: existing app/site, visual refresh, "make this look better".
   - `product-ui`: dashboards, forms, tables, admin tools, dense workflows.
   - `design-dna`: user provides screenshots, URLs, brand references, or wants a reusable style system.
   - `figma-export`: user asks for Figma, editable design files, design handoff, or HTML-to-Figma.
   - `qa-only`: user asks to review, test, or polish an already-built visual artifact.
5. Decide output target: HTML/code, Figma, both, static image/PDF, or design-system assets.
6. Create a pipeline ledger before producing design/code. Track `brief -> prompt -> reference -> spec -> token -> asset -> component -> implementation -> QA`.
7. Create or extract Design DNA: colors, type, spacing, layout, shape, material, motion, imagery, copy voice, interaction states.
8. Pass the image-first gate for new visual design before writing implementation code.
9. Produce a design-spec artifact before frontend implementation.
10. Implement, export to Figma, or hand off using the existing stack and design system. Do not migrate frameworks for taste alone.
11. Verify visually in a browser or design tool when available.
12. Preserve the outcome as reusable tokens, components, assets, and docs unless the user explicitly requests a throwaway draft.

Read these references as needed:

- [references/production-pipeline.md](references/production-pipeline.md) for mandatory phases, gates, artifacts, and traceability.
- [references/execution-protocol.md](references/execution-protocol.md) for no-silent-downgrade rules, tool attempt logs, and hard stops.
- [references/design-process.md](references/design-process.md) for scoping choices, image generation, slicing, asset loading, HTML/Figma delivery, engineering demo structure, and asset-library preservation.
- [references/asset-pipeline.md](references/asset-pipeline.md) before converting generated/reference imagery into frontend assets.
- [references/ui-asset-generation-loop.md](references/ui-asset-generation-loop.md) before generating UI assets or implementing a design with generated media.
- [references/figma-export.md](references/figma-export.md) before creating or converting to editable Figma.
- [references/design-system-schema.md](references/design-system-schema.md) before writing tokens, component inventory, or Figma variables.
- [references/visual-alignment.md](references/visual-alignment.md) before comparing reference and implementation screenshots.

## Scoping Vague Briefs

When the user gives a vague prompt like "make me a good website" or "design a premium UI", ask for scope instead of guessing the whole project. Keep it to one question unless the missing information changes risk.

Example:

`Do you want a fast HTML prototype, a Figma-ready design spec, or both? Recommended: HTML prototype first, then preserve tokens/assets if the direction lands.`

Use range choices such as:

- Fidelity: concept sketch, high-fidelity section comp, production-ready HTML, Figma-ready system.
- Surface: hero only, landing page, product screen, dashboard, poster, deck.
- Direction: clean/editorial, premium consumer, technical SaaS, experimental studio, public-sector/trust-first.
- Delivery: HTML/code, Figma, both, static image/PDF, reusable design system.

## Image-First Mode

Use image generation before code when the task benefits from a high-fidelity visual target.

For new visual design, image-first is the default gate, not an optional flourish. Do not start coding a new landing page, brand site, portfolio, hero, campaign, poster, or product concept until one of these is true:

- generated reference image(s) exist and have been critiqued,
- the user explicitly opts out of image generation,
- the task is a redesign that must preserve an existing UI,
- image generation tooling was attempted and failed, in which case record the failed tool attempt and create a storyboard/prompt set before coding.

For ambiguous new design, generate or storyboard three distinct concept directions before moving forward: conservative/usable, expressive/premium, and experimental/brand-led. Each direction needs a separate artifact-aware concept board or storyboard that previews the requested deliverable, such as mobile app screens, website sections, deck slides, poster variants, logo/brand boards, dashboard states, or design-system samples. Stop after presenting the three concepts and ask the user to confirm a direction. Do not continue to design spec, asset generation, or frontend implementation until the user confirms one direction or explicitly authorizes auto-selection. Read [references/style-exploration.md](references/style-exploration.md).

Concept confirmation is a hard stop. A recommendation is not authorization. In the same assistant turn that presents the three concepts, do not auto-select, do not continue with additional tool calls, and do not create design spec, assets, code, or Figma output. End that turn in `WAITING_FOR_USER_DIRECTION_CONFIRMATION` unless the user already explicitly asked for auto-selection.

When the user's next message confirms a direction, immediately enter `POST_CONFIRMATION_ASSET_LOOP` before implementation. Record the selected direction, create the frame spec and element inventory, run [references/ui-asset-generation-loop.md](references/ui-asset-generation-loop.md), and produce `asset-manifest.json` with `ui_assets_complete: true`. Do not jump directly from direction confirmation to frontend code or Figma export.

- For a single hero/component: generate one horizontal reference frame.
- For a landing page or full site: generate one horizontal image per section, labeled `Section X of N`.
- Default counts when unclear: hero = 1, landing page = 6, full marketing site = 8, product page = 6, portfolio = 6.
- Keep one brand world across all frames: palette, typography, radius, image treatment, CTA language, and spacing cadence.
- Make each section codeable: clear hierarchy, grid, spacing, component states, readable text, and visible CTA priority.
- Treat generated section images as design references. Generate or crop separate usable assets for product photos, hero media, icons, posters, and inspectable objects.
- Save assets in the target project's existing asset path (`public/`, `src/assets/`, `app/assets/`, or adjacent `assets/`) and create a short manifest when multiple assets are produced.
- Run the UI asset generation loop until `asset-manifest.json` has `ui_assets_complete: true`, or stop and report why assets are incomplete.
- If image generation is unavailable after an attempted tool call, write the per-section art direction prompts first, mark the manifest `ui_assets_complete: false`, and do not call the frontend final.

Generate images with the platform's image tool when available. In Codex, prefer the built-in image generation capability. If an external OpenAI image API is configured, use the configured model name from the environment or project docs instead of hardcoding it.

## Asset Extraction

Define "slicing" as structured asset extraction, not slicing the entire comp into web-image tiles. For frontend work:

- Rebuild layout, typography, text, buttons, cards, grids, effects, and responsive behavior in code.
- Extract or generate assets only for semantic media: product/object/person/place imagery, illustrations, logos, icons, textures, screenshots, posters, and complex visual effects that cannot be expressed cleanly in code.
- Semantic media assets are required by default when a selected concept contains preview/stage/project card/thumbnail/mockup/cover/hero media/product media/gallery/poster/brand illustration/texture/inspectable subjects. Header chrome, buttons, forms, nav, panels, inspectors, timelines, and live text stay code-native.
- A CSS-only substitute for semantic media is allowed only when the manifest records that element with `decision: "code"`, a strong `code_native_reason`, and `code_native_approved: true`; if every asset is code-native, also set `all_code_native_approved: true`.
- Do not use a full generated section image as a page background behind live text unless the deliverable is intentionally static.
- Produce an asset manifest whenever assets are created, reused, or intentionally skipped.
- Use multi-round generation for semantic UI assets: hero media, product mockups, headshots, stickers, cover art, transparent PNG cutouts, icon/sprite sheets, and background subjects.
- Do not call a frontend delivery final if semantic media candidates exist but no generated/cropped/exported/reused assets or code-native approvals are recorded.

Read [references/asset-pipeline.md](references/asset-pipeline.md) for asset taxonomy, manifest format, export rules, and QA.
Read [references/ui-asset-generation-loop.md](references/ui-asset-generation-loop.md) for the repeated prompt -> generate -> QA -> manifest loop.

## Delivery Target

Default to HTML/code when the user wants something runnable, testable, or ready for a coding agent. Choose Figma only when the user asks for Figma, a Figma MCP/tool is available, or the task is primarily collaborative design-system work. Choose both when the project needs stakeholder review and implementation fidelity.

If Figma tooling is unavailable, produce a Figma-ready handoff instead: frames, layout grid, tokens, component inventory, asset manifest, and interaction notes.

For editable Figma output, prefer direct Figma construction when Figma tools/MCP are available. Otherwise use an HTML/DOM-to-Figma capture path when available: run the implementation locally, capture rendered DOM/computed styles into Figma-native nodes, then normalize variables, components, auto-layout, and layer names. Do not claim a flat screenshot is an editable Figma deliverable. Read [references/figma-export.md](references/figma-export.md).

When the user can use the A2F Figma plugin, treat it as a supported HTML-to-Figma path: prepare a clean local URL or HTML payload, document A2F import steps, then record the path in `design/figma-export.json` as `dom-to-figma`.

If Figma is requested and no native Figma MCP/tool is callable, do not stop at handoff until you have evaluated an HTML/DOM-to-Figma path. Record the path decision in `design/figma-export.json`: `direct-figma`, `dom-to-figma`, or `handoff-only`, with attempted tools and limitations. Do not claim an official `.fig` file unless a real Figma tool/file export path created one.

When Codex cannot directly run the Figma import, the final response must include a `Figma import instructions` section for the user: plugin/package path, Figma Desktop steps, local URL or payload file, expected result, and limitations. Treat this as required delivery content, not optional guidance.

## Engineering Demo Delivery

Do not deliver a single flat HTML file for a runnable web demo unless the user explicitly asks for a single file, the artifact is a static poster/email/embed, or the environment cannot run a build tool. Even demos should be maintainable.

For a new runnable demo with no existing codebase:

- Default to Vite + React + Tailwind CSS for fast visual prototypes.
- Use Next.js when the demo needs routing, app-like structure, SSR/image optimization, or a path toward production.
- Use plain HTML only for static, archival, email-like, or deliberately no-build deliverables.

Minimum demo structure:

```text
package.json
index.html
src/
  main.tsx
  App.tsx
  styles.css
  data/
  components/
  sections/
public/
  assets/
design/
  DESIGN.md
  asset-manifest.json
  references/
```

Read [references/engineering-delivery.md](references/engineering-delivery.md) before creating a new runnable demo or converting image references into a demo project.

## Design Asset Preservation

Every new runnable design demo must leave behind reusable design assets unless the user explicitly requests a throwaway prototype.

Minimum preservation:

- `design/DESIGN.md`: design read, design DNA, decisions, and anti-references.
- `design/tokens.json` or project-native tokens: color, type, spacing, radius, shadow, motion.
- `public/assets/asset-manifest.json` or equivalent: generated/reused assets and alt text.
- component inventory: reusable components and section components, documented in `design/DESIGN.md` or code comments where appropriate.

For existing codebases, preserve assets in the project's convention: CSS variables, Tailwind theme, theme files, `components/ui`, Figma variables, or design-system docs. If no reusable assets were created, state why and still record the design decisions.

Use [references/design-system-schema.md](references/design-system-schema.md) for the exact token schema, component inventory format, prop/state matrix, and code/Figma mapping.

## Redesign Mode

Audit before changing code.

- Preserve route slugs, nav labels, analytics hooks, form field names, legal copy, and SEO-critical structure unless the user explicitly approves changes.
- Identify current tokens: colors, font stack, radius, shadows, spacing, imagery, component patterns.
- Mark what to preserve, what to retire, and what is broken on mobile.
- Apply the lowest-risk visual lifts first: typography, spacing, palette cleanup, interaction states, then section recomposition.
- Keep the existing stack. If the project already has Tailwind, shadcn/ui, MUI, Carbon, Fluent, Bootstrap, Radix, or custom tokens, work inside that system.

## Product UI Mode

Design for speed, accuracy, and state clarity.

- Prefer restrained density, readable hierarchy, strong table/form ergonomics, and obvious state handling.
- Use official design systems when the product context demands them: Fluent for Microsoft-like enterprise, Material for Google-like surfaces, Carbon for IBM-like analytics, Polaris for Shopify apps, Primer for GitHub/devtool surfaces, GOV.UK or USWDS for public-sector work.
- Include loading, empty, error, disabled, focused, hover, active, and success states.
- Avoid decorative motion that slows scanning. Motion should clarify feedback, transitions, or spatial relationship.

## Design DNA Mode

When references are provided, extract a structured profile before generating.

Read [references/design-dna-schema.md](references/design-dna-schema.md) when the user asks for a reusable style profile, token extraction, or matching a reference.

Capture:

- `design_system`: measurable tokens and component rules.
- `design_style`: qualitative feel, composition, voice, imagery, and material.
- `visual_effects`: canvas/WebGL/3D/shader/scroll/motion effects and performance risk.

Then apply the DNA to the user's content. If references conflict, name the dominant pattern and the alternate pattern.

## Anti-Slop Standards

Actively avoid common AI design tells unless the brief specifically asks for them.

- No default purple/blue AI gradients, generic glowing blobs, or decorative mesh backgrounds as a reflex.
- No centered hero plus three equal feature cards as the default composition.
- No beige/brass/espresso "luxury" palette by default for every premium consumer brief.
- No fake KPI sets, `Acme`, `Jane Doe`, `Lorem ipsum`, or copy like "elevate", "unleash", "next-gen", "seamless", "game-changing".
- No repeated section layout family more than twice in a row.
- No icon soup. Use one icon family already present in the project, or a single well-supported family if adding one.
- No whole sections floating in nested cards. Use cards only when they communicate hierarchy or repeated items.
- No invisible focus states, weak contrast, missing alt text, dead `href="#"` links, or CTA labels that wrap on desktop.

## Visual Standards

- Typography: make the hierarchy obvious, limit paragraph width, use optical line-height, and avoid negative letter spacing.
- Color: lock one accent, one neutral family, and one radius language. Test contrast.
- Layout: use grid for complex composition, stable responsive constraints, and `min-height: 100dvh` for viewport-height sections.
- Imagery: use semantically relevant generated or real bitmap imagery when the subject is inspectable. Avoid abstract filler when users need to inspect a product, person, place, or object.
- Motion: use CSS, Motion, GSAP, or native browser APIs intentionally. Respect `prefers-reduced-motion`.
- Copy: write short, concrete, believable interface copy. Prefer sentence case.
- Accessibility: verify keyboard focus, readable contrast, alt text, semantic landmarks, and responsive tap targets.

## Verification

Before final delivery, run the strongest feasible checks. E2E is useful for this repository's self-test and for real app QA, but it is not required for the skill to be usable.

```bash
python agent-design/scripts/design_audit.py <target-file-or-directory> --fail-on high
python agent-design/scripts/pipeline_validate.py <generated-project>
```

For app/browser QA, optionally run:

```bash
TARGET_URL=<url> npm run test:e2e
```

Without `TARGET_URL`, the Playwright suite uses this repository's built-in fixture.

Read [references/visual-qa-checklist.md](references/visual-qa-checklist.md) before final QA on substantial work.

When browser tools are available:

- Open the page in the Browser or Chrome plugin.
- Capture desktop and mobile screenshots.
- Check first viewport composition, no overlap, no clipping, no horizontal overflow.
- Interact with primary controls, forms, menus, and responsive navigation.
- Fix issues, then re-run the screenshot pass.

## References

Read [references/source-index.md](references/source-index.md) when updating this skill, adding citations, or deciding which external design-skill ideas to study. Synthesize ideas; do not copy long passages from source projects.

## Delivery Contract

For implementation tasks, finish with:

- design read and chosen mode,
- output target and why,
- pipeline phases completed and gates passed,
- files changed,
- generated images or references used,
- design spec produced,
- assets created or reused,
- framework/project structure used,
- tokens, components, Figma variables/components, or equivalent assets preserved,
- Figma import instructions when editable Figma was requested but not directly created,
- traceability ledger location,
- tests run and results,
- remaining design risks, if any.
