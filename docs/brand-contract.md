# Brand contract and local audit

`brand.json` is our small standard-library-readable contract. Use one per brand next to its assets. It is not a compatibility implementation of another toolkit. Start with [the fictional fixture](../demos/sample-brand/brand.json).

Required: schema_version (1), name, colors (named six-digit hex values). Optional arrays: assets and css_files. Paths resolve relative to the manifest and cannot leave its folder, including through symlinks. Do not place a private manifest in this public repo.

Each asset declares path and approval (`draft` or `approved`). Optional sha256 pins exact bytes; expected_fills compares explicit SVG fill attributes only; allowed_fonts lists complete accepted font-family attribute strings. Approval is the operator's assertion, not independently proven by this script. Hashes prove byte integrity, not visual quality or geometric equivalence. Changing harmless formatting also changes a hash.

```sh
python3 scripts/brand.py audit demos/sample-brand/brand.json
python3 scripts/brand.py audit /path/to/private-brand/brand.json --json
python3 scripts/brand.py export demos/sample-brand/brand.json /new/output/folder
```

Audit is read-only and uses no network. It checks declared files only, SHA256 baselines, XML parsing, explicit SVG fill/font attributes, live text and lexical CSS hex literals. It is not an inventory of every file in a project, a computed-style checker, accessibility audit, image comparison or 3D renderer. Non-hex CSS constructs receive UNKNOWN where detected; the heuristic is not a full CSS parser. Six-digit palette declarations compare literally: shorthand/alpha equivalents need normalization before use or are reported outside the palette.

Exit codes: 0 no missing/unknown findings, 1 missing or mismatched evidence, 2 unknown-only findings, 3 invalid input or I/O. A mandatory visual UNKNOWN means this version cannot certify a production release. Example audit intentionally returns 2; automation must explicitly expect that code rather than suppress errors.

Export preflights every selected SVG, requires operator-declared approval and matching SHA256, rejects duplicate basenames and existing output directories, then copies original bytes. It does not draw, recolor, outline, optimize or render variants. Maintain each approved layout as its own master entry; the exporter protects those bytes. No PNG/PDF/3D generation is promised by this command.

Checks: `python3 -m unittest discover -s tests -v`. Cases cover byte drift, CSS drift, non-hex unknowns, live text, malformed contracts, path traversal, byte-preserving exports and overwrite protection. Review generated reports privately; they can expose local brand filenames.
