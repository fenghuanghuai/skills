# OpenCode CLI Reference

Complete reference for all OpenCode CLI commands and options.

## Table of Contents

- [Basic Commands](#basic-commands)
- [Run Command](#run-command)
- [Server Commands](#server-commands)
- [Session Management](#session-management)
- [Authentication](#authentication)
- [Model Management](#model-management)
- [Configuration](#configuration)

## Basic Commands

| Command | Description |
|---------|-------------|
| `opencode` | Start OpenCode TUI |
| `opencode run "message"` | Run non-interactive query |
| `opencode serve` | Start headless server |
| `opencode web` | Start server with web UI |
| `opencode attach <url>` | Attach TUI to running server |
| `opencode auth login` | Configure API keys |
| `opencode models` | List available models |

## Run Command

The `run` command executes OpenCode in non-interactive mode.

### Syntax

```bash
opencode run [options] "message"
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--format <type>` | - | Output format: `default` or `json` |
| `--session <id>` | `-s` | Continue existing session |
| `--file <path>` | `-f` | Attach file to message (can be used multiple times) |
| `--model <model>` | `-m` | Model in format `provider/model` |
| `--agent <name>` | - | Use specific agent |
| `--title <title>` | - | Title for the session |
| `--attach <url>` | - | Attach to running server |
| `--port <port>` | - | Port for local server |
| `--share` | - | Share the session |
| `--variant <level>` | - | Model variant (high, max, minimal) |

### Examples

```bash
# Simple query
opencode run "Explain async/await in JavaScript"

# With file
opencode run --file src/main.py "Review this file"

# Multiple files
opencode run --file src/main.py --file src/utils.py "Review both files"

# JSON output for parsing
opencode run --format json "List all functions"

# Continue session
SESSION_ID=$(opencode run --format json "Initial query" | jq -r '.session_id')
opencode run --session $SESSION_ID "Follow-up question"

# Specific model
opencode run --model anthropic/claude-3-5-sonnet-20241022 "Your question"

# Attach to server
opencode run --attach http://localhost:4096 "Your question"
```

## Server Commands

### serve

Start a headless OpenCode server for API access.

```bash
opencode serve [options]
```

| Option | Description |
|--------|-------------|
| `--port <port>` | Port to listen on (default: random) |
| `--hostname <host>` | Hostname (default: 127.0.0.1) |
| `--mdns` | Enable mDNS discovery |
| `--cors <origin>` | Additional CORS origins |

### web

Start server with web interface.

```bash
opencode web [options]
```

Same options as `serve`.

### attach

Attach TUI to a running server.

```bash
opencode attach <url> [options]
```

| Option | Description |
|--------|-------------|
| `--dir <path>` | Working directory |
| `--session <id>` | Session to continue |

## Session Management

### List Sessions

```bash
opencode session list
opencode session list --max-count 10
opencode session list --format json
```

### Export Session

```bash
opencode export [session-id]
```

### Import Session

```bash
opencode import <file-or-url>
opencode import session.json
opencode import https://opncd.ai/s/abc123
```

## Authentication

### Login

```bash
opencode auth login
```

Prompts to select a provider and enter API key.

### List Providers

```bash
opencode auth list
```

### Logout

```bash
opencode auth logout <provider>
```

## Model Management

### List All Models

```bash
opencode models
opencode models anthropic
opencode models --refresh
```

### Model Format

Models are specified as `provider/model`:

- `anthropic/claude-3-5-sonnet-20241022`
- `openai/gpt-4`
- `google/gemini-2.0-flash-exp`

## Configuration

### Config File

OpenCode reads configuration from `~/.opencode/config.json`.

Example config:

```json
{
  "model": "anthropic/claude-3-5-sonnet-20241022",
  "agents": {
    "code-review": {
      "systemPrompt": "You are a code reviewer..."
    }
  }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENCODE_CONFIG` | Path to config file | `~/.opencode/config.json` |
| `OPENCODE_DISABLE_AUTOUPDATE` | Disable update checks | `false` |
| `OPENCODE_SERVER_PASSWORD` | Server basic auth password | - |
| `OPENCODE_SERVER_USERNAME` | Server basic auth username | `opencode` |

## Global Options

These options work with all commands:

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help |
| `--version` | `-v` | Print version |
| `--print-logs` | - | Print logs to stderr |
| `--log-level <level>` | - | DEBUG, INFO, WARN, ERROR |

## Output Formats

### Default Output

Human-readable formatted output.

```bash
$ opencode run "2+2"
4
```

### JSON Output

Machine-readable JSON for parsing.

```bash
$ opencode run --format json "2+2"
{"type":"data","data":"4","status":"completed"}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error |
| 124 | Timeout (when using system `timeout` command) |
| 130 | Interrupted (Ctrl+C) |
