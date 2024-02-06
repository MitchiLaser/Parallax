#!/usr/bin/env python3

"""
# This script is used to calculate the resistor ratios for the hardware layout of the Parallax oscilloscope
# In the beginning all the input ranges are defined for the analog inputs in the list $In_Ranges$
# These have to be mapped to a voltage between 0V and $U_{max}$.
# The script calculates the resistor and capacitor ratio for the attenuator.

# Afterwards it compares all the input ranges with the largest one in the list and calculates
# the gains for the op-amp and the reference voltage for all the input ranges.

"""


# ########## Initial value definition ##########

# define the input voltage ranges
# this scripts expects the ranges to be symmetrical e.g. 15V means the range goes from -15V to +15V
In_Ranges = [15, 5, 2, 0.5]  # all values in Volts

# define the input range of the ADC. The minimum ADC input voltage is expected to be Ground
U_max = 3  # 3 V, better than 3,3 V because for 3 V the resistor values are closer to real resistors and there is some margin before the clamping diodes kick in

# define the reference voltage for the ADC to get the middle in between the ADC range
U_aref = 3.3  # 3,3 V


# print the input rages as the first information
print(f"Input ranges: {In_Ranges}")

# calculate the resistor and capacitor ratio for the attenuator
Attenuator_Resistor_ratio = (2 * max(In_Ranges)) / U_max - 1  # R_1 / R_2
print(f"Resistor ratio: R_1 / R_2 = {Attenuator_Resistor_ratio}")

# the amplifier has to map a smaller voltage range to the range of the maximum input voltage since the attenuator stays the same for each input range
amp_gains = [max(In_Ranges) / i for i in In_Ranges]
print(f"Values for the amplifier gains: {amp_gains}")

# the offset voltage needs to be calculated for each individual input range
# if only one would be used then this will interfere with the Op-Amp also amplifying the baseline
offsets = [i / Attenuator_Resistor_ratio for i in In_Ranges]
print(f"Offset Voltages: {offsets}")

# correct the offsets to be in the middle:
corrected_offsets = [(U_aref / (2 * amp_gains[i])) * (1 / Attenuator_Resistor_ratio + 1) for i in range(len(In_Ranges))]
print(f"Corrected offset: {corrected_offsets}")

# now calculate the resistor ratios for the voltage follower providing the offset voltage
resistor_ratios = [U_aref / i - 1 for i in corrected_offsets]
print(f"Resistor ratios for the offset voltages: R_a / R_b = {resistor_ratios}")
