#!/usr/bin/env python3
"""Check that Agent Design keeps its core process constraints documented."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SNIPPETS = {
    "SKILL.md": [
        "image-first is the default gate",
        "Do not start coding a new landing page",
        "Do not deliver a single flat HTML file",
        "Default to Vite + React + Tailwind CSS",
        "Use Next.js when",
        "framework/project structure used",
        "Define \"slicing\" as structured asset extraction",
        "Every new runnable design demo must leave behind reusable design assets",
        "design/tokens.json",
        "pipeline ledger",
        "Produce a design-spec artifact",
        "editable Figma",
        "ui_assets_complete: true",
        "multi-round generation",
        "pipeline_validate.py",
        "Stop after presenting the three concepts",
        "Do not continue to design spec",
        "WAITING_FOR_USER_DIRECTION_CONFIRMATION",
        "A recommendation is not authorization",
        "do not auto-select",
        "POST_CONFIRMATION_ASSET_LOOP",
        "Do not jump directly from direction confirmation",
        "design/figma-export.json",
        "dom-to-figma",
        "Do not claim an official `.fig` file",
        "Figma import instructions",
        "artifact-aware concept board",
        "website sections",
        "deck slides",
        "logo/brand boards",
        "Semantic media assets are required by default",
        "preview/stage/project card/thumbnail/mockup/cover",
        "all_code_native_approved",
        "code_native_approved",
    ],
    "references/design-process.md": [
        "For new visual design, this is a gate",
        "Generate references before implementation",
        "Default to Vite + React + Tailwind CSS",
        "Do not deliver a single flat HTML file",
        "Avoid a monolithic one-file implementation",
        "\"Slicing\" means structured asset extraction",
        "Minimum for new runnable demos",
        "component inventory",
        "style-exploration.md",
        "figma-export.md",
        "design-system-schema.md",
        "ui-asset-generation-loop.md",
    ],
    "references/engineering-delivery.md": [
        "A runnable web demo is a small project",
        "Vite + React + Tailwind CSS",
        "Next.js + Tailwind CSS",
        "Image-First Implementation Order",
        "Generated references and final assets are separated",
        "Design Asset Preservation",
        "design/tokens.json",
        "public/assets/asset-manifest.json",
    ],
    "references/asset-pipeline.md": [
        "structured asset extraction",
        "does not mean cutting a full comp into many image tiles",
        "Asset Decision Rules",
        "Manifest Format",
        "If no assets are needed",
        "sprite sheet",
        "PNG files with alpha",
        "ui_assets_complete",
        "Semantic Media Default Rule",
        "Semantic media assets are required by default",
        "preview/stage/project card/thumbnail/mockup/cover",
        "code_native_reason",
        "code_native_approved",
        "all_code_native_approved",
        "preview stage artwork",
        "project card media",
        "\"tool\": \"image generation\"",
        "\"element_id\": \"hero-product-preview\"",
    ],
    "references/production-pipeline.md": [
        "Phase Gates",
        "Style exploration",
        "Design spec",
        "Trace Ledger",
        "No-Skip Rules",
        "Do not downgrade silently",
        "Do not continue past style exploration",
        "recommended direction is not selected direction",
        "WAITING_FOR_USER_DIRECTION_CONFIRMATION",
        "POST_CONFIRMATION_ASSET_LOOP",
        "HTML/DOM-to-Figma conversion",
    ],
    "references/execution-protocol.md": [
        "No Silent Downgrade",
        "Tool Attempt Log",
        "Hard Stops",
        "Completion Proof",
        "three concept directions have been produced but the user has not confirmed one",
        "WAITING_FOR_USER_DIRECTION_CONFIRMATION",
        "Do not use the agent's recommendation as confirmation",
        "POST_CONFIRMATION_ASSET_LOOP",
        "no `figma-export.json` path decision exists",
    ],
    "references/ui-asset-generation-loop.md": [
        "style reference -> element inventory -> code/token/asset decision",
        "Repeat until the manifest says `ui_assets_complete: true`",
        "Multi-Round Generation",
        "Sprite Sheet Rule",
        "PNG with alpha",
        "For semantic media items",
        "code_native_reason",
        "Completeness Gate",
        "semantic media candidates",
        "all_code_native_approved",
        "code_native_approved",
        "\"element_id\": \"hero-preview-frame\"",
        "Invocation Trigger",
        "go with Direction B",
        "POST_CONFIRMATION_ASSET_LOOP",
    ],
    "references/style-exploration.md": [
        "Required Directions",
        "Conservative / usable",
        "Expressive / premium",
        "Experimental / brand-led",
        "Direction Template",
        "user-confirmation gate",
        "Please choose Direction A, B, or C",
        "The gate passes only with",
        "Gate status: WAITING_FOR_USER_DIRECTION_CONFIRMATION",
        "do not decide the winner",
        "The phrase \"Recommended: Direction B\" does not pass the gate",
        "Artifact-Aware Concept Board",
        "Universal Prompt Structure",
        "Mobile App Prompt Template",
        "Website Prompt Template",
        "Deck Prompt Template",
        "Poster Prompt Template",
        "Logo / Brand Prompt Template",
        "创建一张 5.5x3",
        "1 个不含摄影图片的移动端欢迎页",
        "桌面端首屏",
        "封面页",
        "主 logo",
    ],
    "references/design-spec.md": [
        "Frame: Home / Hero",
        "Component States",
        "Design Spec Gate",
    ],
    "references/figma-export.md": [
        "Editable Figma",
        "Direct Figma construction",
        "HTML/DOM to Figma capture",
        "Editability QA",
        "BuilderIO `figma-html`",
        "cranch42/h2d-capture",
        "figma-export.json",
        "dom-to-figma",
        "plugin-ready JSON",
        "Do not claim this path creates an official `.fig` file",
        "\"path\": \"direct-figma | dom-to-figma | handoff-only\"",
        "Codex cannot run a Figma development plugin",
        "User-Run Import Instructions",
        "Plugins -> Development -> Import plugin from manifest",
        "editable Figma was not directly created by Codex",
    ],
    "references/design-system-schema.md": [
        "design/tokens.json",
        "token_mapping",
        "Component Inventory",
        "Component Extraction Rules",
    ],
    "references/visual-alignment.md": [
        "Screenshot Set",
        "Compare Against Reference",
        "Tolerances",
        "qa-report.md",
    ],
    "scripts/pipeline_validate.py": [
        "ui_assets_complete",
        "semantic_media_policy",
        "code_native_reason",
        "code_native_approved",
        "all_code_native_approved",
        "require_semantic_asset",
        "allow_empty_assets",
        "semantic media candidate",
        "READY_ASSET_STATUSES",
        "matching tool_attempt element_id",
        "Missing required design artifact",
        "Runnable demo must include package.json",
        "Figma requested",
        "validate_figma_export",
        "FIGMA_PATHS",
        "dom-to-figma path requires dom_to_figma object",
        "project_path_exists",
        "dom_to_figma import_instructions file does not exist",
    ],
}


def main() -> int:
    failures: list[str] = []
    for relative_path, snippets in REQUIRED_SNIPPETS.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"Missing file: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                failures.append(f"{relative_path} missing: {snippet}")

    if failures:
        print("Agent Design contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Agent Design contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
