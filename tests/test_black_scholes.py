import numpy as np
import pytest
from options_engine.black_scholes import bs_price

def test_black_scholes_call():
    assert bs_price(100, 100, 1, 0.05, 0.2, 0.0, 'call') == pytest.approx(10.4506, abs=1e-4)

def test_black_scholes_put():
    assert bs_price(100, 100, 1, 0.05, 0.2, 0.0, 'put') == pytest.approx(5.5735, abs=1e-4)

def test_black_scholes_parity():
    rng = np.random.default_rng(0)
    S = rng.uniform(45, 150, size=1000)
    K = rng.uniform(45, 150, size=1000)
    T = rng.uniform(0.01, 3.5, size=1000)
    r = rng.uniform(0.01, 0.15, size=1000)
    q = rng.uniform(0.0, 0.05, size=1000)
    sigma = rng.uniform(0.01, 1, size=1000)
    C = bs_price(S, K, T, r, sigma, q, 'call' )# type: ignore
    P = bs_price(S, K, T, r, sigma, q, 'put') # type: ignore
    assert np.max(np.abs(C - P - (S * np.exp(-q*T) - K * np.exp(-r * T)))) < 1e-10
