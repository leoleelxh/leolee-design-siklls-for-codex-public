# Execution Protocol

Use this to prevent silent downgrade. The agent must treat missing gate artifacts as a blocked phase, not as permission to skip the pipeline.

## Deterministic Rule

Before moving from one phase to the next, run a gate check:

```text
Gate check:
- Required artifact:
- Exists: yes | no
- If no, action: create it now | record failed attempt | ask user
- Decision: pass | blocked | bypassed by explicit user request
```

Do not continue into implementation when the gate is `blocked`.

For style exploration, use the strict gate check:

```text
Gate check:
- Phase: style exploration
- Required artifact: three concept directions
- Exists: yes
- User confirmation: no
- Decision: blocked
- State: WAITING_FOR_USER_DIRECTION_CONFIRMATION
```

When this state is active, stop the turn after asking the user to choose. Do not use the agent's recommendation as confirmation.

After the user confirms a direction, use the strict post-confirmation gate:

```text
Gate check:
- Phase: post-confirmation asset planning
- Required artifact: selected direction + element inventory + asset loop plan
- Exists: yes | no
- Decision: pass | blocked
- State: POST_CONFIRMATION_ASSET_LOOP
```

When `POST_CONFIRMATION_ASSET_LOOP` is active, run the UI asset generation loop before implementation or Figma export. Do not continue directly from "Direction B confirmed" to code.

## No Silent Downgrade

The agent may downgrade only when one of these is true:

- the user explicitly requested the downgrade,
- a required tool was attempted and failed,
- the environment cannot support the required path,
- the existing project constraints make the path harmful.

Every downgrade must be recorded in `design/traceability.json` or `DESIGN.md`:

```json
{
  "downgrades": [
    {
      "from": "editable Figma",
      "to": "Figma-ready handoff",
      "reason": "No callable Figma tool available in this environment",
      "attempted": ["tool_search figma", "checked available tools"],
      "approved_by_user": false,
      "status": "accepted limitation"
    }
  ]
}
```

## Tool Attempt Log

If a phase requires a tool, log the attempt.

Examples:

- image generation,
- asset background removal/crop,
- image optimization,
- Figma MCP/create/edit,
- browser screenshot,
- visual QA,
- project build/test.

Required format:

```json
{
  "tool_attempts": [
    {
      "phase": "style exploration",
      "tool": "image generation",
      "purpose": "Generate Direction B hero reference",
      "result": "success",
      "outputs": ["design/references/direction-b-hero.png"]
    }
  ]
}
```

If the image tool exists, use it. If it fails, log the failure and create a storyboard fallback. Do not pretend image references exist.

## Hard Stops

Stop and report instead of continuing when:

- no style reference/storyboard exists for a new visual design,
- three concept directions have been produced but the user has not confirmed one,
- `WAITING_FOR_USER_DIRECTION_CONFIRMATION` is active,
- a direction was confirmed but `POST_CONFIRMATION_ASSET_LOOP` has not produced an element inventory and asset manifest,
- no design spec exists before frontend implementation,
- no asset manifest exists before implementation references assets,
- Figma was requested but no `figma-export.json` path decision exists,
- no token/component preservation exists for a new runnable demo,
- Figma was requested but no editable Figma path or handoff fallback is produced.

## Completion Proof

Final response must include:

- phase gates passed,
- bypassed gates and why,
- tool attempts,
- generated reference files,
- asset manifest path,
- tokens/component inventory path,
- validation command and result.
