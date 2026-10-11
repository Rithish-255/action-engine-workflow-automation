from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


EXPECTED_SEQUENCE = [
    "invoice_created",
    "supplier_validation",
    "manager_approval",
    "finance_check",
    "payment_released",
]


def generate_event_log() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "INV-101",
            "invoice_id": "INV-101",
            "vendor": "VENDOR_01",
            "amount": 18000,
            "po_present": False,
            "events": [
                "invoice_created",
                "supplier_validation",
                "manager_approval",
                "payment_released",
            ],
            "approval_status": "approved",
            "department": "Procurement",
        },
        {
            "case_id": "INV-102",
            "invoice_id": "INV-102",
            "vendor": "VENDOR_02",
            "amount": 9500,
            "po_present": True,
            "events": [
                "invoice_created",
                "manager_approval",
                "payment_released",
            ],
            "approval_status": "approved",
            "department": "Finance",
        },
        {
            "case_id": "INV-103",
            "invoice_id": "INV-103",
            "vendor": "VENDOR_03",
            "amount": 21000,
            "po_present": True,
            "events": [
                "invoice_created",
                "supplier_validation",
                "finance_check",
                "manager_approval",
                "payment_released",
            ],
            "approval_status": "approved",
            "department": "AP",
        },
        {
            "case_id": "INV-104",
            "invoice_id": "INV-104",
            "vendor": "VENDOR_04",
            "amount": 45000,
            "po_present": False,
            "events": [
                "invoice_created",
                "supplier_validation",
                "payment_released",
            ],
            "approval_status": "unapproved",
            "department": "Finance",
        },
    ]


def conformance_check(events: list[str]) -> bool:
    """Check whether the workflow follows the expected process sequence."""
    for idx, expected_step in enumerate(EXPECTED_SEQUENCE):
        if idx >= len(events):
            return False
        if events[idx] != expected_step:
            return False
    return True


def detect_deviation(record: dict[str, Any]) -> list[str]:
    violations: list[str] = []

    if not record["po_present"]:
        violations.append("MISSING_PO")

    if "supplier_validation" not in record["events"]:
        violations.append("SKIPPED_SUPPLIER_VALIDATION")

    if "finance_check" not in record["events"]:
        violations.append("FINANCE_CHECK_BYPASSED")

    if record["approval_status"] == "unapproved":
        violations.append("UNAPPROVED_PAYMENT")

    if record["events"].count("manager_approval") > 1:
        violations.append("LOOPED_APPROVAL")

    return violations


def create_alert(record: dict[str, Any], violations: list[str]) -> dict[str, Any]:
    return {
        "case_id": record["case_id"],
        "invoice_id": record["invoice_id"],
        "vendor": record["vendor"],
        "amount": record["amount"],
        "severity": "HIGH" if record["amount"] > 30000 else "MEDIUM",
        "violations": violations,
        "timestamp": datetime.now().isoformat(),
        "message": f"Workflow violation detected for {record['invoice_id']}.",
    }


def create_ticket(alert: dict[str, Any]) -> dict[str, Any]:
    return {
        "ticket_id": f"TKT-{alert['case_id']}",
        "case_id": alert["case_id"],
        "severity": alert["severity"],
        "status": "OPEN",
        "route_to": "Finance Controller" if alert["severity"] == "HIGH" else "AP Supervisor",
        "summary": "Process deviation flagged by Action Engine",
        "violations": alert["violations"],
        "created_at": alert["timestamp"],
    }


def run_action_engine() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    data = generate_event_log()
    alerts: list[dict[str, Any]] = []
    tickets: list[dict[str, Any]] = []

    for record in data:
        violations = detect_deviation(record)
        if violations:
            alert = create_alert(record, violations)
            ticket = create_ticket(alert)
            alerts.append(alert)
            tickets.append(ticket)

    return alerts, tickets


def save_outputs(alerts: list[dict[str, Any]], tickets: list[dict[str, Any]]) -> None:
    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "alerts.json").write_text(json.dumps(alerts, indent=2), encoding="utf-8")
    (output_dir / "tickets.json").write_text(json.dumps(tickets, indent=2), encoding="utf-8")


if __name__ == "__main__":
    alerts, tickets = run_action_engine()
    save_outputs(alerts, tickets)
    print("[ACTION ENGINE] Workflow violations detected:")
    for alert in alerts:
        print(f"- {alert['case_id']} -> {alert['violations']}")
    print(f"[ACTION ENGINE] Tickets generated: {len(tickets)}")
    print("[ACTION ENGINE] Output files saved to: ", str(Path(__file__).resolve().parents[1] / 'outputs'))
