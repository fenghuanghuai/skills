# OpenCode Troubleshooting

Common issues and solutions when using OpenCode CLI.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Authentication Issues](#authentication-issues)
- [Connection Issues](#connection-issues)
- [Performance Issues](#performance-issues)
- [Output Issues](#output-issues)
- [Server Issues](#server-issues)

## Installation Issues

### Command Not Found

**Error:**
```
bash: opencode: command not found
```

**Solution:**
```bash
curl -fsSL https://opencode.ai/install | bash
```

**Verify installation:**
```bash
opencode --version
```

### Permission Denied

**Error:**
```
bash: /usr/local/bin/opencode: Permission denied
```

**Solution:**
```bash
chmod +x /usr/local/bin/opencode
```

### Installation Fails on Linux

**Error:**
```
curl: (35) error:1407742E:SSL routines:SSL23_GET_SERVER_HELLO:tlsv1 alert protocol version
```

**Solution:**
```bash
# Update curl or use insecure flag (not recommended)
curl -k -fsSL https://opencode.ai/install | bash
```

## Authentication Issues

### API Key Not Found

**Error:**
```
Error: No API key configured for provider 'anthropic'
```

**Solution:**
```bash
opencode auth login
# Select your provider and enter API key
```

**Verify configuration:**
```bash
opencode auth list
```

### Invalid API Key

**Error:**
```
Error: Invalid API key for provider 'anthropic'
```

**Solution:**
```bash
# Remove and re-add the key
opencode auth logout anthropic
opencode auth login
```

### Environment Variable Not Working

**Issue:** API key set in environment variable but not recognized.

**Solution:**
```bash
# Make sure the variable is exported
export ANTHROPIC_API_KEY="your-key-here"

# Or use .env file in your project directory
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

## Connection Issues

### Server Not Running

**Error:**
```
Error: Failed to connect to server at http://localhost:4096
```

**Solution:**
```bash
# Start the server
opencode serve --port 4096

# Or use without server (simpler)
opencode run "Your query"
```

### Port Already in Use

**Error:**
```
Error: Port 4096 is already in use
```

**Solution:**
```bash
# Find what's using the port
lsof -i :4096

# Use a different port
opencode serve --port 5000

# Or kill the existing process
killall opencode
```

### Connection Refused

**Error:**
```
Error: Connection refused
```

**Possible causes:**
1. Server not running
2. Wrong hostname/port
3. Firewall blocking connection

**Solution:**
```bash
# Check if server is running
lsof -i :4096

# Check firewall
sudo ufw status

# Try with localhost instead of 127.0.0.1
opencode run --attach http://localhost:4096 "Your query"
```

## Performance Issues

### Slow Response Time

**Symptom:** Queries take a long time to complete.

**Possible causes:**
1. Network latency
2. Large files being analyzed
3. Server cold start

**Solutions:**
```bash
# Use server mode to avoid cold starts
opencode serve --port 4096 &
opencode run --attach http://localhost:4096 "Your query"

# Analyze specific files instead of entire directory
opencode run --file specific-file.py "Your query"

# Use faster model
opencode run --model anthropic/claude-3-5-haiku-20241022 "Your query"
```

### High Memory Usage

**Symptom:** OpenCode uses too much memory.

**Solution:**
```bash
# Limit file size
opencode run --file small-file.py "Your query"

# Clear session cache
rm -rf ~/.opencode/sessions/*
```

### Timeout Issues

**Error:**
```
Command timed out
```

**Solution:**
```bash
# Increase timeout
timeout 300 opencode run "Your complex query"

# Or break down into smaller queries
opencode run "Part 1: Initial analysis"
opencode run --session <id> "Part 2: Deep dive"
```

## Output Issues

### No Output

**Symptom:** Command runs but produces no output.

**Possible causes:**
1. Output buffering
2. Query was understood but no response needed

**Solution:**
```bash
# Use unbuffered output
opencode run "Your query" | cat

# Or use JSON format
opencode run --format json "Your query"
```

### Garbled Output

**Symptom:** Output contains strange characters or formatting issues.

**Solution:**
```bash
# Set locale
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

opencode run "Your query"
```

### JSON Parsing Errors

**Error:**
```
jq: parse error: Invalid JSON
```

**Solution:**
```bash
# Ensure --format json is used
opencode run --format json "Your query" | jq '.'

# Or capture stderr separately
opencode run --format json "Your query" 2>/dev/null | jq '.'
```

## Server Issues

### Server Won't Start

**Symptom:** `opencode serve` fails to start.

**Check logs:**
```bash
tail -20 ~/.opencode/logs/server.log
```

**Common solutions:**
```bash
# Clear port and restart
killall opencode
rm -f ~/.opencode/server.pid
opencode serve --port 4096
```

### Server Crashes

**Symptom:** Server starts but crashes after a short time.

**Check logs:**
```bash
tail -50 ~/.opencode/logs/server.log
```

**Possible causes:**
1. Out of memory
2. Unhandled exception
3. Port conflict

**Solution:**
```bash
# Increase memory limits (if using Docker)
docker run --memory 4g opencode

# Use different port
opencode serve --port 5000
```

### Zombie Processes

**Symptom:** Multiple `opencode` processes running.

**Solution:**
```bash
# Kill all opencode processes
killall -9 opencode

# Clean up PID files
rm -f ~/.opencode/server.pid
```

## File-Related Issues

### File Not Found

**Error:**
```
Error: File not found: /path/to/file.py
```

**Solution:**
```bash
# Use absolute path
opencode run --file /full/path/to/file.py "Your query"

# Or check current directory
pwd
ls -la
```

### Permission Denied

**Error:**
```
Error: Permission denied: /path/to/file
```

**Solution:**
```bash
# Check file permissions
ls -la /path/to/file

# Fix permissions
chmod +r /path/to/file
```

### Binary File Issues

**Symptom:** OpenCode can't read binary files.

**Solution:**
```bash
# Check file type
file /path/to/file

# Exclude binary files
opencode run --file $(find src -name '*.py') "Your query"
```

## Getting Help

### Enable Debug Logging

```bash
opencode --log-level DEBUG run "Your query"
```

### Check Version

```bash
opencode --version
```

### Update OpenCode

```bash
opencode upgrade
```

### Report Issues

Collect information before reporting:

```bash
# Version info
opencode --version

# Config info
cat ~/.opencode/config.json

# Logs
tail -50 ~/.opencode/logs/server.log

# System info
uname -a
```

Report at: https://github.com/opencode-ai/opencode/issues

### Community Resources

- [GitHub Issues](https://github.com/opencode-ai/opencode/issues)
- [Documentation](https://opencode.ai/docs)
- [Discord Community](https://discord.gg/opencode)
