"""Pydantic schemas for Airtable Connector."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameters model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Primary Airtable.")
    api_token: str = Field(description="Platform API Key / Access Token")
    base_url: str = Field(default="https://api.airtable.com/v0", description="Airtable API base URL.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    success: bool
    message: str

class AppRecordRecord(BaseModel):
    id: str
    name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)

class AppRecordList(BaseModel):
    apps: list[AppRecordRecord]
    total: int

class ListAppRecordParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    limit: int = Field(default=20, ge=1, le=100, description="Max records to return.")

class GetAppRecordParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    apprecord_id: str = Field(description="Airtable AppRecord ID.")

class AuditHealthReport(BaseModel):
    healthy: bool
    total_apps: int
    details: Dict[str, Any] = Field(default_factory=dict)
    summary: str
