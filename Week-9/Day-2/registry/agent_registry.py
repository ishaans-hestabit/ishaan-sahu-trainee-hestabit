from agents.worker_agent import worker
from agents.reflection_agent import reflection
from agents.validator import validator


def build_registry():
    return {
        "worker": worker,
        "reflection": reflection,
        "validator": validator,
    }