# PTY alternatives

Use when tmux is unavailable or overkill.

## `script` (macOS / Linux)

Record a login shell session to a file:

```bash
script -q /tmp/pty.log bash -lc './my-cli.sh'
```

Non-interactive automation is limited; best for recording human-style repros.

## `expect`

When input/output must match strict patterns:

```bash
expect <<'EOF'
set timeout 120
spawn ./myapp
expect "Password:"
send "test\r"
expect eof
EOF
```

Prefer tmux when the agent must **re-enter** the same session across multiple tool calls in one task.

## IDE / agent terminal files

Some harnesses log background shell output to project terminal files. Fine for long servers, but cross-turn capture and key injection are less reliable than a named tmux session on `HARNESS_TMUX_SOCKET`. Use tmux for multi-step TUI verification across agent turns.
