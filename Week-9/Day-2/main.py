import asyncio
import sys
import os
import logging

logging.getLogger("autogen").setLevel(logging.ERROR)
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

sys.path.insert(0, os.path.dirname(__file__))

from registry.agent_registry import build_registry
from orchestrator.planner import build_dag
from orchestrator.dag_executor import execute_dag
from agents.reflection_agent import reflect
from agents.validator import validate
from config import MAX_RETRIES


def print_dag(dag):
    print("\n  Task graph:")
    for task_id, info in dag.items():
        deps = info["dependencies"]
        dep_str = f"  (depends on: {', '.join(deps)})" if deps else "  (no dependencies — runs in parallel)"
        print(f"    {task_id}: {info['description']}")
        print(f"           {dep_str}")
    print()


async def run_pipeline(user_query, registry):
    print("\n[1/5] Planning tasks...")
    dag = build_dag(user_query)
    print_dag(dag)

    print("[2/5] Executing DAG...")
    task_results = await execute_dag(dag, user_query, registry)

    print("[3/5] Reflecting and merging results...")
    merged_answer = await reflect(user_query, task_results)

    print("[4/5] Validating answer...\n")

    for attempt in range(1, MAX_RETRIES + 1):
        verdict = await validate(user_query, merged_answer)

        if verdict["status"] == "PASS":
            print(f"  Validation passed (attempt {attempt})")
            return verdict["answer"]

        print(f"  Validation failed (attempt {attempt}/{MAX_RETRIES})")
        print(f"  Critique: {verdict['critique']}\n")

        if attempt < MAX_RETRIES:
            print(f"  Improving answer based on critique...")
            merged_answer = await reflect(
                user_query,
                task_results,
                critique=verdict["critique"],
            )

    print("  Max retries reached. Returning best available answer.")
    return merged_answer


async def main():
    print("=" * 55)
    print("  Multi-Agent Orchestration System")
    print("  Day 2  |  Planner + DAG + Reflection + Validator")
    print("=" * 55)
    print("  Type your question and press Enter.")
    print("  Type 'exit' to quit.\n")

    registry = build_registry()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        try:
            print()
            answer = await run_pipeline(user_input, registry)

            print("\n[5/5] Final Answer")
            print("-" * 55)
            print(answer)
            print("-" * 55)
            print()
        except Exception as e:
            print(f"\n  Error: {e}")
            print("  Please try again.\n")


if __name__ == "__main__":
    asyncio.run(main())