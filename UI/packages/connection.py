"""
    Communicaion with Serial Devices - As selected
    Author - Sachin Acharya
"""
from serial import Serial, SerialException, SerialTimeoutException
from serial.tools.list_ports import comports
from colorama import Fore, init; init(autoreset=True)

class Communication:   
    def __init__(self):
        """Establishing Connection with Serial Device in 
        selected PORT and Selected baudrate
        """
        self.baudrate: int = 9600 # Change as required
        print(f"{Fore.LIGHTCYAN_EX}Trying to connect via PORT COM4")
        try:
            self.serial_connection: Serial = Serial("COM4", self.baudrate)
        except SerialTimeoutException as e:
            print(f"{Fore.LIGHTRED_EX} %s" % str(e))
        except SerialException:
            print(f"{Fore.LIGHTRED_EX}Cannot connect on COM4.\n{Fore.LIGHTCYAN_EX}Please choose from following available ports\n")
            for port in comports():
                print(f"""    {Fore.CYAN}{port}""")
            print()
            self.serial_connection: Serial = Serial("COM"+input("Select PORT, COM"), self.baudrate)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX} %s: %s" % (e.__class__.__name__, str(e)))
        else:
            print(f"{Fore.GREEN} Connected Successfully")    
    def close(self):
        "Close Connection with Serial Port"
        if self.serial_connection.isOpen():
            self.serial_connection.close()
            print(f"{Fore.GREEN}Connection has been terminated")
        else:
            print(f"{Fore.LIGHTGREEN_EX}Connection has already been broken")
    def getData(self):
        """
        Retrive data from Serial Port
        """
        return self.serial_connection.readline().decode().strip().removeprefix('/*').removesuffix('*/').split(",") # Read single line until \n
    def isOpen(self):
        "Return True if connection is active otherwise return False"
        return self.serial_connection.isOpen()
