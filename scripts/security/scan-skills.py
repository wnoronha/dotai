#!/usr/bin/env python3
"""Skill / agent supply-chain scanner. Stdlib only, no deps.

Scans skills/*/SKILL.md, agents/*.md, commands/**, and scripts/* for:
  1. frontmatter schema violations (name mismatch, unknown keys, over-broad perms)
  2. prompt-injection / jailbreak instructions
  3. exfiltration / RCE patterns (curl|bash, reverse shell, cred access, rm -rf /)
  4. obfuscation (long base64 blobs, hidden HTML comments with instructions)
  5. secret literals (tokens, private keys)
  6. supply-chain URLs (IP literals, known exfil pastes, new domains)

Findings are (severity, path, line, rule, detail).
Exit 0 = clean, 1 = HIGH findings, 2 = usage error.
MEDIUM findings warn but do not fail (use --strict to fail on MEDIUM).

Usage:
  scripts/security/scan-skills.py [--root .] [--strict] [--json-out report.json]
                                  [--sarif-out report.sarif]
"""
import argparse
import json
import pathlib
import re
import sys

SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"

ALLOWED_FRONTMATTER_KEYS = {
    "name", "description", "disable-model-invocation",
    "allowed-tools", "model", "version",
}

# Prompt-injection / instruction-override phrases (case-insensitive).
INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions", "instruction-override"),
    (r"disregard\s+(all\s+)?(previous|prior|above)\s+instructions", "instruction-override"),
    (r"bypass\s+(safety|guardrails|security\s+review|content\s+policy)", "safety-bypass"),
    (r"do\s+not\s+ask\s+(for\s+)?(permission|confirmation)", "no-confirm-bypass"),
    (r"never\s+ask\s+(for\s+)?(permission|confirmation)", "no-confirm-bypass"),
    (r"disable\s+(safety|guardrails|content\s+filter)", "safety-bypass"),
    (r"you\s+are\s+now\s+(dan|jailbroken|unrestricted)", "jailbreak-persona"),
    (r"repeat\s+.*system\s+prompt", "system-prompt-leak"),
    (r"reveal\s+.*system\s+prompt", "system-prompt-leak"),
    (r"send\s+.*(secrets?|tokens?|credentials?|env(ironment)?)\s+to\s+http", "exfil-instruction"),
    (r"exfiltrat\w*", "exfil-instruction"),
]

# Shell / RCE / cred-access patterns. Intentionally anchored to avoid
# flagging legit docs (e.g. `rm -rf "$dst"` in scripts/install is OK;
# `rm -rf /` is not).
SHELL_HIGH = [
    (r"\bcurl\b[^\n]*\|\s*(sh|bash)\b", "curl-pipe-shell"),
    (r"\bwget\b[^\n]*\|\s*(sh|bash)\b", "wget-pipe-shell"),
    (r"\bnc\b[^\n]*\s+-e\s+\S+", "netcat-exec"),
    (r"\b bash\s+-i\s+>&\s*/dev/tcp/", "reverse-shell"),
    (r"rm\s+-rf\s+/(?:\s|$|\"|')", "rm-rf-root"),
    (r"rm\s+-rf\s+~/?(?:\s|$|\"|')", "rm-rf-home"),
    (r"chmod\s+-R\s+777\s+/", "chmod-777-root"),
    (r":\(\)\s*\{\s*:\|\:&\s*\}\s*;", "fork-bomb"),
    (r"cat\s+~/\.ssh/id_\w+", "ssh-key-read"),
    (r"cat\s+~/\.aws/credentials", "aws-cred-read"),
    (r"cat\s+/etc/(passwd|shadow)", "etc-cred-read"),
    (r"env\s*\|\s*(curl|wget|nc)\b", "env-exfil"),
]

SHELL_MEDIUM = [
    # Documented examples use $(...) command substitution; only flag
    # network-coupled cases to stay green on the current tree.
    (r"\bcurl\b[^\n]*\$\(", "curl-subshell"),
]

CRED_READ_MEDIUM = [
    (r"\bAWS_SECRET\w*\b", "aws-secret-ref"),
    (r"\bOPENAI_API_KEY\b", "api-key-ref"),
]

SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "aws-access-key"),
    (r"ghp_[A-Za-z0-9]{36,}", "github-pat"),
    (r"gho_[A-Za-z0-9]{36,}", "github-oauth"),
    (r"xox[bap]- [A-Za-z0-9-]+", "slack-token"),
    (r"sk-ant-[A-Za-z0-9\-_]{20,}", "anthropic-key"),
    (r"sk-[A-Za-z0-9]{20,}", "openai-key"),
    (r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----", "private-key"),
]

LONG_B64_RE = re.compile(r"\b[A-Za-z0-9+/]{200,}={0,2}\b")
URL_RE = re.compile(r"https?://([A-Za-z0-9.\-]+)(?::\d+)?(?:/[^\s)\"'<>]*)?")
IP_LITERAL_RE = re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?")

SUSPICIOUS_DOMAINS = (
    "webhook.site", "ngrok.io", "ngrok-free.app", "pastebin.com",
    "paste.rs", "transfer.sh", "0x0.st", "discord.com/api/webhooks",
)

# Docs use example hosts; don't fail the tree on them.
BENIGN_DOMAINS = {
    "staging.myapp.com", "example.com", "www.example.com",
}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\s*\n?", re.S)


def _line_of(text, pos):
    return text.count("\n", 0, max(0, pos)) + 1


def parse_frontmatter(text, path, findings, require=True):
    m = FRONTMATTER_RE.match(text)
    if not m:
        if require:
            findings.append((SEVERITY_MEDIUM, path, 1, "frontmatter-missing",
                             "no YAML frontmatter block"))
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    fm = {}
    key_lines = {}
    current_key = None
    block_mode = False
    for i, line in enumerate(raw.splitlines(), 1):
        if not line.strip() or line.strip().startswith("#"):
            continue
        # Continuation of a block scalar (>, >-, |, |-) or indented fold.
        if (line.startswith(" ") or line.startswith("\t")) and current_key is not None \
                and (block_mode or current_key == "description"):
            fm[current_key] += " " + line.strip()
            continue
        block_mode = False
        if ":" not in line:
            findings.append((SEVERITY_MEDIUM, path, i + 1, "frontmatter-malformed",
                             f"line {i}: no key: value"))
            current_key = None
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        fm[k] = v
        key_lines[k] = i + 1  # +1 for opening --- line
        current_key = k
        if v in (">", ">-", "|-", "|"):
            block_mode = True
    for k in fm:
        if k not in ALLOWED_FRONTMATTER_KEYS:
            findings.append((SEVERITY_MEDIUM, path, key_lines.get(k, 2),
                             "frontmatter-unknown-key", f"unknown key '{k}'"))
    if "name" not in fm or not fm["name"].strip("\"' "):
        findings.append((SEVERITY_HIGH, path, 2, "frontmatter-no-name",
                         "missing required 'name'"))
    else:
        expected = pathlib.Path(path).parent.name \
            if pathlib.Path(path).name == "SKILL.md" else pathlib.Path(path).stem
        got = fm["name"].strip("\"'")
        if got != expected and path.startswith("skills/"):
            findings.append((SEVERITY_HIGH, path, key_lines.get("name", 2),
                             "frontmatter-name-mismatch",
                             f"name '{got}' != dir '{expected}'"))
    if "description" not in fm:
        findings.append((SEVERITY_MEDIUM, path, 2, "frontmatter-no-description",
                         "missing 'description'"))
    return fm, body


def check_file(path, text, findings):
    is_skill = path.endswith("SKILL.md") or path.startswith("agents/")
    fm, body = parse_frontmatter(text, path, findings, require=is_skill) \
        if path.endswith(".md") else ({}, text)
    _ = fm
    low = body if path.endswith(".md") else text
    body_offset = len(text) - len(low) if path.endswith(".md") else 0

    def line_for(match_start):
        return _line_of(text, body_offset + match_start)

    for pat, rule in INJECTION_PATTERNS:
        for mo in re.finditer(pat, low, re.I):
            findings.append((SEVERITY_HIGH, path, line_for(mo.start()), rule,
                             f"prompt-injection: '{mo.group(0)[:80]}'"))
    for pat, rule in SHELL_HIGH:
        for mo in re.finditer(pat, low):
            findings.append((SEVERITY_HIGH, path, line_for(mo.start()), rule,
                             f"shell-risk: '{mo.group(0)[:80]}'"))
    for pat, rule in SHELL_MEDIUM + CRED_READ_MEDIUM:
        for mo in re.finditer(pat, low):
            findings.append((SEVERITY_MEDIUM, path, line_for(mo.start()), rule,
                             f"suspicious: '{mo.group(0)[:80]}'"))
    for pat, rule in SECRET_PATTERNS:
        for mo in re.finditer(pat, low):
            findings.append((SEVERITY_HIGH, path, line_for(mo.start()), rule,
                             "possible secret literal"))
    for mo in LONG_B64_RE.finditer(low):
        findings.append((SEVERITY_MEDIUM, path, line_for(mo.start()), "long-base64-blob",
                         f"{len(mo.group(0))}-char base64 blob (possible obfuscation)"))
    # Hidden HTML comments that carry instructions are a known skill-hiding trick.
    for mo in re.finditer(r"<!--(.*?)-->", low, re.S):
        inner = mo.group(1)
        if re.search(r"ignore|bypass|curl|wget|exfiltrat|secret|token", inner, re.I):
            findings.append((SEVERITY_HIGH, path, line_for(mo.start()),
                             "hidden-comment-instruction",
                             f"<!-- ...{inner.strip()[:80]}... -->"))
    for mo in URL_RE.finditer(low):
        host = mo.group(1).lower()
        if host in BENIGN_DOMAINS:
            continue
        line = line_for(mo.start())
        if IP_LITERAL_RE.match(mo.group(0)):
            findings.append((SEVERITY_HIGH, path, line, "ip-literal-url", mo.group(0)[:120]))
        elif any(d in host for d in SUSPICIOUS_DOMAINS):
            findings.append((SEVERITY_HIGH, path, line, "suspicious-domain", mo.group(0)[:120]))
        else:
            findings.append((SEVERITY_MEDIUM, path, line, "external-url", mo.group(0)[:120]))


def write_sarif(findings, out_path):
    rules = {}
    for _sev, _path, _line, rule, _detail in findings:
        rules.setdefault(rule, f"skill-security check: {rule}")
    results = []
    for sev, path, line, rule, detail in sorted(findings):
        results.append({
            "ruleId": rule,
            "level": "error" if sev == SEVERITY_HIGH else "warning",
            "message": {"text": f"[{sev}] {detail}"},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": path},
                    "region": {"startLine": max(1, int(line or 1))},
                }
            }],
        })
    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {
                "name": "skill-security",
                "informationUri": "https://github.com/gitleaks/gitleaks-action",
                "version": "1.0.0",
                "rules": [{"id": r, "shortDescription": {"text": d}}
                          for r, d in sorted(rules.items())],
            }},
            "results": results,
        }],
    }
    pathlib.Path(out_path).write_text(json.dumps(sarif, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--sarif-out", default=None)
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    targets = []
    for d in ("skills", "agents", "commands"):
        p = root / d
        if p.is_dir():
            targets += sorted(p.rglob("*.md"))
    sp = root / "scripts"
    if sp.is_dir():
        targets += [f for f in sorted(sp.iterdir()) if f.is_file()]
    # Nested scripts (scripts/security/) also matter.
    sec = root / "scripts" / "security"
    if sec.is_dir():
        for f in sorted(sec.iterdir()):
            if f.is_file() and f not in targets:
                targets.append(f)

    # The scanner documents the patterns it detects (e.g. "curl|bash" in
    # the docstring); never flag itself.
    self_name = pathlib.Path(__file__).name
    targets = [f for f in targets if f.name != self_name]
    findings = []
    for f in targets:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            findings.append((SEVERITY_MEDIUM, str(f), 1, "unreadable", str(e)))
            continue
        try:
            rel = str(f.relative_to(root))
        except ValueError:
            rel = str(f)
        if rel.startswith("scripts/"):
            check_file(rel, text, findings)
            # de-dupe frontmatter-missing noise for shell scripts
            findings[:] = [x for x in findings
                           if not (x[1] == rel and x[3] == "frontmatter-missing")]
        else:
            check_file(rel, text, findings)

    # Executable-bit / symlink hygiene on skill trees.
    for f in targets:
        try:
            rel = str(f.relative_to(root))
        except ValueError:
            rel = str(f)
        if f.is_symlink():
            findings.append((SEVERITY_MEDIUM, rel, 1, "symlink",
                             f"symlink -> {f.resolve()}"))
        elif f.stat().st_mode & 0o111 and f.suffix == ".md":
            findings.append((SEVERITY_MEDIUM, rel, 1, "executable-markdown",
                             "markdown file has +x bit"))

    highs = [x for x in findings if x[0] == SEVERITY_HIGH]
    meds = [x for x in findings if x[0] == SEVERITY_MEDIUM]
    for sev, path, line, rule, detail in sorted(findings):
        print(f"{sev:6} {path}:{line} [{rule}] {detail}")

    if args.json_out:
        pathlib.Path(args.json_out).write_text(json.dumps(
            [{"severity": s, "path": p, "line": ln, "rule": r, "detail": d}
             for s, p, ln, r, d in findings], indent=2))

    if args.sarif_out:
        write_sarif(findings, args.sarif_out)
        print(f"sarif: {args.sarif_out} results={len(findings)}")

    print(f"\nscanned={len(targets)} high={len(highs)} medium={len(meds)}")
    if highs or (args.strict and meds):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
