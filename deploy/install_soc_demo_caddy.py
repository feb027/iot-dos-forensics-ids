#!/usr/bin/env python3
"""Install the /soc-demo Caddy handlers into /etc/caddy/Caddyfile.

Run with sudo from the repo root:
    sudo python3 deploy/install_soc_demo_caddy.py
    sudo caddy validate --config /etc/caddy/Caddyfile
    sudo systemctl reload caddy
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

CADDYFILE = Path("/etc/caddy/Caddyfile")
SNIPPET = Path(__file__).resolve().with_name("Caddyfile.soc-demo-snippet")
SITE_BLOCK = "iot.aquarise.my.id {"
MARKER = "handle /soc-demo/api/*"


def indent_snippet(snippet: str) -> str:
    return "\n".join("    " + line if line.strip() else "" for line in snippet.splitlines())


def main() -> None:
    text = CADDYFILE.read_text()
    if MARKER in text:
        print("SKIP: /soc-demo handlers already exist in /etc/caddy/Caddyfile")
        return

    snippet = SNIPPET.read_text().strip()
    if SITE_BLOCK not in text:
        raise SystemExit(f"ERROR: block {SITE_BLOCK!r} not found in {CADDYFILE}")

    backup = CADDYFILE.with_name(f"Caddyfile.bak.{datetime.now():%Y%m%d-%H%M%S}")
    backup.write_text(text)

    start = text.index(SITE_BLOCK)
    insert_pos = text.index("\n", start) + 1
    insert = "\n    # Fase 6B/6C Interactive AI SOC Demo\n" + indent_snippet(snippet) + "\n\n"
    CADDYFILE.write_text(text[:insert_pos] + insert + text[insert_pos:])
    print(f"Inserted /soc-demo handlers into {CADDYFILE}")
    print(f"Backup written to {backup}")


if __name__ == "__main__":
    main()
