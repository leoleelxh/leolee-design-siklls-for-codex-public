# Design DNA Schema

Use this schema when extracting a reference style or defining a reusable design direction.

```json
{
  "design_system": {
    "color": {
      "mode": "light | dark | adaptive",
      "primary": "#000000",
      "secondary": "#000000",
      "accent": "#000000",
      "neutral_scale": ["#ffffff", "#f5f5f5", "#111111"],
      "contrast_notes": "Where contrast needs protection"
    },
    "typography": {
      "display_family": "visual classification or exact font",
      "body_family": "visual classification or exact font",
      "mono_family": "optional",
      "scale": "compact | standard | editorial | poster",
      "weight_range": "300-800",
      "line_height": "tight | normal | relaxed",
      "letter_spacing": "normal | tight display | tracked labels"
    },
    "spacing": {
      "density": "airy | balanced | dense",
      "section_gap": "small | medium | large | cinematic",
      "container_width": "e.g. 1120px, 1280px, 1440px",
      "grid": "columns, gutters, breakpoints"
    },
    "shape": {
      "radius_scale": "sharp | 4px | 8px | 12px | 16px | pill",
      "border_style": "none | hairline | strong | mixed with rule",
      "shadow_style": "none | soft | tinted | hard | layered"
    },
    "components": {
      "buttons": "shape, contrast, hover, active, focus",
      "cards": "when used and how elevated",
      "forms": "field style and validation treatment",
      "navigation": "position, density, active state"
    },
    "motion": {
      "intensity": 1,
      "duration_range_ms": "150-700",
      "easing": "spring | ease-out | linear | custom",
      "reduced_motion": "fallback behavior"
    }
  },
  "design_style": {
    "artifact_type": "landing page | app | dashboard | poster | deck | other",
    "audience": "who scans it and under what pressure",
    "mood": ["calm", "technical", "editorial"],
    "composition": "centered | asymmetric | grid | editorial | cinematic",
    "imagery": "photo, product render, screenshots, illustration, none",
    "material": "paper, glass, matte, metal, flat, tactile",
    "voice": "plain, premium, playful, clinical, editorial",
    "anti_references": ["patterns to avoid"]
  },
  "visual_effects": {
    "enabled": true,
    "canvas_webgl": "none | canvas | three.js | shader",
    "scroll_effects": "none | reveal | pinned | parallax | horizontal",
    "micro_interactions": "hover, active, focus, drag, cursor",
    "media": "image, video, generated bitmap, 3D object",
    "performance_tier": "low | medium | high",
    "risk_notes": "browser, mobile, accessibility, motion sensitivity"
  }
}
```

Extraction rules:

- Populate every field. Use `unknown` only when the reference truly gives no signal.
- Separate measured facts from inference.
- If a URL is provided, inspect the actual page and assets when possible.
- If screenshots conflict, choose the dominant pattern and list variants.
- Keep the output concise enough to guide implementation.
