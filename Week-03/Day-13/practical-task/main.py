
from security import (
    validate_input,
    detect_prompt_injection,
    redact_sensitive_data,
    get_api_key,
    validate_output,
    prepare_document_context,
    authenticate,
    execute_tool,
)


def secure_assistant(user_input: str) -> str:
    """Process a request through multiple security checks."""

    # Step 1: Validate the input
    valid, result = validate_input(user_input)

    if not valid:
        return f"BLOCKED: {result}"

    cleaned_input = result

    # Step 2: Detect basic prompt-injection attempts
    if detect_prompt_injection(cleaned_input):
        return "BLOCKED: Possible prompt-injection attempt detected."

    # Step 3: Remove recognizable sensitive information
    cleaned_input = redact_sensitive_data(cleaned_input)

    # Step 4: Demo response instead of calling a real LLM
    # Replace this section with a secured LLM integration later.
    response = (
        "Demo assistant received your safe request: "
        + cleaned_input
    )

    # Step 5: Validate the outgoing response
    return validate_output(response)


def main():
    print("=" * 45)
    print("VISIONROOT - SECURE AI ASSISTANT")
    print("=" * 45)

    # Step 6: Demonstrate authentication
    username = input("Demo username (trainee): ").strip()
    password = input("Demo password: ")

    if not authenticate(username, password):
        print("Access denied: authentication failed.")
        return

    print("\nAuthentication successful.")
    print("Type 'exit' to quit.")
    print("Type 'tool-test' to test tool authorization.")
    print("Type 'document-test' to test untrusted documents.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        if user_input.lower() == "tool-test":
            action = input("Action name to request: ").strip()
            print("Assistant:", execute_tool(action))
            continue

        if user_input.lower() == "document-test":
            document = input("Enter sample document text: ")
            print(prepare_document_context(document))
            continue

        print("Assistant:", secure_assistant(user_input))


if __name__ == "__main__":
    main()
