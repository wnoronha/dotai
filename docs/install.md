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
3. Confirm the layout.
	```sh
	ls ~/.dotai/skills | wc -l
	ls ~/.dotai/agents ~/.dotai/scripts
	```
4. Point your harness at the checkout so it loads `skills/*/SKILL.md` and `agents/*.md` by name.
5. Open a `poteto-mode` session in any repo you work in. Session start installs the `pre-push` guard into that repo on its own. To cover every repo at once instead, do this one time:
	```sh
	mkdir -p ~/.dotai/githooks
	cp ~/.dotai/scripts/pre-push ~/.dotai/githooks/pre-push
	git config --global core.hooksPath ~/.dotai/githooks
	```
	Skip the global step if you keep other per-repo hooks. It overrides them.
