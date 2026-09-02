# Development Logs

This directory contains the engineering development journal for Project Aphelion.

## Structure

```
dev-logs/
├── 2025/
│   ├── 2025-10 - The Beginning.md
│   ├── 2025-10 - Session 2.md
│   ├── 2025-11 - Session 3.md
│   └── ...
├── 2026/
│   ├── 2026-02 - Session 8.md
│   └── ...
└── README.md
```

## Naming Convention

```
YYYY-MM - <Title>.md
```

Examples:
- `2025-10 - The Beginning.md`
- `2026-09 - Project Aphelion.md`

## Historical Migration

The original session logs (Sessions 2–12, "The Beginning") were created during the Rocket Telemetry System phase (Oct 2025 – Jun 2026). They have been preserved as-is from the original repository archive. Content is not rewritten.

## Obsidian Workflow

Development logs can be created through Obsidian using the Templater plugin:

1. Create a new note in the Project Aphelion dev-logs folder
2. Templater automatically applies the monthly dev-log template
3. The file is renamed with the correct date and moved to the appropriate year directory

The canonical location for development logs is this directory in the repository. Obsidian accesses them through a symlink configured in the vault.
