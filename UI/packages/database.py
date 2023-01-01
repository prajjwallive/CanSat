"""
Store Data in CSV file
"""
import csv, os
from colorama import Fore, init; init(autoreset=True)

class Database:
    def __init__(self, logfile: str = 'log.csv'):
        "Init Database with State as False - Not storing"
        self.logFile = logfile
        self.state = False        
    def startStorage(self, data: list, isTitle:bool = False):
        "Writing data to CSV file"
        if self.state and len(data) > 1:
            if isTitle and os.path.exists(self.logFile):
                return
            with open(self.logFile, "a") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow(list(data))        
    @property
    def isStoring(self):
        return self.state
    def start(self):
        "Start Storage of Data in CSV"
        self.state = True
        print(f"{Fore.CYAN}Starting Storage in log.csv file")
    def stop(self):
        "Stop Storage of Data in CSV"
        self.state = False
        print(f"{Fore.CYAN}Stopping Storage in log")