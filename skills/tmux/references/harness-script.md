# harness.sh design

## Harness-agnostic

dotai symlinks this skill into each IDE/agent install (`.agents/skills/`, `.claude/skills/`, etc.). The tmux layer is identical.

**Agents** resolve `HARNESS` to the script path (or an existing `tmux-harness` on PATH); they do not add shell aliases. **Humans** may define `alias tmux-harness=…` and use `watch` / `attach-cmd` from any terminal.

## Why a named socket

Default `tmux` attaches to one server per user (`/tmp/tmux-*`). Agent-driven sessions would clutter that list and risk naming collisions with your workflow.

`harness.sh` always passes `-S "$HARNESS_TMUX_SOCKET"`. Your daily tmux is untouched; agent sessions live on `tmux-harness/$USER.sock`.

## State

| Path | Contents |
|------|----------|
| `…/tmux-harness/$USER.sock` | tmux server socket |
| `…/tmux-harness/latest.env` | `HARNESS_TMUX_SOCKET`, `SESSION`, `WORKDIR` after last `new` |

Per-project sockets (optional): `export HARNESS_TMUX_SOCKET="/tmp/tmux-harness-myrepo.sock"` before `new`.

## Safety

- Session names: `harness-<slug>-<pid>`.
- Teardown is per-session only; no `kill-server` subcommand.
- `kill-stale` removes all `harness-*` sessions on **this** socket only.

## Extending

Add subcommands in `main()` and keep each as a thin `tmux_h` wrapper so agents and humans share one entry point.
