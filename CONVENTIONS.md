# Conventions

All inputs and outputs of `options_engine` follow these units. Every test and the report use them too.

## Inputs

| Symbol | Meaning | Unit |
|---|---|---|
| S | Spot price of the underlying | USD |
| K | Strike price | USD |
| T | Time to expiry | Years, ACT/365 (days / 365) |
| r | Risk-free rate | Annual, continuously compounded, decimal (0.05 = 5%) |
| q | Dividend yield | Annual, continuously compounded, decimal |
| σ (sigma) | Volatility of log returns | Annualized, decimal (0.20 = 20%) |
| kind | Option type | `"call"` or `"put"` |

## Greeks

| Greek | Definition | Unit | Common quoting |
|---|---|---|---|
| Delta | ∂V/∂S | USD per USD of spot | as is |
| Gamma | ∂²V/∂S² | per USD of spot | as is |
| Theta | ∂V/∂t, calendar time passing (= −∂V/∂T) | USD per year | divide by 365 for per day |
| Vega | ∂V/∂σ | USD per 1.00 of σ | divide by 100 for per vol point |
| Rho | ∂V/∂r | USD per 1.00 of r | divide by 100 for per 1% |

## Model assumptions

- European exercise only.
- Constant r, q and σ over the option's life.
- Lognormal terminal price (geometric Brownian motion).
- Continuous trading, no transaction costs, no taxes.
