# Editable Figma Export

Use this when the user asks for Figma, editable design files, Figma handoff, or HTML-to-Figma.

## Output Types

| Output | Meaning |
|---|---|
| Editable Figma | Native Figma nodes: frames, text, vectors, fills, effects, variables, components. |
| Figma-ready handoff | Files and specs a designer can recreate quickly in Figma. Not a Figma file. |
| Screenshot/PDF | Static review artifact. Never call it editable Figma. |

## Preferred Paths

Always evaluate paths in this order when Figma is requested:

1. Direct Figma construction via callable Figma MCP/tool.
2. HTML/DOM-to-Figma conversion using a local app URL and open-source converter/plugin path.
3. Figma-ready handoff only after the first two paths are unavailable, failed, or inappropriate.

Record the decision in `design/figma-export.json` before final delivery.

Codex can prepare a plugin, import package, DOM capture payload, and instructions. Codex cannot run a Figma development plugin for the user unless a callable Figma MCP/tool or authorized Figma session is available. If direct creation is not completed, final delivery must guide the user through the import.

### Path A: Direct Figma construction

Use when Figma tools/MCP are available.

1. Discover or create the Figma file.
2. Create variables from `design/tokens.json`.
3. Create text styles, color styles, and effect styles.
4. Build components first: Button, Input, Card, Nav, SectionHeading, etc.
5. Build frames section by section using auto-layout.
6. Bind fills, spacing, radius, and type to variables/styles where possible.
7. Add assets from the asset manifest.
8. Verify editability: text layers editable, components detachable/variant-ready, variables visible, auto-layout active.
9. Export or record the Figma file/link and node IDs.

### Path B: HTML/DOM to Figma capture

Use when code exists and an open-source DOM-to-Figma path is available.

1. Run the app locally.
2. Ensure the target page is visually correct in browser.
3. Capture the rendered DOM, not a screenshot.
4. Convert computed layout/styles into Figma-native layer metadata, plugin import JSON, or clipboard payload.
5. Paste/import into Figma with the selected plugin/tool path, or produce the plugin-ready JSON plus exact import instructions when the agent cannot operate the user's Figma session.
6. Normalize the result: rename layers, convert repeated structures into components, apply variables, fix auto-layout, replace rasterized icons with vectors if needed.
7. Verify editability and record limitations.

Open-source references researched:

- A2F Figma plugin: community plugin for converting HTML/websites into editable Figma layers. Use it as a user-run import path when the user has the plugin available: prepare the local URL or HTML payload, include import steps, and record the path as `dom-to-figma`.
- BuilderIO `figma-html`: GitHub project for converting websites to editable Figma designs; moved toward Builder.io extension, MIT licensed, and documents that conversion is best-effort.
- `lgs/html-figma`: plugin/fork exposing plugin and chrome-extension structure; README shows importing a URL, Storybook capture, and `htmlToFigma(document.body)` usage.
- `sergcen/html-to-figma`: WIP library that converts DOM nodes to Figma nodes via `htmlTofigma(element)` and `addLayersToFrame(...)`.
- `cranch42/h2d-capture`: browser extension that walks the DOM, computes style diffs, resolves images, infers Auto Layout sizing, serializes to Figma clipboard format, and supports flex/grid, SVG inlining, font detection, React annotations, and local file capture.

Non-open alternatives can be useful for benchmarking, but do not treat them as the default open-source implementation path.

Do not claim this path creates an official `.fig` file by itself. Most HTML-to-Figma paths create Figma-native nodes through a plugin, clipboard payload, or import JSON that must be applied inside Figma. The correct deliverable is one of:

- editable Figma file/link when the agent actually created or imported it in Figma,
- `design/figma-export.json` plus plugin-ready payload/import instructions,
- `design/figma-handoff.md` when conversion was unavailable or failed.

## User-Run Import Instructions

When `editable_output_created` is false, create `design/figma/import-instructions.md` for `dom-to-figma` or `design/figma-handoff.md` for `handoff-only`, and include the same steps in the final response.

Use this final response section:

```markdown
**Figma import instructions**
1. Open Figma Desktop and create/open the target file.
2. Import or run the plugin: Plugins -> Development -> Import plugin from manifest..., then select `<plugin manifest path>`.
3. Run `<plugin name>` and provide `<payload path>` or import `<local URL>`.
4. Confirm the generated frames/pages: `<expected pages or frames>`.
5. After import, check editable text, layer names, components, variables, images, and Auto Layout notes.

Status: editable Figma was not directly created by Codex because `<reason>`.
```

If the deliverable uses a third-party/community HTML-to-Figma plugin instead of a bundled plugin, replace step 2 with that plugin's exact install/run path and cite the payload or local URL. Keep the language honest: "run this in Figma" rather than "a `.fig` file was generated."

Required `figma-export.json` shape:

```json
{
  "figma_requested": true,
  "path": "direct-figma | dom-to-figma | handoff-only",
  "editable_output_created": false,
  "created_file_or_link": null,
  "dom_to_figma": {
    "local_url": "http://localhost:5173",
      "tool": "A2F | BuilderIO/figma-html | lgs/html-figma | sergcen/html-to-figma | h2d-capture | other",
      "payload": "design/figma/html-to-figma.json",
      "import_instructions": "design/figma/import-instructions.md"
  },
  "tool_attempts": [],
  "limitations": []
}
```

## Editability QA

A Figma output is acceptable only when:

- text is native editable text, not baked into bitmap,
- frames/layers are selectable and named,
- repeated UI is converted to components or clearly marked for conversion,
- variables/styles exist for colors, type, spacing/radius where tooling supports them,
- auto-layout exists or responsive sizing notes are documented,
- generated assets are linked to `asset-manifest.json`,
- known conversion gaps are documented.

## Figma Handoff Fallback

If Figma tools and DOM-to-Figma conversion are unavailable or failed after an attempted path, deliver:

```text
figma-handoff.md
design/tokens.json
design/frame-spec.md
public/assets/asset-manifest.json
design/component-inventory.json
design/references/
```

State clearly: `Figma-ready handoff produced; editable Figma file was not generated because <reason>.`

Also include `design/figma-export.json` with `path: "handoff-only"` and the attempted direct-Figma and DOM-to-Figma checks.
