# Production Pipeline

Use this as the hard contract for end-to-end design work. A task is not complete until every applicable phase has its required artifact and gate result. Read [execution-protocol.md](execution-protocol.md) before bypassing or downgrading any phase.

## Phase Gates

| Phase | Required artifacts | Gate to next phase |
|---|---|---|
| 0 Intake | `design/brief.md` or brief section in `DESIGN.md`; scope choice; output target | Brief has artifact, audience, goal, constraints, delivery target, and risk notes. |
| 1 Style exploration | `design/style-directions.md`; 3 concept directions or explicit opt-out; prompt(s); three concept images or storyboard; recommendation | User confirmed one direction, requested a hybrid, or explicitly authorized auto-selection. Otherwise stop in `WAITING_FOR_USER_DIRECTION_CONFIRMATION`. |
| 1.5 Post-confirmation asset planning | selected direction recorded in `design/traceability.json`; selected reference(s); `POST_CONFIRMATION_ASSET_LOOP`; element inventory draft | The selected concept has been translated into code/token/component/asset/omit decisions before implementation starts. |
| 2 Design spec | `design/frame-spec.md`; frame specs; layout grid; responsive rules; component states | Every section/screen has measurable frame and state specs. |
| 3 Asset extraction | `public/assets/asset-manifest.json`; element inventory; asset decisions; generated/cropped/exported files; tool attempts | Every visual element is classified as code/token/component/asset/omit and `ui_assets_complete` is true or the phase is explicitly blocked. |
| 4 Design system | `design/tokens.json`; component inventory; token-to-code mapping | Tokens and reusable components are named, mapped, and discoverable. |
| 5 Implementation | Runnable project; components/sections/data split; asset loading | App runs locally, first screen is code-native, not a flat screenshot. |
| 6 Editable Figma, if requested | Figma file/link or `figma-handoff.md`; variables/components/layers | Output is editable Figma nodes or explicitly marked as handoff-only. |
| 7 Visual QA | screenshots or QA notes; browser/design-tool checks; diff notes | Desktop/mobile reviewed; gaps fixed or documented. |
| 8 Preservation | `DESIGN.md`; manifest; tokens; component inventory; trace ledger | Reusable assets saved or draft status documented. |

## No-Skip Rules

- Do not enter implementation before Phase 1 and Phase 2 unless the user opts out, explicitly authorizes auto-selection, or the task is a constrained redesign.
- Do not continue past style exploration after producing three concept directions until user confirmation is recorded.
- Do not treat an agent recommendation as user confirmation; recommended direction is not selected direction.
- Do not make additional tool calls in the same turn after presenting three concepts, except to display the already-created concept artifacts.
- Do not jump from a confirmed direction directly into frontend implementation. First run `POST_CONFIRMATION_ASSET_LOOP`, create the element inventory, and complete the UI asset manifest.
- Do not deliver code without Phase 4 when creating a new runnable design.
- Do not call a screenshot, PNG, or PDF an editable Figma deliverable.
- Do not default to Figma-ready handoff when Figma was requested until native Figma tooling and HTML/DOM-to-Figma conversion have both been evaluated and logged.
- Do not finish without a trace ledger.
- Do not downgrade silently. Record explicit user opt-out, failed tool attempt, or environment blocker before bypassing.
- Do not call a frontend final when `ui_assets_complete` is false.

## Trace Ledger

Maintain `design/traceability.json` or an equivalent section in `DESIGN.md`.

```json
{
  "brief_id": "brief-001",
  "selected_direction": "direction-b",
  "references": [
    {
      "id": "ref-hero-001",
      "file": "design/references/section-01-hero.png",
      "prompt_file": "design/prompts/section-01-hero.md",
      "critique": "Strong hierarchy, needs lower hero density"
    }
  ],
  "tokens": ["color.accent", "type.display", "radius.card"],
  "assets": ["asset.hero-product"],
  "components": ["Button", "HeroSection", "FeatureCard"],
  "implementation": ["src/sections/Hero.tsx"],
  "tool_attempts": [
    {
      "phase": "asset generation",
      "tool": "image generation",
      "purpose": "Generate transparent headshot PNG",
      "result": "success",
      "outputs": ["public/assets/headshot-alpha.png"]
    }
  ],
  "qa": ["qa-desktop-1440", "qa-mobile-390"]
}
```

## Final Report

Final handoff must say:

- which phases were completed,
- which gates were bypassed and why,
- which artifacts are production-ready vs draft,
- which tools were used,
- which assets/tokens/components are reusable,
- which items still need designer/user approval.
