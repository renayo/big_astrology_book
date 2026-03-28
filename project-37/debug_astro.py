import swisseph as swe
from datetime import datetime

swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

# Pick a known Mercury Retrograde date: Feb 17, 2020 to March 10, 2020
known_rx_date = datetime(2020, 2, 25)
jd = swe.julday(known_rx_date.year, known_rx_date.month, known_rx_date.day, 12.0)

res = swe.calc_ut(jd, swe.MERCURY, flags)
speed = res[0][3]

print(f"Date: {known_rx_date}")
print(f"Mercury Speed: {speed}")
print(f"Is Rx? {speed < 0}")

