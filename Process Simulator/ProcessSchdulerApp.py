from copy import deepcopy
from Process import Process
from Scheduler import Scheduler

class ProcessSchedulerApp:
    def inputProcesses(self):
        """
        Prompts the user to input the number of processes and their details.
        Ensures valid input for the number of processes, process ID, arrival time, and execution time.
        
        Returns:
            list: A list of Process objects with the input details.
        """
        processes = []
        while True:
            try:
                numProcesses = int(input("Enter the number of processes: "))
                if numProcesses <= 0:
                    raise ValueError("Number of processes must be a positive integer.")
                break
            except ValueError:
                print("Invalid input. Please enter a positive integer for the number of processes.")
                
        for i in range(numProcesses):
            processID = self.inputProcessID(processes)
            arrivalTime = self.inputArrivalTime()
            executionTime = self.inputExecutionTime()
            processes.append(Process(processID, arrivalTime, executionTime))
                
        return processes
    
    def inputProcessID(self, processes):
        """
        Prompts the user to enter a unique Process ID.
        Ensures the process ID is not empty and is unique to the already given processes.
        
        Args:
            processes (list): List of existing processes to check for uniqueness.
        
        Returns:
            str: A unique process ID.
        """
        while True:
            processID = input("Enter Process ID: ")
            if processID and not any(p.processID == processID for p in processes):
                return processID
            print("Process ID must be unique and not empty.")
            
    def inputArrivalTime(self):
        """
        Prompts the user to enter the arrival time for a process.
        Ensures the arrival time is a positive integer or 0.
        
        Returns:
            int: The arrival time of the process.
        """
        while True:
            try:
                arrivalTime = int(input("Enter Arrival Time: "))
                if arrivalTime < 0:
                    raise ValueError("Arrival time must be a positive integer value or 0.")
                return arrivalTime
            except ValueError:
                print("Invalid input. Please enter a positive integer for the arrival time.")
                
    def inputExecutionTime(self):
        """
        Prompts the user to enter the execution time (burst time) for a process.
        Ensures the execution time is a positive integer.
        
        Returns:
            int: The execution time of the process.
        """
        while True:
            try:
                executionTime = int(input("Enter Execution Time: "))
                if executionTime <= 0:
                    raise ValueError("Execution time must be a positive integer value.")
                return executionTime
            except ValueError:
                print("Invalid input. Please enter a positive integer for the execution time.")
    
    def displayProcesses(self, processes):
        """
        Displays the details of the given processes.

        Args:
            processes (list): List of processes to display.
        """
        print("Current Processes:")
        print(f"{'Process ID':<12}{'Arrival Time':<15}{'Execution Time':<15}")
        for process in processes:
            print(f"{process.processID:<12}{process.arrivalTime:<15}{process.executionTime:<15}")
            
    def addProcess(self, processes):
        """
        Adds a new process to the list of processes.
        Prompts the user to input the Process ID, arrival time, and execution time.

        Args:
            processes (list): List of existing processes to add the new process to.
        """
        processID = self.inputProcessID(processes)
        arrivalTime = self.inputArrivalTime()
        executionTime = self.inputExecutionTime()
        processes.append(Process(processID, arrivalTime, executionTime))
        print("Process added successfully!")
        
    def mainMenu(self, originalProcesses):
        """
        Displays the Main Menu and allows the user to select and run a scheduling algorithm.
        The user can also display the processes, add a new process, or exit the program.

        Args:
            originalProcesses (list): List of original processes to be scheduled.
        """
        while True:
            print("\nMain Menu:")
            print("1. First In, First Out (FIFO)")
            print("2. Shortest Time-to-Completion First (STCF)")
            print("3. Round Robin (RR)")
            print("4. Display Processes")
            print("5. Add Process")
            print("6. Exit")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.runFIFO(originalProcesses)
                elif choice == 2:
                    self.runSTCF(originalProcesses)
                elif choice == 3:
                    self.runRR(originalProcesses)
                elif choice == 4:
                    self.displayProcesses(originalProcesses)
                elif choice == 5:
                    self.addProcess(originalProcesses)
                elif choice == 6:
                    print("\nExiting...")
                    break
                else:
                    print("Invalid choice. Please enter a valid option!")
            except ValueError:
                print("Invalid choice. Please enter a valid option!")
    
    def runFIFO(self, originalProcesses):
        """
        Runs the FIFO scheduling algorithm on the given processes.

        Args:
            originalProcesses (list): List of original processes to be scheduled.
        """
        processes = deepcopy(originalProcesses)
        scheduler = Scheduler(processes)
        scheduler.fifoSchedule()
        scheduler.displayResults()
        
    def runSTCF(self, originalProcesses):
        """
        Runs the STCF scheduling algorithm on the given processes.

        Args:
            originalProcesses (list): List of original processes to be scheduled.
        """
        processes = deepcopy(originalProcesses)
        scheduler = Scheduler(processes)
        scheduler.stcfSchedule()
        scheduler.displayResults()
        
    def runRR(self, originalProcesses):
        """
        Runs the Round Robin scheduling algorithm on the given processes.
        Prompts the user to enter the time quantum. 
        Displays the results after scheduling.

        Args:
            originalProcesses (list): List of original processes to be scheduled.
        """
        while True:
            try:
                timeQuantum = int(input("Enter the time quantum: "))
                if timeQuantum <= 0:
                    raise ValueError("Time Quantum must be a positive integer.")
                break
            except ValueError as e:
                print(e)
                
        processes = deepcopy(originalProcesses)
        scheduler = Scheduler(processes)
        ganttChart = scheduler.rrSchedule(timeQuantum)
        scheduler.displayResults()
        scheduler.displayGanttChart(ganttChart)
        
    def run(self):
        """
        Main method to run the process scheduler application/program.
        Prompts the user to input processes and select a scheduling algorithm.
        """
        processes = self.inputProcesses()
        self.mainMenu(processes)
        
if __name__ == "__main__":
    app = ProcessSchedulerApp()
    app.run()
