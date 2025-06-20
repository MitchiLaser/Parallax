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

# rounding_precision in decimal places
round_prec = 8


# calculate the resistor and capacitor ratio for the attenuator
# see equation 1.12 in the documentation
Attenuator_Resistor_ratio = (2 * max(In_Ranges)) / U_max - 1  # R_1 / R_2
print(f"Resistor Ratio for the Attenuator: R_1 / R_2 = C_2 / C_1 = {Attenuator_Resistor_ratio}")

# the amplifier has to map a smaller voltage range to the range of the maximum input voltage since the attenuator stays the same for each input range
# for the largest input range the factor is 1, all the others need to be scaled to match the highest range.
amp_gains = [max(In_Ranges) / i for i in In_Ranges]

# Offset voltage to map the input signal after the attenuator
# into the range 0V -> 3V (U_max)
# This offset is also amplified, so it needs to be calculated individually
# for each input range.
# Equation 1.15 in the documentation
offsets = [i / Attenuator_Resistor_ratio for i in In_Ranges]

# correct the offsets to be in the middle.
# Originally the offset is calculated to be in the middle between 0V and U_max, but
# U_max is lower than the reference voltage U_aref.
# Now: Correct the offset so that the input signal is exactly in the middle of the ADC range,
# which is U_aref / 2, but keep the input range still in the range of 0V to U_max.
# This gives a small window between GND and a 0V input and a second window between U_max and U_aref.
# The calculus is a little more complicated: It maps a 0V input to (U_aref / 2) * (1 / gain), because the signal is amplified:
#    U_+ * R_1 / (R_1 + R_2) = U_Aref / (2 * gain[i])  (modification of eq. 1.4 with U_in = 0V)
# This can be rearranged to:
# U_+ = (U_aref / (2 * gain[i])) * (1 + 1 / Attenuator_Resistor_ratio)
corrected_offsets = [(U_aref / (2 * amp_gains[i])) * (1 + 1 / Attenuator_Resistor_ratio) for i in range(len(In_Ranges))]

# now calculate the resistor ratios for the voltage divider
# to generate the corrected offset voltage from the 3.3V voltage source (= U_aref)
# You can use the voltage divider equation U_reference_corrected = U_aref * R_2 / (R_1 + R_2)
# and restructure it to get the resistor ratio R_1 / R_2:
#    R_1 / R_2 = U_aref / U_reference_corrected - 1
resistor_ratios = [U_aref / i - 1 for i in corrected_offsets]


def print_results_table(lists: list[list], titles: list[str]) -> None:
    print("┌─" + '─┬─'.join(["─" * len(i) for i in titles]) + "─┐")
    print("│ " + ' │ '.join(titles) + " │")
    print("├─" + '─┼─'.join(["─" * len(i) for i in titles]) + "─┤")
    for i in range(max([len(i) for i in lists])):
        print("│ " + ' │ '.join([str(round(lists[j][i], round_prec)) + " " * (len(titles[j]) - len(str(round(lists[j][i], round_prec)))) for j in range(len(lists))]) + " │")
    print("└─" + '─┴─'.join(["─" * len(i) for i in titles]) + "─┘")


print_results_table(
    [
        In_Ranges,
        amp_gains,
        offsets,
        corrected_offsets,
        resistor_ratios
    ],
    [
        "Input Range",
        "Amplifier Gain",
        "Offset Voltage",
        "Corrected offset Voltage",
        "R_a / R_b corr. Offset"
    ]
)
