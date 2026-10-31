import numpy as np
from dataclasses import dataclass

def takeoff():

    return None

def climb():

    return None

def cruise():

    return None

def landing():

    return None

@dataclass
class Performance:
    
    model: str
    coefficients: dict

    def evalute(self, x):

        model = self.model

        # Map regressors
        x = np.array(self.x)

        # Map the regression coefficients
        b = np.array(self.coefficients)

        # Map the error term
        err = 0.0

        # Solve for the regressand
        y = x*b.T + err

        # 
        match model:
            case "linear":
                y = y
            case "log-linear":
                y = 10^y
            case _:
                raise ValueError("Model is undefined.")

        return y