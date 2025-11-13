import numpy as np
import matplotlib.pyplot as plt

# Import Classes from user-specified file names
from modeling import RLCParameters, StateSpaceModel, EigenvalueAnalyzer
from simulation import InputSignal, RLCSolver 
from systemPlotter import SystemPlotter, SPlaneVisualizer


# --- 1. Define Scenario (Underdamped Case) ---
R_val, L_val, C_val = 1.0, 1.0, 0.1 # R=1.0, L=1.0, C=0.1 --> Underdamped (α=0.5, ω₀≈3.16)
V_input = 10.0
T_end = 5.0
time_points = np.linspace(0, T_end, 500)
initial_state = np.array([0.0, 0.0]) # Start with zero stored energy (ZSR test)

print("--- RLC System Simulation Started ---")
print(f"Parameters: R={R_val}Ω, L={L_val}H, C={C_val}F")

# 2. Modeling and Analysis (Layer 1)
params = RLCParameters(C=C_val, L=L_val, R=R_val)
model = StateSpaceModel(params)
analyzer = EigenvalueAnalyzer(model.A_matrix)
damping_type = analyzer.analyze_damping_type()

print("\n--- Analysis Results ---")
print(f"Damping Type: {damping_type}")
print(f"Eigenvalues (λ): {analyzer.eigenvalues}")


# 3. Simulation (Layer 2)
input_sig = InputSignal(signal_type='step', amplitude=V_input)
solver = RLCSolver(model=model, vC_0=initial_state[0], iL_0=initial_state[1], 
                   t_start=0, t_end=T_end, num_points=500)

try:
    solver.run_simulation(input_sig)
    time, vC_t, iL_t = solver.get_time_series()
    solution_matrix = np.vstack((vC_t, iL_t)).T 
    
    # Console Check
    print("\n--- Numerical Check ---")
    print(f"Final Voltage (Expected {V_input}V): {solution_matrix[-1, 0]:.3f} V")
    print(f"Max Voltage (Overshoot): {np.max(solution_matrix[:, 0]):.3f} V")

    # 4. Visualization (Layer 3)
    plotter = SystemPlotter()
    s_plane_viz = SPlaneVisualizer()

    # Plot 1: Time Response
    plotter.plot_time_response(time, solution_matrix, title=f"Time Response: {damping_type} (Step Input)")
    
    # Plot 2: Energy Analysis
    plotter.plot_energy_exchange(time, solution_matrix, R_val, L_val, C_val, title="Energy Exchange & Dissipation")
    
    # Plot 3: S-Plane Analysis
    s_plane_viz.plot_eigenvalues(analyzer.eigenvalues, damping_type)
    
except RuntimeError as e:
    print(f"\nSimulation Error: {e}")

print("\n--- RLC System Simulation Finished ---")