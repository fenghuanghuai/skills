---
name: opencode-service
description: "OpenCode CLI integration guide. Use when: (1) Building CI/CD pipelines with AI code review, (2) Creating Makefile targets for code analysis, (3) Setting up automated code quality checks, (4) Learning OpenCode CLI usage patterns."
---

# OpenCode CLI Integration Guide

OpenCode is an AI coding agent that can be integrated into your development workflows via CLI.

## Quick Start

```bash
# Install
curl -fsSL https://opencode.ai/install | bash

# Basic usage
opencode run "Review this code"
opencode run --file src/main.py "Find bugs"
opencode run --format json "List functions"
```

## Common Integration Patterns

### Makefile
```makefile
review:
	opencode run "Review code in src/"

security:
	opencode run "Check for vulnerabilities"

analyze:
	opencode run --file src/ "Analyze architecture"
```

### Shell Script
```bash
opencode run "Check code quality"
opencode run --file "$FILE" "Review this"
opencode run --format json "Analyze" | jq '.response'
```

### CI/CD (GitHub Actions)
```yaml
- name: AI Code Review
  run: opencode run "Review changes in this PR"
```

### Cron Job
```cron
0 9 * * * opencode run "Daily code quality check"
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `opencode run "msg"` | Simple query |
| `opencode run --file <path> "msg"` | Query with file |
| `opencode run --format json "msg"` | JSON output |
| `opencode run --session <id> "msg"` | Continue session |
| `opencode serve` | Start persistent server |
| `opencode run --attach <url> "msg"` | Connect to server |

## Advanced Usage

**Server mode for batch processing:**
```bash
opencode serve --port 4096 &
opencode run --attach http://localhost:4096 "Query 1"
opencode run --attach http://localhost:4096 "Query 2"
```

**Model selection:**
```bash
opencode run --model anthropic/claude-3-5-sonnet-20241022 "Your question"
```

**Continue conversation:**
```bash
SESSION_ID=$(opencode run --format json "Review error handling" | jq -r '.session_id')
opencode run --session $SESSION_ID "Now check logging"
```

## References

For detailed documentation, see:

- [CLI Reference](references/cli-reference.md) - Complete command reference
- [Integration Patterns](references/integration-patterns.md) - Advanced integration examples
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions

## Resources

- [OpenCode Docs](https://opencode.ai/docs)
- [CLI Reference](https://opencode.ai/docs/cli)
- [GitHub](https://github.com/opencode-ai/opencode)
