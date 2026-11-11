#!/usr/bin/env bash
# tmux harness — isolated socket + harness-* sessions for agents and humans.
set -euo pipefail

HARNESS_SESSION_RE='^harness-'

socket_path() {
  if [[ -n "${HARNESS_TMUX_SOCKET:-}" ]]; then
    printf '%s\n' "$HARNESS_TMUX_SOCKET"
    return
  fi
  local base="${XDG_RUNTIME_DIR:-/tmp}/tmux-harness"
  printf '%s/%s.sock\n' "$base" "${USER:-$(id -un)}"
}

state_dir() {
  dirname "$(socket_path)"
}

TMUX_BIN="${TMUX_BIN:-tmux}"

tmux_h() {
  local sock
  sock="$(socket_path)"
  mkdir -p "$(dirname "$sock")"
  "$TMUX_BIN" -S "$sock" "$@"
}

ensure_server() {
  tmux_h start-server 2>/dev/null || true
}

harness_sessions() {
  tmux_h list-sessions 2>/dev/null | grep -E "$HARNESS_SESSION_RE" || true
}

usage() {
  cat <<'EOF'
tmux harness — agent tmux on a dedicated socket (won't touch your default tmux).

Works with any dotai-linked harness (Cursor, Claude, Codex, OpenCode, etc.).

  socket                         print socket path; start server
  new SLUG [WORKDIR]             detached session harness-SLUG-PID
  ls                             list harness sessions on this socket
  run SESSION CMD...             send command + Enter
  send SESSION [keys...]         tmux send-keys (e.g. C-c Enter)
  wait SESSION REGEX [SECONDS]   poll capture until regex matches (default 120)
  cap SESSION [LINES]            capture-pane to stdout (default 500 lines)
  kill SESSION                   kill one session
  kill-stale                     kill all harness-* on this socket
  watch SESSION                  attach (for you — interactive)
  attach-cmd [SESSION]           one-liner to watch (SESSION or latest)
  latest                         print latest SESSION from state

Env:
  HARNESS_TMUX_SOCKET  override socket (default: $XDG_RUNTIME_DIR/tmux-harness/$USER.sock)
  WORKDIR              default cwd for new

Examples:
  tmux-harness new dev
  tmux-harness run "$SESSION" npm run dev
  tmux-harness wait "$SESSION" 'Listening on' 90
  tmux-harness attach-cmd
EOF
}

write_latest() {
  local session=$1 workdir=$2
  local sock dir
  sock="$(socket_path)"
  dir="$(state_dir)"
  mkdir -p "$dir"
  cat >"$dir/latest.env" <<ENV
HARNESS_TMUX_SOCKET=$sock
SESSION=$session
WORKDIR=$workdir
ENV
  printf '%s\n' "$session"
}

read_latest_session() {
  local f
  f="$(state_dir)/latest.env"
  if [[ -f "$f" ]]; then
    # shellcheck source=/dev/null
    source "$f"
    printf '%s\n' "${SESSION:-}"
  fi
}

cmd_socket() {
  ensure_server
  socket_path
}

cmd_new() {
  local slug=${1:?slug required}
  local workdir=${2:-${WORKDIR:-$PWD}}
  ensure_server
  local session="harness-${slug}-$$"
  tmux_h new-session -d -s "$session" -c "$workdir"
  write_latest "$session" "$workdir" >/dev/null
  local sock
  sock="$(socket_path)"
  printf 'SESSION=%s\n' "$session"
  printf 'WORKDIR=%s\n' "$workdir"
  printf 'SOCKET=%s\n' "$sock"
  printf 'HARNESS_TMUX_SOCKET=%s\n' "$sock"
  printf 'Watch: tmux -S %q attach -t %q\n' "$sock" "$session"
  printf 'Or:    %s watch %q\n' "$(basename "$0")" "$session"
}

cmd_ls() {
  ensure_server
  harness_sessions
}

cmd_run() {
  local session=$1
  shift
  tmux_h send-keys -t "$session" "$@" Enter
}

cmd_send() {
  local session=$1
  shift
  tmux_h send-keys -t "$session" "$@"
}

cmd_wait() {
  local session=$1 pattern=$2
  local timeout=${3:-120}
  local deadline start now pane
  start=$(date +%s)
  deadline=$((start + timeout))
  while true; do
    pane="$(tmux_h capture-pane -pt "$session" -S -300)"
    if printf '%s' "$pane" | grep -qE "$pattern"; then
      printf '%s\n' "$pane"
      return 0
    fi
    now=$(date +%s)
    if (( now >= deadline )); then
      printf 'timeout after %ss waiting for %s\n' "$timeout" "$pattern" >&2
      tmux_h capture-pane -pt "$session" -S -500
      return 1
    fi
    sleep 1
  done
}

cmd_cap() {
  local session=$1
  local lines=${2:-500}
  tmux_h capture-pane -pt "$session" -S "-$lines"
}

cmd_kill() {
  local session=$1
  tmux_h kill-session -t "$session" 2>/dev/null || true
}

cmd_kill_stale() {
  ensure_server
  local line name
  while IFS= read -r line; do
    name="${line%%:*}"
    tmux_h kill-session -t "$name" 2>/dev/null || true
  done < <(harness_sessions)
}

cmd_watch() {
  local session=$1
  exec tmux_h attach -t "$session"
}

cmd_attach_cmd() {
  local session
  session=${1:-$(read_latest_session)}
  if [[ -z "$session" ]]; then
    echo "no SESSION; run new first or pass a session name" >&2
    exit 1
  fi
  local sock
  sock="$(socket_path)"
  ensure_server
  printf 'tmux -S %q attach -t %q\n' "$sock" "$session"
}

cmd_latest() {
  read_latest_session
}

main() {
  local cmd=${1:-}
  shift || true
  case "$cmd" in
    socket) cmd_socket ;;
    new) cmd_new "$@" ;;
    ls) cmd_ls ;;
    run) cmd_run "$@" ;;
    send) cmd_send "$@" ;;
    wait) cmd_wait "$@" ;;
    cap|capture) cmd_cap "$@" ;;
    kill) cmd_kill "$@" ;;
    kill-stale) cmd_kill_stale ;;
    watch) cmd_watch "$@" ;;
    attach-cmd) cmd_attach_cmd "$@" ;;
    latest) cmd_latest ;;
    -h|--help|help|"") usage ;;
    *)
      echo "unknown command: $cmd" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
