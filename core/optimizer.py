from ortools.sat.python import cp_model
from core.models import SimulationData

class OptimizationResult:
    """Container to safely pass results to PhantomWork (disruptions.py)"""
    def __init__(self, status: str, total_cost: float, assignments: dict[str, str]):
        self.status = status
        self.total_cost = total_cost
        self.assignments = assignments
def optimize_assignments(dataset: SimulationData) -> OptimizationResult:
    model = cp_model.CpModel()
    tasks = dataset.tasks
    employees = dataset.employees
    hourly_costs = dataset.processing_costs_per_hour

    # Generates possible employee-task assignments for optimizer to evaluate.
    x = {}
    for t in tasks:
        for e in employees:
            x[t.id, e.id] = model.new_bool_var(f"assign_{t.id}_{e.id}")
    for t in tasks:
        model.Add(sum(x[t.id, e.id] for e in employees) == 1)
    
    # Strictly enforces employee authorization and prevents assignments without provided cost data.
    for t in tasks:
        for e in employees:
            is_authorized = t.title in e.authorization
            has_cost_profile = (e.id in hourly_costs) and (t.id in hourly_costs[e.id])
            if not (is_authorized and has_cost_profile):
                model.Add(x[t.id, e.id] == 0)
    for e in employees:
        employee_total_hours = []
        for t in tasks:
            employee_total_hours.append(x[t.id, e.id]*int(t.estimated_duration_hours))
        model.Add(sum(employee_total_hours) <= e.availability_hours_per_week)
    seperation_titles = {"Investigation", "Review", "Approval"}
    for e in employees:
        for title_a in seperation_titles:
            for title_b in seperation_titles:
                if title_a != title_b:
                    tasks_a = [t for t in tasks if t.title == title_a]
                    tasks_b = [t for t in tasks if t.title == title_b]
                    for t_a in tasks_a:
                        for t_b in tasks_b:
                            model.Add(x[t_a.id, e.id] + x[t_b.id, e.id] <= 1)

    # Calculates assignment costs so solver can find the cheapest, permitted workflow.
    total_cost_expr = []
    for t in tasks:
        for e in employees:
            if e.id in hourly_costs and t.id in hourly_costs[e.id]:
                hourly_rate = hourly_costs[e.id][t.id]
                total_task_cost = hourly_rate * t.estimated_duration_hours
                total_cost_expr.append(x[t.id, e.id] * round(total_task_cost * 100))
            else:
                total_cost_expr.append(x[t.id, e.id] * 0)
    model.Minimize(sum(total_cost_expr))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status_code = solver.Solve(model)
    status_mapping = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.UNKNOWN: "UNKNOWN"
    }
    status = status_mapping.get(status_code, "UNKNOWN")
    final_assignments = {}
    optimized_cost_dollars = 0.0
    if status in ["OPTIMAL", "FEASIBLE"]:
        optimized_cost_dollars = solver.ObjectiveValue()/100.0
        for t in tasks:
            for e in employees:
                if solver.Value(x[t.id, e.id]) == 1:
                    final_assignments[t.id] = e.id
    return OptimizationResult(
        status=status,
        total_cost=optimized_cost_dollars,
        assignments=final_assignments
    )
if __name__ == "__main__":
    import json
    with open("data/sample_scenario.json", "r") as file:
        data = json.load(file)
    scenario = SimulationData.model_validate(data)
    results = optimize_assignments(scenario)
    print("Optimization Status:", results.status)
    print("Optimized Cost: $", results.total_cost)
    print("Employee Assignment:", results.assignments)