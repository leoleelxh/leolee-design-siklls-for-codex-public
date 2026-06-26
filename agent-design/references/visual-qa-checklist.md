# Visual QA Checklist

Run this before delivering substantial design work.

## First Viewport

- The subject or offer is visible immediately.
- H1 is readable, short, and not clipped.
- Primary CTA is visible without scrolling on desktop.
- Navigation fits on one line and does not crowd the hero.
- Imagery is semantically relevant and not a generic filler shape.

## Layout

- No horizontal overflow at desktop or mobile widths.
- No overlapping text, clipped buttons, cut-off cards, or hidden focus rings.
- Section layouts vary. Avoid repeated center blocks or repeated left-text/right-image sections.
- Containers use stable max-widths and responsive grid tracks.
- Full-height sections use `min-height: 100dvh`, not `height: 100vh`.

## Typography

- Display text has enough line-height for descenders.
- Body copy is limited to comfortable line length.
- Labels are not overused. Eyebrows should be rare and meaningful.
- Avoid title case everywhere unless the brand requires it.
- No generic filler copy, placeholder Latin, or fake company/person names.

## Color And Material

- One accent color is used consistently.
- Neutrals belong to one family.
- Buttons and text pass contrast checks.
- Dark and light sections do not randomly alternate.
- Shadows, borders, radius, and material effects follow one visible rule.

## Imagery

- Product, food, place, person, portfolio, or object pages show inspectable bitmap imagery.
- Generated or real images are clear, not dark/cropped/blurred beyond usefulness.
- Image treatments match the brand palette.
- Alt text exists for meaningful images.
- No fake screenshot boxes when a real screenshot, generated comp, or explicit placeholder slot is needed.

## Interaction States

- Buttons have hover, active, focus, disabled where applicable.
- Forms have focus, validation, error, loading, and success states.
- Loading uses skeletons or state-shaped placeholders, not only generic spinners.
- Empty states explain the next action.
- Motion respects `prefers-reduced-motion`.

## Browser Pass

- Capture desktop screenshot around 1440x900.
- Capture mobile screenshot around 390x844.
- Interact with navigation, menu, primary CTA, forms, tabs, accordions, and any animated surface.
- Verify no console errors for the changed page.
- Re-check after fixes.

Playwright/e2e checks are optional self-test tools. Use them when a runnable app exists or when this repository's test fixture is being maintained. Do not treat e2e as a required dependency of the skill itself.

## Final Question

Would a designer believe this was intentionally art-directed for this brief, or does it still look like a default AI template?
