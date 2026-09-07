# Airtable Connector — Executed Validation Evidence

**Target:** Airtable Web API v0 (`https://api.airtable.com/v0`)  
**Date:** 2026-09-07  
**Credentials:** Airtable User `usrRhntv9gj6nMlzo` (`vlad@bluebeeweb.com`), authenticated via Google OAuth in Google Chrome. Personal Access Token (`patlxlUPMHrG...`) generated with scopes: `data.records:read`, `data.records:write`, `schema.bases:read`, `schema.bases:write`, `workspacesAndBases:read`, `user.email:read` across all workspaces.

## Part A — Authentication and Connection Lifecycle

| Scenario | Result | Evidence |
|---|---|---|
| A1: Auth Validation | Passed | Verified live credentials against `GET /v0/meta/whoami` returning HTTP 200 OK (`vlad@bluebeeweb.com`). |
| A2: Connect Lifecycle | Passed | `connect_airtable_connector` verified credentials, stored connection in Document store (`ctx.store`), and returned masked key (`pa******4b`). |
| A3: List Connections | Passed | `list_connections` retrieved 1 active connection with accurate metadata and masked key. |
| A4: Disconnect Lifecycle | Passed | `disconnect_airtable_connector` deleted the connection from Document store; subsequent listing returned 0 connections. |

## Part B — Live Base and Record Operations (CRUD Lifecycle)

| Scenario | Result | Evidence |
|---|---|---|
| B1: Base Creation & Listing (Read/Discover) | Passed | Base `appndY9qQ9KdCg3mB` ("Imperal Live Test Base") verified via `GET /v0/meta/bases`. `list_apps` returned 1 base. |
| B2: Base Schema Details (Read) | Passed | `get_apprecord` retrieved base `appndY9qQ9KdCg3mB` schema including table `LiveTasks` and its field definitions. |
| B3: Health Audit (Audit) | Passed | `audit_apprecord_health` verified API reachability, counted accessible bases, and returned `healthy: True`. |
| B4: Create Record (Create) | Passed | Created record `recpi2JidVJw3B5O6` in `LiveTasks` via `POST /v0/{baseId}/{table}` with fields `{"Title": "Automated Suite Task", "Status": "Todo"}`. Received HTTP 200. |
| B5: List Records (Read) | Passed | Listed records in `LiveTasks` via `GET /v0/{baseId}/{table}` verifying the created record's existence. |
| B6: Delete Record (Delete/Cleanup) | Passed | Deleted test record via `DELETE /v0/{baseId}/{table}/{recordId}`. Received HTTP 200 with `{"deleted": true}`. |
