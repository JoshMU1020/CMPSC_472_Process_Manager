import os  # python .\print.py.txt
import threading
import multiprocessing
import time
import logging
import psutil
import random
import queue
import argparse
import subprocess


class ProcessManager:
    def __init__(self):
        self.processes = []
        self.process_pids = []
        self.threads = []

        self.queue = multiprocessing.Queue()
        self.thread_message_queue = multiprocessing.Queue()

        self.BUFFER_SIZE = 5
        self.buffer = []
        self.buffer2 = []
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(self.BUFFER_SIZE)
        self.data = threading.Semaphore(0)
        self.total_items = 0

    def worker_function(self, interp):
        if interp is not None:
            logging.info(f"Worker process PID: {os.getpid()}")
            duration = 60
            process = subprocess.Popen([interp, "sleep.py", str(duration)], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        else:
            time.sleep(5)
            logging.info(f"Worker process PID: {os.getpid()}")
            return
        return

    def create_and_start_process(self, uses_t):
        logging.info("Creating new process...")
        self.total_items = random.randint(2, 5) * 4  # Randomly generate the number of data items

        interp_path = "./"
        ans = input("Do you wish to run the standard file [y/n]: ")
        if ans.lower() == 'y':
            pass
        elif ans.lower() == 'n':
            ans = input("Do you wish to run the another file [y/n]: ")
            if ans.lower() == 'y':
                interp_path = str(input("Enter path to .py file you wish to run: "))
            else:
                interp_path = None

        if not uses_t:
            new_process_instance = multiprocessing.Process(target=self.worker_function, args=(interp_path,))
        else:
            new_process_instance = multiprocessing.Process(target=self.synchronize_threads)

        new_process_instance.start()

        # Get the process PID before starting it
        process_pid = new_process_instance.pid
        print("\nPID IS:", process_pid)
        print("NEW PROCESS:", new_process_instance)

        self.process_pids.append(process_pid)
        print(self.process_pids)
        self.processes.append(new_process_instance)

        logging.info(f"Process created with PID: {process_pid}")

        self.queue.put(f"Data from Process {process_pid}")  # Add data to the IPC queue
        return new_process_instance

    def get_process_info_by_pid(self, target_pidi):
        try:
            process = psutil.Process(target_pidi)
            if process.is_running():
                logging.info(f"Process {target_pidi} exists and is still running.")
                return f"Process {target_pidi} exists and is still running."
            else:
                logging.info(f"Process {target_pidi} exists and has completed.")
                return f"Process {target_pidi} exists and has completed."
        except psutil.NoSuchProcess:
            logging.info(f"Process {target_pidi} does not exist.")
            return f"Process {target_pidi} does not exist."

    def process_management_list(self):
        logging.info(f"Process list of ran/running processes.")
        process_info_list = []
        for p_id in self.processes:
            try:
                process = psutil.Process(p_id.pid)
                process_info = {
                    "PID": process.pid,
                    "Status": process.status(),
                    "Parent PID": process.ppid(),
                }
                process_info_list.append(process_info)
            except psutil.NoSuchProcess:
                # Handle the case where the process is not found
                logging.error(f"Process with PID {p_id.pid} not found.")
        return process_info_list

    def terminate_process(self, targeted_pid):
        logging.info(f"Attempting to delete process with PID: {targeted_pid}")
        for process in self.process_pids:
            if process.pid == targeted_pid:
                if process.is_alive():
                    process.terminate()
                    process.join()
                    self.process_pids.remove(process)
                    logging.info(f"Process {targeted_pid} has been forcibly terminated.")
                    return f"Process {targeted_pid} has been forcibly terminated."
                else:
                    logging.info(f"Process {targeted_pid} is already completed.")
                    return f"Process {targeted_pid} is already completed."
            else:
                logging.info(f"Process {targeted_pid} not found in the list of processes.")
                return f"Process {targeted_pid} not found in the list of processes."

    def terminate_all(self):
        logging.info("Attempting to terminate all processes")
        for process in self.process_pids:
            if process.is_alive():
                process.terminate()
                process.join()
                self.process_pids.remove(process)
                logging.info(f"Process {process.pid} has been forcibly terminated.")
            else:
                logging.info(f"Process {process.pid} is already completed.")
        return

    def synchronize_threads(self):
        logging.info("Synchronizing Threads")
        producers = [
            threading.Thread(target=self.producer, args=(self.buffer, self.mutex, self.empty, self.data, 1, 100, 1))
        ]
        consumers = [
            threading.Thread(target=self.consumer, args=(self.buffer, self.mutex, self.empty, self.data, 1)),
            threading.Thread(target=self.consumer, args=(self.buffer, self.mutex, self.empty, self.data, 2))
        ]
        for producer_thread in producers:
            producer_thread.start()
        for consumer_thread in consumers:
            consumer_thread.start()

        time.sleep(5)

        for producer_thread in producers:
            producer_thread.join()
        for consumer_thread in consumers:
            consumer_thread.join()

    def producer(self, buffer, mutex, empty, data, min_value, max_value, pro_id):
        logging.info("Creating producer...")
        for i in range(self.total_items):
            item = random.randint(min_value, max_value)
            logging.info("Aquiring resources...")
            empty.acquire()
            mutex.acquire()
            buffer.append(item)
            logging.info(f"Producer {pro_id} Produced {item}. Buffer: {buffer}")
            logging.info("Releasing resources...")
            mutex.release()
            data.release()
            time.sleep(random.uniform(0.1, 0.5))

    def consumer(self, buffer, mutex, empty, data, con_id):
        logging.info("Creating consumer thread...")
        for i in range(self.total_items // 2):
            logging.info("Aquiring resources...")
            data.acquire()
            mutex.acquire()
            if buffer:
                item = buffer.pop(0)
                logging.info(f"Consumer {con_id} Consumed {item}. Buffer: {buffer}")
            logging.info("Releasing resources...")
            mutex.release()
            empty.release()
            time.sleep(random.uniform(0.1, 0.5))

    def send_message(self, message):
        """Simulate one thread sending a message to another."""
        self.thread_message_queue.put(message)
        logging.info(f"Thread {threading.current_thread().ident} sent a message: {message}")

    def receive_message(self):
        """Simulate one thread receiving a message from another."""
        try:
            message = self.thread_message_queue.get_nowait()
            logging.info(f"Thread {threading.current_thread().ident} received a message: {message}")
        except queue.Empty:
            logging.info(f"Thread {threading.current_thread().ident} received no messages.")

    def ipc_operations(self):
        logging.info("Displaying IPC Operations Menu...")
        print("\nIPC Operations Menu:")
        print("1. Message Passing (Between Threads)")
        ipc_choice = input("Enter your choice: ")

        if ipc_choice == '1':
            # Start a few threads to simulate sending and receiving messages
            thread1 = threading.Thread(target=self.send_message, args=("Hello from Thread 1!",))
            thread2 = threading.Thread(target=self.receive_message)

            thread1.start()
            time.sleep(1)
            thread2.start()
            thread1.join()
            thread2.join()

    def display_log_contents(self, log_file):
        try:
            with open(log_file, 'r') as file:
                log_contents = file.read()
                print(log_contents)
        except FileNotFoundError:
            print(f"Log file '{log_file}' not found.")

    # Save process PIDs to a file
    def save_process_pids(self, filename, process_pids):
        with open(filename, 'w') as file:
            for pid in process_pids:
                file.write(f"{pid}\n")

    # Load process PIDs from a file
    def load_process_pids(self, filename):
        try:
            with open(filename, 'r') as file:
                return [int(line.strip()) for line in file]
        except FileNotFoundError:
            return []


if __name__ == '__main__':
    manager = ProcessManager()

    logging.basicConfig(filename='process_manager.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    with open('process_manager.log', 'w'):
        pass

    # Initialize the ArgumentParser
    parser = argparse.ArgumentParser(description='Process Manager CLI')
    # Define command-line arguments and their descriptions
    parser.add_argument('--begin', action='store_true', help='Begin instance of Process Manager')
    parser.add_argument('--log', action='store_true', help='View log report')
    parser.add_argument('--exit', action='store_true', help='End program')

    # Parse the command-line arguments
    args = parser.parse_args()

    print("\nEnter your command in the form of 'python Process_Manager.py --begin'\n")

    if args.begin:
        while True:
            time.sleep(1)
            logging.info("Displaying Process Manager Menu...")
            print("\n Process Manager Menu:")
            print("Command List : Operation")
            print("------------------------")
            print("1) create       : Create a new process")
            print("2) manage       : Manage created processes")
            print("3) threads      : Manage threads")
            print("4) log          : View log report")
            print("5) exit         : End program")

            choice = input("Enter your choice: ")

            if choice == '1':
                new_process = manager.create_and_start_process(False)
                time.sleep(1)
                target_pid = new_process.pid
                result = manager.get_process_info_by_pid(target_pid)
                print(result)

            elif choice == '2':
                print("\nManagement Menu:")
                print("1. List Running Processes")
                print("2. View Process")
                print("3. Terminate Process")
                command = input("Enter your choice: ")
                if command == '1':
                    result = manager.process_management_list()
                    print("Registered Processes:")
                    for i in result:
                        print(i['PID'])
                elif command == '2':
                    p = int(input("Enter PID of process to view: "))
                    result = manager.process_management_list()
                    print("\n--------------------------------")
                    print("Viewing Information on process: ", p)
                    process_exists = False  # Flag to check if the process exists
                    for i in result:
                        if i['PID'] == p:
                            process_exists = True
                            print("PID:", i['PID'], "Parent PID:", i['Parent PID'], "Status:", i['Status'])
                    if not process_exists:
                        print(f"Process with PID {p} does not exist.")
                elif command == '3':
                    p = int(input("Enter PID of process to Terminate: "))
                    result = manager.process_management_list()
                    for i in result:
                        if i['PID'] == p:
                            if input("Terminate the process? (y/n): ").lower() == "y":
                                termination_result = manager.terminate_process(i['PID'])
                                print(termination_result)

            elif choice == '3':
                # Implement thread management menu
                print("\nThread Management Menu:")
                print("1. Synchronize Threads")
                print("2. IPC Operations")
                thread_choice = input("Enter your choice: ")
                if thread_choice == '1':
                    manager.create_and_start_process(True)  # Call the synchronization method
                elif thread_choice == '2':
                    manager.ipc_operations()  # Call the IPC operations method

            elif choice == '5':
                manager.terminate_all()
                break

    if args.log:
        manager.display_log_contents('process_manager.log')

    if args.exit:
        manager.terminate_all()
        exit()

