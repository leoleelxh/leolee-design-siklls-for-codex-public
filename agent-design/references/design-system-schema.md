# Design System Schema

Use this when preserving tokens, components, Figma variables, or code mappings.

## Tokens

Store tokens in `design/tokens.json` unless the project has a stronger existing convention.

```json
{
  "color": {
    "background": { "default": "#ffffff", "subtle": "#f7f7f5" },
    "text": { "strong": "#111827", "muted": "#5b6472" },
    "accent": { "primary": "#1f6f5f", "onPrimary": "#ffffff" },
    "border": { "default": "#d9ddd6" }
  },
  "typography": {
    "fontFamily": {
      "display": "Geist, system-ui, sans-serif",
      "body": "Geist, system-ui, sans-serif",
      "mono": "JetBrains Mono, ui-monospace, monospace"
    },
    "scale": {
      "display-xl": { "fontSize": "76px", "lineHeight": "82px", "letterSpacing": "-0.04em" },
      "body-md": { "fontSize": "16px", "lineHeight": "26px" }
    }
  },
  "spacing": {
    "section": { "desktop": "96px", "mobile": "56px" },
    "container": { "maxWidth": "1180px", "gutter": "24px" }
  },
  "radius": {
    "sm": "8px",
    "md": "12px",
    "lg": "18px",
    "pill": "999px"
  },
  "shadow": {
    "surface": "0 24px 80px rgb(17 24 39 / 0.14)"
  },
  "motion": {
    "duration": { "fast": "160ms", "normal": "260ms" },
    "easing": { "standard": "cubic-bezier(.2,.8,.2,1)" }
  }
}
```

## Code Mapping

Document where tokens landed:

```json
{
  "token_mapping": [
    {
      "token": "color.accent.primary",
      "css_variable": "--color-accent-primary",
      "tailwind": "accent-primary",
      "figma_variable": "color/accent/primary",
      "used_by": ["Button", "HeroSection"]
    }
  ]
}
```

## Component Inventory

Store as `design/component-inventory.json` or in `DESIGN.md`.

```json
{
  "components": [
    {
      "name": "Button",
      "type": "primitive",
      "source": "src/components/Button.tsx",
      "figma_component": "Button",
      "props": {
        "variant": ["primary", "secondary", "ghost"],
        "size": ["sm", "md", "lg"],
        "disabled": "boolean",
        "loading": "boolean"
      },
      "states": ["default", "hover", "active", "focus-visible", "disabled", "loading"],
      "tokens": ["color.accent.primary", "radius.pill", "motion.duration.fast"]
    }
  ]
}
```

## Component Extraction Rules

Extract a component when:

- it repeats,
- it has multiple states,
- it uses named tokens,
- it maps to a Figma component,
- it is likely to be reused across pages.

Do not extract a component just to make the file tree look busy. Sections should be components; tiny one-off decorative elements do not need component files.
