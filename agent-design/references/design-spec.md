# Design Spec

Use this after selecting a style direction and before implementation.

## Required Spec Artifacts

For each page/screen/section, create a frame spec. Store it in `design/frame-spec.md` or in `DESIGN.md`.

```markdown
## Frame: Home / Hero

Purpose: Hook and primary conversion.
Viewport: desktop 1440x900, mobile 390x844.
Grid: 12 columns, 80px margin, 24px gutter.
Layout: left 5 columns text, right 7 columns visual, collapse to single column under 768px.
Typography:
  H1: display-xl, 76/82 desktop, 44/48 mobile
  Body: text-lg, max 58ch
Tokens:
  color.background.default
  color.accent.primary
  radius.surface.lg
Components:
  HeroSection
  Button primary/default/hover/focus/disabled
Assets:
  asset.hero-product
States:
  default, loading visual placeholder, reduced-motion
Responsive:
  1440, 1024, 768, 390
Acceptance:
  CTA visible above fold; no text clipping; visual crop meaningful on mobile.
```

## Component States

Every reusable component needs:

- default,
- hover,
- active,
- focus-visible,
- disabled,
- loading when applicable,
- empty/error/success when applicable,
- mobile behavior.

## Design Spec Gate

Implementation can start only after:

- every section has a frame spec,
- every asset reference has an asset decision,
- every reusable component has states,
- tokens are named before CSS is written,
- responsive breakpoints are declared.
