import numpy as np

class RLCParameters:
    def __init__(self, C, L, R):
        self.c = C
        self.l = L
        self.r = R
    
    def natural_freq(self):
        return np.sqrt(1 / (self.l * self.c))
    
    def alpha_freq(self):
        return self.r / (2 * self.l)

class StateSpaceModel:
    def __init__(self, params: RLCParameters):
        self.parameters = params
        self.A_matrix = None
        self.B_vector = None
        self.build_matrix()
    
    def build_matrix(self):
        # A = [[0, 1/C], [-1/L, -R/L]]
        self.A_matrix = np.array([[0, 1 / self.parameters.c],
                                [-1 / self.parameters.l, -self.parameters.r / self.parameters.l]])
        # B is a column vector [0, -1/L]
        self.B_vector = np.array([[0], [-1 / self.parameters.l]]) 

class EigenvalueAnalyzer:
    def __init__(self, A_matrix):
        self.A_matrix = A_matrix
        self.eigenvalues = None 
        self.eigenvectors = None
        self.claculate_eigenvalues()

    def claculate_eigenvalues(self):
        lambdas, vectors = np.linalg.eig(self.A_matrix)
        self.eigenvalues = lambdas
        self.eigenvectors = vectors
        
        return self.eigenvalues
    
    def analyze_damping_type(self):
        if self.eigenvalues is None:
            return "Analysis not performed"
            
        lambda1 = self.eigenvalues[0]
        lambda2 = self.eigenvalues[1]

        if not np.isclose(lambda1.imag, 0.0) or not np.isclose(lambda2.imag, 0.0):
            return "Underdamped"
            
        # Check if real parts are close (Critically Damped)
        if np.isclose(lambda1.real, lambda2.real):
            return "Critically Damped"
        else:
            return "Overdamped"