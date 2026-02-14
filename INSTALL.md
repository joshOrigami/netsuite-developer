# Installation Guide

## Requirements
- Python 3.9+
- VSCode
- OpenAI Codex Extension

Verify Python:
    python --version

## Install Skill
Place SKILL.md into:
    <project-root>/.codex/skills/netsuite-developer/

## Install Python Helper
Place:
    <project-root>/tools/query_metadata.py
inside your project root.

## Metadata Structure
.netsuite-metadata/<ENV>/
    manifest.json
    record_index.json
    records/

## Test
python tools/query_metadata.py --env QA list-records
