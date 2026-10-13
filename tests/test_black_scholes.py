import numpy as np
import pytest

from options_engine.black_scholes import bs_price

def test_black_scholes_call():
    assert bs_price(100, 100, 1, 0.00, 0.2, 0.0, 'call')

def test_black_scholes_put():
    assert bs_price(100, 100, 1, 0.05, 0.2, 0.0, 'put')

print(pytest.approx(test_black_scholes_call(), abs=1e-4))
print(pytest.approx(test_black_scholes_put(), abs=1e-4))


def test_black_scholes_parity():
    rng = np.random.default_rng(0)
    S = rng.uniform(45, 160)
    K = rng.uniform(45, 154)
    T = rng.uniform(0.01, 3.5)
    r = rng.uniform(0.01, 0.15)
    sigma = rng.uniform(0.01, 1)
    C = bs_price(S, K, T, r, sigma, 0.0, 'call')
    P = bs_price(S, K, T, r, sigma, 0.0, 'put')
    assert (C - P - (S - K * np.exp(-r * T))) < 1e-10
    assert C - P - (S - K * np.exp(-r * T))

print(test_black_scholes_parity())