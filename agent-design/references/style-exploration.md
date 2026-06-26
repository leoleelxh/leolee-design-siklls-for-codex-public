# Style Exploration

Use this before new visual design when the user has not already chosen a style direction.

This phase is a user-confirmation gate and hard stop. Do not continue to design spec, asset generation, Figma export, or frontend implementation until the user confirms one direction, unless the user explicitly authorized auto-selection in the same request.

Recommendation is advisory only. Do not treat the recommended direction, visual quality, obvious fit, silence, or the agent's own judgment as user authorization.

Before generating concept images, ensure the brief contains the project/name, purpose, artifact type, audience, and desired aesthetic family. Ask for missing values only once. If these values were already gathered during scoping, do not ask again; substitute them into the concept prompts.

## Required Directions

Create three directions unless the user explicitly asks for one exact style. Each direction must be a relatively complete concept board for the requested artifact type, not a single isolated shot.

1. **Conservative / usable**: restrained, production-safe, accessibility-first.
2. **Expressive / premium**: stronger art direction, polished brand feel.
3. **Experimental / brand-led**: high variance, memorable composition, controlled risk.

Each direction must include:

- name,
- one concept image or storyboard,
- one-sentence concept,
- image-generation prompt,
- palette and typography direction,
- layout/composition pattern,
- asset needs,
- strengths,
- risks,
- best-fit use case,
- implementation complexity.

## Artifact-Aware Concept Board

Choose the concept-board template by artifact type. Each direction produces one concept image/storyboard that previews the whole deliverable at the right level of completeness. Mobile app boards are only for mobile app requests, not the universal default.

| Artifact type | Concept board should show |
|---|---|
| Mobile app | 1 welcome/onboarding screen, 1 home screen, 2 product/service/detail screens. |
| Website / web app | Desktop first viewport, one mid-page section, one product/service/detail section, and one mobile responsive crop. |
| Landing page | Hero, proof/features, conversion section, and mobile crop. |
| Dashboard / product UI | Main dashboard, detail/table view, empty/loading/error state, and mobile/tablet adaptation when relevant. |
| PPT/deck | Cover slide, agenda/section divider, content slide, data/visual slide. |
| Poster / social graphic | Main poster, typography/layout detail, alternate crop, asset/texture/detail swatch. |
| Logo / brand identity | Primary logo, lockup/wordmark, icon mark, usage on simple surface plus palette/type swatches. |
| Design system | Foundation tokens, core components, sample screen, states/variants. |

After the user confirms one direction, the later spec, assets, code project, and Figma output must map back to the same artifact type.

## Universal Prompt Structure

Use this structure for each direction, replacing values from the scoped brief:

```text
创建一张 [board_ratio] 的 [artifact_type] 概念样机图，强调设计感并采用统一的设计系统。
项目/应用名称：[project_name]
用途：[project_purpose]
受众：[audience]
审美风格：[direction_aesthetic]
展示内容：[artifact_specific_frames]
样机图中不要包含与产物无关的元素、场景摆拍、外部物体、手、品牌水印或无意义装饰。
所有画面需要体现统一的颜色、字体、间距、圆角、组件语言、图标/图形风格和信息层级。
文字应短、真实、可读，避免 lorem ipsum 和无意义占位。
```

Recommended board ratio:

- Web, mobile, dashboard, deck, design system: `5.5x3` wide board.
- Poster/social: use the final intended ratio plus a detail strip, unless user requests otherwise.
- Logo/brand identity: `5.5x3` brand board.

## Mobile App Prompt Template

Use this only when the artifact type is a mobile app.

```text
创建一张 5.5x3 的新应用样机图，强调设计感并采用统一的设计系统。
应用名称：[app_name]
应用用途：[app_purpose]
审美风格：[direction_aesthetic]
展示 1 个不含摄影图片的移动端欢迎页、1 个移动端首页，以及 2 个产品或服务页面。
四个移动端页面需要放在同一张样机图中，形成一个完整应用概念方向。
样机图中不要包含任何其他元素，不要出现桌面设备、装饰性摄影图片、外部物体、手、场景背景或品牌水印。
页面 UI 需要体现统一的颜色、字体、间距、圆角、组件语言和图标风格。
文字应短、真实、可读，避免 lorem ipsum 和无意义占位。
```

## Website Prompt Template

```text
创建一张 5.5x3 的网站/网页应用概念样机图，强调设计感并采用统一的设计系统。
项目名称：[project_name]
用途：[project_purpose]
受众：[audience]
审美风格：[direction_aesthetic]
展示 1 个桌面端首屏、1 个中段功能/价值展示区、1 个产品或服务详情区，以及 1 个移动端响应式裁切预览。
样机图中不要包含与网页无关的设备摆拍、手、场景摄影或品牌水印。
所有区域需要体现统一的导航、按钮、卡片、网格、字体、颜色和动效暗示。
```

## Deck Prompt Template

```text
创建一张 5.5x3 的演示文稿设计概念样机图，强调统一的演示设计系统。
项目名称：[project_name]
用途：[project_purpose]
受众：[audience]
审美风格：[direction_aesthetic]
展示 1 张封面页、1 张目录/章节页、1 张正文内容页，以及 1 张数据或视觉叙事页。
不要包含真实摄影场景、手、设备摆拍或无关装饰。
需要体现统一的版式网格、标题层级、图表语言、页码/章节系统、颜色和字体。
```

## Poster Prompt Template

```text
创建一张 [final_ratio] 的海报/社交视觉概念图，强调完整视觉系统和可落地的平面设计。
项目名称：[project_name]
用途：[project_purpose]
受众：[audience]
审美风格：[direction_aesthetic]
展示主海报构图、标题字体处理、关键信息区域、图形/纹理/插画细节，以及一个可用于延展的裁切版本。
不要包含与海报无关的设备摆拍、手、场景摄影或品牌水印。
文字需要短、真实、可读，信息层级清晰。
```

## Logo / Brand Prompt Template

```text
创建一张 5.5x3 的品牌识别概念板，强调可编辑和可延展的设计系统。
品牌名称：[project_name]
品牌用途：[project_purpose]
受众：[audience]
审美风格：[direction_aesthetic]
展示主 logo、横向 lockup、独立 icon mark、基础色板、字体方向，以及 1 个简单应用场景。
不要包含摄影场景、复杂包装摆拍、手、无关物体或品牌水印。
图形应清晰、可矢量化、可在 Figma 中重建。
```

For the three default directions, replace `[direction_aesthetic]` with:

- Direction A: conservative/usable version of the user's requested style.
- Direction B: expressive/premium version of the user's requested style.
- Direction C: experimental/brand-led version of the user's requested style.

If the user specified one exact aesthetic, still create three variants inside that aesthetic unless they explicitly requested only one concept.

## Direction Template

```markdown
## Direction A: <name>

Concept image: design/references/direction-a.png
Concept: ...
Prompt: use the artifact-specific concept-board template with project_name/project_purpose/audience/direction_aesthetic filled in.
Palette: ...
Typography: ...
Composition: ...
Artifact mapping: how this concept maps to final engineering project and Figma frames/components.
Assets needed: ...
Strengths: ...
Risks: ...
Best fit: ...
Implementation complexity: low | medium | high
```

## Gate

Stop after presenting all three directions and ask the user to choose. In the same assistant turn that presents the three concepts:

- do not decide the winner,
- do not write `Selected direction`,
- do not call further tools,
- do not create design spec,
- do not generate implementation assets,
- do not scaffold or edit frontend code,
- do not create or export Figma output.

Use this exact state marker in the response:

```text
Gate status: WAITING_FOR_USER_DIRECTION_CONFIRMATION
```

Then use a concise confirmation prompt:

```text
Please choose Direction A, B, or C before I continue to design spec, asset generation, and implementation. Recommended: Direction B because <reason>.
```

The gate passes only with one of:

- user chooses Direction A/B/C,
- user asks for a hybrid direction and you produce the hybrid concept,
- user explicitly says to auto-select the recommended direction.

The phrase "Recommended: Direction B" does not pass the gate. The agent must wait for the user's next message unless the original user request already said to auto-select.

Record the result:

```text
Selected direction: Direction B
Confirmed by: user | auto-selected by explicit instruction
Reason: strongest fit for <audience/goal>, feasible in <framework>, supports <brand constraint>.
Rejected: Direction A because...
Rejected: Direction C because...
```

If image generation is unavailable after an attempted tool call, still write the three prompts and a storyboard. Mark the gate as `storyboard-only`, present the three directions, and wait for user confirmation.
