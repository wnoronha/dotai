# Install dotai

## Steps

1. Clone the repo to a stable path.
	```sh
	git clone <url> ~/workspace/dotai
	```
2. Link the canonical mirror. Skills resolve `~/.dotai` as a fallback path.
	```sh
	ln -s ~/workspace/dotai ~/.dotai
	```
3. Install into each project that needs the stack. From the project root:
	```sh
	~/.dotai/scripts/install .
	```
	The installer detects the harnesses the project uses and symlinks skills into `.agents/skills/` (cursor, codex, opencode) and `.claude/skills/` (claude), agents into the matching `agents/` dirs, and the `pre-push` guard into `.git/hooks/`. Symlinked dirs are appended to the project `.gitignore`. Nothing installs globally.
4. Confirm what loaded.
	```sh
	ls .agents/skills/ .claude/skills/ 2>/dev/null
	```

## Variants

- Preview first: add `--dry-run`.
- One harness only: `--only claude`.
- Every harness: `--all`.
- Vendor instead of symlink (teammates without your checkout): `--copy`. Copied files are meant to be committed, so no gitignore entry is added.
- Remove: `scripts/install . --uninstall`. Only symlinks it owns go quietly.
- Flag list: `scripts/install --help`.
