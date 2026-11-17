#!/usr/bin/env python3
"""Append or revise JSON knowledge records and generate a Copilot-readable TXT mirror.

Uses only Python standard library. Never commit actual business records to public Git.
Example:
  python scripts/knowledge_store.py upsert --store knowledge.json --input new-records.json --mirror knowledge.txt
  python scripts/knowledge_store.py render --store knowledge.json --mirror knowledge.txt
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid
from datetime import datetime, timezone

TYPES = {"Decision", "Action", "Risk", "Issue", "Fact"}
STATUSES = {"Proposed", "Confirmed", "Closed", "Superseded"}
REVIEW = {"Pending Review", "Verified", "Rejected"}
CORE = ("title", "record_type", "project", "description", "status", "source_chat")
FIELDS = set(CORE) | {"id", "owner", "event_date", "source_link", "last_reviewed",
                      "review_status", "created_at", "updated_at", "rationale",
                      "due_date", "related_record_ids", "tags"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_atomic(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".copilotkb-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write(content)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def check_record(r):
    if not isinstance(r, dict) or set(r) - FIELDS:
        raise ValueError("Record contains unsupported fields")
    if any(not isinstance(r.get(k), str) or not r[k].strip() for k in CORE):
        raise ValueError(f"Record missing nonempty core fields: {CORE}")
    if r["record_type"] not in TYPES or r["status"] not in STATUSES:
        raise ValueError("Invalid record_type or status")
    if r.get("review_status") not in REVIEW:
        raise ValueError("Invalid review_status")
    uuid.UUID(r["id"])


def check_store(doc):
    if not isinstance(doc, dict) or doc.get("schema_version") != "1.0.0" or not isinstance(doc.get("records"), list):
        raise ValueError("Invalid knowledge store root")
    keys = []
    for r in doc["records"]:
        check_record(r)
        keys.append(r["id"])
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate IDs in the knowledge store")


def normalize(raw, stamp, old=None):
    r = dict(raw)
    r.setdefault("id", str(uuid.uuid4()))
    for key in ("owner", "event_date", "source_link", "last_reviewed", "rationale", "due_date"):
        r.setdefault(key, None)
    r.setdefault("review_status", "Pending Review")
    r.setdefault("related_record_ids", [])
    r.setdefault("tags", [])
    r["created_at"] = old["created_at"] if old else stamp
    r["updated_at"] = stamp
    check_record(r)
    return r


def mirror(doc):
    lines = ["CopilotKB Knowledge Register", "JSON file is authoritative; this TXT view is derived.",
             "Schema: " + doc["schema_version"], "Last updated: " + str(doc.get("updated_at")), ""]
    for r in doc["records"]:
        lines += [
            "## " + r["title"], "Record ID: " + r["id"],
            "Project: " + r["project"], "Type: " + r["record_type"],
            "Status: " + r["status"], "Review status: " + r["review_status"],
            "Description: " + r["description"], "Owner: " + str(r.get("owner") or "Not stated"),
            "Event date: " + str(r.get("event_date") or "Not stated"),
            "Source chat: " + r["source_chat"],
            "Source link: " + str(r.get("source_link") or "Unavailable"),
            "Rationale: " + str(r.get("rationale") or "Not stated"),
            "Due date: " + str(r.get("due_date") or "Not stated"),
            "Last reviewed: " + str(r.get("last_reviewed") or "Not reviewed"),
            "Related IDs: " + ", ".join(r.get("related_record_ids") or []),
            "Tags: " + ", ".join(r.get("tags") or []), ""
        ]
    return "\n".join(lines).rstrip() + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("upsert", "render"):
        q = sub.add_parser(name)
        q.add_argument("--store", required=True)
        q.add_argument("--mirror", required=True)
        if name == "upsert":
            q.add_argument("--input", required=True)
            q.add_argument("--allow-update", action="store_true")
    args = p.parse_args()
    path = Path(args.store)
    doc = read(path) if path.exists() else {"schema_version": "1.0.0", "updated_at": None, "records": []}
    check_store(doc)
    if args.command == "upsert":
        data = read(args.input)
        incoming = data.get("records") if isinstance(data, dict) and "records" in data else data
        if isinstance(incoming, dict):
            incoming = [incoming]
        if not isinstance(incoming, list) or not incoming:
            raise ValueError("Input must be a record or a nonempty list of records")
        existing = {r["id"]: i for i, r in enumerate(doc["records"])}
        stamp = now()
        changes = []
        for raw in incoming:
            old = doc["records"][existing[raw["id"]]] if isinstance(raw, dict) and raw.get("id") in existing else None
            if old and not args.allow_update:
                raise ValueError("Existing ID requires --allow-update: " + raw["id"])
            changes.append(normalize(raw, stamp, old))
        ids = [r["id"] for r in changes]
        if len(set(ids)) != len(ids):
            raise ValueError("Duplicate incoming IDs; changes not saved")
        for r in changes:
            if r["id"] in existing:
                doc["records"][existing[r["id"]]] = r
            else:
                doc["records"].append(r)
        doc["updated_at"] = stamp
        check_store(doc)
        if path.exists():
            shutil.copy2(path, path.with_name(path.name + ".bak"))
        write_atomic(path, json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    write_atomic(args.mirror, mirror(doc))
    print(f"Updated {len(doc['records'])} knowledge records; mirror: {args.mirror}")


if __name__ == "__main__":
    main()
