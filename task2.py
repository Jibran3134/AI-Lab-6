# task2_airport_agent.py

# ============================================================
# Task 2: Smart Airport Check-in Planning Agent
# ============================================================


# ------------------------------------------------------------
# 1. Goal Formulation
# ------------------------------------------------------------

initial_state = "Airport Entrance"
goal_state = "Boarded"


# Processing time for each checkpoint
processing_time = {
    "Airport Entrance": 0,
    "Verify Identity": 5,
    "Check-in Baggage": 10,
    "Pass Security Screening": 15,
    "Complete Immigration": 20,
    "Reach Boarding Gate": 5,
    "Boarded": 0
}


# ------------------------------------------------------------
# 2. Problem Formulation
# ------------------------------------------------------------

# Airport checkpoints represented using an adjacency-list graph

airport_graph = {

    "Airport Entrance": [
        "Verify Identity"
    ],

    "Verify Identity": [
        "Check-in Baggage"
    ],

    "Check-in Baggage": [
        "Pass Security Screening"
    ],

    "Pass Security Screening": [
        "Complete Immigration",
        "Reach Boarding Gate"
    ],

    "Complete Immigration": [
        "Reach Boarding Gate"
    ],

    "Reach Boarding Gate": [
        "Boarded"
    ],

    "Boarded": []
}


# ------------------------------------------------------------
# 3. Transition Model
# ------------------------------------------------------------

def transition_model(current_state, action):

    if action in airport_graph[current_state]:
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
    for next_state in airport_graph[state]:

        if next_state not in visited:

            generate_state_space(
                next_state,
                visited
            )


# ------------------------------------------------------------
# 6. Path Cost
# ------------------------------------------------------------

def calculate_path_cost(path):

    total_cost = 0

    for state in path:

        total_cost += processing_time[state]

    return total_cost


# ------------------------------------------------------------
# 7. Planning Agent
# ------------------------------------------------------------

def find_plan(current_state, visited, path):

    # Mark current state as visited
    visited.add(current_state)

    # Add current state to path
    path.append(current_state)

    # Goal Test
    if goal_test(current_state):

        return True

    # Explore possible actions
    for action in airport_graph[current_state]:

        # Do not revisit completed checkpoints
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

    # If this path does not lead to the goal,
    # remove the state from the current path
    path.pop()

    return False


# ============================================================
# Display Results
# ============================================================

print("\n" + "=" * 60)
print("SMART AIRPORT CHECK-IN PLANNING AGENT")
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

for state, neighbors in airport_graph.items():

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
# Display Final Plan
# ------------------------------------------------------------

if plan_found:

    print("\nPlanned Checkpoint Sequence:")

    for i, checkpoint in enumerate(
        planned_path,
        start=1
    ):

        print(
            f"{i}. {checkpoint}"
        )


    # Calculate total processing time
    total_time = calculate_path_cost(
        planned_path
    )

    print(
        f"\nTotal Processing Time: "
        f"{total_time} minutes"
    )

else:

    print("\nNo valid plan found.")