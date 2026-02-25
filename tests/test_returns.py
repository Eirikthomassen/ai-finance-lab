import pandas as pd
from energy_snapshot import pct_return

def test_pct_return_basic():
    s = pd.Series([100.0, 105.0, 110.0])
    r = pct_return(s, trading_days=2)
    assert round(r, 6) == 10.0