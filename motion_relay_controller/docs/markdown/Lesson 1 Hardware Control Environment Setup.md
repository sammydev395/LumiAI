Lesson 1 Hardware Control
Environment Setup
1. GPIO Brief Introduction
GPIO (General Purpose Input/Output) port on Raspberry Pi is a set of pins
used for connecting and controlling external electronic components. It is
provided with multiple functions and can be used as digital and analog inputs
and outputs.

2. GPIO Port Introduction
Raspberry Pi 5 features a 40-pin GPIO header with a voltage of 3.3v.
Therefore, you should avoid connecting any voltage level higher than 3.3v to
the GPIO pins on the Raspberry Pi 5 without using a voltage level converter.
The functions of GPIO pins are shown in the following diagram:

1

3. GPIO Library Installation
Raspberry Pi GPIOD library is a user-space library used to control the
GPIO (General Purpose Input/Output) pins. It is based on the GPIOLIB
abstract layer of the GPIO character device interface in the Linux kernel with a
simple and flexible API. This allows developers to easily use C language and
other programming languages to configure and control GPIO. Here is a
demonstration of how to install the GPIOD library.
1) Press “Ctrl+Alt+T” to open the command line terminal, then enter
“pinout” and press “Enter” to view the pin numbers.

2

2) Enter the “sudo apt-get update -y && sudo apt-get upgrade -y”
command to update the operation system and software packages.

3) Enter the “sudo apt-get autoremove -y && sudo apt-get autoclean -y
3

&& sudo apt-get clean -y” command to clean the unnecessary software
packages and cache files in the system.

4) Enter the “sudo apt-get remove --purge --auto-remove firefox geany -y”
command to clean “Firefox” and “Geany” software packages in the system.

5) Enter the “sudo apt-get install -y vim git terminator htop curl
python3-opencv gedit libjpeg-dev xclip wl-clipboard” command to install
multiple software packages.

6) Enter the “mkdir ~/.pip” command to create a directory named “.pip” in
home directory.

4

7) Enter the “vim ~/.pip/pip.conf” command to open the “pip.conf” file.

8) Press the “i” key to enter the editable mode and enter the following
code.

5

9) After that, press “Esc” key to enter the “:wq”, then press “Enter” to save
the file and exit.

10) Enter the “pip3 install gpiod” command to install the “gpiod” Library.

11) After the installation is complete, enter the “gpiodetect” to scan the
GPIO port in the system. If the installation is successful, you can see the
corresponding information about the GPIO controller and the port.

6

