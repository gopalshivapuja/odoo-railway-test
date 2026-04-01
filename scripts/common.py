#!/usr/bin/env python3
"""Shared XML-RPC helpers for Odoo automation scripts."""

import os
import sys
import xmlrpc.client


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"ERROR: Missing required environment variable: {name}")
        sys.exit(1)
    return value


def get_odoo_config() -> tuple[str, str, str, str]:
    url = get_required_env("ODOO_URL")
    db = get_required_env("ODOO_DB")
    username = get_required_env("ODOO_USERNAME")
    password = get_required_env("ODOO_PASSWORD")
    return url, db, username, password


def connect_odoo() -> tuple[str, str, int, str, xmlrpc.client.ServerProxy]:
    url, db, username, password = get_odoo_config()
    print(f"Connecting to Odoo at {url}...")
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
    uid = common.authenticate(db, username, password, {})
    if not uid:
        print("ERROR: Authentication failed.")
        sys.exit(1)
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)
    return url, db, uid, password, models
