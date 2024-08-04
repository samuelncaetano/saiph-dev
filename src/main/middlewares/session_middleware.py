active_sessions = {}


def session_middleware(handler):  # type: ignore
    def wrapper(request, *args, **kwargs):  # type: ignore
        session_id = request.headers.get("Session-ID")

        if session_id and session_id in active_sessions:
            raise ValueError("Session already active")

        response = handler(request, *args, **kwargs)

        if session_id:
            active_sessions[session_id] = True

        return response

    return wrapper
