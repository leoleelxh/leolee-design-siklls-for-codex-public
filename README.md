# Agent Design Skill

Codex-first design skill for design scoping, image-led art direction, design-to-code implementation, asset handoff, redesign audits, and visual QA.

这个仓库实现了 `docs/prd.md` 和 `docs/prd-adition.md` 的目标：把开源设计类 skills 的思路综合成一个专属的 `agent-design` skill，并把真实设计流程沉淀成规范。Playwright/Chrome 是仓库自测工具，不是 skill 运行的必要依赖。

## What It Does

- 用户输入模糊时，先用专业范围选项澄清：范围、风格、保真度、交付形态和资产深度。
- 先判断设计语境，再决定是 `image-first`、`redesign`、`product-ui`、`design-dna` 还是 `qa-only`。
- 对新页面强制走「范围澄清 -> 生图参考 -> 切图/assets -> HTML/Figma 交付 -> 浏览器或设计工具检查 -> 资产沉淀」的闭环，除非用户明确跳过生图或工具不可用。
- 对可运行 demo 默认使用工程化项目结构，优先 Vite/React/Tailwind 或 Next.js/Tailwind，不默认输出单文件 HTML。
- 把“切图”定义为结构化资产提取：布局、文字、组件、状态用代码重建，只有语义图片、纹理、图标、logo、复杂插画等进入 assets。
- 新 demo 必须沉淀设计资产：`DESIGN.md`、tokens、asset manifest、组件/section 清单；除非用户明确要一次性草稿。
- 增加 production pipeline gate：brief、style exploration、design spec、asset extraction、design system、implementation、editable Figma、visual QA、preservation 每阶段都有产物和验收门槛。
- 增加 editable Figma 链路：优先 Figma 工具/MCP 直接建 frames/variables/components；否则参考开源 HTML/DOM-to-Figma 方案，把渲染 DOM 转成可编辑 Figma 节点，再做变量和组件归一。
- 对已有项目先审计，再做低风险视觉升级，避免破坏路由、SEO、表单、分析事件和品牌资产。
- 用 `agent-design/scripts/design_audit.py` 扫描常见 AI 设计痕迹和基础 UX 问题。
- 可选使用 Playwright 在桌面和移动端跑视觉自测，也支持对运行中的本地项目设置 `TARGET_URL`。

## Structure

```text
agent-design/
  SKILL.md
  agents/openai.yaml
  references/
    design-process.md
    engineering-delivery.md
    asset-pipeline.md
    production-pipeline.md
    style-exploration.md
    design-spec.md
    figma-export.md
    design-system-schema.md
    visual-alignment.md
    design-dna-schema.md
    source-index.md
    visual-qa-checklist.md
  scripts/
    design_audit.py
e2e/
  design-skill.spec.ts
  fixtures/premium-landing.html
docs/prd.md
```

## Install As A Codex Skill

Copy or symlink `agent-design/` into your Codex skills directory, or publish this repository and install it through your preferred skill workflow.

Example local copy:

```bash
cp -r agent-design ~/.codex/skills/agent-design
```

Then invoke it in Codex:

```text
Use $agent-design to redesign this landing page with image-first exploration and browser QA.
```

## Optional Self-Testing

Install dependencies:

```bash
npm install
```

Run deterministic audit. This is the default test because it does not require a browser:

```bash
npm test
```

Run optional Playwright visual checks against the built-in fixture:

```bash
npm run test:e2e
```

Run Playwright against a local app:

```bash
TARGET_URL=http://localhost:3000 npm run test:e2e
```

The Playwright suite uses the local Chrome channel and checks desktop/mobile layout, CTA visibility, horizontal overflow, image alt text, and basic button contrast.

## Platform Note

This skill is designed for Codex and similar environments that can generate images and inspect pages in a browser. Claude without image-generation tooling is not the target runtime. If you use an external image model API, configure it in your environment and let the agent read that configuration instead of hardcoding a model name.

## References

The implementation is original, but it synthesizes public design-skill ideas and cites the sources in [agent-design/references/source-index.md](agent-design/references/source-index.md).

Primary references:

- Impeccable: https://impeccable.style/
- Taste Skill: https://github.com/Leonxlnx/taste-skill
- Agent Skills Hub AI Design list: https://agentskillshub.top/best/ai-design/
- Dominik Kundel's Codex image-first design-to-app idea: https://x.com/dkundel/status/2049591675518165134

Reference categories covered:

- 通用 UI 审美护栏：Impeccable、Taste Skill
- 从图片到代码：Taste Skill 的 `image-to-code`、Impeccable 的 `craft`、Codex Build Web Apps plugin/workflows
- 高保真设计交付台：Huashu Design、Open Design
- 设计系统沉淀：Google Stitch Skills、Design DNA、Hue、design-extract
- 灵感与资源库：awesome-design-skills、awesome-claude-design

Before public release, choose a license that matches your intended usage and add it at the repository root.
