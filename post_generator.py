def generate_post(execution_result, snapshot):
    if execution_result["action"] == "BUY":
        return (
            "LOG ENTRY\n\n"
            f"BTC spot trigger active.\n"
            f"Entry watching around ${snapshot['price']:.2f}.\n\n"
            "Small size.\n"
            "Tight risk."
        )

    return (
        "LOG ENTRY\n\n"
        "No clean trigger yet.\n"
        "Watching the chain."
    )
