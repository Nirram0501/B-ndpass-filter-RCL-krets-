import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.ticker import FuncFormatter

# Frekvensområde
F_MIN = 100
F_MAX = 10_000

CSV_FILE = "/Users/martintandberg/Desktop/Skole/ITGK/Egne prosjekter/esda/Note-demper/frekvensAnalyse.csv"

if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]

df = pd.read_csv(CSV_FILE, sep=",", comment="#", header=0)

df.columns = ["freq_hz", "amplitude_dbv"] + list(df.columns[2:])

# Filtrer ønsket frekvensområde
df = df[(df["freq_hz"] >= F_MIN) & (df["freq_hz"] <= F_MAX)]

freq = df["freq_hz"].values
amp  = df["amplitude_dbv"].values

# Finn topp innenfor området
peak_idx  = np.argmax(amp)
peak_freq = freq[peak_idx]
peak_amp  = amp[peak_idx]

fig, ax = plt.subplots(figsize=(14, 6))

ax.semilogx(freq, amp, color="#8B1A1A", linewidth=0.8, label="Spektrum")

ax.axvline(
    x=peak_freq,
    color="#0022FF",
    linewidth=0.5,
    linestyle="--",
    label=f"Topp: {peak_freq/1000:.2f} kHz  ({peak_amp:.1f} dBV)",
)

ax.plot(peak_freq, peak_amp, "o", color="#004CFF", markersize=7, zorder=5)

ax.annotate(
    f"  {peak_freq/1000:.2f} kHz\n  {peak_amp:.1f} dBV",
    xy=(peak_freq, peak_amp),
    xytext=(peak_freq * 1.4, peak_amp - 5),
    arrowprops=dict(arrowstyle="->", color="#FF4500"),
    color="#FF0000",
    fontsize=9,
)

ax.set_xlabel("Frekvens (Hz)", fontsize=11)
ax.set_ylabel("Amplitude (dBV)", fontsize=11)
ax.set_title("Frekvensspektrum (100 Hz – 10 kHz)", fontsize=13)

# Viktig: fast grense
ax.set_xlim(F_MIN, F_MAX)

ax.grid(True, which="both", linestyle=":", linewidth=0.5, color="gray", alpha=0.6)
ax.legend(fontsize=9)

def hz_fmt(x, _):
    return f"{x/1000:.0f} kHz" if x >= 1000 else f"{int(x)} Hz"
ax.xaxis.set_major_formatter(FuncFormatter(hz_fmt))

plt.tight_layout()
plt.savefig("spectrum_plot.png", dpi=150)
plt.show()

print(f"Høyeste punkt i området 100Hz–10kHz: {peak_freq:.1f} Hz  ({peak_amp:.1f} dBV)")