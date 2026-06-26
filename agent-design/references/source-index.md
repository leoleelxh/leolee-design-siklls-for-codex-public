# Source Index

This project synthesizes public design-skill and design-agent ideas. Use this file for attribution, further study, and release notes. Do not vendor or copy long passages from sources.

## Reference Map

Use these categories when explaining what this skill absorbed and when expanding the skill.

| Category | Sources | Absorbed role |
|---|---|---|
| General UI taste guardrails | Impeccable, Taste Skill | Anti-slop checks, brief inference, design QA, visual standards |
| Image to code | Taste Skill `image-to-code`, Impeccable `craft`, Codex Build Web Apps plugin/workflows | Convert visual references into code-native layout, assets, and verification |
| High-fidelity delivery bench | Huashu Design, Open Design | HTML-native high-fidelity prototypes, local-first design delivery, animation-rich previews |
| Design system preservation | Google Stitch Skills, Design DNA, Hue, design-extract | Tokens, design DNA, component systems, style extraction, reusable libraries |
| Inspiration and resource libraries | awesome-design-skills, awesome-claude-design | Ecosystem survey, aesthetic references, community patterns |
| HTML/DOM to editable Figma | A2F Figma plugin, BuilderIO/figma-html, lgs/html-figma, sergcen/html-to-figma, cranch42/h2d-capture | Convert rendered DOM/computed styles into editable Figma nodes or clipboard payloads |

## Primary References

- Impeccable: https://impeccable.style/
  - Patterns absorbed: design vocabulary, slop detection, product-context files, DESIGN.md portability, live/browser iteration, `craft`-style image-to-code thinking, and source-writing workflows.
- Taste Skill: https://github.com/Leonxlnx/taste-skill
  - Patterns absorbed: anti-generic frontend rules, brief inference, redesign audits, `image-to-code` and image-generation reference boards, dials for variance/motion/density, and final pre-flight checks.
- Agent Skills Hub AI Design list: https://agentskillshub.top/best/ai-design/
  - Patterns absorbed: ecosystem survey, top open-source references, MCP/design-system integrations, and category coverage.
- Dominik Kundel / Codex image-first design-to-app idea: https://x.com/dkundel/status/2049591675518165134
  - Pattern absorbed: generate a visual design first with image models, then have Codex implement and iterate with browser feedback.

## Notable Design Skill Projects

These were used as inspiration categories and release attribution, not as copied content.

| Project | Link | Useful idea |
|---|---|---|
| open-design | https://github.com/nexu-io/open-design | Local-first design/prototype workflow |
| Figma-Context-MCP | https://github.com/GLips/Figma-Context-MCP | Figma layout context for coding agents |
| huashu-design | https://github.com/alchaincyf/huashu-design | HTML-native high-fidelity prototypes and animation |
| stitch-skills | https://github.com/google-labs-code/stitch-skills | Agent Skills for Stitch-compatible design workflows |
| open-codesign | https://github.com/OpenCoworkAI/open-codesign | Local-first prompt-to-prototype workflow |
| qiaomu-mondo-poster-design | https://github.com/joeseesun/qiaomu-mondo-poster-design | Poster and cover design prompts |
| logo-generator-skill | https://github.com/op7418/logo-generator-skill | Logo-generation workflow |
| design-dna | https://github.com/zanwei/design-dna | Structured design tokens, style, and visual effects |
| awesome-design-skills | https://github.com/bergside/awesome-design-skills | Curated DESIGN.md and SKILL.md references |
| awesome-claude-design | https://github.com/rohitg00/awesome-claude-design | Aesthetic family prompts and community signals |
| awesome-claude-design | https://github.com/VoltAgent/awesome-claude-design | DESIGN.md inspiration set |
| design-extract | https://github.com/Manavarya09/design-extract | Design-system extraction and multi-platform emitters |
| typeui | https://github.com/bergside/typeui | UI skill tooling and design-system packaging |
| styleseed | https://github.com/bitjaru/styleseed | Rule-based design system and component skins |
| ai-design-components | https://github.com/ancoleman/ai-design-components | UI/UX and backend component design skills |
| figma-console-mcp | https://github.com/southleft/figma-console-mcp | Figma as a design-system API |
| design-systems-mcp | https://github.com/southleft/design-systems-mcp | Token and component guidance through MCP |
| Claude-Code-Design-AI | https://github.com/mikesheehan54/Claude-Code-Design-AI | Screenshot-to-React and UX architecture |
| html-anything | https://github.com/nexu-io/html-anything | Agentic HTML surfaces and export workflow |
| agentation | https://github.com/benjitaylor/agentation | Visual feedback loop for agents |
| vibe | https://github.com/mondaycom/vibe | Mature product design-system resources |
| StoryGen-Atelier | https://github.com/0xsline/StoryGen-Atelier | Storyboard and video-generation workflow |
| hue | https://github.com/dominikmartn/hue | Brand-learning design system skill |
| penpot-mcp | https://github.com/penpot/penpot-mcp | Penpot MCP bridge |
| uSpec | https://github.com/redongreen/uSpec | Component design-system documentation |
| melta-ui | https://github.com/tsubotax/melta-ui | AI-readable design system |
| story-ui | https://github.com/southleft/story-ui | Storybook story generation |
| Mck-ppt-design-skill | https://github.com/likaku/Mck-ppt-design-skill | Consulting-style PowerPoint design system |
| typeui.sh | https://github.com/bergside/typeui.sh | Design-system skill CLI |
| Codex Build Web Apps plugin/workflows | Codex ecosystem, local availability varies | Code-native app construction from visual direction and browser feedback |
| A2F Figma plugin | https://www.figma.com/community/plugin/1645412835513678534/a2f-any-html-website-to-figma-import-websites-to-figma-designs-web-html-css | User-run HTML/website to editable Figma import path |
| BuilderIO figma-html | https://github.com/BuilderIO/figma-html | Website to editable Figma, MIT, moved toward Builder.io extension |
| lgs html-figma | https://github.com/lgs/html-figma | Figma plugin/chrome extension, `htmlToFigma(document.body)` library path, known best-effort limitations |
| sergcen html-to-figma | https://github.com/sergcen/html-to-figma | WIP DOM node to Figma node library with browser and Figma-side functions |
| h2d-capture | https://github.com/cranch42/h2d-capture | Open-source browser extension capturing DOM/computed styles to Figma clipboard format |

## Synthesis Notes

- Prefer process and QA patterns over static style recipes.
- Keep the skill Codex-first: image generation, implementation, and browser verification belong in one loop.
- Treat image references as direction; turn them into code-native layout and separately managed assets.
- Treat design systems as constraints to honor, not decoration to overwrite.
- Decide HTML, Figma, both, or static output based on the user's job-to-be-done.
- Use deterministic scripts for repeatable checks, and human/designer judgment for composition quality.
- Cite sources in public docs, but keep this skill original and compact.
