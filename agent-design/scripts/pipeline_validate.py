#!/usr/bin/env python3
"""Validate that a generated design project followed the Agent Design pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def exists_any(root: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            return path
    return None


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


SEMANTIC_MEDIA_HINTS = [
    "preview",
    "stage",
    "thumbnail",
    "thumb",
    "mockup",
    "cover",
    "poster",
    "project card",
    "gallery",
    "avatar",
    "headshot",
    "sticker",
    "portfolio",
    "product media",
    "product preview",
    "hero media",
    "brand mark",
    "illustration",
    "texture",
    "visual media",
    "inspectable",
    "orb",
    "bloom",
    "kinetic",
]

ASSET_DECISIONS = {"generate", "crop", "export", "reuse", "sprite"}
ALL_DECISIONS = ASSET_DECISIONS | {"code", "token", "component", "omit"}
BAD_CODE_REASONS = {"faster", "looks close enough", "easy", "simpler", "quick", "placeholder"}
READY_ASSET_STATUSES = {"ready", "production", "approved", "reused"}


def looks_like_semantic_media(item: dict[str, Any]) -> bool:
    text = " ".join(
        str(item.get(key, "")).lower()
        for key in ["id", "role", "description", "usage", "item"]
    )
    return any(hint in text for hint in SEMANTIC_MEDIA_HINTS)


def strong_code_reason(item: dict[str, Any]) -> bool:
    reason = str(item.get("code_native_reason", "")).strip().lower()
    if len(reason) < 24:
        return False
    return reason not in BAD_CODE_REASONS


def asset_path_exists(root: Path, manifest_path: Path, asset_file: str) -> bool:
    asset_path = Path(asset_file)
    candidates = [asset_path] if asset_path.is_absolute() else [root / asset_file, manifest_path.parent / asset_file]
    return any(candidate.exists() for candidate in candidates)


def project_path_exists(root: Path, path_value: Any) -> bool:
    if not path_value:
        return False
    candidate = Path(str(path_value))
    if candidate.is_absolute():
        return candidate.exists()
    return (root / candidate).exists()


def validate_manifest(
    path: Path,
    root: Path,
    failures: list[str],
    require_semantic_asset: bool,
    allow_empty_assets: bool,
) -> None:
    try:
        manifest = load_json(path)
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid JSON manifest {path}: {exc}", failures)
        return

    if manifest.get("ui_assets_complete") is not True:
        fail(f"{path} must set ui_assets_complete: true for final delivery.", failures)

    if "element_inventory" not in manifest:
        fail(f"{path} missing element_inventory.", failures)

    if "assets" not in manifest:
        fail(f"{path} missing assets array.", failures)

    if "omitted" not in manifest:
        fail(f"{path} missing omitted array.", failures)

    if "tool_attempts" not in manifest:
        fail(f"{path} missing tool_attempts array.", failures)

    if "semantic_media_policy" not in manifest:
        fail(f"{path} missing semantic_media_policy.", failures)

    inventory = manifest.get("element_inventory", [])
    if not isinstance(inventory, list) or not inventory:
        fail(f"{path} element_inventory must be a non-empty array.", failures)
        inventory = []

    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        fail(f"{path} assets must be an array.", failures)
        assets = []

    tool_attempts = manifest.get("tool_attempts", [])
    if not isinstance(tool_attempts, list):
        fail(f"{path} tool_attempts must be an array.", failures)
        tool_attempts = []

    inventory_ids: set[str] = set()
    for item in inventory:
        if not isinstance(item, dict):
            fail(f"{path} has non-object element_inventory entry.", failures)
            continue
        item_id = str(item.get("id", "")).strip()
        decision = str(item.get("decision", "")).strip()
        if not item_id:
            fail(f"{path} inventory entry missing id: {item}", failures)
        else:
            inventory_ids.add(item_id)
        if not item.get("description"):
            fail(f"{path} inventory entry missing description: {item}", failures)
        if decision not in ALL_DECISIONS:
            fail(f"{path} inventory entry has invalid or missing decision: {item}", failures)
        if decision == "code" and (not strong_code_reason(item) or item.get("code_native_approved") is not True):
            fail(f"{path} code-native entry needs strong code_native_reason and code_native_approved: true: {item}", failures)
        if decision == "omit" and not item.get("reason"):
            fail(f"{path} omitted inventory entry missing reason: {item}", failures)

    semantic_items = [item for item in inventory if isinstance(item, dict) and looks_like_semantic_media(item)]
    semantic_asset_items = [item for item in semantic_items if item.get("decision") in ASSET_DECISIONS]
    semantic_code_items = [item for item in semantic_items if item.get("decision") == "code"]
    semantic_bad_decision_items = [
        item
        for item in semantic_items
        if item.get("decision") not in ASSET_DECISIONS and item.get("decision") != "code"
    ]

    for item in semantic_code_items:
        if not strong_code_reason(item) or item.get("code_native_approved") is not True:
            fail(f"{path} semantic media marked code without approved code_native_reason: {item}", failures)

    for item in semantic_bad_decision_items:
        fail(
            f"{path} semantic media candidate must be asset-backed or approved code-native: {item}",
            failures,
        )

    if not allow_empty_assets and not assets and manifest.get("all_code_native_approved") is not True:
        fail(f"{path} assets array is empty without all_code_native_approved: true.", failures)

    if require_semantic_asset and semantic_items and not semantic_asset_items:
        if manifest.get("all_code_native_approved") is not True:
            fail(
                f"{path} has semantic media candidates but no generated/cropped/exported/reused asset decision or all_code_native_approved: true.",
                failures,
            )

    if require_semantic_asset and semantic_asset_items and not assets:
        fail(f"{path} has semantic asset decisions but assets array is empty.", failures)

    if require_semantic_asset and semantic_asset_items and not tool_attempts:
        fail(f"{path} semantic assets require tool_attempts documenting generation/crop/export/reuse.", failures)

    attempt_element_ids: set[str] = set()
    for attempt in tool_attempts:
        if not isinstance(attempt, dict):
            fail(f"{path} has non-object tool_attempts entry.", failures)
            continue
        for key in ["element_id", "action", "status"]:
            if not attempt.get(key):
                fail(f"{path} tool_attempt entry missing {key}: {attempt}", failures)
        element_id = str(attempt.get("element_id", "")).strip()
        if element_id:
            attempt_element_ids.add(element_id)

    asset_element_ids: set[str] = set()
    for asset in assets:
        if not isinstance(asset, dict):
            fail(f"{path} has non-object asset entry.", failures)
            continue
        for key in ["element_id", "file", "role", "source", "usage", "status"]:
            if not asset.get(key):
                fail(f"{path} asset entry missing {key}: {asset}", failures)
        element_id = str(asset.get("element_id", "")).strip()
        if element_id:
            asset_element_ids.add(element_id)
            if inventory_ids and element_id not in inventory_ids:
                fail(f"{path} asset element_id not found in element_inventory: {asset}", failures)
        asset_file = asset.get("file")
        if asset_file and not asset_path_exists(root, path, str(asset_file)):
            # Accept paths relative to project root or manifest dir.
            fail(f"{path} references missing asset file: {asset_file}", failures)
        status = str(asset.get("status", "")).strip().lower()
        if status and status not in READY_ASSET_STATUSES:
            fail(f"{path} asset status must be ready/production/approved/reused: {asset}", failures)

    for item in inventory:
        if isinstance(item, dict) and item.get("decision") in ASSET_DECISIONS:
            item_id = str(item.get("id", "")).strip()
            if item_id and item_id not in asset_element_ids:
                fail(f"{path} asset-backed inventory item has no matching asset element_id: {item}", failures)
            if item_id and require_semantic_asset and item in semantic_asset_items and item_id not in attempt_element_ids:
                fail(f"{path} semantic asset item has no matching tool_attempt element_id: {item}", failures)


FIGMA_PATHS = {"direct-figma", "dom-to-figma", "handoff-only"}


def validate_figma_export(path: Path, root: Path, failures: list[str]) -> None:
    try:
        figma_export = load_json(path)
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid JSON Figma export {path}: {exc}", failures)
        return

    if figma_export.get("figma_requested") is not True:
        fail(f"{path} must set figma_requested: true when --require-figma is used.", failures)

    export_path = figma_export.get("path")
    if export_path not in FIGMA_PATHS:
        fail(f"{path} path must be direct-figma, dom-to-figma, or handoff-only.", failures)

    if "editable_output_created" not in figma_export:
        fail(f"{path} missing editable_output_created.", failures)

    attempts = figma_export.get("tool_attempts", [])
    if not isinstance(attempts, list) or not attempts:
        fail(f"{path} must include tool_attempts for Figma path discovery.", failures)

    if export_path == "direct-figma" and not figma_export.get("created_file_or_link"):
        fail(f"{path} direct-figma path requires created_file_or_link.", failures)

    if export_path == "dom-to-figma":
        dom_to_figma = figma_export.get("dom_to_figma")
        if not isinstance(dom_to_figma, dict):
            fail(f"{path} dom-to-figma path requires dom_to_figma object.", failures)
        else:
            for key in ["local_url", "tool", "payload", "import_instructions"]:
                if not dom_to_figma.get(key):
                    fail(f"{path} dom_to_figma missing {key}.", failures)
            if dom_to_figma.get("payload") and not project_path_exists(root, dom_to_figma.get("payload")):
                fail(f"{path} dom_to_figma payload file does not exist: {dom_to_figma.get('payload')}", failures)
            if dom_to_figma.get("import_instructions") and not project_path_exists(root, dom_to_figma.get("import_instructions")):
                fail(
                    f"{path} dom_to_figma import_instructions file does not exist: {dom_to_figma.get('import_instructions')}",
                    failures,
                )

    if export_path == "handoff-only" and figma_export.get("editable_output_created") is True:
        fail(f"{path} handoff-only cannot set editable_output_created: true.", failures)


def validate_project(
    root: Path,
    mode: str,
    require_figma: bool,
    allow_single_html: bool,
    require_semantic_asset: bool,
    allow_empty_assets: bool,
) -> list[str]:
    failures: list[str] = []

    if not root.exists():
        return [f"Project path does not exist: {root}"]

    if mode == "new-runnable":
        if not allow_single_html and not (root / "package.json").exists():
            fail("Runnable demo must include package.json. Single flat HTML is not accepted by default.", failures)

        if not exists_any(root, ["src", "app"]):
            fail("Runnable demo must include src/ or app/.", failures)

        if not exists_any(root, ["src/components", "components"]):
            fail("Runnable demo must include reusable components/.", failures)

        if not exists_any(root, ["src/sections", "sections"]):
            fail("Runnable demo must include sections/.", failures)

    required_design_files = [
        "design/DESIGN.md",
        "design/style-directions.md",
        "design/frame-spec.md",
        "design/traceability.json",
    ]
    for relative_path in required_design_files:
        if not (root / relative_path).exists():
            fail(f"Missing required design artifact: {relative_path}", failures)

    if not exists_any(root, ["design/tokens.json", "src/data/design-tokens.ts", "src/styles/tokens.css"]):
        fail("Missing design tokens: design/tokens.json or project-native token file.", failures)

    if not exists_any(root, ["design/component-inventory.json", "design/DESIGN.md"]):
        fail("Missing component inventory artifact.", failures)

    manifest = exists_any(root, ["public/assets/asset-manifest.json", "design/asset-manifest.json", "assets/asset-manifest.json"])
    if not manifest:
        fail("Missing asset manifest.", failures)
    else:
        validate_manifest(manifest, root, failures, require_semantic_asset, allow_empty_assets)

    if require_figma:
        figma_export = exists_any(root, ["design/figma-export.json"])
        figma_handoff = exists_any(root, ["design/figma-handoff.md"])
        if not figma_export:
            fail("Figma requested: missing figma-export.json path decision.", failures)
        else:
            validate_figma_export(figma_export, root, failures)
        if not figma_handoff and figma_export:
            try:
                export_data = load_json(figma_export)
            except Exception:  # noqa: BLE001
                export_data = {}
            if export_data.get("path") == "handoff-only":
                fail("Figma handoff-only path requires design/figma-handoff.md.", failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Design generated project artifacts.")
    parser.add_argument("project", help="Generated project directory.")
    parser.add_argument("--mode", choices=["new-runnable", "handoff"], default="new-runnable")
    parser.add_argument("--require-figma", action="store_true", help="Require Figma export/handoff artifact.")
    parser.add_argument("--allow-single-html", action="store_true", help="Allow a no-build single HTML exception.")
    parser.add_argument(
        "--allow-no-semantic-assets",
        action="store_true",
        help="Do not require semantic media assets when inventory contains semantic media.",
    )
    parser.add_argument(
        "--allow-empty-assets",
        action="store_true",
        help="Allow an empty assets array without all_code_native_approved: true.",
    )
    args = parser.parse_args()

    root = Path(args.project).resolve()
    failures = validate_project(
        root,
        args.mode,
        args.require_figma,
        args.allow_single_html,
        not args.allow_no_semantic_assets,
        args.allow_empty_assets,
    )

    if failures:
        print("Agent Design pipeline validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Agent Design pipeline validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
