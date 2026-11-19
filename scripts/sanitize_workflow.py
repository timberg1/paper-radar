#!/usr/bin/env python3
"""Bereinigt einen n8n-Workflow-Export für die Veröffentlichung.

Aufruf: python3 scripts/sanitize_workflow.py export-import.json workflows/import.json

Entfernt:
- gepinnte Testdaten (pinData) und die Instanz-ID
- Webhook-IDs (z. B. vom Chat Trigger)
- interne IDs der Credentials (der Name bleibt, damit man die Zuordnung sieht)
- Telegram-Chat-IDs (werden durch DEINE_CHAT_ID ersetzt)

Bricht mit Fehler ab, wenn danach noch etwas wie ein Schlüssel aussieht.
"""
import json
import re
import sys

PLATZHALTER = "DEINE_CHAT_ID"

# Muster, die auf Geheimnisse hindeuten
VERDAECHTIG = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"), "Anthropic-API-Key"),
    (re.compile(r"\b\d{8,10}:[A-Za-z0-9_\-]{30,}\b"), "Telegram-Bot-Token"),
    (re.compile(r'"(apiKey|api_key|accessToken|password|token)"\s*:\s*"[^"]+"', re.I), "Feld mit Schlüssel"),
]


def bereinigen(workflow: dict) -> dict:
    workflow.pop("pinData", None)
    workflow.get("meta", {}).pop("instanceId", None)
    workflow.pop("shared", None)

    for node in workflow.get("nodes", []):
        node.pop("webhookId", None)

        for cred in node.get("credentials", {}).values():
            if isinstance(cred, dict):
                cred.pop("id", None)

        params = node.get("parameters", {})
        if "chatId" in params:
            params["chatId"] = PLATZHALTER
    return workflow


def pruefen(text: str) -> list[str]:
    return [name for muster, name in VERDAECHTIG if muster.search(text)]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    quelle, ziel = sys.argv[1], sys.argv[2]
    with open(quelle, encoding="utf-8") as f:
        workflow = json.load(f)

    text = json.dumps(bereinigen(workflow), ensure_ascii=False, indent=2)

    funde = pruefen(text)
    if funde:
        print(f"ABBRUCH: {quelle} enthält noch: {', '.join(funde)}")
        print("Bitte im Export prüfen und entfernen. Es wurde nichts geschrieben.")
        return 1

    with open(ziel, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"OK: {quelle} -> {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
