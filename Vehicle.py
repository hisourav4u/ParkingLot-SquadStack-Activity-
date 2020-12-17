class Vehicle:
	def __init__(self,registrationNumber,driverAge):
		self.driverAge = driverAge
		self.registrationNumber = registrationNumber

class Car(Vehicle):

	def __init__(self,registrationNumber,driverAge):
		Vehicle.__init__(self,registrationNumber,driverAge)

