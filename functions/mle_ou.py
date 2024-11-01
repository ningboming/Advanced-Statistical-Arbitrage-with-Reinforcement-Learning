import numpy as np
from numpy import exp
from numpy import log
from numpy import pi

def mle_ou(x, dt):
  '''
  MLE for OU proess dX_t = μ*(θ − X_t)dt + σ*dB_t
  x: time series, np.array
  dt: time difference
  Output: estimations of parameters and maximum log-likelihood
  '''
  n = x.size
  X_x  = np.sum(x[:-1])
  X_y  = np.sum(x[1:])
  X_xx = np.sum(x[:-1]**2)
  X_xy = np.sum(x[:-1]*x[1:])
  X_yy = np.sum(x[1:]**2)

  # estimated long-run mean
  if n*(X_xx - X_xy) - (X_x**2-X_x*X_y) == 0.0:
    theta  = (X_y*X_xx - X_x*X_xy) / 0.00001
  else:
    theta  = (X_y*X_xx - X_x*X_xy) / (n*(X_xx - X_xy) - (X_x**2-X_x*X_y))

  # estimated speed of mean reversion
  if X_xx - 2*theta*X_x + n*theta**2 == 0.0:
    mu = - 1/dt * log((X_xy - theta*X_x - theta*X_y + n*theta**2) / 0.00001)
  else:
    mu = - 1/dt * log((X_xy - theta*X_x - theta*X_y + n*theta**2) / (X_xx - 2*theta*X_x + n*theta**2))

  # estimated vol
  a = exp(- mu * dt)
  sigma_sq = 2*mu/(n*(1 - a**2)) * (X_yy - 2*a*X_xy + a**2*X_xx - 2*theta*(1-a)*(X_y-a*X_x) + n*theta**2*(1-a)**2)

  # log-likelihood
  sigma_hat_sq = sigma_sq * (1 - exp(- 2 * mu * dt)) / (2*mu)
  ll = - 1/2 * log(2*pi) - log(np.sqrt(sigma_hat_sq)) - 1/(2*n*sigma_hat_sq) * np.sum((x[1:] - x[:-1]*a - theta*(1 - a))**2)

  res = {'mu': mu, 'theta': theta, 'sigma': np.sqrt(sigma_sq), 'll': ll}
  return res