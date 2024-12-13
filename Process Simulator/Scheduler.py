from Process import Process

class Scheduler:
    def __init__(self, processes):
        """
        Initialises the Scheduler with a list of processes.
        
        Args:
            processes (list): List of Process objects to be scheduled.
        """
        self.processes = processes

    def fifoSchedule(self):
        """
        First In, First Out (FIFO) scheduling algorithm.
        Processes are scheduled in the order they arrive.
        """
        # Sort processes by arrival time
        self.processes.sort(key=lambda x: x.arrivalTime)
        currentTime = 0
        
        for process in self.processes:
            # If the current time is less than the arrival time of the process, move the current time forward
            if currentTime < process.arrivalTime:
                currentTime = process.arrivalTime
                
            # Calculate response, completion, turnaround and waiting times
            process.responseTime = currentTime - process.arrivalTime
            process.completionTime = currentTime + process.executionTime
            process.turnaroundTime = process.completionTime - process.arrivalTime
            process.waitingTime = process.turnaroundTime - process.executionTime
            
            # Update the current time to the completion time of the current process
            currentTime = process.completionTime

    def stcfSchedule(self):
        """
        Shortest Time-to-Completion First (STCF) scheduling algorithm.
        Pre-emptively selects the process with the shortest remaining time.
        """
        # Sort processes by arrival time
        self.processes.sort(key=lambda x: x.arrivalTime)
        completed = []
        currentTime = 0
        readyQueue = []

        while self.processes or readyQueue:
            # Add all processes that have arrived by the current time to the ready queue
            while self.processes and self.processes[0].arrivalTime <= currentTime:
                readyQueue.append(self.processes.pop(0))
                
            if readyQueue:
                # Sort the ready queue by remaining time and select the process with the shortest remaining time
                readyQueue.sort(key=lambda x: x.remainingTime)
                currentProcess = readyQueue.pop(0)
                
                # If the process is being executed for the first time, calculate its response time
                if currentProcess.responseTime == -1:
                    currentProcess.responseTime = currentTime - currentProcess.arrivalTime
                    
                # Execute the process for one time unit
                currentTime += 1
                currentProcess.remainingTime -= 1
                
                # If the process has finished executing - calculate its completion, turnaround and waiting times
                if currentProcess.remainingTime == 0:
                    currentProcess.completionTime = currentTime
                    currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
                    currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.executionTime
                    completed.append(currentProcess)
                else:
                    # If the process has not finished executing, add it back to the ready queue
                    readyQueue.append(currentProcess)
            else:
                # If no processes are ready, move the current time forward
                currentTime += 1

        # Update the processes list with the completed processes
        self.processes = completed

    def rrSchedule(self, timeQuantum):
        """
        Round Robin (RR) scheduling algorithm.
        Processes are scheduled in a round-robin manner with a specified time quantum.
        
        Args:
            timeQuantum (int): The time quantum for the Round Robin scheduling.
        
        Returns:
            list: A Gantt chart representing the order and time slices of process execution.
        """
        ganttChart = []
        currentTime = 0
        queue = self.processes[:]
        
        while queue:
            process = queue.pop(0)
            
            # If the current time is less than the arrival time of the process, move the current time forward
            if currentTime < process.arrivalTime:
                currentTime = process.arrivalTime
            
            if process.remainingTime > timeQuantum:
                
                # If the process has more remaining time than the time quantum, execute it for the time quantum
                if process.responseTime == -1:
                    process.responseTime = currentTime - process.arrivalTime
                currentTime += timeQuantum
                process.remainingTime -= timeQuantum
                queue.append(process)
                ganttChart.append((process.processID, currentTime))
                
            else:
                # If the process can finish within the time quantum, execute it to completion
                if process.responseTime == -1:
                    process.responseTime = currentTime - process.arrivalTime
                currentTime += process.remainingTime
                process.remainingTime = 0
                process.completionTime = currentTime
                process.turnaroundTime = process.completionTime - process.arrivalTime
                process.waitingTime = process.turnaroundTime - process.executionTime
                ganttChart.append((process.processID, currentTime))
        
        return ganttChart

    def calculateCpuUtilisation(self):
        """
        Calculates and displays the CPU utilisation.
        """
        totalExecutionTime = sum(p.executionTime for p in self.processes)
        totalTime = max(p.completionTime for p in self.processes)
        cpuUtilisation = (totalExecutionTime / totalTime) * 100
        
        print(f"CPU utilisation: {cpuUtilisation:.2f}%")

    def displayResults(self):
        """
        Displays the results of the scheduling, including process ID, arrival time, execution time,
        completion time, turnaround time, response time, and waiting time for each process.
        """
        print(f"\n{'Process ID':<12}{'Arrival':<10}{'Execution':<10}{'Completion':<12}{'Turnaround':<12}{'Response':<10}{'Waiting':<10}")
        
        for process in self.processes:
            print(f"{process.processID:<12}{process.arrivalTime:<10}{process.executionTime:<10}{process.completionTime:<12}{process.turnaroundTime:<12}{process.responseTime:<10}{process.waitingTime:<10}")
        
        print("\nSummary:")
        totalTurnaroundTime = sum(p.turnaroundTime for p in self.processes)
        totalResponseTime = sum(p.responseTime for p in self.processes)
        totalWaitingTime = sum(p.waitingTime for p in self.processes)
        
        print(f"Average Turnaround Time: {totalTurnaroundTime / len(self.processes):.2f}")
        print(f"Average Response Time: {totalResponseTime / len(self.processes):.2f}")
        print(f"Average Waiting Time: {totalWaitingTime / len(self.processes):.2f}")
        self.calculateCpuUtilisation()

    def displayGanttChart(self, ganttChart):
        """
        Displays the Gantt chart representing the order and time slices of process execution.
        
        Args:
            ganttChart (list): A list of tuples representing the process ID and end time of each time slice.
        """
        print("\nGantt Chart:")
        print("'The Gantt chart represents the order and time slices of process execution'")
        
        for processID, endTime in ganttChart:
            print(f"{processID} -> {endTime}", end=" | ")
        print()