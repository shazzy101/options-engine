import numpy as np
from numpy import exp, sqrt, log
from scipy.stats import norm

def bs_price(S, K, T, r, sigma, q=0.0, kind='call'):
    """

    Parameters:
    S : float
        Current stock price in USD
    K : float
        Strike price in USD
    T : float
        Time to expiry in years
    r : float
        Risk-free interest rate (annualized), continuously compounded
    sigma : float
        Volatility of the underlying stock (annualized), continuously compounded
    q : float
        Dividend yield (annualized), continuously compounded
    kind : str
        Type of the option ('call' or 'put')

    Returns:
    float
        The price of the option
    """

    d1 = (np.log(S/K) + (r-q+(sigma**2/2))*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    C = S*exp(-q*T)*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)
    P = K*exp(-r*T)*norm.cdf(-d2) - S*exp(-q*T)*norm.cdf(-d1) 

    if kind == 'call':
        return C
    elif kind == 'put':
        return P
    else:
        raise ValueError("invalid kind")