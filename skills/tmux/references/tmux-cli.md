# Tmux CLI reference (harness subset)

With `harness.sh`, prefix commands with `tmux -S "$(tmux-harness socket)"` or use the script subcommands instead of raw tmux.

## Sessions and panes

```bash
tmux new-session -d -s NAME -c /path/to/cwd
tmux new-window -t NAME -n winname -c /path
tmux split-window -t NAME:winname -h
tmux select-pane -t NAME:winname.0
```

## Output

```bash
tmux capture-pane -pt TARGET -S -LINES    # -S negative = scrollback lines
tmux capture-pane -pt TARGET -e -S -500   # include ANSI color escapes
tmux pipe-pane -t TARGET -o 'cat >>/tmp/transcript.log'
```

`-p` prints to stdout (agent-friendly). Without `-p`, tmux uses its internal copy buffer.

## Input

```bash
tmux send-keys -t TARGET Enter
tmux send-keys -t TARGET C-m              # same as Enter
tmux send-keys -t TARGET M-f              # meta/alt combinations
tmux send-keys -t TARGET -l 'literal text'
```

Special names: `Enter`, `Escape`, `Space`, `BSpace`, `DC` (Delete), `IC` (Insert), `C-c`, `C-d`, `C-z`, `PageUp`, `PageDown`, `Up`, `Down`.

## Inspection

```bash
tmux list-sessions
tmux list-panes -t NAME -F '#{pane_index} #{pane_current_command}'
tmux display-message -p -t TARGET '#{session_name} #{window_name} #{pane_pid}'
```

## Teardown

```bash
tmux kill-session -t NAME
tmux kill-window -t NAME:winname
```

Avoid `kill-server` in agent workflows.

## Target syntax

- Session: `NAME`
- Window: `NAME:0` or `NAME:winname`
- Pane: `NAME:0.1` or `NAME:winname.1`

`$SESSION` from the harness skill should stay stable for the whole drive.
