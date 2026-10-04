# Package validation

Version: 1.0.0  
Validation date: 4 October 2026

## Checks actually executed

The package's Python static checker was executed successfully. It uses only local files and the Python standard library.

```text
PASS: Standalone guides exist and match their SHA-256 manifest.
PASS: All 10 substantive modules are identical across the two platform packs.
PASS: Both project packs contain all 14 individually loadable recipes.
PASS: Each guide includes 16 source articles, 16 behavioral scenarios, 7 templates, and 7 prompts.
PASS: The standalone editions share exactly the same substantive handbook; integration prefaces differ.
PASS: Markdown fences, explicit anchors, and local Markdown links are structurally valid.
PASS: Cursor loader metadata and portable/optional instruction targets are valid.
PASS: Both native loaders explicitly route to every substantive module.
STATIC VALIDATION PASSED. This does not test live host loading or model behavior.
```

The complete bundle includes the checker. From its extracted root, run:

```bash
python tools/validate_pack.py
```

## What these checks establish

The two standalone guides exist, match the recorded checksums, and contain the intended source mapping, templates, prompts, and behavioral scenarios. The shared substantive modules are identical in the Cursor and portable packages. The Markdown links and explicit anchors resolve locally. The Cursor entry point has the intended metadata, and the portable configuration points to an existing loader.

## What has not been tested

No live Cursor, Cline, or OpenCode session was launched. The behavioral scenarios B01–B16 are supplied for use in the actual environment; their model outcomes have not been measured here. No source algorithm, provider integration, project-memory service, or upstream agent was executed. No privacy, retention, authorization, or deployment configuration of the user's environment was inspected.

File correctness is not a guarantee of instruction-following or privacy compliance. Test the loader in a fresh, credential-free workspace before using it on a consequential project.
