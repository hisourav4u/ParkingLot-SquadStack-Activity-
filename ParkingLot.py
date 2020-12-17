
#importing required modules. argparse module to deal with the command line arguments.
import Vehicle
import argparse

class ParkingLot:
        def __init__(self):
                #ParkingLot class will be having the following properties
                self.totalNumberOfSlots = 0
                self.slotNumber = 0
                self.numOfOccupiedSlots = 0

        #to create a parking lot we will be required total number of slots as parmeter
        def createParkingLot(self,totalNumberOfSlots):
                #checking if the requested number of slots is a valid number
                if totalNumberOfSlots<0:
                        return -1
                
                #creating that many number of vacant slots
                self.slots = [0] * totalNumberOfSlots
                self.totalNumberOfSlots = totalNumberOfSlots
                
                return self.totalNumberOfSlots

        #find the next available slot to park a car
        def getNextEmptySlot(self):
                for loopIndex in range(len(self.slots)):
                        if self.slots[loopIndex] == 0:
                                return loopIndex

        #park a car with given registration number and driver age
        def park(self,registrationNumber,driverAge):
                
                #if vacant slot available then park the car and return the slot number allocated
                if self.numOfOccupiedSlots < self.totalNumberOfSlots: 
                        slotNumber = self.getNextEmptySlot()
                        self.slots[slotNumber] = Vehicle.Car(registrationNumber,driverAge)
                        
                        #increase the number of occupied slots by 1 for every successful parking
                        self.numOfOccupiedSlots = self.numOfOccupiedSlots + 1
                        
                        return slotNumber+1
                else:
                        return -1

        #vacate a parking slot by taking the slot number as input
        def leave(self,slotToVacate):
                #checking if the slot number to vacate is valid or not
                if self.totalNumberOfSlots<slotToVacate or slotToVacate<1:
                        return "Does Not Exist", None, None

                #if the slot is allocated to a car, vacate it and return the regNo and driver age of that car
                if self.numOfOccupiedSlots > 0 and self.slots[slotToVacate-1] != 0:
                        registrationNumber=self.slots[slotToVacate-1].registrationNumber
                        driverAge=self.slots[slotToVacate-1].driverAge
                        self.slots[slotToVacate-1] = 0
                        #decrease the number of occupied slots by 1 for every successful leaving
                        self.numOfOccupiedSlots = self.numOfOccupiedSlots - 1
                        return True, registrationNumber, driverAge

                #if the slot is not allocated to any car, return
                else:
                        return False, None, None

        #get the list of slot numbers from the driver age as input
        def getSlotNumbersFromDriverAge(self,driverAge):
                
                #create a blank list to hold the slot numbers
                slotNumbersList = []
                for loopIndex in range(len(self.slots)):
                        #if entered driver age matches with the stored car details, append the slot number to the list
                        if self.slots[loopIndex]!=0 and self.slots[loopIndex].driverAge == driverAge:
                                slotNumbersList.append(str(loopIndex+1))
                        else:
                                continue
                return slotNumbersList

        #get the list of registration Numbers from the driver age as input
        def getRegistrationNumbersFromDriverAge(self,driverAge):

                #create a blank list to hold the registration numbers
                registrationNumbersList = []

                #loop through each slots and if any car is parked with given driver age, append the registration number to the list
                for slot in self.slots:
                        if slot == 0:
                                continue
                        if slot.driverAge == driverAge:
                                registrationNumbersList.append(slot.registrationNumber)
                                
                return registrationNumbersList
                        
        #get the slot number for a particular registration number of a parked car
        def getSlotNumberFromRegistrationNumber(self,registrationNumber):
                
                #loop through each slot and if any car is found parked with the given registration number, return the slot number
                for loopIndex in range(len(self.slots)):
                        if self.slots[loopIndex]!=0 and self.slots[loopIndex].registrationNumber == registrationNumber:
                                return loopIndex+1
                        else:
                                continue
                return -1
                        

        def command(self,commandInput):

                """
                Each input command is having some particular prefix.
                Check if an input command starts with a prefix and then call the required method accordingly.
                Convert the input command to lowercase. This is to make sure that inconsistent casing in input file does not affect adversely

                Split the input commands with space as delimeter.
                It will separate the prefix and required parameters (i.e, driverAge, totalNumberOfSlots, carRegistrationNumber etc..)
                
                After splitting the commands we will fetch the parameters as and when required by the index.
                
                For example,

                "Park KA-01-HH-1234 driver_age 21"
                
                It starts with "park", so park method needs to be called.
                And the required parameters for park method,
                
                "Park" [index_0] | "KA-01-HH-1234" [index_1] | "driver_age" [index_2] | 21 [index_3]
                
                registrationNumber is at index 1, driverAge is at index 3.

                Similarily for other commands:

                "Create_parking_lot 6"
                Starts with "create_parking_lot", method-> createParkingLot()

                "Create_parking_lot" [index_0] | 6 [index_1]
                required parameter capacity is at index 1

                "Slot_numbers_for_driver_of_age 21"
                Starts with "Slot_numbers_for_driver_of_age", method->getSlotNumbersFromDriverAge()

                "Slot_numbers_for_driver_of_age" [index_0] | 21 [index_1]
                required parameter driverAge is at index 1

                and so on.
                
                
                """
                
                if commandInput.lower().startswith("create_parking_lot"):
                        capacity = int(commandInput.split(" ")[1])
                        result = self.createParkingLot(capacity)

                        #if result=-1, that means the requested capacity is not valid
                        if result==-1:
                                print("Parking lot with requested capacity cannot be created")
                        else:

                                #Taking care between single or no SLOT and multiple SLOTS
                                if result==0 or result==1:
                                        slot_slots="slot"
                                else:
                                        slot_slots="slots"
                                        
                                print("Created parking of "+str(result)+" "+slot_slots)

                elif commandInput.lower().startswith("park"):
                        registrationNumber = commandInput.split(" ")[1]
                        
                        driverAge = commandInput.split(" ")[-1]
                        
                        result = self.park(registrationNumber,driverAge)

                        #if result=-1, that means slot is not available for parking
                        if result == -1:
                                print("Sorry, vacant slot not available at this moment.")
                        else:
                                print("Car with vehicle registration number "+'"'+registrationNumber+'"'+" has been parked at slot number "+str(result))

                elif commandInput.lower().startswith("leave"):
                        slotToVacate = int(commandInput.split(" ")[1])
                        
                        status, registrationNumber, driverAge = self.leave(slotToVacate)

                        #For invalid slot Numbers (greater than total capacity or less than 1)
                        if status=="Does Not Exist":
                                print("Slot "+str(slotToVacate)+" does not exist")

                        #If status is True
                        elif status:
                                print("Slot number "+str(slotToVacate)+" vacated, the car with vehicle registration number "+'"'+registrationNumber+'"'+" left the space, the driver of the car was of age "+str(driverAge))
                        #If status is False
                        else:
                                print("Slot "+str(slotToVacate)+" already vacant")

                elif commandInput.lower().startswith("slot_numbers_for_driver_of_age"):
                        driverAge = commandInput.split(" ")[1]
                        
                        slotNumbersList = self.getSlotNumbersFromDriverAge(driverAge)

                        #If we get any value in the list then print the values. Else, display a message
                        if len(slotNumbersList)>=1:
                                print(", ".join(slotNumbersList))
                        else:
                                print("Driver of age "+str(driverAge)+" has not parked car")
                        

                elif commandInput.lower().startswith("slot_number_for_car_with_number"):
                        registrationNumber = commandInput.split(" ")[1]
                        
                        slotNumber = self.getSlotNumberFromRegistrationNumber(registrationNumber)

                        #If we get any valid slot number, print it. Else, display a message
                        if slotNumber == -1:
                                print("Not found")
                        else:
                                print(slotNumber)

                elif commandInput.lower().startswith("vehicle_registration_number_for_driver_of_age"):
                        driverAge = commandInput.split(" ")[1]
                        
                        registrationNumbersList = self.getRegistrationNumbersFromDriverAge(driverAge)

                        #If we get any value in the list then print the values. Else, display a message
                        if len(registrationNumbersList)>=1:
                                print(", ".join(registrationNumbersList))
                        else:
                                print("Driver of age "+str(driverAge)+" has not parked car")
                        
                                
                else:
                        exit(0)

def main():

        parkingLot = ParkingLot()
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", action="store", required=False, dest="inputFile", help="Input File")
        args = parser.parse_args()
        
        """
        Lets have both options. Reading inputs from a file and taking inputs at runtime.
        If user provides an input file beforehand, we will use it as command line arguments, or we will go with runtime inputs        
        """
        
        if args.inputFile:
                with open(args.inputFile) as inputCommands:
                        for commandInput in inputCommands:
                                commandInput = commandInput.rstrip("\n")
                                parkingLot.command(commandInput)
        else:
                        while True:
                                commandInput = input("-> ")
                                parkingLot.command(commandInput)

if __name__ == "__main__":
        main()
