#!/usr/bin/env python3
"""Project 22b: Composite Charts and Group Dynamics"""
import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# Beatles founding members (real birthdates, AstroDatabank)
BEATLES = [
    ('John Lennon', 1940, 10, 9),
    ('Paul McCartney', 1942, 6, 18),
    ('George Harrison', 1943, 2, 25),
    ('Ringo Starr', 1940, 7, 7),
]

# Rolling Stones founding members
ROLLING_STONES = [
    ('Mick Jagger', 1943, 7, 26),
    ('Keith Richards', 1943, 12, 18),
    ('Charlie Watts', 1941, 6, 2),
    ('Bill Wyman', 1936, 10, 24),
]

def datetime_to_jd(year, month, day):
    return swe.julday(year, month, day, 12.0)

def get_planet_positions(year, month, day):
    jd = datetime_to_jd(year, month, day)
    positions = {}
    for planet, name in [(swe.SUN, 'sun'), (swe.MOON, 'moon'), 
                          (swe.MERCURY, 'mercury'), (swe.VENUS, 'venus')]:
        positions[name] = swe.calc_ut(jd, planet)[0][0]
    return positions

def compute_composite(members):
    """Compute midpoint composite chart."""
    all_positions = [get_planet_positions(*m[1:]) for m in members]
    composite = {}
    for planet in ['sun', 'moon', 'mercury', 'venus']:
        angles = [p[planet] for p in all_positions]
        # Circular mean
        sin_sum = np.sum([np.sin(np.radians(a)) for a in angles])
        cos_sum = np.sum([np.cos(np.radians(a)) for a in angles])
        composite[planet] = np.degrees(np.arctan2(sin_sum, cos_sum)) % 360
    return composite

def main():
    print("=" * 60)
    print("PROJECT 22b: COMPOSITE CHARTS GROUP DYNAMICS")
    print("=" * 60)
    
    beatles_composite = compute_composite(BEATLES)
    stones_composite = compute_composite(ROLLING_STONES)
    
    print("\nBeatles Composite Chart:")
    for planet, pos in beatles_composite.items():
        print(f"  {planet}: {pos:.1f}°")
    
    print("\nRolling Stones Composite Chart:")
    for planet, pos in stones_composite.items():
        print(f"  {planet}: {pos:.1f}°")
    
    # Internal harmony - aspect analysis
    def aspect_tension(composite):
        tensions = []
        planets = list(composite.values())
        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                diff = abs(p1 - p2) % 360
                if diff > 180: diff = 360 - diff
                # Check square/opposition
                if 85 <= diff <= 95 or 175 <= diff <= 185:
                    tensions.append(diff)
        return len(tensions)
    
    beatles_tension = aspect_tension(beatles_composite)
    stones_tension = aspect_tension(stones_composite)
    
    print(f"\nBeatles hard aspects: {beatles_tension}")
    print(f"Rolling Stones hard aspects: {stones_tension}")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for ax, composite, name in [(axes[0], beatles_composite, 'Beatles'),
                                 (axes[1], stones_composite, 'Rolling Stones')]:
        planets = list(composite.keys())
        positions = list(composite.values())
        colors = ['gold', 'silver', 'orange', 'pink']
        
        ax.barh(planets, positions, color=colors)
        ax.set_xlabel('Zodiac Position (degrees)')
        ax.set_title(f'{name} Composite')
        ax.set_xlim(0, 360)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'composite_comparison.png', dpi=150)
    plt.close()
    
    # Results
    results = pd.DataFrame([
        {'group': 'Beatles', 'sun': beatles_composite['sun'], 
         'hard_aspects': beatles_tension},
        {'group': 'Rolling Stones', 'sun': stones_composite['sun'],
         'hard_aspects': stones_tension},
    ])
    results.to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)
    print(f"\nResults saved to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()

