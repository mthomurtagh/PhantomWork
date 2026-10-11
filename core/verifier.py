from typing import List, Dict
import json
from core.models import SimulationData
from core.optimizer import optimize_assignments
class VerificationResult:
    """Container to safely pass independent compliance audit results back to PhantomWork"""
    def __init__(self, passed: bool, violations: List[str]):
        self.passed = passed
        self.violations = violations
def verify_assignments(dataset: SimulationData, assignments: Dict[str, str]) -> VerificationResult:
    violations = []
    task_ids = {t.id for t in dataset.tasks}
    task_map = {t.id: t for t in dataset.tasks}
    employee_ids = {e.id: e for e in dataset.employees}
    employee_map = {e.id: e for e in dataset.employees}
    hourly_costs = dataset.processing_costs_per_hour

    # Verifies that every required task is assigned to an existing staff member.
    for t_id in task_ids:
        if t_id not in assignments:
            violations.append(f"Task Assignment Error: Task '(t_id)' is completely unassigned.")
        else:
            assigned_emp_id = assignments[t_id]
            if assigned_emp_id not in employee_ids:
                violations.append(f"Task Assignment Error: Task '{t_id}' references non-existent employee '(assigned_emp_id)'.")
    if violations:
        return VerificationResult(passed=False, violations=violations)

    # Checks if employees are allowed, priced, and avaliable for their assigned task. 
    employees_accumulated_hours: Dict[str, float] = {e_id: 0.0 for e_id in employee_ids}
    employee_assigned_titles: Dict[str, List[str]] = {e_id: [] for e_id in employee_ids}
    for t_id, emp_id in assignments.items():
        task = task_map[t_id]
        employee = employee_map[emp_id]
        if task.title not in employee.authorization:
            violations.append(f"Cost Error: No processing cost data exists for Employee '{emp_id}' is assigned to task '{t_id}' ({task.title})) but is not authorized.")
        if (emp_id not in hourly_costs) or (t_id not in hourly_costs[emp_id]):
            violations.append(f"Cost Error: No processing cost data exists for Employee '{emp_id}' performing task '{t_id}'.")
        employees_accumulated_hours[emp_id] += task.estimated_duration_hours
        employee_assigned_titles[emp_id].append(task.title)
    for emp_id, total_hours in employees_accumulated_hours.items():
        employee = employee_map[emp_id]
        if total_hours > employee.availability_hours_per_week:
            violations.append(
                f"Availability Error: Employee '{emp_id}' is assigned {total_hours} hours, "
                f"exceeding their weekly capacity limit of {employee.availability_hours_per_week} hours."
            )

    # Ensures that conflicting financial duties are handled by separate employees.        
    segregation_pairs = [
        ("Investigation","Review"),
        ("Review","Approval"),
        ("Investigation", "Approval")
    ]
    for emp_id, assigned_titles in employee_assigned_titles.items():
        for title_a, title_b in segregation_pairs:
            if title_a in assigned_titles and title_b in assigned_titles:
                violations.append(
                    f"Separation of Duties Error: Employee '{emp_id}' cannot perform both '(title_a)' and '(title_b)' actions."
                )
    return VerificationResult(passed=len(violations) == 0, violations=violations)

if __name__ == "__main__":
    print("--- Running PhantomWork Verifier Self-Audit ---")
    with open("data/sample_scenario.json", "r") as file:
        data = json.load(file)
    scenario = SimulationData.model_validate(data)
    results = optimize_assignments(scenario)
    print("\nOptimization Run Finished.")
    print("Status:", results.status)
    print("Total Optimize Cost: $", results.total_cost)
    audit = verify_assignments(scenario, results.assignments)
    print("\n---Test 1: Verifying Optimized Results---")
    print("Verification Passed:", audit.passed)
    print("Violations Found:", len(audit.violations))
    print("Violations Found:", len(audit.violations))
    for violation in audit.violations:
        print(f" \u274c, {violation}")
    print("\n---Test 2: Auditing a Corrupted/Invalid Assignment Payload---")
    corrupted_assignments = results.assignments.copy()
    investigation_task_id = next((t.id for t in scenario.tasks if t.title == "Investigation"), None)
    review_task_id = next((t.id for t in scenario.tasks if t.title == "Review"), None)
    if investigation_task_id and review_task_id:
        bad_actor_emp_id = scenario.employees[0].id
        corrupted_assignments[investigation_task_id] = bad_actor_emp_id
        print(f"Simulating Rule Break: Forcing employee '{bad_actor_emp_id}' onto both '{investigation_task_id}' and '{review_task_id}'...")
        failed_audit = verify_assignments(scenario, corrupted_assignments)
        print("Verification Passed:", failed_audit.passed)
        print("Violations Found:", len(failed_audit.violations))
        for violation in failed_audit.violations:
            print(f" \u274c, {violation}")
