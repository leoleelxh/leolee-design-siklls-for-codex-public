# Visual Alignment QA

Use this after implementation or Figma export.

## Screenshot Set

Capture at minimum:

- desktop 1440x900,
- tablet 768x1024 when layout changes around tablet,
- mobile 390x844,
- any critical modal/menu/form state.

## Compare Against Reference

For each key frame, compare:

- hierarchy: same primary focal point,
- typography: approximate size, line-height, tracking, weight,
- spacing: section padding, gutters, card rhythm,
- color: token matches and contrast,
- media: crop, aspect ratio, semantic relevance,
- components: states and token mapping,
- responsive behavior: no clipping, overflow, or unreadable text.

## Tolerances

Use judgment, but flag:

- H1 differs by more than one visible scale step,
- CTA moves below first viewport when reference keeps it above fold,
- section rhythm collapses or becomes much denser,
- mobile crop hides the subject,
- generated asset is used as full comp background instead of semantic media,
- screenshot is passed off as editable Figma.

## Output

Record `design/qa-report.md`:

```markdown
# QA Report

Reference: design/references/section-01-hero.png
Implementation: qa/desktop-1440.png
Status: pass | needs-fix | accepted-delta

Findings:
- ...

Fixes made:
- ...

Accepted deltas:
- ...
```
