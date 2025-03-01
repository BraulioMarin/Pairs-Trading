import numpy as np

class KalmanFilterHedgeRatio:
    def __init__(self, q=0.01, r=0.01):
        
        self.x = np.array([1.0, 0.0])  
        self.A = np.eye(2)  
        self.Q = np.eye(2) * q  
        self.R = np.array([[r]]) 
        self.P = np.eye(2) * 10  

    def predict(self):
        
        self.x = self.A @ self.x  
        self.P = self.A @ self.P @ self.A.T + self.Q  

    def update(self, x, y):
        
        C = np.array([[1, x]])  
        S = C @ self.P @ C.T + self.R  
        K = self.P @ C.T @ np.linalg.inv(S)  
        
        self.x = self.x + K @ (y - C @ self.x)  
        self.P = (np.eye(2) - K @ C) @ self.P  

    def get_hedge_ratio(self):
        
        return self.x[1]