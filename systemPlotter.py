import numpy as np
import matplotlib.pyplot as plt

class SystemPlotter:
    def plot_time_response(self, time: np.ndarray, solution: np.ndarray, title: str = "RLC Series Circuit Time Response"):
        vC_t = solution[:, 0]
        iL_t = solution[:, 1]
        
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Time (t) [s]', fontsize=12)
        ax1.set_ylabel('Inductor Current (iL) [A]', color=color, fontsize=12)
        ax1.plot(time, iL_t, color=color, label='Inductor Current (iL)')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, linestyle='--', alpha=0.7)

        ax2 = ax1.twinx()  
        color = 'tab:red'
        ax2.set_ylabel('Capacitor Voltage (vC) [V]', color=color, fontsize=12) 
        ax2.plot(time, vC_t, color=color, label='Capacitor Voltage (vC)')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title(title, fontsize=14, fontweight='bold')
        fig.tight_layout() 
        plt.show()

    def plot_energy_exchange(self, time: np.ndarray, solution: np.ndarray, R: float, L: float, C: float, title: str = "Energy Exchange and Dissipation Analysis"):
        vC_t = solution[:, 0]
        iL_t = solution[:, 1]
        
        E_L = 0.5 * L * iL_t**2
        E_C = 0.5 * C * vC_t**2
        
        plt.figure(figsize=(10, 6))
        plt.plot(time, E_L, label=f'Inductor Energy (E_L)', linestyle='-')
        plt.plot(time, E_C, label=f'Capacitor Energy (E_C)', linestyle='-')
        plt.plot(time, E_L + E_C, label='Total Stored Energy', linestyle='--', color='black')

        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Time (t) [s]', fontsize=12)
        plt.ylabel('Energy [Joules]', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.show()

class SPlaneVisualizer:
    def plot_eigenvalues(self, eigenvalues: np.ndarray, damping_type: str):
        real_parts = np.real(eigenvalues)
        imag_parts = np.imag(eigenvalues)
        
        plt.figure(figsize=(8, 8))
        
        plt.axhline(0, color='black', linestyle='-', linewidth=0.8)
        plt.axvline(0, color='black', linestyle='-', linewidth=0.8)
        
        plt.axvspan(np.min(real_parts) - 1, 0, color='green', alpha=0.1, label='Stable Region')

        plt.scatter(real_parts, imag_parts, color='red', marker='x', s=150, linewidths=2, label='Eigenvalues (λ)')
        
        for i, (r, j) in enumerate(zip(real_parts, imag_parts)):
            label = f'λ{i+1} = {r:.2f}' 
            if j != 0:
                sign = '+' if j > 0 else ''
                label += f' {sign}{j:.2f}j'
            plt.annotate(label, (r, j), textcoords="offset points", xytext=(5, 5), fontsize=10)
        
        plt.title(f'Root Locations on S-Plane ({damping_type})', fontsize=14, fontweight='bold')
        plt.xlabel('Real Part (σ) - Damping Rate', fontsize=12)
        plt.ylabel('Imaginary Part (jω) - Oscillation Frequency', fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        plt.axis('equal')
        plt.show()