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

    
def bs_greeks(S, K, T, r, sigma, q=0.0, kind='call'):
    """
    Calculate the Greeks for a European option using the Black-Scholes model.

    Returns:
    dict
        A dictionary containing the Greeks: delta, gamma, vega, theta, and rho.
    """
    d1 = (np.log(S/K) + (r-q+(sigma**2/2))*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    gamma = exp(-q*T)*norm.pdf(d1) / (S*sigma*np.sqrt(T))
    vega = S*exp(-q*T)*norm.pdf(d1) * np.sqrt(T)
    if kind == 'call':
        delta = exp(-q*T)*norm.cdf(d1)
        theta = -S*exp(-q*T)*norm.pdf(d1)*sigma/(2*np.sqrt(T)) - r*K*exp(-r*T)*norm.cdf(d2) + q*S*exp(-q*T)*norm.cdf(d1)
        rho = K*T*exp(-r*T)*norm.cdf(d2)
    elif kind == 'put':
        delta = exp(-q*T)*(norm.cdf(d1) - 1)
        theta = -S*exp(-q*T)*norm.pdf(d1)*sigma/(2*np.sqrt(T)) + r*K*exp(-r*T)*norm.cdf(-d2) - q*S*exp(-q*T)*norm.cdf(-d1)
        rho = -K*T*exp(-r*T)*norm.cdf(-d2)
    else:
        raise ValueError("invalid kind")

    return {'delta': delta, 'gamma': gamma, 'vega': vega, 'theta': theta, 'rho': rho}

