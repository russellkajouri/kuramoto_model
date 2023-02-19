

class oscillator:
	def __init__(self, phase = 0.0, frequency = 0.0):
		self.phi = phase

		# the intrinsic frequency of the oscillator
		self.omega = frequency

		# the local frequency of the oscillator due to the interacting
		self.omega_prime = self.omega
		pass


	def __str__(self):
		return( f"phase: {self.phi}, frequency: {self.omega}" )

	def set_phase(self, phase : float ):
		self.phi = phase
		pass

	def set_intrinsic_frequency(self, frequency : float ):
		self.omega = frequency
		self.omega_prime = self.omega
		pass

	def set_frequency(self, frequency : float ):
		self.omega_prime = frequency
		pass

	def set_Nneighbors(self, Nneighbors : int ):
		self.Nneighbors = Nneighbors
		pass

	def get_phase(self):
		return self.phi

	def get_intrinsic_frequency(self):
		return self.omega

	def get_frequency(self):
		return self.omega_prime

	def get_Nneighbors(self):
		return self.Nneighbors



