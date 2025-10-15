# Mod-8-Up-Counter---TinkerCAD
# Functionality:
## This document explains the Arduino code for simulating a mod8 up counter using the digitalWrite function.
![Copy of Lesson 1 - Blinking LED](https://github.com/Samanthapudi-Shakeer/Mod-8-Up-Counter---TinkerCAD/blob/main/Copy%20of%20Lesson%201%20-%20Blinking%20LED.png)
Counts from 0 to 7 in a loop.
Outputs the counter value on three digital pins.
Resets to 0 when the count reaches 8 (mod8 behavior).
# Hardware Requirements:

Three D Flip-flops or JK Flip-flops (connected as a 3-bit counter)
Resistors (values depend on the specific flip-flops used)
Breadboard and jumper wires
LEDs (optional, for visualization) - Each LED cathode (negative terminal) goes to a resistor, and the anode (positive terminal) goes to a corresponding flip-flop output (Q).
# Software:

This code assumes you have the hardware components connected correctly. It generates clock pulses and sets up feedback connections within the flip-flops to achieve the counting behavior.

# Code Breakdown:

## Pin Definitions:
CLOCK_PIN: Pin connected to the clock input of the first flip-flop.
Q0_PIN, Q1_PIN, Q2_PIN: Pins connected to the outputs (Q) of the three flip-flops.
setup Function:
Configures CLOCK_PIN and output pins (Q0_PIN, Q1_PIN, Q2_PIN) as outputs for the clock and counter outputs, respectively.
loop Function:
Generates a short clock pulse using digitalWrite to trigger the flip-flops.
The actual counter logic is implemented through the hardware connections themselves (no code required in the loop). The feedback connections between the flip-flops ensure proper counting behavior.
Optional: LEDs for Visualization:

Connect LEDs (with resistors) to the output pins (Q0_PIN, Q1_PIN, Q2_PIN) to visualize the binary representation of the counter value. The LED will be lit when the corresponding flip-flop output is HIGH.

Important Notes:

Ensure the flip-flops and resistors are connected as described for a 3-bit counter with proper feedback connections. Consult the datasheets of your specific flip-flops for details.
Adjust the delayMicroseconds value in the code (if used) based on your clock requirements and flip-flop characteristics.
Consider using pull-up or pull-down resistors on the data inputs of the flip-flops if required by their datasheets.
