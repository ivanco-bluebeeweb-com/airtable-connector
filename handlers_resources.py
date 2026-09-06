"""Resource handlers for Airtable Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListAppRecordParams, GetAppRecordParams,
    AppRecordRecord, AppRecordList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_apps", "List apps in Airtable.", action_type="read", chain_callable=True, event="airtable-connector.list_apps", effects=["read:apps"], data_model=AppRecordList)
async def list_apps(params: ListAppRecordParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_apps(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.ok({"apps": items, "total": len(items)}, summary=f"Found {len(items)} apps.")
    except Exception as e:
        return ActionResult.error(f"Error listing apps: {e}")

@chat.function("get_apprecord", "Get details of one AppRecord in Airtable.", action_type="read", chain_callable=True, event="airtable-connector.get_apprecord", effects=["read:apprecord"], data_model=AppRecordRecord)
async def get_apprecord(params: GetAppRecordParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_apprecord(params.apprecord_id)
        rid = str(r.get("id") or params.apprecord_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.ok({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved AppRecord {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving AppRecord: {e}")

@chat.function("audit_apprecord_health", "Audit health of Airtable apps and connectivity.", action_type="read", chain_callable=True, event="airtable-connector.audit_apprecord_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_apprecord_health(params: ConnectionIdParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_apps(limit=50)
        return ActionResult.ok({
            "healthy": True,
            "total_apps": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"Airtable healthy. Sampled {len(items)} apps."
        }, summary=f"Airtable health check passed with {len(items)} apps.")
    except Exception as e:
        return ActionResult.error(f"Error auditing Airtable health: {e}")
