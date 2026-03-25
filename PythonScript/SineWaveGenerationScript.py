import numpy as np
import os



script_location = os.path.dirname(os.path.abspath(__file__))    # Finds directory of script (PythonScript)
script_root = os.path.dirname(script_location)                  # Finds parent directory of PythonScript (BowelProbe)
target_folder = os.path.join(script_root, "LTspiceSim")         # Enters child directory "LTspiceSim" in BowelProbe

os.makedirs(target_folder, exist_ok=True) # Create "LTspiceSim" if it doesn't exist yet


# --- AD9833 Config ---
freqs = [500, 1000, 2500, 5000, 10000]      # Waveform frequencies
mclk = 16e6                                 # AD9833 Master Clock (16 MHz)
dac_bits = 10                               # AD9833 DAC Resolution
Vpp = 0.600                                 # Nominal output voltage
V_dc = 0.300                                # DC offset voltage
sim_time = 0.500                            # Simulation duration (seconds)

# --- Calcuated Values ---
levels = 2**dac_bits # (2^10 = 1024 bits)
time_step = 1 / mclk

for f in freqs:
    filename = f"AD9833_{f}Hz.txt" # Makes file

    full_path = os.path.join(target_folder, filename)
    
    t = np.arange(0, sim_time, time_step) # Time array with start t = 0, stop at sim_time, step by time_step
    
    # Generate Ideal Sine
    sine = np.sin(2 * np.pi * f * t)
    
    # Normalize to [0,1] range
    sine_norm = (sine + 1) / 2
    
    quantized_DAC = np.floor(sine_norm * levels)     # Turns pure sine into stepping DAC
    quantized_sine = quantized_DAC / levels          # Normalize DAC wave to [0,1]
    
    Vout = (quantized_sine * Vpp) + V_dc


    # Write to PWL File for LTspice
    # Format: TIME (seconds) VOLTAGE (volts)
    
    # Stack time and voltage into two columns
    data = np.column_stack((t, Vout))

    # Write everything at once (C-engine speed)
    np.savetxt(full_path, data, fmt='%.9f %.6f')
    print(f"Done: {filename} ({len(t)} points)")

            
    print(f"Generated {filename}")