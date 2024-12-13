class Process:
    def __init__(self, processID, arrivalTime, executionTime):
        """
        Initialises a Process object with the given parameters.
        
        Args:
            processID (str): The unique identifier of the process.
            arrivalTime (int): The time at which the process arrives in the system.
            executionTime (int): The total CPU time required by the process.
        """
        self.processID = processID  # Unique identifier of the process
        self.arrivalTime = arrivalTime  # Time at which the process arrives in the system
        self.executionTime = executionTime  # Total CPU time required by the process
        self.remainingTime = executionTime  # Remaining CPU time required by the process
        
        self.responseTime = -1  # Time taken by the system to start the execution of the process
        self.completionTime = 0  # Time at which the process completes its execution
        self.turnaroundTime = 0  # Time taken by the system to execute the process
        self.waitingTime = 0  # Time for which the process waits in the ready queue