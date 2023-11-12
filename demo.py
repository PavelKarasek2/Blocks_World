from planning import Plan
from state import State

initial_state = State()
initial_state_blocks = initial_state.create_state_from_file(f"demo_initial.txt")

#display initial state
State.display(initial_state_blocks, message="Initial State")

# get the goal state
goal_state = State()
goal_state_blocks = goal_state.create_state_from_file(f"demo_goal.txt")

#display goal state
State.display(goal_state_blocks, message="Goal State")

p = Plan(initial_state_blocks, goal_state_blocks)
num_steps = p.execute_plan()