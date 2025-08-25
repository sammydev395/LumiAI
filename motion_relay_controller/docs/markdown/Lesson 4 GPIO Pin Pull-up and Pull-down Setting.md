Lesson 5 GPIO Pin Pull-up and
Pull-down Setting
1. GPIO Pin Introduction
GPIO (General Purpose Input/Output) port is a set of pins on the master of
electronic devices used to send and receive electronic signals. You can
connect these pins to external hardware devices to achieve functions for
external communication, external hardware control, or external hardware data
collection.

2. Pull-up and Pull-down Resistors Introduction
There are three statuses of pull-up, pull-down, and no pull in each GPIO. If
the GPIO is in output mode, it is usually set to no pull status, while pull-up and
pull-down settings are mainly used in input mode.
The purpose of a pull-up resistor is to ensure that the voltage level of the
input port is high when there is no signal input. When the input signal is low
voltage level, the voltage level of the input port is also low.
Without a pull-up resistor, the input port is floating and its voltage level is
unknown when there is no external input signal. The purpose of setting a
pull-up resistor is to ensure that the voltage of the input port is high level when
there is no input signal.
The purpose of a pull-down resistor is to ensure that the voltage of the
input port is low level when there is no input signal.

3. Raspberry Pi 5 GPIO Pin Introduction
Raspberry Pi 5 features a 40-pin header that allows for easy use with a
variety of expansion boards. GPIOD library can control these GPIO pins to
1

read, write, interrupt, PWM, etc.
The distribution diagram of the GPIO pins is as follows:

4. Input Reading
1) Import the program file “PULL_UP_DOWN.py” into the home directory
of the Raspberry Pi 5 system, as the diagram shown below:

2

2) Press “Ctrl+Alt+T” to open the command line terminal and enter the
“sudo python3 PULL_UP_DOWN.py” command, then press “Enter” to execute
the program.

3) After executing the program, pin17 will be set to input mode with a
pull-up resistor, and measured with a multimeter, showing a voltage value of
3.33v, representing the high voltage level.

5. Program Analysis

1) Import the necessary modules.

2) Initialize the GPIO controller and set the required GPIO port.

3

3) Set the pin17 to output mode, and use the “set_flags()” method to set
the pin17 to pull-up mode.

The “gpiod.LINE_REQUEST_FLAG_BIAS_PULL_UP” is the pull-up mode,
and the “gpiod.LINE_REQUEST_FLAG_BIAS_PULL_DOWN” is the pull-down
mode.

4

