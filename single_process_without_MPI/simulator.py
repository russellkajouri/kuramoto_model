from agent import oscillator
import math, random, sys, copy
from typing import List

class kuramoto:
	def __init__(self, Noscillators : int ) -> None:

		# float number of oscillators is not corrent!
		if type( int() ) != type( Noscillators ):
			print( "***ERROR***: Float number of oscillators is impossible!", file = sys.stderr )
			exit( 0 )

		# negative number or zero is not correct!
		elif Noscillators <= 0:
			print( "***ERROR***: Meaningless number of oscillators.", file = sys.stderr )
			exit( 0 )
			pass

		self.N = Noscillators
		self.Oscillator = [ oscillator() for i in range( self.N ) ]

		self.dump = False
		self.sync = False
		self.log  = False

		self.rk4_integrator = False

		self.licence()
		print( f"{self.N} oscillators has been defined." )
		pass


	def licence(self) -> None:
		print( " " * 10, "K U R A M O T O - M O D E L" )
		print( " " * 10, "Last update: 29 JAN 2023, V 0.01" )
		print( " " * 10, "Created by Russell Kajouri, russellkajouri@gmail.com" )
		print( "" )
	# ---------------------------------------------------------------------------------------------

	# to set value of phase randomly
	def set_uniform_phase(self, lowBound : float = -math.pi, highBound : float = math.pi ) -> None:

		# if the low and high bounds are same to each other, then that means the
		# phase of all oscillators are the same.
		if lowBound == highBound:
			for Osc in self.Oscillator:
				Osc.set_phase( phase = lowBound )
				pass
		# if the high bound of the border is less than the low bound,
		# we swap them with each other
		elif highBound < lowBound:
			lowBound, highBound = highBound, lowBound
			print( "swap bounds" )
			pass

		for Osc in self.Oscillator:
			Osc.set_phase( phase = random.uniform( lowBound, highBound ) )
			pass
		print( "Phases were assigned" )
		pass

	# to set value of phase by user not randomly
	def set_phases( self, phis : List[float] ) -> None:
		if len( phis ) != self.N:
			print( "***ERROR***Unexpected number of oscillators' phase", file = sys.stderr )
			exit( 0 )
			pass

		for osc, ph in zip( self.Oscillator, phis ):
			osc.set_phase( phase = ph )
			pass
		pass

	# ---------------------------------------------------------------------------------------------

	# to set the value of intrinsic frequencies of oscillators
	def set_guassin_frequency(self, mean : float = 0.0, std_dev : float = 1.0 ) -> None:
		if std_dev < 0:
			print( "***ERROR***Impossible std_dev.", file = sys.stderr )
			pass
		elif std_dev == 0:
			for osc in self.Oscillator:
				osc.set_intrinsic_frequency( frequency = mean )
				pass
		else:
			for osc in self.Oscillator:
				osc.set_intrinsic_frequency( frequency = random.gauss( mean, std_dev ) )
				pass
			pass
		print( "Frequencies were assigned." )
		pass

	# to get the value of intrinsic frequencies of oscillators
	def set_frequencies(self, frequencies = List[float] ) -> None:
		if len( frequencies ) != self.N:
			print( "***ERROR***Unexpected number of oscillators' frequency", file = sys.stderr )
			exit( 0 )
			pass

		for osc, freq in zip( self.Oscillator, frequencies ):
			osc.set_intrinsic_frequency( frequency = freq )
			pass
		pass

	# ---------------------------------------------------------------------------------------------

	# to show the value of phases
	def get_phases(self) -> list:
		phis = []
		for osc in self.Oscillator:
			phis.append( osc.get_phase() )

		return phis

	# to show the value of phases
	def get_frequencies(self) -> list:
		freqs = []
		for osc in self.Oscillator:
			freqs.append( osc.get_frequency() )

		return freqs

	# ---------------------------------------------------------------------------------------------

	def isSquare( self, c ) -> bool:
		return all( len( row ) == len( c ) for row in c )
	def set_coupling(self, coupling ) -> None:
		if type( coupling ) == type( float() ) or type( coupling ) == type( int() ):
			self.K = [ [ float( coupling ) for i in range( self.N ) ] for j in range( self.N ) ]
			pass
		elif type( coupling ) == List[List[ int() ] ] or type( coupling ) == List[List[ float() ] ]:
			if( isSquare( coupling ) ):
				self.K - copy.deepcopy( coupling )
				pass
			pass

		for i, ocs in enumerate( self.Oscillator ):
			ocs.set_Nneighbors( int( sum( [ 1 if b > 0 else 0 for b in self.K[i] ] ) )  )

		print( "Copuling strength were assigned" )
		pass

	def get_coupling( self ):
		return self.K

	def get_neighborsList(self):
		Nneigh = []
		for osc in self.Oscillator:
			Nneigh.append( osc.get_Nneighbors() )
			pass
		return Nneigh

	# ---------------------------------------------------------------------------------------------

	def integrator_rk4(self, dt : float = 0.005 ) -> None:
		self.dt = dt
		self.rk4_integrator = True;
		pass

	def rk4_one_step( self ) -> None:
		# store the value of updated phase
		updated_phase = []
		for i, osc in enumerate( self.Oscillator ):

			# first sentence
			local_phase = osc.get_phase()
			k1 = 0.0
			for j, osc2 in enumerate( self.Oscillator ):
				if self.K[ i ][ j ] > 0:
					k1 += self.K[ i ][ j ] * math.sin( osc2.get_phase() - local_phase )
				pass
			k1 /= osc.get_Nneighbors()
			k1 += osc.get_intrinsic_frequency()

			# second sentence
			local_phase = osc.get_phase() + self.dt * k1 * 0.500
			k2 = 0.0
			for j, osc2 in enumerate( self.Oscillator ):
				if self.K[ i ][ j ] > 0:
					k2 += self.K[ i ][ j ] * math.sin( osc2.get_phase() - local_phase )
				pass
			k2 /= osc.get_Nneighbors()
			k2 += osc.get_intrinsic_frequency()

			# third sentence
			local_phase = osc.get_phase() + self.dt * k2 * 0.500
			k3 = 0.0
			for j, osc2 in enumerate( self.Oscillator ):
				if self.K[ i ][ j ] > 0:
					k3 += self.K[ i ][ j ] * math.sin( osc2.get_phase() - local_phase )
				pass
			k3 /= osc.get_Nneighbors()
			k3 += osc.get_intrinsic_frequency()


			# fourth sentence
			local_phase = osc.get_phase() + self.dt * k3
			k4 = 0.0
			for j, osc2 in enumerate( self.Oscillator ):
				if self.K[ i ][ j ] > 0:
					k4 += self.K[ i ][ j ] * math.sin( osc2.get_phase() - local_phase )
				pass
			k4 /= osc.get_Nneighbors()
			k4 += osc.get_intrinsic_frequency()

			# update phase
			updated_phase.append( osc.get_phase() + self.dt * 0.1666 * ( k1 + 2. * ( k2 + k3 ) + k4 ) )

			pass

		# after finishing one step rk4, we update all phases
		for up, osc in zip(updated_phase, self.Oscillator):
			osc.set_frequency( ( up - osc.get_phase() ) / self.dt )
			osc.set_phase( phase = up )
			pass


	# ---------------------------------------------------------------------------------------------

	def set_dump(self, filename: str = None, period: int = None ) -> None:

		if filename == None:
			print( "***ERROR***undefined name of output file", file=sys.stderr )
			exit(0)
			pass

		if period < 1:
			print( "***ERROR***Unexpected period counter, set_dump", file=sys.stderr )
			exit(0)
			pass

		self.output_name = filename
		self.dump_lag_time = period
		self.dump = True
		pass

	def dump_data(self, current_step : int ) -> None:
		dumper = open( self.output_name, 'at' )
		dumper.write( "#time_step id phase frequency\n" )

		for i, osc in enumerate( self.Oscillator ):
			print( current_step, i+1 , osc.get_phase(), osc.get_frequency(), sep=' ', file = dumper )
			pass

		print("", file = dumper)
		dumper.close()
		pass

	# ---------------------------------------------------------------------------------------------

	def set_compute_sync(self, filename: str = None, period: int = None) -> None:
		if filename == None:
			print( "***ERROR***undefined name of output file", file=sys.stderr )
			exit(0)
			pass

		if period < 1:
			print( "***ERROR***Unexpected period counter, set_compute_sync", file=sys.stderr )
			exit(0)
			pass

		self.output_name_sync = filename
		self.sync_lag_time = period
		self.sync = True
		pass

	def dump_sync(self, current_step: int ):
		dumper = open( self.output_name_sync, 'at' )

		ave_cosine = 0.0
		ave_sine   = 0.0
		for osc in self.Oscillator:
			ave_cosine += math.cos( osc.get_phase() )
			ave_sine   += math.sin( osc.get_phase() )
			pass

		ave_cosine /= self.N
		ave_sine   /= self.N

		ave_phase = math.atan2( ave_sine, ave_cosine )

		dumper.write( f"{current_step} {(ave_cosine*ave_cosine + ave_sine*ave_sine)} {ave_phase}\n" )
		dumper.close()
		pass

	# ---------------------------------------------------------------------------------------------

	def set_log(self, period: int = None) -> None:
		if period < 1:
			print( "***ERROR***Unexpected period counter, set_log", file=sys.stderr )
			exit(0)
			pass

		self.log_lag_time = period
		self.log = True
		pass


	# ---------------------------------------------------------------------------------------------

	def run(self, steps: int = 0 ) -> None:

		i_step = 0
		while i_step <= steps:

			# to dump data every N steps
			if self.dump == True and i_step % self.dump_lag_time == 0:
				self.dump_data( i_step )
				pass

			# to dump sync data every N steps
			if self.sync == True and i_step % self.sync_lag_time == 0:
				self.dump_sync( i_step )
				pass

			if self.log == True and i_step % self.log_lag_time == 0:
				print( f"{i_step}/{steps}" )
				pass

			if self.rk4_integrator == True:
				self.rk4_one_step()
				pass

			i_step += 1
			pass

		print( "run complete!" )
