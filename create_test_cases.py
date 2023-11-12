# List of initial states
first_half = "square(A)\nsquare(B)\nsquare(C)\nsquare(D)\nsquare(E)\n\n"

states = [
    "on(A, table)\non(B, table)\non(E, table)\non(C, A)\non(D, table)",
    "on(A, table)\non(B, A)\non(E, C)\non(C, B)\non(D, E)",
    "on(A, table)\non(B, C)\non(C, A)\non(D, table)\non(E, B)",
    "on(A, B)\non(B, table)\non(C, table)\non(D, E)\non(E, table)",
    "on(A, C)\non(B, table)\non(C, D)\non(D, table)\non(E, table)",
    "on(A, table)\non(B, A)\non(C, B)\non(D, table)\non(E, C)",
    "on(A, B)\non(B, table)\non(C, A)\non(D, E)\non(E, table)",
    "on(A, B)\non(B, table)\non(C, D)\non(D, table)\non(E, C)",
    "on(A, C)\non(B, A)\non(C, table)\non(D, table)\non(E, B)",
    "on(A, B)\non(B, C)\non(C, D)\non(D, E)\non(E, table)"
]

# Create and write to the files
for i, state in enumerate(states, start=1):
    filename = f"test_states/state_{i}.txt"
    with open(filename, "w") as file:
        file.write(first_half)
        file.write(state)
        print(f"Created {filename}")

print("Files created successfully.")
