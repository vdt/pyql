import numpy as np


from quantlib.models.equity.heston_model import (
    HestonModelHelper, HestonModel, ImpliedVolError
)

from quantlib.models.equity.bates_model import (BatesModel, BatesDoubleExpModel)
from quantlib.processes.heston_process import HestonProcess
from quantlib.processes.bates_process import BatesProcess

from quantlib.settings import Settings
from quantlib.time.api import (
    today, Actual360, NullCalendar, Period, Months, Years, Date, July,
    Actual365Fixed, TARGET, Weeks, ActualActual
)
from quantlib.termstructures.yields.flat_forward import FlatForward
from quantlib.quotes import SimpleQuote
from quantlib.termstructures.yields.zero_curve import ZeroCurve

def flat_rate(forward, daycounter):
    return FlatForward(
        quote           = SimpleQuote(forward),
        settlement_days = 0,
        calendar        = NullCalendar(),
        daycounter      = daycounter
    )

DtSettlement = today()

settings = Settings()
settings.evaluation_date = DtSettlement

daycounter = ActualActual()
calendar = NullCalendar()

iRate = .1
iDiv = .04

risk_free_ts = flat_rate(iRate, daycounter)
dividend_ts = flat_rate(iDiv, daycounter)

s0 = SimpleQuote(32.0)

# Bates model

v0 = 0.05
kappa = 5.0;
theta = 0.05;
sigma = 1.0e-4;
rho = 0.0;
Lambda = .1
nu = .01
delta = .001

pb = BatesProcess(risk_free_ts, dividend_ts, s0, v0,
                       kappa, theta, sigma, rho,
                       Lambda, nu, delta)

print(pb)

# error: the arguments Lambda, nu, delta have changed
mb = BatesModel(pb)
print(mb)

# double exponential model

ph = HestonProcess(risk_free_ts, dividend_ts, s0, v0,
                       kappa, theta, sigma, rho)

print(ph)

# constructor with default arguments: it works
me = BatesDoubleExpModel(ph)
print(me)

# speficy the arguments: it works
me = BatesDoubleExpModel(ph, Lambda=0.234, nuUp=0.43, nuDown=0.54, p=.6)
print(me)

