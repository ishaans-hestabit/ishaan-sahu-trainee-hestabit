import asyncio
from agents.worker_agent import run_worker


async def execute_dag(dag, user_query, registry):
    completed = {}
    remaining = set(dag.keys())

    print("\n  DAG execution starting")
    print(f"  Total tasks: {len(dag)}\n")

    wave = 1
    while remaining:
        ready = [
            task_id for task_id in remaining
            if all(dep in completed for dep in dag[task_id]["dependencies"] if dep in dag)
        ]

        if not ready:
            raise RuntimeError("DAG has a cycle or unresolvable dependency.")

        print(f"  Wave {wave} — running {len(ready)} task(s) in parallel: {ready}")

        async def run_task(tid=None):
            description = dag[tid]["description"]
            dep_context = ""
            for dep in dag[tid]["dependencies"]:
                dep_context += f"\n[Result of {dep}]: {completed[dep]}\n"

            result = await run_worker(user_query, description, dep_context)
            print(f"    [done] {tid}")
            return tid, result

        tasks = [run_task(tid) for tid in ready]
        results = await asyncio.gather(*tasks)

        for task_id, result in results:
            completed[task_id] = result
            remaining.remove(task_id)

        wave += 1

    print()
    return completed