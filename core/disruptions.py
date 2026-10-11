import json
import copy
from typing import Tuple
from core.models import SimulationData
from core.optimizer import optimize_assignments, OptimizationResult
def simulate_employee_disruption(dataset: SimulationData, unavailable_employee_id: str)   ->   Tuple[OptimizationResult, SimulationData]:
    """
    Simulates a temporary workplace disruption by dropping an employee's availability to 0.
    Returns the new optimization results alongside the modified scenario model.
    """

    # Copies original scenario so disruptions do not modify company data
    modified_scenario = copy.deepcopy(dataset)
    employee_found = False
    for employee in modified_scenario.employees:
        if employee.id == unavailable_employee_id:
            employee.availability_hours_per_week = 0
            employee_found = True
            break
    if not employee_found:
        raise ValueError(f"Employee '{unavailable_employee_id}' does not exist.")
    
    # Recalculates the cheapest workflow alternative after an employee becomes unavailable.
    new_optimization_result = optimize_assignments(modified_scenario)
    return new_optimization_result, modified_scenario
if __name__ == "__main__":
    print("---Running PhantomWork Disruption Simulator Test Run---")
    with open("data/sample_scenario.json", "r") as file:
        data = json.load(file)
    original_scenario = SimulationData.model_validate(data)
    target_disruption_id = "EMPLOY_001"
    print(f"Simulating complete sudden unavailability for an employee: '{target_disruption_id}'...")
    new_results, altered_scenario = simulate_employee_disruption(original_scenario, target_disruption_id)
    print("\n--- Disruption Re-optimization Output Report ---")
    print(f"Solver Outcome Status: {new_results.status}")
    if new_results.status in ["OPTIMAL", "FEASIBLE"]:
        print(f"Recalculated System Cost: ${new_results.total_cost:.2f}")
        print(f"New Work Allocation Plan: {new_results.assignments}")
    else:
        print("CRITICAL SAFEGUARD TRIGGERED: The workflow system has been rendered INFEASIBLE!")
        print("PhantomWork confirms that no compliant, rule-abiding operational plan can be solved without this employee.")
    target_worker_original = next(e for e in original_scenario.employees if e.id == target_disruption_id)
    print(f"\nIntegrity Check = Original scenario tracking capacity hours remain: {target_worker_original.availability_hours_per_week} hours.")



