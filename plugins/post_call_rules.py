def my_custom_rule(input):  # receives the model response
    print("------------------------------------------------")
    if len(input) < 20:
        print(f"Response too short: {input}")
        return {
            "decision": False,
            "message": "This violates LiteLLM Proxy Rules. Response too short",
        }
    return {"decision": True}  # message not required since, request will pass
