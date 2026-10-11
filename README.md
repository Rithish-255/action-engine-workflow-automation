# Action Engine Automation for Workflow Deviations

A minor project demonstrating an action engine that detects workflow violations, creates alerts, and generates corrective tickets in enterprise process execution.

## Objective

This project simulates an enterprise workflow monitoring engine that:

- checks whether each invoice follows the expected process order,
- detects rules violations such as missing purchase order or skipped supplier validation,
- raises real-time alerts,
- converts alerts into corrective tickets,
- routes tickets to the correct operational owner.

## Key Process Concepts

- Conformance checks (`CONFORMANCE`)
- Workflow deviation detection
- Automated routing
- Alert generation
- Ticket creation
- Process execution automation

## Real-World Context

This project reflects operational finance workflows in which payment or processing should not proceed without a valid purchase order, proper validation, and approval closure.

## Project Structure

- `README.md` — project overview
- `requirements.txt` — Python dependencies
- `src/action_engine.py` — rule engine logic and alert/ticket generation
- `src/main.py` — entry point for execution
- `outputs/alerts.json` — generated alerts
- `outputs/tickets.json` — generated tickets

## Run Instructions

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Expected Output

```text
[ACTION ENGINE] Workflow violations detected:
- INV-101 -> ['MISSING_PO', 'FINANCE_CHECK_BYPASSED']
- INV-102 -> ['FINANCE_CHECK_BYPASSED']
- INV-104 -> ['MISSING_PO', 'SKIPPED_SUPPLIER_VALIDATION', 'UNAPPROVED_PAYMENT']
[ACTION ENGINE] Tickets generated: 3
[ACTION ENGINE] Output files saved to: /project/outputs
```

## Business Impact

This project illustrates how organizations can move from passive monitoring to active process execution by automatically flagging anomalies and initiating remediation workflows.
