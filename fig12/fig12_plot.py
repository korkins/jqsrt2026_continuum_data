import numpy as np                        # ver. 2.3.3
import matplotlib.pyplot as plt           # ver. 3.10.7
from scipy.interpolate import interp1d    # ver. 1.16.2

# =====================
# Adjustable parameters
# =====================
fig_width = 15    # figure width
fig_height = 6    # figure height

xlabel = "Wavelength,  $\\lambda$ (nm)"
ylabel = "Total  atmospheric  optical  thickness,  $\\tau$"
xlabel_fontsize = 14
ylabel_fontsize = 14
xtick_fontsize = 12
ytick_fontsize = 12
legend_fontsize = 12

# =====================
# Axis limits
# =====================
x_min, x_max = 300, 900       # wavelength range in nm
y_min, y_max = 1e-4, 1e1       # optical thickness range


print('\nWARNING: some txt files on GitHub are zipped — make sure to unzip\n')


# =====================
# Data loading
# =====================

# H2O HITRAN
dat = np.loadtxt("fig12_tau_lbl_h2o_hitran.txt", skiprows=1)
vcm_h2o = dat[:, 1]
wav_nm_h2o = 10_000_000 / vcm_h2o
tau_h2o_std = dat[:, 2]

# O2 HITRAN
dat = np.loadtxt("fig12_tau_lbl_o2_hitran.txt", skiprows=1)
vcm_o2 = dat[:, 1]
wav_nm_o2 = 10_000_000 / vcm_o2
tau_o2_hit = dat[:, 2]

# O2-O2 Continuum: Finkenzeller & Volkamer, JQSRT 2022: 297:0.1:500nm
dat = np.loadtxt("fig12_tau_cia_o4_finkenzeller_volkamer.txt", skiprows=1)
wav_nm_o2_FinkVolk = dat[:, 0]
tau_o2_FinkVolk = dat[:, 3]

# O2-O2 Continuum: HITRAN database
dat = np.loadtxt("fig12_tau_cia_o4_hitran.txt", skiprows=1)
wav_nm_o4 = dat[:, 0]
tau_o4 = dat[:, 1]

# O2-Air Continuum: HITRAN database
dat = np.loadtxt("fig12_tau_cia_o2a-air_hitran.txt", skiprows=1)
vcm_o2_air = dat[:, 0]
wav_nm_o2_air = 10_000_000/vcm_o2_air
tau_o2_air = dat[:, 1]

# O2-Air Continuum: HITRAN database - alternative
dat = np.loadtxt("fig12_tau_cia_o2-air_hitran_altern_756_770nm.txt", skiprows=1)
wav_nm_o2_air_altern = dat[:, 0]
tau_o2_air_altern = dat[:, 1]

# O3 Continuum: Bremen X-section data, US 1976 Atmopshere, Simpson integration over zkm
dat = np.loadtxt("fig12_tau_cnt_o3_bremen_us1976_simps.txt", skiprows=1)
wav_nm_o3 = dat[:, 0]
tau_o3 = dat[:, 1]

# NO2 Continuum: Bremen X-section data, US 1976 Atmopshere, Simpson integration over zkm
dat = np.loadtxt("fig12_tau_cnt_no2_bremen_us1976_simps.txt", skiprows=1)
wav_nm_no2 = dat[:, 0]
tau_no2 = dat[:, 1]

# WV Continuum: MT_CKD v.4.3, US 1976 Atmopshere, Simpson integration over zkm
dat = np.loadtxt("fig12_tau_cnt_h2o_us1976_simps.txt", skiprows=1)
wav_nm_wvc = dat[:, 1]
tau_wvc = dat[:, 2]

# O2-O2 B-band: 671-704 nm - note two datasets
dat = np.loadtxt("fig12_tau_cia_o4_spiering_671_704nm.txt", skiprows=0)
wav_nm_spiering_671_704nm = dat[:, 0]
tau_spiering_671_704nm = dat[:, 1]
#
dat = np.loadtxt("fig12_tau_cia_o4_hitran_alternate_675_704nm.txt", skiprows=0)
wav_nm_hitran_alternate_675_704nm = dat[:, 0]
tau_hitran_alternate_675_704nm = dat[:, 1]

#---------------------------------------------------------------------------------------------------------------------------
# Interpolate all components to wav_nm = [300:0.1:900] nm grid
# H2O LBL & O2 LBL already at this resolution

kwrd_kind='linear' # linear, quadratic, cubic
dwav = 0.1
wav_nm = np.arange(300.0, 900+dwav, dwav)

cf = interp1d(wav_nm_o3, tau_o3, fill_value=0.0, bounds_error=False, kind=kwrd_kind)
tau_o3_combined = cf(wav_nm)

cf = interp1d(wav_nm_no2, tau_no2, fill_value=0.0, bounds_error=False, kind=kwrd_kind)
tau_no2_combined = cf(wav_nm)

cf = interp1d(wav_nm_wvc, tau_wvc, fill_value=0.0, bounds_error=False, kind=kwrd_kind)
tau_wvc_combined = cf(wav_nm)

cf = interp1d(wav_nm_o4, tau_o4, fill_value=0.0, bounds_error=False, kind=kwrd_kind)
tau_o4_combined = cf(wav_nm)

cf = interp1d(wav_nm_spiering_671_704nm, tau_spiering_671_704nm, fill_value=0.0, bounds_error=False, kind=kwrd_kind)
tau_spiering_combined = cf(wav_nm)

cf = interp1d(wav_nm_o2_air, tau_o2_air, fill_value=0.0, bounds_error=False, kind=kwrd_kind)
tau_o2_air_combined = cf(wav_nm)

tau_continuum_combined = tau_o3_combined + tau_no2_combined + tau_wvc_combined + \
                         tau_o4_combined + tau_spiering_combined + tau_o2_air_combined

tau_wav_cont_comb = np.zeros((len(tau_continuum_combined), 2))
tau_wav_cont_comb[:, 0] = wav_nm
tau_wav_cont_comb[:, 1] = tau_continuum_combined
np.savetxt("tau_continuum_combined.txt", tau_wav_cont_comb, fmt=['%6.2f', '%.4e'], header="wav (nm), tau_cont_comb")

#----------------------------------------------------------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

ax.plot(wav_nm_h2o, tau_h2o_std, color='gray',  linestyle='-', linewidth=1.5, marker='none', markersize=10, alpha=0.5, label='H2O LBL')
ax.plot(wav_nm_o2, tau_o2_hit,   color='cyan',  linestyle='-', linewidth=1.5, marker='none', markersize=10, alpha=1.0, label='O2 LBL')

ax.plot(wav_nm_o3, tau_o3, color='blue',  linestyle='-', linewidth=3, marker='none', markersize=8, alpha=1, label='O3')
ax.plot(wav_nm_no2, tau_no2, color='green',  linestyle='-', linewidth=1.5, marker='none', markersize=8, alpha=1, label='NO2')

ax.plot(wav_nm_wvc, tau_wvc, color='black',  linestyle='--', linewidth=1.5, marker='none', markersize=10, alpha=1.0, label='MT_CKD')

ax.plot(wav_nm_o2_FinkVolk, tau_o2_FinkVolk,   color='black',  linestyle='-', linewidth=3, marker='none', markersize=10, alpha=1.0, label='O2-O2 F&V 2022')
ax.plot(wav_nm_o4, tau_o4, color='red',  linestyle='--', linewidth=1.5, marker='none', markersize=8, alpha=1, label='O2-O2 HIT 2019')

ax.plot(wav_nm_spiering_671_704nm, tau_spiering_671_704nm, color='yellow',  linestyle='-', linewidth=1.5, marker='none', markersize=8, alpha=1, label='BO2-Air (Main)')
ax.plot(wav_nm_hitran_alternate_675_704nm, tau_hitran_alternate_675_704nm, color='yellow',  linestyle='--', linewidth=1.5, marker='none', markersize=8, alpha=1, label='BO2-Air (Alt.)')

ax.plot(wav_nm_o2_air, tau_o2_air, color='magenta',  linestyle='-', linewidth=1.5, marker='none', markersize=8, alpha=1, label='AO2-Air (Main)')
ax.plot(wav_nm_o2_air_altern, tau_o2_air_altern, color='magenta',  linestyle='--', linewidth=1.5, marker='none', markersize=8, alpha=1, label='AO2-Air (Alt.)')

ax.plot(wav_nm, tau_continuum_combined, color='red',  linestyle='-', linewidth=1.5, marker='none', markersize=8, alpha=1, label='Combined')


# Set Y-axis to log scale
ax.set_yscale('log')

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

# Legend
ax.legend(fontsize=legend_fontsize, loc="upper left", ncol=3, bbox_to_anchor=(0.03, 1.0))

# Grid for easier reading
ax.grid(True, which='major')  # show grid for both major and minor ticks

# add secondary x-axis on top
secax = ax.secondary_xaxis('top', functions=(lambda v: 1e7/v, lambda w: 1e7/w))
secax.set_xlabel("Wavenumber,  $\\nu$ (cm$^{-1}$)", fontsize=xlabel_fontsize)
top_ticks = [12500, 15000, 17500, 20000, 22500, 25000, 27500, 30000]
secax.set_xticks(top_ticks)
secax.tick_params(axis='x', labelsize=xtick_fontsize)

# =====================
# Save figure
# =====================
plt.savefig("fig12.jpg", dpi=600, bbox_inches='tight')

# Show plot
plt.show()