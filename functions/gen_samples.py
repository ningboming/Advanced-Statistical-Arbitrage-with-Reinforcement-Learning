import numpy as np

def gen_ou(m, x0, mu, theta, sigma, T, n):
  '''
  The function generates an ornstein uhlenbec process. dXt = μ*(θ−Xt)dt + σ*dBt 
  Input:
    m = sample size
    x0: initial value
    mu: mean reversion rate
    theta: long-term mean
    sigma: volatility
    T: maturity time
    n: number of data points
  Output: 
    OU time series, np.array
  '''
  result = []
  dt = T / (n - 1) # time = np.linspace(0, T, n+1)
  exp_minus_mu_deltat = np.exp(- mu * dt) 

  for i in range(m):
    x = np.zeros(n)
    x[0] = x0
    
    # Calculate the random term. 
    if mu == 0:
      dWt = np.sqrt(dt) * np.random.randn(n)  # Handle the case of mu = 0 i.e. no mean reversion. 
    else:
      dWt = np.sqrt((1 - np.exp(-2*mu*dt))/(2 * mu)) * np.random.randn(n)

    # Iterate through time calculating each price. 
    for t in range(1, n):   
      x[t] = x[t-1] * exp_minus_mu_deltat + theta * (1 - exp_minus_mu_deltat) + sigma * dWt[t]

    # Add new sample
    result.append(list(x))
    
  return result

def gen_gbm(m, x0, mu, sigma, T, n):
  '''
  The function generates an gbm process. dXt = mu * Xt dt + sigma * Xt dWt 
  Input:
    m = sample size
    x0: initial value
    mu: drift rate
    sigma: volatility
    T: maturity time
    n+1: number of data points
  Output: 
    list of GBM time series
  '''
  result = []
  dt = T / n   # time = np.linspace(0, T, n+1)

  for i in range(m):
    x = np.zeros(n)
    x[0] = x0

    # Iterate through time calculating each price. 
    for t in range(1, n):   
      x[t] = x[t-1] + mu * x[t-1] * dt + sigma * x[t-1] * np.random.normal() * np.sqrt(dt)
      
    # Add new sample
    result.append(list(x))
    
  return result