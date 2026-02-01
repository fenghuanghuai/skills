# OpenCode Integration Patterns

Advanced integration patterns and examples for using OpenCode in various scenarios.

## Table of Contents

- [CI/CD Integration](#cicd-integration)
- [Makefile Patterns](#makefile-patterns)
- [Shell Script Patterns](#shell-script-patterns)
- [Docker Integration](#docker-integration)
- [Server Mode Patterns](#server-mode-patterns)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)

## CI/CD Integration

### GitHub Actions

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install OpenCode
        run: curl -fsSL https://opencode.ai/install | bash

      - name: Review Changed Files
        run: |
          opencode run "Review the changes in this PR. Focus on: bugs, security, performance."

      - name: Security Scan
        run: |
          opencode run --file src/ "Check for security vulnerabilities"

      - name: Generate Summary
        if: always()
        run: |
          opencode run --format json "Summarize the review" > review.json
          cat review.json
```

### GitLab CI

```yaml
stages:
  - review

ai_review:
  stage: review
  before_script:
    - curl -fsSL https://opencode.ai/install | bash
  script:
    - opencode run "Review merge request changes"
    - opencode run --file src/ "Check for security issues"
  artifacts:
    paths:
      - review-output.json
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('AI Review') {
            steps {
                sh 'opencode run "Review changes in this build"'
                sh 'opencode run --file src/ "Security scan"'
            }
        }
    }
}
```

## Makefile Patterns

### Code Review Targets

```makefile
.PHONY: review security test docs help

# Full code review
review:
	opencode run "Review all code in src/"

# Security review
security:
	opencode run "Check for security vulnerabilities in src/"

# Test review
test:
	opencode run --file tests/ "Review test coverage and quality"

# Documentation review
docs:
	opencode run --file README.md --file docs/ "Review documentation"

# Help with specific file
help-file:
	opencode run --file $(FILE) "Explain how this file works"

# Batch review with server
review-batch:
	opencode serve --port 4096 & \
	opencode run --attach http://localhost:4096 "Review src/auth/" && \
	opencode run --attach http://localhost:4096 "Review src/api/" && \
	killall opencode
```

### Analysis Targets

```makefile
.PHONY: analyze deps complexity

# Dependency analysis
analyze:
	opencode run "Analyze the dependency structure of this project"

# Complexity analysis
complexity:
	opencode run --file src/ "Identify the most complex functions"

# Architecture review
arch:
	opencode run "Review the overall architecture and suggest improvements"
```

## Shell Script Patterns

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Get staged files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -n "$FILES" ]; then
    echo "Running AI review on staged files..."
    for FILE in $FILES; do
        echo "Reviewing $FILE..."
        opencode run --file "$FILE" "Check for bugs and style issues"
    done
fi
```

### Pre-push Hook

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Running final review..."
opencode run "Review all changes being pushed"
opencode run "Check for any security issues"
```

### Deployment Script

```bash
#!/bin/bash
# deploy.sh

set -e

echo "Running pre-deployment checks..."

# Code quality
opencode run "Check code quality before deployment"

# Security check
SECURITY_OUTPUT=$(opencode run --format json --file src/ "Security scan")
if echo "$SECURITY_OUTPUT" | jq -e '.issues | length > 0'; then
    echo "Security issues found!"
    exit 1
fi

# Get deployment approval
opencode run "Should I deploy? Consider: test results, security, code quality"

echo "Deployment approved. Proceeding..."
# deployment commands...
```

## Docker Integration

### Dockerfile

```dockerfile
FROM ubuntu:22.04

# Install OpenCode
RUN curl -fsSL https://opencode.ai/install | bash

WORKDIR /app

# Copy application code
COPY . .

# Run analysis during build
RUN opencode run --file src/ "Review code for issues"

CMD ["opencode", "run", "Start the application server"]
```

### Docker Compose

```yaml
services:
  app:
    build: .
    volumes:
      - ./src:/app/src

  reviewer:
    image: opencode:latest
    volumes:
      - ./src:/app/src
    command: opencode run --file /app/src "Continuous code review"
```

## Server Mode Patterns

### Batch Processing

```bash
#!/bin/bash
# Start server once
opencode serve --port 4096 &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Process multiple files
for FILE in src/**/*.py; do
    echo "Processing $FILE..."
    opencode run --attach http://localhost:4096 --file "$FILE" "Review this file"
done

# Cleanup
kill $SERVER_PID
```

### Continuous Monitoring

```bash
#!/bin/bash
# Start server in background
opencode serve --port 4096 &
SERVER_PID=$!

# Monitor loop
while true; do
    # Check for new commits
    LATEST_COMMIT=$(git rev-parse HEAD)

    if [ "$LATEST_COMMIT" != "$LAST_COMMIT" ]; then
        echo "New commit detected, running review..."
        opencode run --attach http://localhost:4096 "Review new changes"
        LAST_COMMIT=$LATEST_COMMIT
    fi

    sleep 60
done
```

## Error Handling

### Timeout Handling

```bash
#!/bin/bash
# Set timeout for opencode
TIMEOUT=180

opencode run "Complex analysis" &
PID=$!

# Wait with timeout
for i in $(seq 1 $TIMEOUT); do
    if ! kill -0 $PID 2>/dev/null; then
        echo "Command completed"
        exit 0
    fi
    sleep 1
done

# Timeout reached
kill $PID
echo "Command timed out after ${TIMEOUT}s"
exit 1
```

### Retry Logic

```bash
#!/bin/bash
MAX_RETRIES=3
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
    if opencode run "Your query"; then
        echo "Success"
        exit 0
    fi

    echo "Attempt $i failed, retrying in ${RETRY_DELAY}s..."
    sleep $RETRY_DELAY
done

echo "All retries failed"
exit 1
```

### Fallback Handling

```bash
#!/bin/bash
# Try opencode, fall back to alternative
if ! opencode run "Your query"; then
    echo "OpenCode failed, using fallback..."
    python analyze.py
fi
```

## Performance Optimization

### Parallel Processing

```bash
#!/bin/bash
# Process files in parallel
for FILE in src/**/*.py; do
    opencode run --file "$FILE" "Quick review" &
done

wait  # Wait for all background jobs
```

### Server Caching

```bash
#!/bin/bash
# Start server once for multiple queries
opencode serve --port 4096 &
sleep 3

# All queries share the same server context
opencode run --attach http://localhost:4096 "Query 1"
opencode run --attach http://localhost:4096 "Query 2"
opencode run --attach http://localhost:4096 "Query 3"

# Cleanup
killall opencode
```

### Result Caching

```bash
#!/bin/bash
CACHE_DIR=.opencode-cache
mkdir -p $CACHE_DIR

FILE_HASH=$(md5sum $FILE | cut -d' ' -f1)
CACHE_FILE="$CACHE_DIR/$FILE_HASH.json"

if [ -f "$CACHE_FILE" ]; then
    echo "Using cached result..."
    cat "$CACHE_FILE"
else
    echo "Running analysis..."
    opencode run --format json --file "$FILE" "Analyze this" > "$CACHE_FILE"
    cat "$CACHE_FILE"
fi
```

## Advanced Patterns

### Session Persistence

```bash
#!/bin/bash
# Create a persistent session
SESSION_ID=$(opencode run --title "Code Review" "Start reviewing project" | jq -r '.session_id')

# Use same session across multiple scripts
opencode run --session $SESSION_ID "Review authentication module"
opencode run --session $SESSION_ID "Review database layer"
opencode run --session $SESSION_ID "Summarize all findings"
```

### Multi-Stage Pipeline

```bash
#!/bin/bash
# Stage 1: Initial analysis
ANALYSIS=$(opencode run --format json "Analyze codebase structure")
echo "$ANALYSIS" > stage1.json

# Stage 2: Deep dive based on analysis
CRITICAL_FILES=$(echo "$ANALYSIS" | jq -r '.critical_files[]')
for FILE in $CRITICAL_FILES; do
    opencode run --file "$FILE" "Deep security review"
done > stage2.json

# Stage 3: Final report
opencode run --file stage1.json --file stage2.json "Generate final report"
```

### Interactive Wrapper

```bash
#!/bin/bash
# Interactive mode with user confirmation

while true; do
    echo "Enter your query (or 'quit' to exit):"
    read -r QUERY

    if [ "$QUERY" = "quit" ]; then
        break
    fi

    echo "Processing..."
    opencode run "$QUERY"

    echo "Press Enter to continue..."
    read
done
```
