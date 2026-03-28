# Project 22: Astro-Weather Forecasting vs. Meteorological Data

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do planetary positions — particularly placement in astrological elements (Fire, Earth, Air, Water) — correlate with measurable changes in daily precipitation and temperature across the global historical weather record? Does the ancient claim "Water signs bring rain" survive scrutiny?

---

## 💡 Why This Matters

Weather prediction is one of astrology's oldest claimed practical applications. Ancient agricultural calendars were partly astrological; folk traditions in many cultures link lunar phases and planetary positions to planting conditions. With 129,562 NOAA stations spanning 124 years, this is the most comprehensive possible test: if any systematic planetary weather correlation exists, this dataset will find it.

---

## 📊 The Data

| Source | Description |
|---|---|
| NOAA GHCN-Daily | Global Historical Climatology Network; 129,562 station files; daily PRCP and TMAX; 1900–2024 |
| Swiss Ephemeris | Planetary positions for all 12 bodies in both Tropical and Vedic (Lahiri) zodiacs, every day 1900–2024 |

Both data sources are genuine. NOAA GHCN-Daily is the premier publicly available long-term daily weather dataset. A pre-computed planetary lookup table (`astro_weather_features.csv`) was generated using the Swiss Ephemeris, recording daily sign and element for each body.

---

## 📈 Results

### 1. The "Water Sign" Hypothesis: Seasonal Artifact

| Sun Element (Tropical) | Mean Precipitation (tenths mm) |
|---|---|
| Fire | 23.05 |
| Earth | 23.31 |
| Air | 23.40 |
| **Water** | **23.45** |

The Water sign bias exists — but it's tiny: **+1.7% above average**, with near-zero practical significance.

### ⚠️ The Critical Confound

**The stronger Water sign / precipitation correlation found in pilot analysis (+14%) was a regional seasonal artifact.**

The Sun moves through Cancer (June–July) during Northern Hemisphere summer monsoon season, through Scorpio (October–November) during Northern Hemisphere autumn rains, and through Pisces (February–March) during late-winter precipitation in many climates. Any correlation between "Sun in Water signs" and increased precipitation in a Northern-Hemisphere-dominated dataset is tracking *seasonality* — the calendar, not astrology.

**Hemisphere split confirms it:**

| Hemisphere | Wettest Sign Element |
|---|---|
| Northern (104,205 stations) | Differences negligible — fractions of a percent |
| Southern (25,357 stations) | Air/Water wetter, Fire/Earth drier — *reversed* from Northern |

In the Southern Hemisphere, Water and Air sign periods are wetter — because June–August (Fire signs) is the Southern winter/dry season, while October–March (Air/Water signs) is the Southern summer/wet season. Both hemispheres track their own seasonal calendars.

**Conclusion:** The Tropical Zodiac functions as a calendar. Different regions have different rain calendars. When the dataset is dominated by any geographic region, zodiacal correlations emerge — but they track climate, not planetary influence.

### 2. Moon Sign: Consistent Null

| Hemisphere | Moon in Water | Moon in Fire | Difference |
|---|---|---|---|
| Northern | 23.43 | 23.35 | +0.4% |
| Southern | 22.10 | 22.02 | +0.4% |

The Moon moves through all 12 signs every 27.3 days. It shows no consistent precipitation variation by sign in either hemisphere.

### 3. Slow Planets: Climate-Epoch Proxies

The full element analysis found the Neptune Tropical result strikingly large (+0.899 mean PRCP difference). But Neptune moves ~1° per year, spending ~14 years in each sign. Its "sign" at any given time is nearly identical to its sign a year earlier — and to the sign 14 years ago. Neptune-in-Water is a multi-decade climate epoch marker, not a causal variable. The correlation tracks decadal climate patterns (El Niño cycles, Atlantic Multidecadal Oscillation) that happen to coincide with Neptune's extremely slow sign transitions.

This is the **"Slow Planet as Climate Proxy"** pattern: outer planets serve as demographic/climate-epoch tags, not astrological signals.

### 4. Tithi Analysis — One Potentially Non-Trivial Signal

The Tithi analysis (30 lunar day bins based on Moon–Sun angular separation) revealed a persistent pattern:

| Lunar Phase | Approximate PRCP (tenths mm) |
|---|---|
| Waxing Quarter (Tithi 8–9) | ~46.0 (highest) |
| Waning Quarter (Tithi 23–24) | ~45.5 |
| New Moon (Tithi 1) | ~41.5 |
| Full Moon (Tithi 16) | ~40.9 |

**Precipitation dips ~11% during New Moon and Full Moon (syzygy) periods** compared to Quarter Moon phases. This pattern is physically plausible: at syzygy (Sun, Moon, Earth aligned), tidal forces are maximized, which may affect atmospheric circulation. Notably, this *contradicts* the folk belief that Full Moons bring storms — it suggests they may actually correlate with slightly drier conditions.

This is the one potentially non-trivial signal in the dataset. It requires replication and mechanism investigation before interpretation.

---

## 🔍 What the Numbers Mean

Fast planets (Sun, Moon, Mercury, Venus, Mars) cycle through all signs frequently and correlate with precipitation primarily through **seasonal timing**. Their "element" is effectively a calendar proxy.

Slow planets (Jupiter through Pluto) spend years in a sign and act as **climate-epoch markers** — tagging multi-year climate patterns they coincide with by chance of slow motion.

The question "do Water signs bring rain?" dissolves on inspection: the Tropical Zodiac *is* a calendar, and different parts of the calendar are wetter or drier depending on geography. There is no evidence of a planetary mechanism beyond this.

---

## ⚠️ Statistical Caveats

- Multiple testing: 12 bodies × 2 zodiacs × 4 elements × 2 weather variables = hundreds of comparisons. No results should be treated as confirmed without preregistered replication.
- Seasonal confounding is the primary concern for all Sun-based correlations.
- Station coverage is uneven globally — Northern Hemisphere is overrepresented.
- Effect sizes are tiny: even the largest effects are fractions of a percent of mean precipitation, with no practical meteorological significance.

---

## 🌟 Conclusion

After analyzing 124 years of daily precipitation data from 129,562 global weather stations:

1. The "Water sign" precipitation effect is a **seasonal confound** — the Tropical Zodiac tracks the calendar, which tracks climate
2. Moon sign placement has **no detectable effect** on daily precipitation
3. Outer planet "element" correlations reflect **multi-decade climate patterns**, not planetary influence
4. The **Tithi syzygy suppression** (New/Full Moon ~11% drier than Quarter phases) is the only consistent globally-replicated pattern — and it contradicts the folk belief about Full Moon weather

The data does not support traditional astro-meteorological claims.
