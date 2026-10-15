import numpy as np
import pytest
from options_engine.black_scholes import bs_greeks, bs_price

def test_greeks_call():
    assert bs_greeks(100,100,1,0.05,0.2,0,'call') == pytest.approx({'delta': 0.6368, 'gamma': 0.018762, 'vega': 37.5240, 'theta': -6.4140, 'rho': 53.2325}, rel=1e-4)

def test_greeks_put():
    assert bs_greeks(100,100,1,0.05,0.2,0,'put') == pytest.approx({'delta': -0.3632, 'gamma': 0.018762, 'vega': 37.5240, 'theta': -1.6579, 'rho': -41.8905}, rel=1e-4)

def test_finite_difference_greeks():
    rng = np.random.default_rng(0)
    S = rng.uniform(45, 150, size=1000)
    K = rng.uniform(45, 150, size=1000)
    T = rng.uniform(0.05, 3.5, size=1000)
    r = rng.uniform(0.01, 0.15, size=1000)
    q = rng.uniform(0.0, 0.05, size=1000)
    sigma = rng.uniform(0.05, 1, size=1000)

    h1 = 1e-4 * S
    h2 = 1e-4 * sigma
    h3 = 1e-4 * r
    h4 = 1e-4 * T
    up_call = bs_price(S+h1, K, T, r, sigma, q, kind='call') 
    down_call = bs_price(S-h1, K, T, r, sigma, q, kind='call') 
    delta_fd_call = (up_call - down_call) / (2*h1)
    gamma_fd_call = (up_call - 2*(bs_price(S, K, T, r, sigma, q, kind='call')) + down_call) / (h1**2) 
    vega_fd_call = (bs_price(S, K, T, r, sigma+h2, q, kind='call') - bs_price(S, K, T, r, sigma-h2, q, kind='call')) / (2*h2)
    rho_fd_call = (bs_price(S, K, T, r+h3, sigma, q, kind='call') - bs_price(S, K, T, r-h3, sigma, q, kind='call')) / (2*h3) 
    theta_fd_call = -((bs_price(S, K, T+h4, r, sigma, q, kind='call') - bs_price(S, K, T-h4, r, sigma, q, kind='call')) / (2*h4)) 

    assert (delta_fd_call) == pytest.approx(bs_greeks(S, K, T, r, sigma, q, kind='call')['delta'], rel=1e-5)
    assert (gamma_fd_call) == pytest.approx(bs_greeks(S, K, T, r, sigma, q, kind='call')['gamma'], rel=1e-4)
    assert (vega_fd_call) == pytest.approx(bs_greeks(S, K, T, r, sigma, q, kind='call')['vega'], rel=1e-5)
    assert (rho_fd_call) == pytest.approx(bs_greeks(S, K, T, r, sigma, q, kind='call')['rho'], rel=1e-5)
    assert (theta_fd_call) == pytest.approx(bs_greeks(S, K, T, r, sigma, q, kind='call')['theta'], rel=1e-5)

    up_put = bs_price(S+h1, K, T, r, sigma, q, kind='put')
    down_put = bs_price(S-h1, K, T, r, sigma, q, kind='put') 
    delta_fd_put = (up_put - down_put) / (2*h1)
    gamma_fd_put = (up_put - 2*(bs_price(S, K, T, r, sigma, q, kind='put')) + down_put) / (h1**2) 
    vega_fd_put = (bs_price(S, K, T, r, sigma+h2, q, kind='put') - bs_price(S, K, T, r, sigma-h2, q, kind='put')) / (2*h2)
    rho_fd_put = (bs_price(S, K, T, r+h3, sigma, q, kind='put') - bs_price(S, K, T, r-h3, sigma, q, kind='put')) / (2*h3) 
    theta_fd_put = -((bs_price(S, K, T+h4, r, sigma, q, kind='put') - bs_price(S, K, T-h4, r, sigma, q, kind='put')) / (2*h4)) 
    
    assert (delta_fd_put) == pytest.approx((bs_greeks(S, K, T, r, sigma, q, kind='put')['delta']), rel=1e-5)
    assert (gamma_fd_put) == pytest.approx((bs_greeks(S, K, T, r, sigma, q, kind='put')['gamma']), rel=1e-4)
    assert (vega_fd_put) == pytest.approx((bs_greeks(S, K, T, r, sigma, q, kind='put')['vega']), rel=1e-5)
    assert (rho_fd_put) == pytest.approx((bs_greeks(S, K, T, r, sigma, q, kind='put')['rho']), rel=1e-5)
    assert (theta_fd_put) == pytest.approx((bs_greeks(S, K, T, r, sigma, q, kind='put')['theta']), rel=1e-5)