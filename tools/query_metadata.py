#!/usr/bin/env python3
"""
query_metadata.py

Minimal CLI tool for querying NetSuite metadata exported
under the v1 Metadata Provider Contract.

Returns JSON only.

Author: Joshua Meiri, Origami Precision, LLC
Copyright (c) 2026 Joshua Meiri, Origami Precision, LLC
License: MIT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any


BASE_DIR = Path(".netsuite-metadata")


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_env(env: str | None) -> str:
    if env:
        return env

    active_file = BASE_DIR / "active_env.json"
    if active_file.exists():
        data = load_json(active_file)
        return data.get("active_env")

    raise ValueError("Environment not specified and active_env.json not found.")


def load_record_index(env: str) -> Dict[str, Any]:
    return load_json(BASE_DIR / env / "record_index.json")


def load_record(env: str, record_key: str) -> Dict[str, Any]:
    index = load_record_index(env)
    for rec in index["records"]:
        if rec["record_key"] == record_key:
            return load_json(BASE_DIR / env / rec["file"])
    raise ValueError(f"Record '{record_key}' not found in index.")


def list_records(env: str) -> Dict[str, Any]:
    index = load_record_index(env)
    return {
        "environment": env,
        "records": [r["record_key"] for r in index["records"]],
    }


def list_fields(env: str, record_key: str) -> Dict[str, Any]:
    record = load_record(env, record_key)
    return {
        "environment": env,
        "record_key": record_key,
        "fields": list(record.get("fields", {}).keys()),
    }


def find_field(env: str, field_id: str) -> Dict[str, Any]:
    index = load_record_index(env)
    matches = []

    for rec in index["records"]:
        record = load_json(BASE_DIR / env / rec["file"])
        fields = record.get("fields", {})
        if field_id in fields:
            matches.append({
                "record_key": rec["record_key"],
                "field_definition": fields[field_id]
            })

    return {
        "environment": env,
        "field_id": field_id,
        "matches": matches
    }


def suggest_suiteql(env: str, record_key: str, field_list: list[str]) -> Dict[str, Any]:
    record = load_record(env, record_key)
    primary = record.get("primary_table", {})
    table = primary.get("suiteql_table")

    if not table:
        raise ValueError(f"No SuiteQL table defined for {record_key}")

    fields = record.get("fields", {})
    columns = []

    for f in field_list:
        if f not in fields:
            raise ValueError(f"Field '{f}' not found on {record_key}")
        col = fields[f].get("suiteql_column")
        if not col:
            raise ValueError(f"No SuiteQL column mapping for field '{f}'")
        columns.append(col)

    select_clause = ", ".join(columns)

    type_filter = primary.get("suiteql_type_filter")
    where_clause = ""
    if type_filter:
        where_clause = f" WHERE type = '{type_filter}'"

    query = f"SELECT {select_clause} FROM {table}{where_clause}"

    return {
        "environment": env,
        "record_key": record_key,
        "suiteql": query
    }


def main():
    parser = argparse.ArgumentParser(description="Query NetSuite metadata.")
    parser.add_argument("--env", help="Environment: qa or prod")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list-records")

    get_record_parser = subparsers.add_parser("get-record")
    get_record_parser.add_argument("record_key")

    list_fields_parser = subparsers.add_parser("list-fields")
    list_fields_parser.add_argument("record_key")

    find_field_parser = subparsers.add_parser("find-field")
    find_field_parser.add_argument("field_id")

    suiteql_parser = subparsers.add_parser("suggest-suiteql")
    suiteql_parser.add_argument("record_key")
    suiteql_parser.add_argument("--fields", required=True)

    args = parser.parse_args()

    try:
        env = resolve_env(args.env)

        if args.command == "list-records":
            result = list_records(env)

        elif args.command == "get-record":
            result = load_record(env, args.record_key)

        elif args.command == "list-fields":
            result = list_fields(env, args.record_key)

        elif args.command == "find-field":
            result = find_field(env, args.field_id)

        elif args.command == "suggest-suiteql":
            fields = args.fields.split(",")
            result = suggest_suiteql(env, args.record_key, fields)

        else:
            parser.print_help()
            sys.exit(1)

        print(json.dumps(result, indent=2))


    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

