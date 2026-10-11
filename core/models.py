from pydantic import BaseModel, Field, model_validator, ValidationError
import json

# Define the data structures representing financial workflow.
class Employee(BaseModel):
    id: str
    name: str
    qualifications: list[str]
    authorization: list[str]
    availability_hours_per_week: int = Field(ge=0)
class Task(BaseModel):
    id: str
    title: str
    description: str
    estimated_duration_hours: float = Field(gt=0)
    prerequisites: list[str]
class CorporateRules(BaseModel):
    rule_id: str
    title: str
    description: str
    type: str
    task_ids: list[str] = Field(default_factory=list)
class BaselineAssignment(BaseModel):
    task_id: str
    assigned_employee_id: str
class Baseline(BaseModel):
    description: str
    assignments: list[BaselineAssignment] 

# Groups all preexiating workflow information into a one scenario for program analysis. 
class SimulationData(BaseModel):
    workflow_title: str
    employees: list[Employee]
    tasks: list[Task]
    processing_costs_per_hour: dict[str, dict[str, float]] 
    corporate_rules: list[CorporateRules]
    baseline_assignments: Baseline

    # Checks if employee and task IDs exist and if employees are authorized for assigned tasks listed in processing costs.
    @model_validator(mode='after')
    def cross_reference_validate(self) -> 'SimulationData':

        # Creates an internal search engine for the program to quickly find employee information (name, qualifications, authorization, avaliability) and task information (title, duration, prerequisites).
        task_ids = {t.id for t in self.tasks}
        task_map = {t.id: t for t in self.tasks}
        employee_map = {e.id: e for e in self.employees}

        # Verifies that the employee and the authorized role exist and that employees are authorized to perform these tasks.
        for employee_id, task_costs in self.processing_costs_per_hour.items():
            if employee_id not in employee_map:
                raise ValueError(f"Processing cost references a non-existent employee: '{employee_id}'")
            emp = employee_map[employee_id]
            for task_id, hourly_rate in task_costs.items():
                if task_id not in task_ids:
                    raise ValueError(f"Processing cost references a non-existent task: '{task_id}'")
                task = task_map[task_id]
                if task.title not in emp.authorization:
                    raise ValueError(f"Employee '{employee_id}' is not authorized for task '{task_id}'")
        
        # Verifies that the original workflow plan assigns tasks to employees that exist in the company's disclosed data.
        for assignment in self.baseline_assignments.assignments:
            task_id = assignment.task_id
            employee_assignment = assignment.assigned_employee_id
            if task_id not in task_ids:
                raise ValueError (f"Baseline assignment references a non-existent task: '{task_id}'")
            if employee_assignment not in employee_map:
                raise ValueError (f"Baseline assignment references a nonexistent employee: '{employee_assignment}'")
        return self

# Loads and validates JSON scenario and prints summary to confrim the data is ready for use.
if __name__ == "__main__":
    with open("data/sample_scenario.json", "r") as file:
        data = json.load(file)
    scenario = SimulationData.model_validate(data)
    print("Scenario validated succesfully!")
    print(f"Employees:{len(scenario.employees)}")
    print(f"Tasks: {len(scenario.tasks)}")