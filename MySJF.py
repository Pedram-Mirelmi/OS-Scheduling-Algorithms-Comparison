from typing import Callable
from RandomGeneratingTools import *
from my_queue import MyPriorityQueue
import sys

# Pedram - Mirelmi - 610398176

MEAN = 'mean'
STD = 'std'
ARRIVAL = 'arrival'
BURST = 'burst'
class SimpleSJFProcess:
    def __init__(self, burst_time: int, arrival_time: int):
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.last_time_pushed_to_queue = arrival_time
        self.total_waiting_time = 0
        self.turnaround_time = 0
        self.compare_flag = ARRIVAL

    def __lt__(self, other):
        if not isinstance(other, SimpleSJFProcess):
            raise TypeError(f'Object of type SimpleSJFProcess must be passed. but {type(other).__name__} was passed')
        
        if self.compare_flag == ARRIVAL:
            return self.arrival_time < other.arrival_time
        
        # else BURST
        return self.burst_time < other.burst_time

class SimpleSJF:
    def __init__(self,
                 n: int = 10 ** 3,
                 context_switch_time: int = 0,
                 randomGeneratorFunc: Callable = getUniformRandomNumber) -> None:
        self.number_of_processes_each_time = n
        self.context_switch_time = context_switch_time
        self.processes_queue = MyPriorityQueue()
        self.ready_queue = MyPriorityQueue()
        self.randomGenerator = randomGeneratorFunc
        self.total_processes = 0
        self.maximum_burst_time = 0
        


    def runTestNTimes(self, n: int) -> float:
        responses = {STD: [0] * n, MEAN: [0] * n}
        waitings = {STD: [0] * n, MEAN: [0] * n}
        turnarounds = {STD: [0] * n, MEAN: [0] * n}
        for i in range(n):
            new_result = self.__runTest(); new_result: tuple
            responses[MEAN][i] = new_result[0][0]
            responses[STD][i] = new_result[0][1]
            waitings[MEAN][i] = new_result[1][0]
            waitings[STD][i] = new_result[1][1]
            turnarounds[MEAN][i] = new_result[2][0]
            turnarounds[STD][i] = new_result[2][1]
        final_result = {'response times':
                        {
                            'mean of mean': np.mean(responses[MEAN]),
                            'mean of std': np.mean(responses[STD]),
                            'std of mean': np.std(responses[MEAN]),
                            'std of std': np.std(responses[STD])
                        },
                        'waiting times':
                        {
                            'mean of mean': np.mean(waitings[MEAN]),
                            'mean of std': np.mean(waitings[STD]),
                            'std of mean': np.std(waitings[MEAN]),
                            'std of std': np.std(waitings[STD]),
                        },
                        'turnaround times':
                        {
                            'mean of mean': np.mean(turnarounds[MEAN]),
                            'mean of std': np.mean(turnarounds[STD]),
                            'std of mean': np.std(turnarounds[MEAN]),
                            'std of std': np.std(turnarounds[STD]),
                        },
                        'total number of processes': self.total_processes,
                        'maximum burst time': self.maximum_burst_time}
        self.total_processes = 0
        self.maximum_burst_time = 0
        return final_result


    def __runTest(self) -> tuple:
        timer = 0
        randoms = self.randomGenerator(n=self.number_of_processes_each_time)
        
        self.addProcesses(randoms)

        response_times_list = [0] * len(randoms)
        waiting_times_list = [0] * len(randoms)
        turnaround_times_list = [0] * len(randoms)
        counter = 0


        timer = self.waitForNewProcesses()

        while (not self.processes_queue.isEmpty()) or (not self.ready_queue.isEmpty()):
            self.addNewArrivedProcessesToReadyQueue(timer)

            current_process = self.ready_queue.dequeue(); current_process: SimpleSJFProcess
            timer += self.context_switch_time

            current_process.total_waiting_time += timer - current_process.last_time_pushed_to_queue
            response_times_list[counter] = timer - current_process.arrival_time # because of FCFS
            
            waiting_times_list[counter] = timer - current_process.arrival_time
            '''
                handle process here
            '''
            timer += current_process.burst_time
            self.maximum_burst_time = max(self.maximum_burst_time, current_process.burst_time)
            turnaround_times_list[counter] = current_process.total_waiting_time + current_process.burst_time
            self.total_processes += 1
            
            if self.ready_queue.isEmpty():
                timer = max(self.waitForNewProcesses(), timer)
            counter += 1
           

        return [ (np.mean(response_times_list), np.std(response_times_list)),
               (np.mean(waiting_times_list), np.std(waiting_times_list)),
               (np.mean(turnaround_times_list), np.std(turnaround_times_list))]

        


    def addNewArrivedProcessesToReadyQueue(self, timer: int):
        next_process = self.processes_queue.next(); next_process: SimpleSJFProcess
        while next_process != None and next_process.arrival_time <= timer:
            self.processes_queue.dequeue()
            next_process.compare_flag = BURST
            self.ready_queue.enqueue(next_process)
            next_process = self.processes_queue.next()

    def waitForNewProcesses(self):
        if not self.processes_queue.isEmpty():
            return self.processes_queue.next().arrival_time
        return sys.maxsize

    def addProcesses(self, randoms):
        for num in randoms:
            self.processes_queue.enqueue(item=SimpleSJFProcess(*num))



import json
def printNormalTestResult(n: int, mean: float, std: float, test_results: dict, context_switch_time: int):
    print(f'ran test {n} times with parameters: \
       \ngenerating numbers with normal distribution with mean {mean:.10E} and std of {std:.10E}')
    print(json.dumps(test_results, default=str, indent=4))
    
def printUniformTestResult(n: int, high:int, test_results: dict, context_switch_time: int):
    print(f'ran test {n} times with parameters:\
       \ngenerating numbers with Uniform distribution with low 0 and high {high}')
    print(json.dumps(test_results, default=str, indent=4))
