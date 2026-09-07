"""HTTP client for Airtable Web API."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_BASE = "https://api.airtable.com/v0"

class AirtableClient:
    def __init__(self, api_token: str, base_url: str = ""):
        self.api_token = api_token.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_BASE).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-Airtable-Connector/1.0.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/meta/whoami", headers=self.headers)
                if resp.status_code in (200, 201, 204):
                    return {"status": "ok", "data": resp.json() if resp.content else {}}
                return {"status": "error", "error": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def list_apps(self, limit: int = 20) -> list[dict[str, Any]]:
        """List Airtable bases (app records)."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/meta/bases", headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()
                bases = data.get("bases", [])
                return bases[:limit]
            return []

    async def get_apprecord(self, apprecord_id: str) -> dict[str, Any]:
        """Get Airtable base schema/tables for a specific base ID."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/meta/bases/{apprecord_id}/tables", headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            return {"id": apprecord_id, "tables": []}

    async def create_record(self, base_id: str, table_name_or_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        """Create a single record in a table."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}/{base_id}/{table_name_or_id}",
                headers=self.headers,
                json={"fields": fields}
            )
            if resp.status_code in (200, 201):
                return resp.json()
            return {"error": f"HTTP {resp.status_code}: {resp.text}"}

    async def list_records(self, base_id: str, table_name_or_id: str, max_records: int = 20) -> list[dict[str, Any]]:
        """List records in a table."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.base_url}/{base_id}/{table_name_or_id}",
                headers=self.headers,
                params={"maxRecords": max_records}
            )
            if resp.status_code == 200:
                return resp.json().get("records", [])
            return []

    async def delete_record(self, base_id: str, table_name_or_id: str, record_id: str) -> dict[str, Any]:
        """Delete a record from a table."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.delete(
                f"{self.base_url}/{base_id}/{table_name_or_id}/{record_id}",
                headers=self.headers
            )
            if resp.status_code == 200:
                return resp.json()
            return {"error": f"HTTP {resp.status_code}: {resp.text}"}
