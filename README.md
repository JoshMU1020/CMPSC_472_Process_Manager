# CMPSC 472 Project: Advanced Process Manager
___

CMPSC 472 Project #1

Instructor: Janghoon Yang

Advanced Process Managment

Student Name: Joshua Murillo

## Project Overview:

This project was assigned as an assignment from my CMPSC 472, Operating Systems class. The purpose of this project is to design and implement an advanced Process Manager. This Project Manager will emphasize process synchronization and allow users to interact with the Project Manager through the creation, management, and synchronization of a multithreaded environment. The Project Manager should provide these functions to a user via a command-line user interface that uses system calls or system call-like functions provided by various libraries for the processing and threading control. This repository is to include the source code for the Project Manager and a Project report listed as the readme of this repository.

## Implimentation Process:
When designing this process manager, I looked at the individual requirements and looked for various Python libraries that showcased similar functionalities to what the project's requirements described. The libraries that stuck out the most to me were the os, threading, multiprocessing, subprocess, and pstil python libraries. These libraries showcased examples of functionalities that greatly resembled the related topics that I was tasked with showing in my process manager implementation despite the limitations of the Python language with regard to process management. That said, when testing some of these libraries' functionalities, I ran into a number of issues with my initial Windows development environment. Some libraries, such as the os and psuitl libraries, could not access all of their functions as they were not compatible with the Windows environment system. I attempted to design my process manager implementation in both Google Colab and Jupiter notebooks environments but fell into some issues with trying out the libraries there as well. In the end, I found success when attempting to develop the software on a Linux machine where all of the libraries that I wanted to incorporate into my software were available with full functionality. 

## Implimented Features:
The following describe the extent of the implimentations of the concepts that were expected to be implimented into my process manager software.

### 1. Process Creation:
Process creation is initiated in the **create_and_start_process** method. It allows the program to start new processes, either with or without threading depending on what the user desires. By default, the 'Create' function create a process based on a build-in **worker_function**. This function will, if the 'default.py' script is discoverable, create a process based on the contents of that program as a subprocess. Otherwise, if the external files are not found, the **worker_function** will fall back to the built in process representation comprized of a sleep function to simulate the process running and doing work. Users can choose to create processes with the default settings or specify a custom Python script file with the option to use threading or not.

### 2. Process Management:


### 3. Thread Support:
This process manager demonstrates support for threading within processes. Threading is simulated in the **create_and_start_process** function where a variable is assigned to a randomly generated value representing the amount of items/data that a process may want to manipulate. This process, if the user specifies, can then be created to use this variable to create threads to acquire use, and release resources by implementing Process Synchronization which will be described further below.

### 4. Inter-Process Communication (IPC):


### 5. Process Synchronization:


### 6. Command-Line Interface (CLI):


### 7. Logging and Reporting:


## How to run the Preocess Manager:
This repository showcases a number of files that relate to the process manager. That said, The ony file that primarily matters is the Process_manager.py file. This file was designed to be able to work on its own using a built in worker function to simulate the work of processes functioning with various time requirements. In order to run the project itself, there are two main methods of doing so.

**OPTION ONE:**

The best way to test the project is right in GitHUb codespaces. The repository should first be forked, then the user can run a codespace to access a bash terminal where the user can input the initiating command line interface command, "python Process_Manager.py --begin". This command with initiate the class and prompt the user to begin using the process manager to create and monitor processes. This method is prefered as both the main program and the optional subprocess simulating programs are all in the same directory, so they are easy to locate and use.

**OPTION TWO:**

The other way of using the process manager, is by downloading the Process_Manager.py file to your local machine and running it in a linux terminal. To do this, you will need to open the terminal and verify that you have python 3 and pip installed. If not, you will need to aquire them. Once you have python and pip, do:

pip install --upgrade pip

pip install psutil

Once complete, in the terminal, change to the directory where the Process_Manager.py file is located. Then, similar to before, you can type "python3 Process_Manager.py --begin". Keep in mind that some linux terminals will need to have 'python3' specified before the command instead of just 'python'. Now you should be able to run the project just as you would in codespaces with one difference. If you wanted to use the optional subprocess simulating programs, you will need to also download them and keep note of what directory they are in. If this is done, then when prompted, teh user can select "Create Other" from the command line menu and if desired, will be able to input either "path/to/default.py" or "path/to/other_process.py" to create a subprocess based on either of thoese files. **NOTE:** The way the the Process_Manager.py file is set up, you can write the path to any .py file to create a proces based on the at python file, it may not work correctly for other files. It should still fuction and create a psudo process out of that call though, so long as the directory exists as a .py file since it is creating is as a subprocess. 

Of these two methods, the safest way to test this code out for yourself is through codespaces.

## Process Manager Feature Testing:
### 1. Testing Process Creation:

### 2. Testing Process Management:

### 3. Testing Thread Support:

### 4. Testing Inter-Process Communication (IPC):

### 5. Testing Process Synchronization:

### 6. Testing Command-Line Interface (CLI):

### 7. Testing Logging and Reporting:


## Project Results:
