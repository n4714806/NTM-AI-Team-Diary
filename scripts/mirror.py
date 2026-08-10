#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCE_REPO = "n4714806/WAI_NTM"
SOURCE_ISSUES = {3: "journal", 4: "quotes"}
OUT_DIR = Path("mirror")
STATE_PATH = Path("mirror_state.json")

TOKEN_PATTERNS = [
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b", re.I),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b", re.I),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:password|passwd|secret|token|private key|2fa)\b\s*[:=]", re.I),
]
SENSITIVE_PATTERNS = [
    re.compile(r"[A-Za-z]:\\[^\s]+"),                 # Windows paths
    re.compile(r"/(?:home|Users|mnt|var|etc)/[^\s]+"), # local paths
    re.compile(r"\bPID\s*[:=#]?\s*\d+\b", re.I),
    re.compile(r"https://github\.com/n4714806/WAI_NTM(?:/[^\s]*)?", re.I),
    re.compile(r"https://api\.github\.com/repos/n4714806/WAI_NTM(?:/[^\s]*)?", re.I),
    re.compile(r"\b(?:nonce|lockfile|installation token|private key|credential)\b", re.I),
]
MACHINE_LINE = re.compile(r"^[A-Z][A-Z0-9_ -]{2,40}:\s*(?:PASS|FAIL|YES|NO|NONE|BLOCKED|ACTIVE|INACTIVE|UNKNOWN|[A-Z0-9_./-]+)\s*$")


def api_get(url, token):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def contains_secret(text):
    return any(p.search(text or "") for p in TOKEN_PATTERNS)


def sanitize_text(text, issue_no):
    if not text or contains_secret(text):
        return None, "secret-pattern"

    # Never publish fenced code blocks or HTML comments.
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    # Drop machine-packet style lines from human-facing mirror.
    kept = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if MACHINE_LINE.match(line.strip()):
            continue
        if any(p.search(line) for p in SENSITIVE_PATTERNS):
            continue
        kept.append(line)
    text = "\n".join(kept).strip()

    # Extra hard-stop terms for journal public export.
    if issue_no == 3:
        lowered = text.lower()
        hard_stop = [
            "production secret", "github app private", "watcher pid", "worker pid",
            "exact token", "credential value", "internal filesystem", "private repo url",
        ]
        if any(x in lowered for x in hard_stop):
            return None, "journal-hard-stop"

    # Require actual Traditional-Chinese prose; avoids publishing raw packets/logs.
    cjk = len(re.findall(r"[\u3400-\u9fff]", text))
    if cjk < 12:
        return None, "not-human-readable-zh"

    return text, None


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"seen": {"3": [], "4": []}, "last_run": None}


def save_state(state):
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_entry(issue_no, c, body):
    created = c.get("created_at") or ""
    author = c.get("user", {}).get("login", "unknown")
    cid = c.get("id")
    title = "團隊日誌" if issue_no == 3 else "語錄"
    return (
        f"## {title}｜{created[:10] or '日期未知'}\n\n"
        f"{body}\n\n"
        f"<sub>來源：private source comment #{cid}；作者帳號：{author}。公開鏡像僅供文化／閱讀用途，沒有任何控制權。</sub>\n"
    )


def main():
    token = os.environ.get("NTM_PRIVATE_READ_TOKEN")
    if not token:
        print("NTM_PRIVATE_READ_TOKEN missing; mirror skipped safely.")
        return 0

    OUT_DIR.mkdir(exist_ok=True)
    state = load_state()
    changed = False

    for issue_no, stem in SOURCE_ISSUES.items():
        url = f"https://api.github.com/repos/{SOURCE_REPO}/issues/{issue_no}/comments?per_page=100"
        comments = api_get(url, token)
        seen = set(str(x) for x in state["seen"].setdefault(str(issue_no), []))
        new_entries = []

        for c in comments:
            cid = str(c.get("id"))
            if cid in seen:
                continue
            body, reason = sanitize_text(c.get("body", ""), issue_no)
            # Mark as seen even if skipped, so sensitive content is never repeatedly processed/logged.
            seen.add(cid)
            if body:
                new_entries.append(render_entry(issue_no, c, body))
            else:
                print(f"Skipped source comment {cid}: {reason}")

        state["seen"][str(issue_no)] = sorted(seen, key=lambda x: int(x))
        if new_entries:
            path = OUT_DIR / f"{stem}.md"
            header = (
                "# 公開鏡像｜團隊日誌\n\n"
                if issue_no == 3 else
                "# 公開鏡像｜語錄本\n\n"
            )
            disclaimer = (
                "> 這是經安全過濾後的公開鏡像，不是 WAI_NTM 的控制來源、決策來源或完整歷史。\n\n"
            )
            existing = path.read_text(encoding="utf-8") if path.exists() else header + disclaimer
            path.write_text(existing.rstrip() + "\n\n" + "\n\n---\n\n".join(new_entries) + "\n", encoding="utf-8")
            changed = True

    save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
