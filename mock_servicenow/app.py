"""Mock ServiceNow incident API with switchable faults.

This is a simplified stand-in modelled on the ServiceNow Table API
(/api/now/table/incident). It is NOT real ServiceNow: lookups are by incident
number, and only the fields needed for this lab exist.

Fault modes (set via POST /_admin/fault {"mode": "..."}):
  none               healthy
  auth_expired       every call returns 401
  rate_limit         every call returns 429 with Retry-After
  rate_limit_first2  the first 2 calls return 429, then the API recovers
  schema_v2          "API v2": create needs `summary`, responses use
                     `summary`/`status` instead of `short_description`/`state`
"""
import os
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from lab_logging import log

VALID_TOKEN = os.environ.get("SERVICENOW_TOKEN", "lab-valid-token")

app = FastAPI(title="Mock ServiceNow (Table API-style)")
STATE: dict = {}


def reset_state() -> None:
    STATE.clear()
    STATE["fault"] = "none"
    STATE["rl_count"] = 0
    STATE["next_id"] = 10002
    STATE["incidents"] = {
        "INC0004521": {
            "number": "INC0004521",
            "short_description": "Outlook keeps asking for password",
            "state": "In Progress",
            "urgency": "2",
            "work_notes": ["Assigned to Service Desk"],
        },
        "INC0004522": {
            "number": "INC0004522",
            "short_description": "Cannot access shared drive",
            "state": "New",
            "urgency": "3",
            "work_notes": [],
        },
        "INC0010001": {
            "number": "INC0010001",
            "short_description": "VPN disconnects every 10 minutes",
            "state": "On Hold",
            "urgency": "2",
            "work_notes": ["Waiting for user to test on wired network"],
        },
    }


reset_state()


def render(rec: dict) -> dict:
    """Shape an incident for the response, honouring the schema_v2 fault."""
    out = dict(rec)
    if STATE["fault"] == "schema_v2":
        out["summary"] = out.pop("short_description")
        out["status"] = out.pop("state")
    return out


def fail(request: Request, status: int, message: str, detail: str, headers=None):
    log(
        "api",
        "error_response",
        request.headers.get("x-trace-id"),
        status=status,
        message=message,
        detail=detail,
        fault_mode=STATE["fault"],
    )
    return JSONResponse(
        status_code=status,
        content={"error": {"message": message, "detail": detail}, "status": "failure"},
        headers=headers or {},
    )


def gate(request: Request):
    """Auth and rate-limit checks shared by all table endpoints."""
    mode = STATE["fault"]
    auth = request.headers.get("authorization", "")
    if mode == "auth_expired" or auth != f"Bearer {VALID_TOKEN}":
        return fail(request, 401, "User Not Authenticated", "Required to provide Auth information")
    if mode == "rate_limit":
        return fail(request, 429, "Too Many Requests", "Rate limit exceeded", {"Retry-After": "1"})
    if mode == "rate_limit_first2" and STATE["rl_count"] < 2:
        STATE["rl_count"] += 1
        return fail(request, 429, "Too Many Requests", "Rate limit exceeded", {"Retry-After": "1"})
    return None


@app.middleware("http")
async def access_log(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        log(
            "api",
            "http_request",
            request.headers.get("x-trace-id"),
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            latency_ms=round((time.time() - start) * 1000),
            fault_mode=STATE["fault"],
        )
    return response


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/_admin/fault")
async def set_fault(request: Request):
    body = await request.json()
    STATE["fault"] = body.get("mode", "none")
    STATE["rl_count"] = 0
    return {"fault": STATE["fault"]}


@app.post("/_admin/reset")
def admin_reset():
    reset_state()
    return {"ok": True}


@app.post("/api/now/table/incident")
async def create_incident(request: Request):
    if (blocked := gate(request)) is not None:
        return blocked
    body = await request.json()
    if STATE["fault"] == "schema_v2":
        if not body.get("summary"):
            return fail(request, 422, "Invalid request", "Field 'summary' is required")
        short = body["summary"]
    else:
        short = body.get("short_description")
        if not short:
            return fail(request, 400, "Invalid request", "Field 'short_description' is required")
    number = f"INC{STATE['next_id']:07d}"
    STATE["next_id"] += 1
    rec = {
        "number": number,
        "short_description": short,
        "state": "New",
        "urgency": str(body.get("urgency", "3")),
        "work_notes": [],
    }
    STATE["incidents"][number] = rec
    return JSONResponse(status_code=201, content={"result": render(rec)})


@app.get("/api/now/table/incident/{number}")
def get_incident(number: str, request: Request):
    if (blocked := gate(request)) is not None:
        return blocked
    rec = STATE["incidents"].get(number)
    if rec is None:
        return fail(request, 404, "No Record found", "Record doesn't exist or ACL restricts the record retrieval")
    return {"result": render(rec)}


@app.patch("/api/now/table/incident/{number}")
async def update_incident(number: str, request: Request):
    if (blocked := gate(request)) is not None:
        return blocked
    rec = STATE["incidents"].get(number)
    if rec is None:
        return fail(request, 404, "No Record found", "Record doesn't exist or ACL restricts the record retrieval")
    body = await request.json()
    if body.get("work_notes"):
        rec["work_notes"].append(body["work_notes"])
    return {"result": render(rec)}
