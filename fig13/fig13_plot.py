import numpy as np                 # ver. 2.3.3
import matplotlib.pyplot as plt    # ver. 3.10.7

# =====================
# Adjustable parameters
# =====================
fig_width = 15    # figure width
fig_height = 6    # figure height

xlabel = "Wavelength, $\\lambda$ (nm)"
ylabel = "Convolved Transmittance, T (%)"
xlabel_fontsize = 14
ylabel_fontsize = 14
xtick_fontsize = 12
ytick_fontsize = 12
legend_fontsize = 12

# =====================
# Axis limits
# =====================
x_min, x_max = 300, 900       # wavelength range in nm
y_min, y_max = 82, 101

# =====================
# Data loading
# =====================

dat = np.loadtxt("fig13_Toci_o2_h2o_cont.txt", skiprows=1)
wavnm = dat[:, 0]
To2 = dat[:, 1]
Th2o = dat[:, 2]
Tcont = dat[:, 3]

tau_eff_o2 = -np.log(To2)
tau_eff_h2o = -np.log(Th2o)
tau_eff_cont = -np.log(Tcont)

fig, ax = plt.subplots(figsize=(fig_width, fig_height))

ax.plot(wavnm[124:133], To2[124:133]*100, color='magenta',  linestyle='-', linewidth=1.5, marker='o', markersize=3, alpha=1, label='O2-γ LBL')
ax.plot(wavnm[163:182], To2[163:182]*100, color='blue',  linestyle='-', linewidth=1.5, marker='o', markersize=3, alpha=1, label='O2-B LBL')
ax.plot(wavnm[211:233], To2[211:233]*100, color='cyan',  linestyle='-', linewidth=1.5, marker='o', markersize=3, alpha=1, label='O2-A LBL')

ax.plot(wavnm[2:], Th2o[2:]*100, color='black',  linestyle='-', linewidth=1.5, marker='o', markersize=3, alpha=1, label='H2O LBL')
ax.plot(wavnm[2:], Tcont[2:]*100, color='red',  linestyle='-', linewidth=1.5, marker='o', markersize=3, alpha=1, label='Continuum')

# Set Y-axis to log scale
#ax.set_yscale('log')

# Set axis limits
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Labels and font sizes
ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)
ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)

# Tick label font sizes
ax.tick_params(axis='x', labelsize=xtick_fontsize)
ax.tick_params(axis='y', labelsize=ytick_fontsize)

# Custom x-ticks
xticks = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
ax.set_xticks(xticks)

# Custom y-ticks
yticks = [82, 84, 86, 88, 90, 92, 94, 96, 98, 100]
ax.set_yticks(yticks)

# Grid for easier reading
ax.grid(True, which='major')  # show grid for both major and minor ticks

# add secondary x-axis on top
secax = ax.secondary_xaxis('top', functions=(lambda v: 1e7/v, lambda w: 1e7/w))
secax.set_xlabel("Wavenumber, $\\nu$ (cm$^{-1}$)", fontsize=xlabel_fontsize)
top_ticks = [12500, 15000, 17500, 20000, 22500, 25000, 27500, 30000]  # in nm, for example
secax.set_xticks(top_ticks)
secax.tick_params(axis='x', labelsize=xtick_fontsize)

# Legend
ax.legend(fontsize=legend_fontsize, loc="lower left", bbox_to_anchor=(0.4, 0.1))

# ----------------------------------------------------
# Add RIGHT secondary y-axis for tau (log scale)
# ----------------------------------------------------
ax_tau = ax.twinx()                  # right-side y-axis
ax_tau.set_yscale("log")
ax_tau.set_ylabel("Effective Optical Thickness, $\\tau$", fontsize=ylabel_fontsize)

# Make the entire right y-axis gray
ax_tau.spines["right"].set_color("gray")
ax_tau.tick_params(axis='y', colors="gray")
ax_tau.yaxis.label.set_color("gray")

# Plot tau on the right axis
line_tau, = ax_tau.plot(
    wavnm[2:], tau_eff_cont[2:], 
    color="gray", linewidth=1.5, linestyle="-",
    marker='o', markersize=3,
    label="Continuum $\\tau$"
)

# Optional: tau axis limits
ax_tau.set_ylim(1e-4, 1e-1)


# =====================
# Save figure
# =====================
plt.savefig("fig13.jpg", dpi=600, bbox_inches='tight')

# Show plot
plt.show()