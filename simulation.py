import numpy as np
from scipy.integrate import solve_ivp
from modeling import StateSpaceModel 

class InputSignal:
    def __init__(self, signal_type: str, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0):
        self.signal_type = signal_type.lower()
        self.amplitude = amplitude
        self.omega = 2 * np.pi * frequency
        self.phase = phase

        if self.signal_type not in ['step', 'sinusoidal', 'zero']:
            raise ValueError(f"'{signal_type}' not supported.")

    def get_input(self, t: float) -> float:
        if self.signal_type == 'zero':
            return 0.0
        elif self.signal_type == 'step':
            if t >= 0:
                return self.amplitude
            else:
                return 0.0
        elif self.signal_type == 'sinusoidal':
            return self.amplitude * np.sin(self.omega * t + self.phase)
        else:
            return 0.0

    def str(self):
        if self.signal_type == 'zero':
            return "Zero Input"
        elif self.signal_type == 'step':
            return f"Step Response, Amplitude {self.amplitude} V"
        elif self.signal_type == 'sinusoidal':
            return f"Sinusoidal Response, Amplitude {self.amplitude} V, Frequency {self.omega / (2 * np.pi):.2f} Hz"
        else:
            return "Unknown Signal"

def rateFunction(t, x, A_matrix, B_vector, input_func):
    """ Calculates x' = Ax + Bu """
    u = input_func(t) 
    Ax = A_matrix @ x
    Bu = B_vector[:, 0] * u 
    x_prime = Ax + Bu
    return x_prime

class RLCSolver:
    def __init__(self, model: StateSpaceModel, vC_0, iL_0, t_start, t_end, num_points):
        self.A = model.A_matrix
        self.B = model.B_vector
        self.initial_state = np.array([vC_0, iL_0])
        self.t_span = [t_start, t_end]
        self.time_points = np.linspace(t_start, t_end, num_points)
        self.input_signal = None
        self.solution = None

    def run_simulation(self, input_signal_obj: InputSignal):
        self.input_signal = input_signal_obj
        args = (self.A, self.B, self.input_signal.get_input)

        self.solution = solve_ivp(
            fun=rateFunction,            
            t_span=self.t_span,           
            y0=self.initial_state,        
            t_eval=self.time_points,      
            args=args,                    
            method='RK45'
        )

        if not self.solution.success:
            raise RuntimeError("Numerical solve failed: " + self.solution.message)
            
        return self.solution
    
    def get_time_series(self):
        if self.solution is None or not self.solution.success:
            return None, None, None
            
        time = self.solution.t
        vC_t = self.solution.y[0, :] 
        iL_t = self.solution.y[1, :] 
        

        return time, vC_t, iL_t
