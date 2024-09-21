def format_error_response(*, message, status_code):
    error_message = {"detail": message}
    if isinstance(message, dict):
        consolidated_message = " ".join(
            f"{key}: {detail}" for key, value in message.items() for detail in value
        )
        error_message["detail"] = consolidated_message
    return error_message, status_code
