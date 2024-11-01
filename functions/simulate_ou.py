import numpy as np
from numpy import exp

def simulate_ou(x0, mu, theta, sigma, dt, n):
  '''
  Simulate an ornstein uhlenbec process. dXt = μ*(θ − Xt)dt + σ*dBt 
  x0: initial value
  mu: mean reversion rate
  theta: long-term mean
  sigma: volatility
  dt: time difference
  n: number of data points
  Output: an OU time series
  '''
  x = np.zeros(n)
  x[0] = x0
  exp_minus_mu_deltat = exp(- mu * dt) 
  # Calculate the random term. 
  if mu == 0:
    # Handle the case of mu = 0 i.e. no mean reversion. 
    dWt = np.sqrt(dt) * np.random.randn(n)
  else:
    dWt = np.sqrt((1 - exp(-2*mu*dt))/(2 * mu)) * np.random.randn(n)
  # And iterate through time calculating each price. 
  for t in range(n)[1:]:   
    x[t] = x[t-1] * exp_minus_mu_deltat + theta * (1 - exp_minus_mu_deltat) + sigma * dWt[t]
  return x