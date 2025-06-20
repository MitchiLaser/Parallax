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

# The internal resistor of the multiplexer
resistor_multiplexer = 100


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

# Now find the right resistors from the E48 row
E48 = [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53]
Resistors = sorted([E48[i] * 10**j * 1000 for i in range(len(E48)) for j in range(3)])  # E48 resistors in kOhm, from 1 Ohm to 9.53 kOhm

# There are the following parameters that need to be optimized:
# 1. The attenuator resistors, just take two with the right ratio and it will work for all input ranges.
best = [0, 0]
for i in range(len(Resistors)):
    for j in range(i + 1):
        if abs(Resistors[i] / Resistors[j] - Attenuator_Resistor_ratio) < abs(Resistors[best[0]] / Resistors[best[1]] - Attenuator_Resistor_ratio):
            best = [i, j]
print(f"\nBest resistors for Attenuator: {round(Resistors[best[0]] / 1000, round_prec)} kΩ and {round(Resistors[best[1]] / 1000, round_prec)} kΩ, ratio: {round(Resistors[best[0]] / Resistors[best[1]], round_prec)}")

# 2. The two resistors for the reference voltage. One of them is fixed ant the others should match the calculated ratios.
# R_a is the fixed resistor and R_b is attache to the multiplexer
best_fixed = 0
best_variable = [0, 0, 0, 0]
for i in range(len(Resistors)):
    current_best = [0, 0, 0, 0]
    for j in range(len(Resistors)):
        # This is the possible second resistor for all of the input ranges
        for k in range(len(resistor_ratios)):
            # check each range if the current resistor combination is closer to the desired ratio
            if abs(Resistors[i] / (Resistors[j] + resistor_multiplexer) - resistor_ratios[k]) < abs(Resistors[i] / (Resistors[current_best[k]] + resistor_multiplexer) - resistor_ratios[k]):
                current_best[k] = j
    # This print statement was useful during development to see the progress
    # print(f"Fixed: {Resistors[i]}, Variable / Ratio:    {"    ".join([str(round(Resistors[j] / 1000, round_prec)) + ' kΩ » ' + str(round(Resistors[i] / (Resistors[j] + resistor_multiplexer), round_prec)) for j in current_best])}")
    # calculate the sum of error squares and compare with the currently best result
    error_squares = sum([(Resistors[i] / (Resistors[current_best[j]] + resistor_multiplexer) - resistor_ratios[j])**2 for j in range(len(resistor_ratios))])
    error_best = sum([(Resistors[best_fixed] / (Resistors[best_variable[j]] + resistor_multiplexer) - resistor_ratios[j])**2 for j in range(len(resistor_ratios))])
    # These two print statements were useful during development to see the progress
    # print(f"Current Error: {error_squares}, Error Best: {error_best}")
    # print("")
    if error_squares < error_best:
        best_fixed = i
        best_variable = [j for j in current_best]
print("\nBest choices for the reference voltage:")
print(f"Fixed resistor: {round(Resistors[best_fixed] / 1000, round_prec)} kΩ")
print(f"Variable resistors and Ratios: {''.join(['\n\t' + str(round(Resistors[i] / 1000, round_prec)) + ' kΩ    ' + str(round(Resistors[best_fixed] / (Resistors[i] + resistor_multiplexer), round_prec)) for i in best_variable])}")

# 3. The two resistors for the attenuator, where one of them is close to infinitely high
# The resistor ratio should be calculated with the following relation: Ratio[i] = Amp_gains[i] - 1
# because this is a non inverting amplifier (Equation 1.17)
target_ratios = [i - 1 for i in amp_gains]
print(f"Target Ratios: {', '.join([str(i) for i in target_ratios])}")
best_fixed = 0
best_variable = [0, 0, 0, 0]
# the first resistor is fixed whereas the second one is variable
for i in range(len(Resistors)):
    current_best = [0, 0, 0, 0]
    for j in range(len(Resistors)):
        # This is the possible second resistor for all amplifier gains
        for k in range(len(target_ratios)):
            # check for each target gain if the current resistor combination is closer to the desired ratio
            if abs(Resistors[i] / (Resistors[j] + resistor_multiplexer) - target_ratios[k]) < abs(Resistors[i] / (Resistors[current_best[k]] + resistor_multiplexer) - target_ratios[k]):
                current_best[k] = j
    # This print statement was useful during development to see the progress
    # print(f"Fixed: {Resistors[i]}, Variable / Ratio:    {"    ".join([str(round(Resistors[j] / 1000, round_prec)) + ' kΩ » ' + str(round(Resistors[i] / (Resistors[j] + resistor_multiplexer), round_prec)) for j in current_best])}")
    error_squares = sum([(Resistors[i] / (Resistors[current_best[j]] + resistor_multiplexer) - target_ratios[j])**2 for j in range(len(target_ratios))])
    error_best = sum([(Resistors[best_fixed] / (Resistors[best_variable[j]] + resistor_multiplexer) - target_ratios[j])**2 for j in range(len(target_ratios))])
    # These two print statements were useful during development to see the progress
    # print(f"Current Error: {error_squares}, Error Best: {error_best}")
    # print("")
    if error_squares < error_best:
        best_fixed = i
        best_variable = [j for j in current_best]
print("\nBest choices for the amplifier gains:")
print(f"Fixed resistor: {round(Resistors[best_fixed] / 1000, round_prec)} kΩ")
print(f"Variable resistors and Ratios: {''.join(['\n\t' + str(round(Resistors[i] / 1000, round_prec)) + ' kΩ    ' + str(round(Resistors[best_fixed] / (Resistors[i] + resistor_multiplexer), round_prec)) for i in best_variable])}")
