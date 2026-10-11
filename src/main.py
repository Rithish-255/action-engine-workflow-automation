from action_engine import run_action_engine, save_outputs


def main() -> None:
    alerts, tickets = run_action_engine()
    save_outputs(alerts, tickets)

    print("[ACTION ENGINE] Workflow violations detected:")
    for alert in alerts:
        print(f"- {alert['case_id']} -> {alert['violations']}")

    print(f"[ACTION ENGINE] Tickets generated: {len(tickets)}")
    print("[ACTION ENGINE] Output files saved to: /project/outputs")


if __name__ == "__main__":
    main()
