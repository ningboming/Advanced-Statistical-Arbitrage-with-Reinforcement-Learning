import numpy as np
import matplotlib.pyplot as plt

def compute_profit(series1, series2, b, actions):
    cash = 100
    shares = 0
    cum_profit = []
    for i in range(len(series1)):
        if actions[i] == 1:
            shares = cash / series1[i]
            cash = cash - shares * (series1[i] - b * series2[i])
        if actions[i] == -1:
            cash = cash + shares * (series1[i] - b * series2[i])
            shares = 0
        cum_profit.append(cash + shares * (series1[i] - b * series2[i]))
    profit = (cum_profit[-1] - 100) / 100
    return cum_profit, profit

def plot_actions(test_series, test_actions):
    plt.figure(figsize=(10, 6))
    plt.plot(test_series)
    n = len(test_series)
    trade_nums = 0
    # Plotting the actions
    for i in range(n):
        if test_actions[i] == 1:
            if trade_nums == 0:
                plt.plot(i, test_series[i], 'go', label='Buying points')
            else:
                plt.plot(i, test_series[i], 'go')
            trade_nums += 1
        if test_actions[i] == -1:
            if trade_nums == 1:
                plt.plot(i, test_series[i], 'ro',  label='Selling points')
            else:
                plt.plot(i, test_series[i], 'ro')
    plt.legend(loc="upper left")
    plt.xlabel("Time")
    plt.ylabel("Simulated Spread Price")
    plt.grid(True)
    plt.show()

import numpy as np

def summarize_total_equity(x):
  '''
  This function is to summarize the statistics of a equity curve
  x: the total equity curve
  '''
  returns = (x[1:] - x[:-1]) / x[:-1]
  daily_return = np.mean(returns) 
  daily_std = np.std(returns)
  daily_sharpe = daily_return / daily_std
  #annual_ret = 252 * daily_return
  #annual_std = 252**(1/2) * daily_std
  #annual_sharpe = 252**(1/2) * daily_sharpe
  max_drawdown = (np.min(x) - x[0]) / x[0]
  cumul_pnl = (x[-1] - x[0]) / x[0]  
  result = {'DailyRet': round(daily_return*100, 4),
            'DailyStd': round(daily_std*100, 4),
            'DailySharp': round(daily_sharpe, 4),
            #'AnnualRet': annual_ret, 
            #'AnnualStd': annual_std,
            #'AnnualSharpe': annual_sharpe,
            'MaxDrawdown': round(max_drawdown*100, 4),
            'CumulPnL': round(cumul_pnl*100, 4),
            }
  return result
