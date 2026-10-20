# Architecture

Documentation-first. README routes to docs/, templates/ and skills/brand-guide-kit/. The skill references the same documents. scripts/check.py validates local Markdown links and required entrypoints using Python standard library; it performs no network calls. Git is the version store. There is no application server, database or environment configuration.

V0.2 adds scripts/brand.py: JSON brand contract, scoped asset audit and preflighted byte-copy export. Python standard library only, no network. See docs/brand-contract.md for exact limits and exit codes.
