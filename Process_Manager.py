import os  # python .\print.py.txt
import threading
import multiprocessing
import time
import logging
import psutil
import random
import queue
import argparse


class ProcessManager:
    def __init__(self):
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

    def worker_function(self):
        logging.info(f"Worker process PID: {os.getpid()}")
        work_time = random.randint(1, 5) * 10
        time.sleep(work_time)  # Simulate some work
        return

    """def thread_worker_function(self):
        logging.info(f"Worker thread PID: {threading.current_thread().ident}")
        time.sleep(5)
        return"""

    def create_and_start_process(self, uses_t):
        logging.info("Creating new process...")
        self.total_items = random.randint(2, 5) * 4  # Randomly generate number of data items
        if uses_t:
            new_process_instance = multiprocessing.Process(target=self.synchronize_threads)
        else:
            new_process_instance = multiprocessing.Process(target=self.worker_function)
        process_pid = new_process_instance.pid

        new_process_instance.start()
        self.process_pids.append(new_process_instance)
        logging.info(f"Process created with PID: {process_pid}")

        self.queue.put(f"Data from Process {process_pid}")  # Add data to the IPC queue

        """self.synchronize_threads()
        sleep_time = random.randint(2, 5) * 4  # Random multiple of 5 between 5 and 60
        num_threads = int(sleep_time / 10)
        self.create_and_start_thread(num_threads)"""

        return new_process_instance

    '''def create_and_start_thread(self, num_threads):
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.thread_worker_function)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        return'''

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
        for p_id in self.process_pids:
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


if __name__ == '__main__':
    # Your existing code for the menu
    logging.basicConfig(filename='process_manager.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    with open('process_manager.log', 'w'):
        pass

    # Initialize the ArgumentParser
    parser = argparse.ArgumentParser(description='Process Manager CLI')

    # Define command-line arguments and their descriptions
    parser.add_argument('--create', action='store_true', help='Create a new process')
    parser.add_argument('--list', action='store_true', help='List running processes')
    parser.add_argument('--terminate', type=int, help='Terminate a process by PID')
    parser.add_argument('--threads', action='store_true', help='Manage threads')
    parser.add_argument('--log', action='store_true', help='View log report')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Create a ProcessManager instance
    manager = ProcessManager()
    new_process = manager.create_and_start_process(False)

    if args.create:
        new_process = manager.create_and_start_process(False)
        target_pid = new_process.pid
        result = manager.get_process_info_by_pid(target_pid)
        print(result)

    if args.list:
        result = manager.process_management_list()
        print("Registered Processes:")
        for i in result:
            print(i['PID'])

    if args.terminate:
        termination_result = manager.terminate_process(args.terminate)
        print(termination_result)

    if args.threads:
        thread_choice = input("Enter your choice for thread management (1 for synchronization, 2 for IPC Operations): ")
        if thread_choice == '1':
            manager.create_and_start_process(True)  # Call the synchronization method
        elif thread_choice == '2':
            manager.ipc_operations()  # Call the IPC operations method

    if args.log:
        manager.display_log_contents('process_manager.log')
        
