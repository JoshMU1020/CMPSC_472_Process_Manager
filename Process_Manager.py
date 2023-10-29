import threading
import multiprocessing
import time
import logging
import psutil
import random
import queue


class ProcessManager:
    def __init__(self):
        self.process_pids = []
        self.threads = []
        #self.lock = threading.Lock()  # Synchronization lock
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
        #print(f"Worker process PID: {os.getpid()}")
        time.sleep(5)  # Simulate some work
        return

    def thread_worker_function(self):
        # with self.lock:  # Acquire the lock
        logging.info(f"Worker thread PID: {threading.current_thread().ident}")
        # print(f"Worker thread PID: {threading.current_thread().ident}")
        time.sleep(5)
        return

    def create_and_start_process(self):
        logging.info("Creating new process...")
        self.total_items = random.randint(2, 5) * 4  # Randomly generate number of data items
        new_process_instance = multiprocessing.Process(target=self.synchronize_threads)
        process_pid = new_process_instance.pid
        new_process_instance.start()
        self.process_pids.append(new_process_instance)
        logging.info(f"Process created with PID: {process_pid}")

        # Add data to the IPC queue
        self.queue.put(f"Data from Process {process_pid}")

        #self.synchronize_threads()

        #sleep_time = random.randint(2, 5) * 4  # Random multiple of 5 between 5 and 60
        #num_threads = int(sleep_time / 10)
        #self.create_and_start_thread(num_threads)

        return new_process_instance

    def create_and_start_thread(self, num_threads):
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.thread_worker_function)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        return

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
        process_info_list = []
        for p_id in self.process_pids:
            process = psutil.Process(p_id.pid)
            process_info = {
                "PID": process.pid,
                "Name": process.name(),
                "Status": process.status(),
                "Parent PID": process.ppid(),
            }
            process_info_list.append(process_info)
        return process_info_list

    def terminate_process(self, targeted_pid):
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

    def producer(self, buffer, mutex, empty, data, min_value, max_value, pro_id):
        for i in range(self.total_items):
            item = random.randint(min_value, max_value)
            empty.acquire()
            mutex.acquire()
            buffer.append(item)
            logging.info(f"Producer {pro_id} Produced {item}. Buffer: {buffer}")
            mutex.release()
            data.release()
            time.sleep(random.uniform(0.1, 0.5))

    def consumer(self, buffer, mutex, empty, data, con_id):
        for i in range(self.total_items // 2):
            data.acquire()
            mutex.acquire()
            if buffer:
                item = buffer.pop(0)
                logging.info(f"Consumer {con_id} Consumed {item}. Buffer: {buffer}")
            mutex.release()
            empty.release()

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


if __name__ == '__main__':
    # Your existing code for the menu
    logging.basicConfig(filename='process_manager.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    with open('process_manager.log', 'w'):
        pass
    manager = ProcessManager()

    while True:
        logging.info("Displaying Process Manager Menu...")
        print("\nProcess Manager Menu:")
        print("1. Create Process")
        print("2. Manage Running Processes")
        print("3. Manage Threads")
        print("4. View Log Report")
        print("5. Exit")

        choice = input("Enter your choice: ")

        #new_process = manager.create_and_start_process()
        #time.sleep(1)

        if choice == '1':
            new_process = manager.create_and_start_process()
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
                target_pid = new_process.pid
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
                manager.synchronize_threads()  # Call the synchronization method
            elif thread_choice == '2':
                manager.ipc_operations()  # Call the IPC operations method

        elif choice == '4':
            # Implement logger menu here
            pass

        elif choice == '5':
            exit()

        else:
            print("Invalid choice. Please try again.")
