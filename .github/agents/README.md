# Workspace custom agents

These files define workspace-level custom agents for VS Code Copilot Chat.

## Location and format

- Folder: `.github/agents/`
- File extension: `.agent.md`
- Optional YAML frontmatter controls name, description, tools, and visibility.

## Included agents

- `planner.agent.md`
- `implementer.agent.md`
- `security-review.agent.md`
- `orchestrator.agent.md` (hidden; handoff coordinator)

## If agents do not appear

1. Update VS Code to 1.106+ and update GitHub Copilot Chat.
2. Ensure workspace trust is enabled.
3. Run `Developer: Reload Window`.
4. Open Chat, choose `Configure Custom Agents`, and verify these files are detected.
5. Open Chat diagnostics (right-click in Chat -> Diagnostics) to inspect load errors.
