# CMPSC 472 Project: Advanced Process Manager
___

CMPSC 472 Project #1

Instructor: Janghoon Yang

Advanced Process Managment

Student Name: Joshua Murillo


 
## Project Overview:

The purpose of this project is to design and implement an advanced Process Manager. The Project Manager will emphasize process synchronization and allow users to interact with the Project Manager through creating, management, and synchronization of a multithreaded environment. The Project Manager should provide these functions to a user via a command-line user interface that uses system calls for the processing and threading control. This projects includes the source code for the Project Manager and a Project report listed as the readme of this repository.


## Implimented Features:
### 1. Process Creation:
- Preocess Creation Mechanism that allows users to create new processes.
  - Done using system calls for preocess creation (Ex. fork(), exec()).
### 2. Process Management:
- List preocesses.
- Terminate processes.
- Monitor currently running processes.
- Allows users access to information about running processes (Ex. process id (PID), parent process id, and current state).
### 3. Thread Support:
- Process Manager supports multiple threads.
- Includes thread mechanisms of:
  - Creation.
  - Termination.
  - Synchronization
- Uses system calls for thread creatioon (Ex. pthread_create) and synchronization (Ex. mutexes, semaphores)
### 4. Inter-Process Communication (IPC):
- Impliments IPC mechanisms for the purpose of allowing processes and threads to communicate and share data.
- Possable methodesinclude, **message passing, shared memory, or pipes** for IPC.
- Uses system calls for IPC operations (Ex. pipe, msgget, shmget)
### 5. Process Synchronization:
- Impliments synchronization primitives like mutexes and semaphores.
- Uses synchronization mechanics to address issues such as producer-consumer and reader-writer problems
### 6. Command-Line Interface (CLI):
- Showcases a user-frendly interface to interact with the process manager.
- UI allows users to create preocesses and threads and allows for the synchronization of threads and use of IPC operations.
### 7. Logging and Reporting:
- Impliments logging and reporting features to track and display the execution of preocesses and threads.
- Used to log significant events, error, and process synchronization related information.

## How to run the Preocess Manager:

## Process Manager Feature Testing:

## Process Manager Project Result:
