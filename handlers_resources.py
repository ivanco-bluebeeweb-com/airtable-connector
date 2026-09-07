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

@chat.function("list_apps", "List apps/bases in Airtable.", action_type="read", chain_callable=True, event="airtable-connector.list_apps", effects=["read:apps"], data_model=AppRecordList)
async def list_apps(params: ListAppRecordParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_apps(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or "unknown")
            rname = r.get("name") or rid
            items.append({
                "id": rid,
                "name": rname,
                "status": r.get("permissionLevel") or "active",
                "created_at": str(r.get("createdAt") or ""),
                "raw": r
            })
        return ActionResult.success({"apps": items, "total": len(items)}, summary=f"Found {len(items)} bases.")
    except Exception as e:
        return ActionResult.error(f"Error listing bases: {e}")

@chat.function("get_apprecord", "Get details of one base in Airtable.", action_type="read", chain_callable=True, event="airtable-connector.get_apprecord", effects=["read:apprecord"], data_model=AppRecordRecord)
async def get_apprecord(params: GetAppRecordParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_apprecord(params.apprecord_id)
        rid = str(r.get("id") or params.apprecord_id)
        rname = r.get("name") or rid
        return ActionResult.success({
            "id": rid,
            "name": rname,
            "status": "active",
            "created_at": "",
            "raw": r
        }, summary=f"Retrieved base {rname}.")
    except Exception as e:
        return ActionResult.error(f"Error getting base details: {e}")

@chat.function("audit_apprecord_health", "Audit health of Airtable bases and connectivity.", action_type="read", chain_callable=True, event="airtable-connector.audit_apprecord_health", effects=["read:health"], data_model=AuditHealthReport)
async def audit_apprecord_health(params: ConnectionIdParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_apps(limit=10)
        total = len(raw_items)
        return ActionResult.success({
            "healthy": True,
            "total_apps": total,
            "details": {"sample_count": total},
            "summary": f"Airtable healthy. Accessible bases: {total}."
        }, summary=f"Airtable health check passed with {total} bases.")
    except Exception as e:
        return ActionResult.error(f"Health audit failed: {e}")
