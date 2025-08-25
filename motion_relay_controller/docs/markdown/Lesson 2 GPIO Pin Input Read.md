Lesson 2 GPIO Pin Input Reading
1. GPIO Pin Introduction
GPIO (General Purpose Input/Output) port is a set of pins on the master of
electronic devices used to send and receive electronic signals. You can
connect these pins to external hardware devices to achieve functions for
external communication, external hardware control, or external hardware data
collection.

2. Input Introduction
GPIO input detects each pin’s voltage level status, which is classified as
either high or low. A high level represents the presence of voltage represented
by the numerical symbol “1”, and a low level typically refers to GND
represented by the numerical symbol “0”.

3. Raspberry Pi 5 GPIO Pin Introduction
Raspberry Pi 5 features a 40-pin header that allows for easy use with a
variety of expansion boards. GPIOD library can control these GPIO pins to
read, write, interrupt, PWM, etc.
The distribution diagram of the GPIO pins is as follows:

1

4. Input Reading
1) Import the program file “GPIO_IN.py” into the home directory of the
Raspberry Pi 5 system.

2) Press “Ctrl+Alt+T” to open the command line terminal and enter the
“sudo python3 GPIO_IN.py” command, then press “Enter” to execute the
2

program.

3) After executing the program, it prints the input data of pin17. A voltage
input will be represented as “1”, while no voltage input will be represented as
“0”. Press “Ctrl+C” to stop running the program.

5. Program Analysis

1) Import the necessary modules.
2) Initialize the GPIO controller and set the required GPIO port.
3) Use the “line.get_value()” method to read the status of GPIO pin17.
4) Release the GPIO port and close the GPIO controller at the end.
3

