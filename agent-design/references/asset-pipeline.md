# Asset Pipeline

Use this reference when turning generated images, screenshots, Figma frames, or visual references into frontend assets. Read [ui-asset-generation-loop.md](ui-asset-generation-loop.md) before creating assets from a style reference.

## Definition

"Slicing" means structured asset extraction for implementation. It does not mean cutting a full comp into many image tiles and placing those tiles on a webpage.

The correct design-to-frontend split:

| Design material | Frontend treatment |
|---|---|
| Layout, spacing, grids, typography, text, buttons, cards | Rebuild in code. |
| Colors, radius, shadows, motion, type scale | Convert into tokens. |
| Product/object/person/place imagery | Export, crop, or generate as semantic assets. |
| Logos and icons | Prefer SVG or established icon libraries; export only real brand/custom marks. |
| Textures, patterns, complex illustrations | Export as lightweight assets when CSS/SVG is not better. |
| Full section comp | Keep as reference only, not as production background, unless static poster/screenshot embed. |
| UI screenshots/mockups | Use only when the UI itself is the media being shown; otherwise build UI in code. |

## Required Flow

1. **Reference inventory**: list each generated/reference frame and its role.
2. **Implementation inventory**: identify what must become code, token, component, or asset.
3. **Token extraction**: extract color, type, spacing, radius, shadow, motion, media treatment.
4. **Asset decision**: for each visual element, choose `reuse`, `generate`, `crop`, `export`, `code`, or `omit`.
5. **Asset creation loop**: create only semantic assets, with role-based names; use repeated image-generation/crop/export attempts until each required asset passes QA.
6. **Manifest**: document every asset and skipped asset.
7. **Implementation**: load assets through the framework's asset path and rebuild layout in code.
8. **QA**: compare implemented screenshot with reference and verify alt text, crop, contrast, file size, and responsive behavior.

## Asset Decision Rules

- Use `code` for typography, boxes, grids, CSS gradients, simple shapes, buttons, cards, charts that need live data, and responsive layout.
- Use `generate` for new hero imagery, product-style visuals, campaign art, editorial photos, and bespoke illustrations.
- Use `crop` when a generated reference contains a usable semantic object or texture that should appear in the final design.
- Use `export` for existing Figma assets, logos, custom icons, brand marks, and approved imagery.
- Use `reuse` when the project already has a suitable asset.
- Use `omit` for decorative filler that does not support the design.

Never make live UI text part of an image asset unless the final artifact is a static poster, social image, ad creative, or screenshot showcase.

For icons/stickers/reaction sets, choose either individual SVGs or a sprite sheet with metadata. For transparent subjects such as headshots, objects, stickers, floating product cutouts, or background foreground subjects, generate or process PNG files with alpha.

## Semantic Media Default Rule

Semantic media assets are required by default for new visual projects. Treat preview/stage/project card/thumbnail/mockup/cover media as inspectable product media, not as disposable decoration. The UI frame can be code-native; the media inside it must be generated, cropped, exported, reused, or explicitly approved as code-native.

For new visual projects, these elements default to `generate`, `crop`, `export`, or `reuse`, not `code`, unless there is a strong recorded reason:

- hero preview media,
- preview stage artwork,
- project thumbnails,
- project card media,
- portfolio cards,
- product mockups,
- product/service covers,
- gallery items,
- poster/social covers,
- avatar/headshot imagery,
- stickers/reaction art,
- logo or custom brand marks,
- brand illustrations,
- complex texture/light-pattern assets.

Do not replace these with CSS-only fake panels just because they are easy to code. CSS can frame, mask, animate, and layer them, but the inspectable media itself should be a real asset.

UI framework elements should normally remain code-native: header, prompt composer, buttons, bottom nav, tabs, layer list, inspector, timeline, form controls, table rows, cards as containers, shadows, masks, and responsive layout.

Concrete asset names should follow the role, for example:

- `hero-preview-frame.webp`
- `project-orbital-bloom.webp`
- `project-kinetic-logo.webp`
- `project-product-spin.webp`
- `texture-film-grain.png`

If a semantic media item is marked `code`, the manifest must include `code_native_reason` and `code_native_approved: true` that prove why it should be code-native, for example: live data chart, editable text, simple generated gradient, or interactive state. "Faster" or "looks close enough" is not a valid reason. If every media candidate is code-native, the manifest must also include `all_code_native_approved: true`.

## Asset Paths

Choose the path that matches the project:

```text
Vite/React:
  public/assets/
  src/assets/          # only for imported component assets

Next.js:
  public/assets/

Plain HTML:
  assets/

Figma handoff:
  output/<project>/assets/

Existing app:
  Use the existing asset convention.
```

## Manifest Format

Every project with assets should include `asset-manifest.json`.

```json
{
  "ui_assets_complete": true,
  "semantic_media_policy": "all semantic media generated/cropped/exported/reused or justified as code-native",
  "references": [
    {
      "file": "design/references/section-01-hero.png",
      "role": "visual reference only",
      "used_as_asset": false
    }
  ],
  "element_inventory": [
    {
      "id": "hero-product-preview",
      "source_reference": "design/references/section-01-hero.png",
      "description": "Inspectable product media shown inside the hero preview frame",
      "decision": "generate",
      "target_format": "webp"
    },
    {
      "id": "primary-button",
      "description": "Live CTA button",
      "decision": "code",
      "code_native_reason": "Live text, responsive sizing, hover/focus states, and keyboard interaction",
      "code_native_approved": true
    }
  ],
  "assets": [
    {
      "element_id": "hero-product-preview",
      "file": "public/assets/hero-product-crop.webp",
      "role": "hero product media",
      "source": "generated crop from section-01 reference",
      "alt": "Product interface shown on a calm green surface",
      "usage": "Hero visual",
      "status": "production"
    }
  ],
  "omitted": [
    {
      "item": "decorative glow around hero card",
      "reason": "Rebuilt in CSS for responsiveness"
    }
  ],
  "tool_attempts": [
    {
      "tool": "image generation",
      "action": "generate",
      "element_id": "hero-product-preview",
      "status": "success"
    }
  ],
  "qa": [
    {
      "element_id": "hero-product-preview",
      "status": "passed",
      "checks": ["desktop crop", "mobile crop", "alt text", "visual language"]
    }
  ]
}
```

If no assets are needed, still write a short manifest:

```json
{
  "ui_assets_complete": true,
  "semantic_media_policy": "no semantic media required",
  "references": [],
  "element_inventory": [
    {
      "id": "hero-gradient",
      "description": "Abstract background wash behind hero typography",
      "decision": "code",
      "code_native_reason": "Pure CSS gradient background, no inspectable media subject",
      "code_native_approved": true
    }
  ],
  "assets": [],
  "all_code_native_approved": true,
  "omitted": [
    {
      "item": "all visual elements",
      "reason": "Implemented as code-native typography, layout, CSS gradients, and components"
    }
  ],
  "tool_attempts": [],
  "qa": []
}
```

## Quality Rules

- Use modern formats where possible: WebP/AVIF for photos, SVG for vector marks, PNG only when transparency or tooling requires it.
- Name files by role: `hero-product.webp`, not `image-1.png`.
- Include width/height or stable aspect-ratio constraints in implementation.
- Keep meaningful image alt text in both manifest and code.
- Avoid heavy assets for simple CSS effects.
- Verify mobile crops separately; desktop-safe images often fail on mobile.
- Do not mark `ui_assets_complete: true` until every required generated/cropped/exported asset is present and referenced by the implementation.
