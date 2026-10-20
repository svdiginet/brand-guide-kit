---
name: brand-guide-kit
description: Create, maintain or audit a brand guide and its asset kit, including logo fidelity, typography, icons, small-size variants, reproducible 3D and production handoffs. Use when a user asks to build or review brand guidelines; not for trademark clearance or unrelated website development.
---

# Brand Guide Kit

Use this checkout as the single source of criteria. Resolve the actual skill directory if installed through a symlink. Repository root is two directories above this file's containing directory.

## Read only what applies

- Always: [brand system standard](../../docs/brand-system-standard.md).
- Create/update: [guide template](../../templates/brand-guide.md).
- Audit: [audit template](../../templates/audit.md).
- 3D work: [3D specification](../../templates/3d-spec.md).
- Brand contracts and asset integrity: [local auditor](../../docs/brand-contract.md). Use one private `brand.json` per target brand. Run audit read-only first; UNKNOWN is not approval. Export copies approved pinned SVG bytes only, never redraws variants.
- Research refresh: [official references](../../docs/references.md).

## Workflow

1. Inspect the user's approved reference, existing guide and assets. Separate an approved visual direction from an approved production master. Ask for critical missing references; never invent brand facts.
2. Audit before editing an existing kit. Label findings VERIFIED, MISSING or UNKNOWN and cite exact files or measurements. Prioritize inconsistent geometry, missing fonts, tiny-size failures, misleading 3D angles and unusable exports.
3. Preserve originals. Propose bounded changes under the user's approval rules. Do not silently alter a logo to make it easier to trace. Use one approved master for derivatives, or identify an optical variant explicitly.
4. Follow the user's brand colors and typography. Official external references inform criteria, never supply copied artwork or permission to redistribute assets.
5. For 3D, derive views from one model and record actual parameters. A generated raster is a concept reference, not measured camera evidence. Keep flat and dimensional variants distinct.
6. Verify relevant rendered outputs: exact type and geometry, small-size examples, all exported pages, image loading and supplier proof status. File existence is not visual approval. Report limitations and no broader certification.
7. Update the target project's guide, asset index and changelog when authorized. Keep client files and evidence in that target project, outside this public toolkit. Never publish, send or change a live brand without authorization.

## Maintaining this kit

Update the existing standard rather than copying it into each entry point. Check official sources when adding or changing source-derived claims. Record review dates, changed criteria and evidence. Run `python3 scripts/check.py` from the repository root after editing. That command checks documentation integrity only; it cannot validate external artwork, public-source freshness or private data absence.

The workflow is the same in Codex and Claude Code. No platform-specific hook, browser or paid provider is required. Use tools actually available in the calling session, and state what could not be inspected.
