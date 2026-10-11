import json
import streamlit as st
from core.models import SimulationData
from core.optimizer import optimize_assignments
from core.verifier import verify_assignments
st.set_page_config(page_title="PhantomWork Dashboard", layout="wide")
st.title("PhantomWork")
st.subheader("The Self-Auditing Financial Shadow Operations Engine")
st.markdown("---")

# Loads and validates company's financial workflow before processing.
try:
    with open("data/sample_scenario.json", "r") as file:
        data = json.load(file)
    scenario = SimulationData.model_validate(data)
    st.sidebar.success("sample_scenario.json Loaded & Validated")
except Exception as e:
    st.sidebar.error(f"Structural Validation Failed: {e}")
    st.stop()
opt_result = optimize_assignments(scenario)
audit_result = verify_assignments(scenario, opt_result.assignments)

# Calculates original cost, compares it with optimized costs to calculate monetary savings (percentage and dollar amounts).
baseline_cost = 0.0
task_map = {t.id: t for t in scenario.tasks}
hourly_costs = scenario.processing_costs_per_hour
for assignment in scenario.baseline_assignments.assignments:
    t_id = assignment.task_id
    e_id = assignment.assigned_employee_id
    if e_id in hourly_costs and t_id in hourly_costs[e_id]:
        duration = task_map[t_id].estimated_duration_hours
        baseline_cost += hourly_costs[e_id][t_id] * duration
optimized_cost = opt_result.total_cost
dollar_savings = baseline_cost - optimized_cost
percentage_savings = (dollar_savings/baseline_cost) * 100 if baseline_cost > 0 else 0
col1,col2,col3 = st.columns(3)
with col1:
    st.metric(label="Original Baseline Cost", value=f"${baseline_cost:,.2f}")
with col2:
    st.metric(label="Optimized Path Cost", value=f"${optimized_cost:,.2f}", delta=f"${dollar_savings:,.2f} Cost Reduction")
with col3:
    st.metric(label="Calculated Net Efficiency Savings", value=f"{percentage_savings:,.1f}%")
st.markdown("## Employee Operational Assignments")

# Displays how employee assignments alter between the original and optimized workflows.
comparison_table = []
baseline_lookup = {a.task_id: a.assigned_employee_id for a in scenario.baseline_assignments.assignments}
employee_map = {e.id: e.name for e in scenario.employees}

for t in scenario.tasks:
    original_emp_id = baseline_lookup.get(t.id, "Unassigned")
    optimized_emp_id = opt_result.assignments.get(t.id, "Unassigned")
    original_name = employee_map.get(original_emp_id, original_emp_id)
    optimized_name = employee_map.get(optimized_emp_id, optimized_emp_id)
    status_change = "Reassigned" if original_emp_id != optimized_emp_id else "Kept Baseline"
    comparison_table.append({
        "Task title": t.title,
        "Original Allocation": original_name,
        "Optimized Allocation": optimized_name,
        "Operational Action": status_change
    })
st.table(comparison_table)
st.markdown("### Independent System Compliance Audit")
if audit_result.passed:
    st.success("COMPLIANCE STATUS PASSED (0 Violations Detected)")
    st.info("The proposed optimized assignment complies with all known corporate constraints")
else:
    st.error(f"COMPLIANCE STATUS: FAILED ({len(audit_result.violations)} Violations Flagged)")
    for violation in audit_result.violations:
        st.markdown(f"\u274c {violation}")

