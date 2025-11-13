# 🚀 Project Overview: My RLC State-Space Simulation
After spending time in circuit theory, I decided to use State-Space analyzing method on a very simple and cool circuit: a RLC series.
The project has three parts: Modeling, Simulation, and Plotter.
# 🧠 Modeling Philosophy: Future from Current Variables
State-Space analyze works like this: in the circuit, we can write a simple equation: d/dt(x) = Ax + Bu.
 * State Vector x : This vector contains the capacitor voltages (v_C) and self-inductance currents (i_L). Basically, it says that the future state of the circuit could be found from these current variables. Finding the future of the whole circuit with just these variables is the goal.
 * A-Matrix: This matrix holds the R, L, and C values. The Eigenvalues of A are the roots of the characteristic equation—they tell us exactly how the damping works.
 * Input (u): This is the input signal.
So, we form this equation and then try to solve it with numerical methods by SciPy.
# 💻 Code Structure
 * Modeling: Classes calculate the parameters that we need (natural frequencies, alpha frequency, state space matrices), and the Eigenvalues.
 * Simulation: We have the methods and functions for the numerical solving.
 * Plotter: Provides visualization, including the critical S-Plane visualization—which connects the roots directly to the physical damping behavior.
Couldn't explain it better. Take a look at the code. (Hope it helps :)))
Also, this code had edits by Gemini (it was so messy).
Thanks for taking your time (I hope at least someone reads it :))))))))
