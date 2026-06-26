# UI Asset Generation Loop

Use this when generated style references contain visual elements that need frontend assets.

## Invocation Trigger

Run this immediately after the user confirms a concept direction. Treat confirmation phrases like "choose B", "go with Direction B", "continue with this one", or "use the recommended direction" as the start of `POST_CONFIRMATION_ASSET_LOOP`, not as permission to skip into code.

The first post-confirmation action is to map the selected reference into an element inventory. The second action is to generate/crop/export/reuse required semantic assets until the manifest is complete. Only then continue to implementation or Figma export.

## Principle

A style reference is not enough. After selecting a direction, create the actual UI assets through a loop:

```text
style reference -> element inventory -> code/token/asset decision -> asset prompt -> generated asset -> QA -> manifest -> implementation
```

Repeat until the manifest says `ui_assets_complete: true`.

## Completeness Gate

For a new visual product, app, site, deck, poster, or brand demo, scan the selected concept for semantic media candidates before implementation. If the element inventory includes preview, stage, project card, thumbnail, mockup, cover, poster, hero media, product media, gallery item, texture, illustration, sticker, headshot, logo, brand mark, or inspectable product/service imagery, at least one matching `generate`, `crop`, `export`, `reuse`, or `sprite` asset must become `ready` or `production`.

Only bypass generated/cropped/exported/reused assets when every semantic media candidate is truly code-native. In that case, each item needs `decision: "code"`, `code_native_reason`, and `code_native_approved: true`, and the manifest needs `all_code_native_approved: true`. Without that proof, stop before final delivery.

## Element Inventory

For each selected reference frame, list all visual elements:

```json
{
  "element_inventory": [
    {
      "id": "hero-product-preview",
      "source_reference": "design/references/section-01-hero.png",
      "description": "Floating product studio mockup",
      "decision": "generate",
      "target_format": "webp",
      "needs_transparency": false,
      "code_native_reason": null
    },
    {
      "id": "primary-button",
      "description": "Rounded CTA with hover state",
      "decision": "code",
      "code_native_reason": "Live text, responsive sizing, interactive states",
      "code_native_approved": true
    }
  ]
}
```

Decision values:

- `code`: layout, typography, buttons, cards, grids, simple gradients, live UI.
- `token`: colors, spacing, radius, shadows, motion.
- `component`: repeated UI patterns.
- `generate`: semantic bitmap or illustration needed.
- `crop`: existing/generated reference contains usable subject.
- `export`: Figma/brand/logo/custom vector asset.
- `sprite`: related small icons/stickers that should ship together.
- `omit`: decoration that does not serve the final design.

## Multi-Round Generation

For each `generate`, `crop`, `export`, `reuse`, or `sprite` item:

1. Write an asset-specific prompt or export instruction.
2. Generate/crop/export the asset as a separate file.
3. QA the asset:
   - subject is clear,
   - transparent cutout actually has alpha if required,
   - crop works at desktop and mobile aspect ratios,
   - no baked-in UI text unless static art,
   - visual language matches selected direction,
   - file format is correct.
4. If QA fails, revise the prompt and regenerate.
5. Add the final asset to manifest.

Do not proceed to frontend implementation until all required asset items are `ready`, `production`, `omitted`, or approved `code`.

For semantic media items, `code` is allowed only with a strong `code_native_reason`. Preview stages, project thumbnails, mockups, cover art, stickers, avatars, and brand illustrations should normally be generated/cropped/exported/reused as assets.

If the selected direction contains media but the model believes the media can be code-native, it must still write the element inventory first and explicitly approve each code-native item. Do not infer that "all assets are CSS" without a manifest.

## Format Rules

| Asset type | Preferred format |
|---|---|
| Photo/hero/product mockup | `.webp` or `.avif` |
| Transparent cutout/headshot/object/sticker | `.png` with alpha |
| Logo/custom mark/vector icon | `.svg` |
| Icon set/sticker set | SVG set or sprite sheet plus metadata |
| Texture/noise/pattern | small `.png`, `.webp`, CSS, or SVG |
| Open graph/static poster | `.png` or `.jpg` |

For transparent subjects, generate or process a separate PNG with alpha. Do not fake transparency with a white background.

## Sprite Sheet Rule

Use a sprite sheet when multiple small related assets are used together, such as icons, stickers, badges, emoji-like reactions, or mini illustrations.

Required files:

```text
public/assets/icons-sprite.png
public/assets/icons-sprite.json
```

Metadata example:

```json
{
  "sprite": "icons-sprite.png",
  "cell_size": [96, 96],
  "items": [
    {
      "id": "wechat-sticker",
      "x": 0,
      "y": 0,
      "width": 96,
      "height": 96,
      "alt": "Rounded chat sticker with smiling face"
    }
  ]
}
```

Prefer individual SVG files over bitmap sprites when the icons are simple vector shapes or come from an icon library.

## Manifest Completion

`asset-manifest.json` must include:

```json
{
  "ui_assets_complete": true,
  "semantic_media_policy": "all semantic media generated/cropped/exported/reused or justified as code-native",
  "references": [],
  "element_inventory": [
    {
      "id": "hero-preview-frame",
      "description": "Inspectable preview media for the selected concept",
      "decision": "generate",
      "target_format": "webp"
    }
  ],
  "assets": [
    {
      "element_id": "hero-preview-frame",
      "file": "public/assets/hero-preview-frame.webp",
      "role": "hero preview media",
      "source": "generated asset",
      "alt": "Generated preview media matching the selected concept",
      "usage": "Hero preview frame",
      "status": "production"
    }
  ],
  "all_code_native_approved": false,
  "omitted": [],
  "tool_attempts": [
    {
      "tool": "image generation",
      "action": "generate",
      "element_id": "hero-preview-frame",
      "status": "success"
    }
  ],
  "qa": [
    {
      "element_id": "hero-preview-frame",
      "status": "passed"
    }
  ]
}
```

If generation failed, set `ui_assets_complete: false`, explain why, and do not claim the frontend is final.

## Examples

For a social/content generator product, likely generated assets:

- GIF preview thumbnail: WebP or PNG sequence depending on UI need.
- AI headshot: PNG with alpha when floating over UI; WebP when framed in card.
- WeChat sticker: PNG alpha or sprite sheet.
- XHS cover: PNG/JPG as static poster art.
- Product studio/mockup: WebP hero media.
- Background cutout: PNG alpha if subject must float; CSS gradient if abstract.

Everything else, including panels, text, buttons, labels, cards, tabs, and grids, should be code-native.
