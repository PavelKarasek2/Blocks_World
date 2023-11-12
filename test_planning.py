from planning import Plan
from state import State

f =  open("/home/user/Documents/St.Olaf/Csci379/karase1/project_01/num_steps.csv","w")
f.write("init_goal,num_steps, Initial, Goal\n")

num_steps_total = 0
for i in range(1,11):
    for g in range(1,11):
        if g==i:
            continue
        print(f"\n\n\n\n\n\n\n\n\n\nTESTING INITIAL STATE {i} AND GOAL STATE {g}\n\n")
        # get the initial state
        initial_state = State()
        initial_state_blocks = initial_state.create_state_from_file(f"test_states/state_{i}.txt")

        #display initial state
        State.display(initial_state_blocks, message="Initial State")

        # get the goal state
        goal_state = State()
        goal_state_blocks = goal_state.create_state_from_file(f"test_states/state_{g}.txt")

        #display goal state
        State.display(goal_state_blocks, message="Goal State")

        p = Plan(initial_state_blocks, goal_state_blocks)
        num_steps = p.execute_plan()
        num_steps_total += num_steps
        f.write(f"I{i}_G{g},{num_steps}, {i}, {g}\n")

avg_num_steps = num_steps_total/90
print(f"\n\n\n\n\nTHE AVERAGE NUMBER OF STEPS: {avg_num_steps}")