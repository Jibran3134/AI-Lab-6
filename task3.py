# task3_course_registration_agent.py

# ============================================================
# Task 3: University Course Registration Planning Agent
# ============================================================


# ------------------------------------------------------------
# 1. Goal Formulation
# ------------------------------------------------------------

initial_state = "Student Login"
goal_state = "Registration Completed"


# Each registration step has a processing cost of 1
step_cost = 1


# ------------------------------------------------------------
# 2. Problem Formulation
# ------------------------------------------------------------

# Registration workflow represented as an adjacency-list graph

registration_graph = {

    "Student Login": [
        "Authenticate Student"
    ],

    "Authenticate Student": [
        "Verify Prerequisites"
    ],

    "Verify Prerequisites": [
        "Select Courses"
    ],

    "Select Courses": [
        "Verify Fee Status"
    ],

    "Verify Fee Status": [
        "Confirm Enrollment"
    ],

    "Confirm Enrollment": [
        "Registration Completed"
    ],

    "Registration Completed": []
}


# ------------------------------------------------------------
# 3. Transition Model
# ------------------------------------------------------------

def transition_model(current_state, action):

    if action in registration_graph[current_state]:

        return action

    return None


# ------------------------------------------------------------
# 4. Goal Test
# ------------------------------------------------------------

def goal_test(state):

    return state == goal_state


# ------------------------------------------------------------
# 5. Generate Reachable State Space
# ------------------------------------------------------------

def generate_state_space(state, visited):

    # Mark current state as visited
    visited.add(state)

    # Visit connected states
    for next_state in registration_graph[state]:

        # Prevent revisiting states
        if next_state not in visited:

            generate_state_space(
                next_state,
                visited
            )


# ------------------------------------------------------------
# 6. Path Cost
# ------------------------------------------------------------

def calculate_path_cost(path):

    # Every registration step costs 1 unit
    return (len(path) - 1) * step_cost


# ------------------------------------------------------------
# 7. Planning Agent
# ------------------------------------------------------------

def find_plan(current_state, visited, path):

    # Mark current state as visited
    visited.add(current_state)

    # Add current state to the path
    path.append(current_state)

    # Check whether goal has been reached
    if goal_test(current_state):

        return True

    # Explore possible actions
    for action in registration_graph[current_state]:

        # Do not revisit completed steps
        if action not in visited:

            next_state = transition_model(
                current_state,
                action
            )

            if next_state is not None:

                if find_plan(
                    next_state,
                    visited,
                    path
                ):

                    return True

    # Remove state if it does not lead to the goal
    path.pop()

    return False


# ============================================================
# Display Results
# ============================================================

print("\n" + "=" * 60)
print("UNIVERSITY COURSE REGISTRATION PLANNING AGENT")
print("=" * 60)


# ------------------------------------------------------------
# Initial State
# ------------------------------------------------------------

print("\nInitial State:")
print(initial_state)


# ------------------------------------------------------------
# Goal State
# ------------------------------------------------------------

print("\nGoal State:")
print(goal_state)


# ------------------------------------------------------------
# State-Space Graph
# ------------------------------------------------------------

print("\nState-Space Graph:")

for state, neighbors in registration_graph.items():

    if neighbors:

        print(
            f"{state} -> {', '.join(neighbors)}"
        )

    else:

        print(
            f"{state} -> []"
        )


# ------------------------------------------------------------
# Generate Reachable States
# ------------------------------------------------------------

visited_states = set()

generate_state_space(
    initial_state,
    visited_states
)

print("\nReachable States:")

for state in visited_states:

    print("-", state)


# ------------------------------------------------------------
# Generate Planned Path
# ------------------------------------------------------------

visited = set()
planned_path = []

plan_found = find_plan(
    initial_state,
    visited,
    planned_path
)


# ------------------------------------------------------------
# Display Execution Sequence
# ------------------------------------------------------------

if plan_found:

    print("\nExecution Sequence:")

    for i, state in enumerate(
        planned_path,
        start=1
    ):

        print(
            f"{i}. {state}"
        )


    # --------------------------------------------------------
    # Display Path Cost
    # --------------------------------------------------------

    total_cost = calculate_path_cost(
        planned_path
    )

    print(
        f"\nTotal Path Cost: "
        f"{total_cost} units"
    )

else:

    print("\nNo valid registration plan found.")