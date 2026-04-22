session_messages = []


def add_to_session(role, content):
    session_messages.append({"role": role, "content": content})
    if len(session_messages) > 10:
        session_messages.pop(0)


def get_session_context():
    if not session_messages:
        return ""
    return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in session_messages)
