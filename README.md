# PhantomWork
### The Self Auditing Financial Shadow
**Policy-Restricted Financial Workflow Optimization Simulation**
PhantomWork is a financial operations simulator tasked with optimizing employee assignments, verify internal corporate authorization, and reassess workflows in the case of operation disruption.
Users input financial tasks, staff credentials, processing costs, and corporate guidelines. Phantomwork assesses possible assignments, produces cost comparisons, confirms guideline adherence, ane suggests recovery alternatives.

## The Conflict
Financial institutions must balance **operational efficiency, employee authorixation, and internal controls**.
A cost efficient employee assignment is not always effective.  
For example:
- An employee may lack the credentials to approve a transaction.
- The same employee may be restricted from investigating and approving a transaction.
- A required reviewer may become unavailable during a prominent work period.
- Additional approvals may increase processing costs.
As these obstacles and constraints accumulate, finding an efficient and valid assignment becomes progressively more difficult
**PhantomWork explores these challenges without modifying real financial systems.**

## What PhantomWork Does
### 1. User-Defined Inputs
Users define:
- **Financial tasks:** Investigation, review, approval, and reconciliatory affairs.
- **Staff credentials:** Employee qualifications, authorization, and avaliability.
- **Processing costs:** The cost of assigning specific employees to specific tasks.
- **Corporate guidelines:** Executive approval requirements and separation-of-duties rules.
- **Operational disruptions:** Changes to staffing, costs, and/or approval requirements.
### 2. Workflow Optimization
PhantomWork searches for lowest-cost employee-task assignments that satisfy constraints defined by the user.
The optimizer considers:
- Employee credentials
- Employee avaliability
- Assignment costs
- Approval requirements
- Separation of duties
### 3. Independent Verification
A separate verification component checks whether proposed assignments satisfy the corporate rules defined by the user
This helps distinguish a **low-cost assignment** from **a effective low cost assignment**.
### 4. Disruption Simulation
Users can modify operating conditions such as:
- Making a reviewer unavaliable
- Revoking an employee's authorization for approvals
- Requiring an additional approval
- Increasing an employee's processing cost
PhantomWork recalculates assignments under the new conditions.
If no valid assignments can be established, the system reports that limitation rather than bypassing required controls.

## What PhantomWork Outputs
- **Optimized assignments:** Which employee should perform which task.
- **Workflow costs:** Total processing cost under the proposed assignment.
- **Estimated savings:"** Cost differences relative to the user defined baseline
- **Recovery alternatives:** Revised assignments after user defined disruptions
- **Feasibility results:** Confirmation of whether the updated workflow can satisfy its requirements

## Example Scenario
A financial operations team must investigate, review and approve a reconciliation exception.
The company's internal policies require:
- Qualified employees for each task
- Authorized employees for approvals
- Separation-of-duties between the investigation and approvals
PhantomWork searches for a cost-efficient valid assignment.
If a reviewer becomes unavailable, the system recalculates the assignment and evaluates whether workflow can continue within the same parameters.
**The goal is not simply to minimize cost, but rather to minimize costs without violating user defined restrictions.**

## Technical Approach
PhantomWork individually assesses optimization and verification.
**Optimization engine**
Searches for employee-task assignments that minimize processing costs while satisfying explicit constraints.
**Independent verifier**
Checks the resulting assignments against staff qualifications, authorizations, and approval requirements.
**Disruption evaluator**
Recalculates assignments when the user changes operation conditions.
A workflow is considered *optimal* only when solver establishes optimality within the modeled restrictions set by them.

## Technology Stack
|Technology|Purpose|
|Python|Core application logic|
|Streamlit|Interactive user interface|
|Google OR-Tools|Constraint-based optimization|
|Pydantic|Structured data validation|
|pytest|Automated testing|
|Hugging Face|AI-assisted policy and interpretation, if implemented|

## Installation and Usage 
### Requirements
- Python 3.10 or newer
- Streamlit
- Google OR-Tools
- Pydantic

### Running PhantomWork
1. Download or clone the Github Repository
2. Open the PhantomWork project folder in terminal
3. Insteall the following required dependecies:
'''bash
python -m pip install streamlit ortolls pydantic
4. Launch the dashboard
'''bash
python -m streamlit run app.py
'''
5. Open the local URL provided by Streamlit.

### Using the Dashboard
1. PhantomWork automatically loads and validates the included sample financial workflow.
2. Review the original workflow costs, optimized costs, and estimated savings.
3. Examine the employee assignment comparison and indepedent assignment audit.
4. Select an employee in the Disruption Simulator
5. Click **Simulate Employee Disruption** to generate replacement assignments.
6. Review the updated costs, audit results, and employee reassignment report.

## Optimization Results
| Metric | Result |
|---|---:|
| Original Workflow Cost | $3,300 |
| Optimized Workflow Cost | $2,725 |
| Estimated Savings | $575 |
| Cost Reduction | 17.4% |

## Disruption Simulation Results
| Simulated Disruption | Reoptimized Cost | Additional Cost | Assignment Audit |
|---|---|--:|---|
| Peter Parker Unavailable | $3,175 | +$450 | Passed |
| Barry Allen Unavailable | $3,075 | +$350 | Passed |

The disruption simulator temporarily removes an employee's availability and recalculates task assignments under the implemented constraints.

The dashboard displays the financial impact of the disruption, indepedently checks whether the new assignments follow implemented workplace rules, and compares employee assignments before and after the simulation.



## Demo
*Demo video, application screenshots, demonstration link will be added here.*

## Scope and Limitations
PhantomWork is a prototype built around user-supplied financial workflow data.
- It does not connect to real bank accounts or production financial systems.
- It checks compliance in accordance to user inputted modeled corporate policy, not legal or general regulatory compliance.
- Estimated savings depend on supplied costs and baseline.
- Optimization results only to constraints represented in the model.
- Occasional disruptions may make workflow infeasible within corporate parameters.
## Built For
**Knight Hacks IX-2026**
A hackathon project exploring financial operations, constrained optimization, internal controls, and operational resilience.

## License
This project is Licensed under the MIT License. See the LICENSE file for details.
