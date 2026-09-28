import heapq
import math

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

st.set_page_config(page_title="Hospital Robot Search", layout="wide")
st.title("Emergency Supply Robot Search")
st.write("Compare Greedy Best-First Search and A* on the hospital corridor graph.")

locations = {
    "Pharmacy": (0, 0), "Main_Corridor": (2, 1), "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2), "Laboratory": (5, 5), "Emergency_Ward": (8, 6)
}
hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Emergency_Ward": 5.0, "Laboratory": 3.2},
    "Laboratory": {"Emergency_Ward": 3.6},
    "Emergency_Ward": {}
}

def heuristic(node, goal):
    return math.dist(locations[node], locations[goal])

def search(start, goal, algorithm):
    frontier = [(heuristic(start, goal), 0, start)]
    came_from = {start: None}
    costs = {start: 0}
    visited = set()
    order = []
    while frontier:
        _, queued_cost, current = heapq.heappop(frontier)
        if current in visited or (algorithm == "A*" and queued_cost != costs[current]):
            continue
        visited.add(current)
        order.append(current)
        if current == goal:
            break
        for neighbor, edge_cost in hospital_graph[current].items():
            new_cost = costs[current] + edge_cost
            if neighbor not in visited and (algorithm == "GBFS" or new_cost < costs.get(neighbor, math.inf)):
                if algorithm == "GBFS":
                    came_from.setdefault(neighbor, current)
                    costs.setdefault(neighbor, new_cost)
                    priority, queued = heuristic(neighbor, goal), new_cost
                else:
                    came_from[neighbor] = current
                    costs[neighbor] = new_cost
                    priority, queued = new_cost + heuristic(neighbor, goal), new_cost
                heapq.heappush(frontier, (priority, queued, neighbor))
    if goal not in visited:
        return order, None, None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    cost = sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))
    return order, path, cost

nodes = list(locations)
left, right = st.columns(2)
start = left.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
goal = right.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])
if st.button("Run Search", type="primary"):
    expansion_order, path, cost = search(start, goal, algorithm)
    if path is None:
        st.error("No path was found between the selected locations.")
    else:
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Expansion order:** {' → '.join(expansion_order)}")
        st.write(f"**Solution path:** {' → '.join(path)}")
        st.write(f"**Total path cost:** {cost:.2f}")
        G = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        fig, ax = plt.subplots(figsize=(10, 6))
        nx.draw_networkx_nodes(G, locations, node_size=2400, node_color="lightblue", ax=ax)
        nx.draw_networkx_edges(G, locations, arrows=True, arrowsize=20, ax=ax)
        nx.draw_networkx_labels(G, locations, font_size=8, ax=ax)
        nx.draw_networkx_edge_labels(G, locations, edge_labels=nx.get_edge_attributes(G, "weight"), ax=ax)
        nx.draw_networkx_edges(G, locations, edgelist=list(zip(path, path[1:])), edge_color="red", width=3, arrows=True, arrowsize=20, ax=ax)
        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")
        st.pyplot(fig)

