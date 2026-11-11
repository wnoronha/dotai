---
name: tmux
description: "Drives interactive CLIs and TUIs in isolated tmux sessions: launch detached panes, send keys, poll for readiness, capture transcripts, and tear down only what the agent started. Harness-agnostic (dotai: Cursor, Claude, Codex, OpenCode, etc.). Use for tmux harness, PTY verification, interactive terminal apps, or when verify skills need a scripted TUI drive."
disable-model-invocation: true
---

# Tmux agent harness

Use tmux when an **agent** (any dotai-linked harness — Cursor, Claude, Codex, OpenCode, …) must **interact** with a terminal UI: prompts, pagers, REPLs, `npm run dev` log tails, or multi-step CLI flows. Prefer one-shot shell commands for non-interactive work.

## Principles

1. **One harness session per drive** — never attach to or reuse the user's personal tmux sessions.
2. **Name what you own** — session names start with `harness-` plus a slug and `$$` or a short random suffix.
3. **Kill sessions, not servers** — teardown is `tmux kill-session -t <name>`. Never `tmux kill-server`.
4. **Evidence is capture-pane** — store transcripts for verification; do not rely on memory across turns.
5. **Readiness is observed** — wait for a log line, prompt string, or exit code pattern in captured output, not a fixed sleep alone.

## Preconditions

```bash
command -v tmux >/dev/null || { echo "tmux not installed"; exit 1; }
```

Run drives from the project directory (`-c` on `new-session`). Export env vars the app needs before `send-keys`.

Default path: resolve `$HARNESS` (see [Utility script](#utility-script)) and run the **Agent flow** there. That keeps sessions on `HARNESS_TMUX_SOCKET`, not the user's default tmux server.

## Lifecycle

Copy and track:

```text
Harness progress:
- [ ] Resolve $HARNESS (Utility script)
- [ ] new SLUG → SESSION
- [ ] run START_CMD
- [ ] wait for readiness pattern
- [ ] send / cap as needed
- [ ] kill SESSION (even on failure)
```

Record `SESSION` in the agent's notes for this task so later steps target the same session. Map each step to `"$HARNESS" new|run|wait|cap|send|kill` in the Utility script section.

Do not kill by broad `pkill node` / `pkill python` unless the verify skill explicitly requires it and documents port ownership.

### Fallback (no harness script)

Only if the script is missing and cannot be installed from dotai: every `tmux` command must use the harness socket, e.g. `tmux -S "$HARNESS_TMUX_SOCKET" …`. Without `-S`, sessions attach to the user's personal tmux and violate the principles above. See [references/tmux-cli.md](references/tmux-cli.md) for flags.

## Session targeting

- Prefer `-t "$SESSION"` on the harness socket via `"$HARNESS"` or `tmux -S "$HARNESS_TMUX_SOCKET"`.
- Multiple windows: `new-window` on that same socket target.
- List harness sessions: `"$HARNESS" ls`.

## When to use something else

| Situation | Use |
|-----------|-----|
| Single non-interactive command | Shell tool |
| HTTP/API proof | `curl` or project verify skill |
| Browser UI | Playwright/CDP per project verify skill |
| Strict expect()/regex on a PTY without tmux | `script` or `expect` (see [references/pty-alternatives.md](references/pty-alternatives.md)) |

## Pairing with verification skills

When driving an app for **verify-this** or a project `verify-*` skill:

1. Run **doctor** checks (binary, version, port free) before creating a session.
2. Launch in tmux; readiness = what that skill defines (log line, health URL, prompt).
3. Save transcripts under the path the verify skill names (e.g. `/tmp/verify-this/<slug>/treatment/transcript.txt`).
4. Teardown instances; keep evidence files.

## Failure modes

| Symptom | Likely cause | Fix |
|---------|----------------|-----|
| Empty capture | Command exited instantly | Check exit via `tmux display-message -p -t "$SESSION" '#{pane_dead}'` and pane content |
| Garbled TUI | Capturing mid-redraw | Brief sleep; widen `-S` history |
| Session exists | Name collision | Use `$$` or random suffix; list/kill stale `harness-*` you own |
| Keys ignored | Focus wrong pane/window | Target `session:window.pane` explicitly |

## Utility script

**`scripts/harness.sh`** (alias **`tmux-harness`**): all agent sessions run on a **separate tmux socket** so they never collide with your normal tmux server and you can attach with one printed command. Same script whether skills were loaded from Cursor, Claude, Codex, or OpenCode.

Default socket: `$XDG_RUNTIME_DIR/tmux-harness/$USER.sock` (else `/tmp/tmux-harness/$USER.sock`). Override with `HARNESS_TMUX_SOCKET`.

### Agents: resolve the script (no alias required)

Do **not** edit the user's shell rc, install global aliases, or touch git config to "set up" `tmux-harness`. The alias is optional human UX.

At the start of harness work (once per shell session), resolve the helper and export it:

```bash
if command -v tmux-harness >/dev/null 2>&1; then
  HARNESS=tmux-harness
elif [[ -x "${DOTAI_ROOT:-$HOME/.dotai}/skills/tmux/scripts/harness.sh" ]]; then
  HARNESS="${DOTAI_ROOT:-$HOME/.dotai}/skills/tmux/scripts/harness.sh"
else
  echo "tmux harness script not found; set DOTAI_ROOT or install dotai skills" >&2
  exit 1
fi
export HARNESS
```

Use `"$HARNESS"` for all subcommands below. If the file exists but is not executable, `chmod +x` on that path only — do not change other dotai files.

Tell the user the **Watch:** line from `new` so they can attach in another terminal; do not run interactive `watch` yourself unless they ask.

### Humans: optional alias

```bash
alias tmux-harness='$HOME/.dotai/skills/tmux/scripts/harness.sh'
```

### Agent flow (short)

```bash
eval "$("$HARNESS" new myslug)"   # SESSION= in output; or parse SESSION= line
"$HARNESS" run "$SESSION" npm run dev
"$HARNESS" wait "$SESSION" 'Listening on' 120
"$HARNESS" cap "$SESSION" 300 > /tmp/transcript.txt
"$HARNESS" kill "$SESSION"
```

### Watch while an agent works

After `new`, the script prints a **Watch:** line. Any time:

```bash
"$HARNESS" attach-cmd              # copies-friendly one-liner (latest session)
"$HARNESS" watch "$SESSION"        # attach now (detaches with usual tmux keys)
tmux -S "$("$HARNESS" socket)" ls  # list harness sessions on this socket
```

`latest.env` beside the socket records `HARNESS_TMUX_SOCKET`, `SESSION`, and `WORKDIR` for `source .../latest.env`.

### Command overview

| Command | Purpose |
|---------|---------|
| `socket` | Print socket path; ensure server is up |
| `new SLUG [DIR]` | Create `harness-SLUG-$$`, print env + watch one-liner |
| `ls` | List `harness-*` sessions on harness socket |
| `run SESSION CMD...` | `send-keys` + Enter |
| `send SESSION ...` | Raw `send-keys` (`C-c`, `Enter`, literal text) |
| `wait SESSION REGEX [SEC]` | Poll pane until regex matches |
| `cap SESSION [LINES]` | `capture-pane` to stdout |
| `kill SESSION` | `kill-session` |
| `kill-stale` | Kill all harness-owned sessions on this socket |
| `watch SESSION` | Interactive attach (human) |
| `attach-cmd [SESSION]` | Print `tmux -S … attach -t …` |
| `latest` | Print latest session name |

Agents should use `cap` / `wait` / `run`; humans use `watch` / `attach-cmd`. Never `kill-server`.

## Additional resources

- Tmux CLI flags and targeting: [references/tmux-cli.md](references/tmux-cli.md)
- Non-tmux PTY options: [references/pty-alternatives.md](references/pty-alternatives.md)
- Harness implementation notes: [references/harness-script.md](references/harness-script.md)
