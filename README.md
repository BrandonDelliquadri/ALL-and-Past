# README
For installation and use of a test implementation of ALL and Past.
## Written by:
Brandon Delliquadri - brandon@delliquadri.com

## Specifications:
Warning to future users: 
ALL, which runs using python, had some trouble running and downloading libraries on some IDEs.

We reccomend the following to run ALL:
* Pycharm 2020
* Python version 3.6

## Installation:
1) Download all files from this github
2) Open the ALL folder as a project in Pycharm
3) Open baseline.py and ensure that all of the import statements are installed
a. Some IDEs had issues installing pandas and torch so if it doesn't work try a different IDE or python version
4) Run ALL by itself to make sure it can run independently
## Before Running
There are a few imperative pieces of information and instructions before running the system.
* Run "ipconfig" in a command prompt and note down your IPv4 address in the "Ethernet adapter VirtualBox Host-Only Network:" section
	* This will be used to run Past
* Open PastTutorial.java in the PAST files and change lines 220 and 257 to be the root directory of ALL on your system
	* After doing this, export PAST to a jar file
* Make sure a PAST jar, "xmlpull_1_1_3_4a.jar", and "xpp3-1.1.3.4d_b2.jar" are installed
	* These should be included with the github files already
* **If you are trying to run the implementation**
	* In ALL's baseline.py change line 20 testing = true
		* When Testing is enabled ALL will pause multiple times to wait for user input to ensure that Past has finished it's processes (This will be detailed further in the running section)

## Running
It is important to note that ALL and Past do not work together automatically and will need someone to manually start Past, send matrices to Past, and recieve matrices from Past. This is all done via command prompt that will be explained in the following steps.
**Steps to run**
1) If necessary make any alterations baseline.py. There are 3 variables that make testing flexable including: epoch_num, times, and mod.
2) Run ALL from your IDE
3) ALL console will ask you to press enter once Past has been run. We will do that in the next step.
4) Open command prompt and cd to the 3 jars mentioned in the before running section
5) Run Past with the following command:
a) java -cp "[name of your Past.jar];xmlpull_1_1_3_4a.jar;xpp3-1.1.3.4d_b2.jar" rice/tutorial/past/PastTutorial [port] [Virtualbox ip address] [port] [number of nodes]
b) Example: java -cp "OmegaPastJar-2.1.jar;xmlpull_1_1_3_4a.jar;xpp3-1.1.3.4d_b2.jar" rice/tutorial/past/PastTutorial 9001 192.168.56.1 9001 2
6) Assuming Past ran successfully press enter back on ALL to have it start training a model
7) ALL, depending on mod integer, will ask the user to use Past to send the matrix to the nodes.
a) To do this just type "1" and press enter on the command prompt running Past. This will get the matrix automatically from the folder you set in line 220 of PastTutorial.java
8) After some time ALL may ask to receive a matrix (this is a simulation of matrix loss)
a) To do this just type "2" and press enter on the command prompt running Past. This will automatically write a new input file
9) Press enter back on ALL to continue the process
a) ALL will automatically read the new file using torch.load
10) Continue steps 7-9 until ALL is complete

## After Running
Output matrix will hold the content of the most recent matrix and the output of the ALL system (including some performance metrics) will be saved in result folder.

