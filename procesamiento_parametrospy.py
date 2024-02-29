import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# %% DEFINIR FUNCIONES
def analyze_dataframe(df,plot_title):
    if not isinstance(df.index, pd.DatetimeIndex) or df.shape[1] != 2:
        raise ValueError("DataFrame must have a datetime index and two columns of floats")

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle(plot_title)
    
    # Determine overall range for histograms and heatmaps
    min_val = df.min().min()
    max_val = df.max().max()
    bins = np.arange(min_val, max_val + 0.5, 0.5)  # Adjust bin width here if needed
    
    # ECDF Plot
    for column in df.columns:
        sorted_data = np.sort(df[column])
        yvals = np.arange(1, len(sorted_data)+1) / float(len(sorted_data))
        axes[0, 0].plot(sorted_data, yvals, marker='.', linestyle='none', label=column)
    axes[0, 0].set_title('ECDF')
    axes[0, 0].legend()
    
    # Histogram with shared range and bins
    axes[0, 1].hist(df[df.columns[0]], bins=bins, alpha=0.5, label=df.columns[0])
    axes[0, 1].hist(df[df.columns[1]], bins=bins, alpha=0.5, label=df.columns[1])
    axes[0, 1].set_title('Histogram')
    axes[0, 1].legend()
    
    # Boxplot
    axes[1, 0].boxplot([df[df.columns[0]], df[df.columns[1]]], labels=df.columns)
    axes[1, 0].set_title('Boxplot')
    
    correlation = df.corr().iloc[0, 1]
    print(f"Correlation: {correlation}")
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[df.columns[0]], df[df.columns[1]])
    r_squared = r_value**2
    print(f"R-squared: {r_squared}")
    
    # Heatmap of joint occurrence with equal axis
    joint_occurrence, xedges, yedges = np.histogram2d(df[df.columns[0]], df[df.columns[1]], bins=bins)
    masked_joint_occurrence = np.ma.masked_where(joint_occurrence == 0, joint_occurrence)
    cmap = plt.cm.viridis
    cmap.set_bad(color='white', alpha=0)
    axes[1, 1].imshow(np.flipud(masked_joint_occurrence),
                      cmap=cmap, interpolation='nearest', aspect='auto',
                      extent=[min_val, max_val, min_val, max_val])
    axes[1, 1].set_aspect('equal')
    
    # Adjusting tick labels for the heatmap
    # tick_labels = np.arange(min_val, max_val + 0.5, 1)
    # axes[1, 1].set_xticks(tick_labels)
    # axes[1, 1].set_yticks(tick_labels)
    # axes[1, 1].set_xticklabels([f"{x:.1f}" for x in tick_labels], rotation=90)
    # axes[1, 1].set_yticklabels([f"{y:.1f}" for y in tick_labels])
    axes[1, 1].set_title('Heatmap of Joint Occurrence')
    axes[1, 1].set_xlabel(list(df)[1])
    axes[1, 1].set_ylabel(list(df)[0])
    # Overlay R-squared value on the heatmap
    axes[1, 1].text(max_val, min_val, f'R² = {r_squared:.3f}', ha='right', va='bottom', color='black')
   

    plt.tight_layout()
    plt.show()
    
    

# %% IMPORTAR Y FORMATEAR DATOS
path_to_data = "//10.0.4.3/proyectos/M - Monitoreo en General/Procesamiento de datos"
latu_file = "Descarga_param_2024-02-09 13 08 25_1 (1).xlsx"
bettair_file = "BET00210084-Martín.xlsx"

# Diccionario de parámetros e ID para datos LATU
dict_params_latu = {2016:"PM_2.5",
                    2101:"NO2",
                    2235:"NO",
                    2106:"NOx",
                    2107:"SO2"}

# importar y formatear datos LATU
datos_LATU = pd.read_excel(f"{path_to_data}/{latu_file}",
                           sheet_name="Datos",
                           index_col=[0])
datos_LATU.index = pd.to_datetime(datos_LATU.index,
                                  format="%Y-%m-%d %H:%M:%S")
datos_LATU["Parametro_nombre"] = datos_LATU["Parametro"].map(dict_params_latu)

# Crear dataframes individuales para cada parámetro
datos_LATU_PM2P5 = pd.DataFrame(datos_LATU[datos_LATU["Parametro"]==2016]["Valor"].copy())
datos_LATU_PM2P5.rename(columns={"Valor":"PM2P5(µg/m³)"},inplace=True)
datos_LATU_NO2 = pd.DataFrame(datos_LATU[datos_LATU["Parametro"]==2101]["Valor"].copy())
datos_LATU_NO2.rename(columns={"Valor":"NO2(µg/m³)"},inplace=True)
datos_LATU_NO = pd.DataFrame(datos_LATU[datos_LATU["Parametro"]==2235]["Valor"].copy())
datos_LATU_NO.rename(columns={"Valor":"NO(µg/m³)"},inplace=True)
datos_LATU_NOx = pd.DataFrame(datos_LATU[datos_LATU["Parametro"]==2106]["Valor"].copy())
datos_LATU_NOx.rename(columns={"Valor":"NOx(µg/m³)"},inplace=True)  
datos_LATU_SO2 = pd.DataFrame(datos_LATU[datos_LATU["Parametro"]==2107]["Valor"].copy())
datos_LATU_SO2.rename(columns={"Valor":"SO2(µg/m³)"},inplace=True)

# Importar y formatear datos Bettair
datos_BETTAIR = pd.read_excel(f"{path_to_data}/{bettair_file}",
                              index_col=[0])
datos_BETTAIR.index = pd.to_datetime(datos_BETTAIR.index,format="%Y-%m-%d %H:%M:%S")
# Pasar a GMT -3 y deslocalizar fecha
datos_BETTAIR = datos_BETTAIR.tz_convert("Etc/GMT-3")
datos_BETTAIR = datos_BETTAIR.tz_localize(None)

# Crear dataframes individuales para cada parámetro
datos_BETTAIR_PM2P5 = pd.DataFrame(datos_BETTAIR['PM2P5(µg/m³)'].copy())
datos_BETTAIR_NO2 = pd.DataFrame(datos_BETTAIR['NO2(µg/m³)'].copy())
datos_BETTAIR_NO = pd.DataFrame(datos_BETTAIR['NO(µg/m³)'].copy())
datos_BETTAIR_NOx = pd.DataFrame(datos_BETTAIR_NO2.copy()+datos_BETTAIR_NO.copy())
datos_BETTAIR_NOx.rename(columns={"0":"NOx"},inplace=True)
datos_BETTAIR_SO2 = pd.DataFrame(datos_BETTAIR['SO2(µg/m³)'].copy())

# %% Remuestrear datos de LATU a 5 minutos SIN SACAR VALORES NEGATIVOS
datos_LATU_SO2_5min_con_negativos = pd.DataFrame(datos_LATU_SO2.resample("5T").mean().copy())
datos_LATU_NO2_5min_con_negativos = pd.DataFrame(datos_LATU_NO2.resample("5T").mean().copy())
datos_LATU_PM2P5_5min_con_negativos = pd.DataFrame(datos_LATU_PM2P5.resample("5T").mean().copy())
datos_LATU_NO_5min_con_negativos = pd.DataFrame(datos_LATU_NO.resample("5T").mean().copy())

# %% Juntar datos cada 5 minutos en dataframes para cada parámetro
# SO2 5 minutos
datos_SO2_5min_con_negativos = pd.merge(datos_LATU_SO2_5min_con_negativos,
                                        datos_BETTAIR_SO2,
                                        how="inner",
                                        left_index=True,right_index=True)
datos_SO2_5min_con_negativos.rename(columns={"SO2(µg/m³)_x":"LATU",
                                             "SO2(µg/m³)_y":"BETTAIR"},
                                    inplace=True)
datos_SO2_5min_con_negativos.dropna(inplace=True)

analyze_dataframe(datos_SO2_5min_con_negativos,"SO2 5 min (ug/m**3)")

# %% SO2 1 hora
datos_SO2_1h_con_negativos = datos_SO2_5min_con_negativos.resample("1h").mean().copy()
datos_SO2_1h_con_negativos.dropna(inplace=True)
analyze_dataframe(datos_SO2_1h_con_negativos,"SO2 1 h (ug/m**3)")

# %% SO2 24 horas
datos_SO2_24h_con_negativos = datos_SO2_5min_con_negativos.resample("24h").mean().copy()
datos_SO2_24h_con_negativos.dropna(inplace=True)
analyze_dataframe(datos_SO2_24h_con_negativos,"SO2 24 h (ug/m**3)")

# %% PM2P5 5 min
datos_PM2P5_5min_con_negativos = pd.merge(datos_LATU_PM2P5_5min_con_negativos,
                                        datos_BETTAIR_PM2P5,
                                        how="inner",
                                        left_index=True,right_index=True)
columns = list(datos_PM2P5_5min_con_negativos)
datos_PM2P5_5min_con_negativos.rename(columns={columns[0]:"LATU",
                                             columns[1]:"BETTAIR"},
                                    inplace=True)
datos_PM2P5_5min_con_negativos.dropna(inplace=True)

analyze_dataframe(datos_PM2P5_5min_con_negativos,"PM2.5 5 min (ug/m**3)")

# %% PM2P5 24 hora
datos_PM2P5_24h_con_negativos = datos_PM2P5_5min_con_negativos.resample("24h").mean().copy()
datos_PM2P5_24h_con_negativos.dropna(inplace=True)
analyze_dataframe(datos_PM2P5_24h_con_negativos,"PM2.5 24 h (ug/m**3)")

# %% NO2 5 min
datos_NO2_5min_con_negativos = pd.merge(datos_LATU_NO2_5min_con_negativos,
                                        datos_BETTAIR_NO2,
                                        how="inner",
                                        left_index=True,right_index=True)
columns = list(datos_NO2_5min_con_negativos)
datos_NO2_5min_con_negativos.rename(columns={columns[0]:"LATU",
                                             columns[1]:"BETTAIR"},
                                    inplace=True)
datos_NO2_5min_con_negativos.dropna(inplace=True)

analyze_dataframe(datos_NO2_5min_con_negativos,"NO2 5 min (ug/m**3)")

# %% NO2 1 hora
datos_NO2_1h_con_negativos = datos_NO2_5min_con_negativos.resample("1h").mean().copy()
datos_NO2_1h_con_negativos.dropna(inplace=True)
analyze_dataframe(datos_NO2_1h_con_negativos,"NO2 1 h (ug/m**3)")
















































				
