# Engineering Delivery

Use this reference when producing a runnable demo, prototype, or production-facing implementation from a design direction.

## Non-Negotiable Rule

A runnable web demo is a small project, not a single loose HTML file.

Do not output one flat `index.html` unless:

- the user explicitly asks for a single self-contained HTML file,
- the artifact is a poster, email, tiny embed, or archival snapshot,
- the runtime cannot install or run a build tool,
- the work is a throwaway visual proof and the user accepted that tradeoff.

If any exception applies, say so briefly in the handoff.

## Framework Choice

| Context | Default |
|---|---|
| Existing app/project | Use the existing stack and conventions. |
| Fast standalone web demo | Vite + React + Tailwind CSS. |
| Multi-route marketing/app demo | Next.js + Tailwind CSS. |
| Dense product UI needing official system | Existing app stack plus official DS package where appropriate. |
| Static poster/social/print artifact | Image/PDF plus source prompts/assets. |
| Figma collaboration | Figma if tools are available, otherwise Figma-ready handoff. |

Choose Vite for speed and clean handoff. Choose Next.js when routing, metadata, image optimization, deployment path, or production shape matters.

## Required Project Shape

For a new Vite/React/Tailwind demo:

```text
project/
  package.json
  index.html
  vite.config.ts
  tsconfig.json
  src/
    main.tsx
    App.tsx
    styles.css
    data/
      content.ts
      design-tokens.ts
    components/
      Button.tsx
      Container.tsx
      SectionHeading.tsx
    sections/
      Hero.tsx
      Proof.tsx
      Features.tsx
      CTA.tsx
  public/
    assets/
      asset-manifest.json
  design/
    DESIGN.md
    tokens.json
    references/
```

For Next.js:

```text
project/
  package.json
  next.config.ts
  app/
    layout.tsx
    page.tsx
    globals.css
  components/
  sections/
  data/
  public/
    assets/
      asset-manifest.json
  design/
    DESIGN.md
    tokens.json
    references/
```

Use `components/` for reusable primitives, `sections/` for page sections, `data/` for editable copy/content, and `design/` for design rationale and tokens. Do not bury all layout and copy in one monolithic component.

## Build Commands

When starting from scratch, prefer official scaffolding commands:

```bash
npm create vite@latest <project-name> -- --template react-ts
cd <project-name>
npm install
npm install tailwindcss @tailwindcss/vite
```

For Next.js:

```bash
npx create-next-app@latest <project-name> --typescript --tailwind --eslint --app --src-dir=false
```

If the current workspace already has a package manager, match it. Use npm only when there is no existing convention.

## Image-First Implementation Order

For new design work:

1. Create design brief and section plan.
2. Generate reference image(s) before code.
3. Save references under `design/references/` or `output/<project>/references/`.
4. Create or crop semantic assets and place them in `public/assets/`.
5. Write `public/assets/asset-manifest.json`.
6. Write `design/tokens.json` or project-native token files.
7. Write `design/DESIGN.md` with design DNA, component inventory, asset decisions, and implementation notes.
8. Create tokens/content files.
9. Build reusable components and sections.
10. Compare browser screenshots with references and revise.

Do not use the full generated section image as a hidden crutch behind live text unless the deliverable is intentionally a static poster. Build the layout in code and load only real assets.

Read [asset-pipeline.md](asset-pipeline.md) before creating or cropping assets.
Read [ui-asset-generation-loop.md](ui-asset-generation-loop.md) before building UI from generated references.
Read [design-system-schema.md](design-system-schema.md) before writing tokens or component inventory.

## Design Asset Preservation

Every new runnable demo must preserve these artifacts:

```text
design/DESIGN.md
design/tokens.json              # or project-native token file
public/assets/asset-manifest.json
src/components/                 # reusable primitives
src/sections/                   # page sections
src/data/                       # editable content and/or design tokens
```

`DESIGN.md` should include:

- design read and target audience,
- Design DNA summary,
- token rationale,
- component inventory,
- asset decisions,
- image-generation references used,
- QA notes and remaining risks.

`tokens.json` should include at least:

- colors,
- typography,
- spacing,
- radius,
- shadow/elevation,
- motion.

If the project already uses CSS variables, Tailwind theme, a theme provider, or Figma variables, write tokens there and document the mapping in `design/DESIGN.md`.

## Maintainability Standards

- Keep visible copy in `data/content.ts` or an equivalent data file when it is repeated or likely to change.
- Keep tokens in CSS variables, Tailwind theme utilities, `design/tokens.json`, or `data/design-tokens.ts`.
- Keep each section as its own component once the page has more than two sections.
- Keep assets named by role: `hero-product.webp`, `feature-workflow.webp`, `texture-noise.png`.
- Include responsive behavior in the implementation, not as a postscript.
- Add accessible labels, alt text, focus states, loading/empty/error states where relevant.
- Run the app locally and inspect desktop/mobile.

## Handoff Checklist

Before final delivery:

- The project runs with documented commands.
- The first screen is built from code, not one static screenshot.
- Generated references and final assets are separated.
- Assets have a manifest with role, source, alt text, and usage.
- The design system/tokens are discoverable and saved.
- Reusable primitives and sections exist when the page has multiple sections.
- `DESIGN.md` captures the design decisions and component inventory.
- The page is split into maintainable components/sections.
- Browser QA or screenshot review has been performed when possible.
- Visual alignment is recorded in `design/qa-report.md` when references were generated.
- `python agent-design/scripts/pipeline_validate.py <project>` passes, unless a documented exception applies.
