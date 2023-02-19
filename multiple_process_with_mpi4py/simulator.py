from agent import oscillator
import math, random, sys, copy
from typing import List
from mpi4py import MPI

class kuramoto:
	def __init__(self, Noscillators : int, timestep: int = 0 ) -> None:

		MPI.Init()

		# to start MPI communication env.
		self.comm = MPI.COMM_WORLD

		# to get the rank of each process
		self.rank = self.comm.Get_rank()

		# to get the size of all process
		self.size = self.comm.Get_size()

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

		if self.size > 1:
			self.share = int( self.N / (self.size - 1) )



		if self.rank == 0:
			self.dump = False
			self.sync = False
			self.log  = False

			self.licence(self.size)
			print( f"{self.N} oscillators were defined." )
			pass

		self.rk4_integrator = False
		self.timestep = timestep


		# to assign the share (portion) of each process
		# if the size of processes is more than 1,
		# then the first process is the master, and others are slaves
		# if the size is 1, then master and slave are the same
		if self.size > 1:
			if self.rank != 0:
				self.bound_start = ( self.rank-1 ) * self.share
				self.bound_end   = self.bound_start + self.share
				if self.rank == self.size - 1:
					self.bound_end = self.N
					pass
				print( "proc %d start bound %d end bound %d"%(self.rank, self.bound_start, self.bound_end) )
				pass
			else:
				self.bound_start = self.bound_end = 0
		else:
			self.bound_start = 0
			self.bound_end   = self.N
			pass
		pass


	def licence(self, s: int) -> None:
		print( "K U R A M O T O - M O D E L" )
		print( "Last update: 29 JAN 2023, V 0.02" )
		print( "MPI compatible, mpi4py, No. proc(s)", s )
		print( "Created by Russell Kajouri, russellkajouri@gmail.com" )
		print( "" )

	def __del__( self ):
		if self.rank == 0:
			# to close the dumping obj of snapshot
			if self.dump == True:
				self.snap_dumper.close()

			# to close the dumping obj of sync data
			if self.sync == True:
				self.sync_dumper.close()
				pass
			print( "run complete!" )

		MPI.Finalize()

	def get_timestep() -> int:
		if self.rank == 0:
			return self.timestep


	# ---------------------------------------------------------------------------------------------

	# to set value of phase randomly
	def set_uniform_phase(self, lowBound : float = -math.pi, highBound : float = math.pi ) -> None:
		if self.rank == 0:
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

		# to broadcast the data to other process
		self.Oscillator = self.comm.bcast( self.Oscillator, root=0 )

		# to checks the situatio you can active the below commands
		#for osc in self.Oscillator:
		#	print( self.rank, osc.get_phase() )
		pass

	# to set value of phase by user not randomly
	def set_phases( self, phis : List[float] ) -> None:
		if self.rank == 0:
			if len( phis ) != self.N:
				print( "***ERROR***Unexpected number of oscillators' phase", file = sys.stderr )
				exit( 0 )
				pass

			for osc, ph in zip( self.Oscillator, phis ):
				osc.set_phase( phase = ph )
				pass
			pass
		# to broadcast the data to other process
		self.Oscillator = self.comm.bcast( self.Oscillator, root=0 )
		pass

	# ---------------------------------------------------------------------------------------------

	# to set the value of intrinsic frequencies of oscillators
	def set_guassin_frequency(self, mean : float = 0.0, std_dev : float = 1.0 ) -> None:
		if self.rank == 0:
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

		self.Oscillator = self.comm.bcast( self.Oscillator, root=0 )

		# to check out the details of the code, uncomment the below commands
		#for osc in self.Oscillator:
		#	print( self.rank, osc.get_phase(), osc.get_frequency() )
		#	pass
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

		self.Oscillator = self.comm.bcast( self.Oscillator, root=0 )
		pass

	# ---------------------------------------------------------------------------------------------

	# to show the value of phases
	def get_phases(self) -> list:
		if self.rank == 0:
			phis = []
			for osc in self.Oscillator:
				phis.append( osc.get_phase() )

			return phis

	# to show the value of phases
	def get_frequencies(self) -> list:
		if self.rank == 0:
			freqs = []
			for osc in self.Oscillator:
				freqs.append( osc.get_frequency() )

			return freqs

	# ---------------------------------------------------------------------------------------------

	# all process can read the coupling strength
	# we don't have any broadcast in this section
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

		print( "proc ", self.rank, "Copuling strength were assigned" )
		pass

	def get_coupling( self ):
		if self.rank == 0:
			return self.K

	def get_neighborsList(self):
		if self.rank == 0:
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
		for i, osc in enumerate( self.Oscillator[ self.bound_start : self.bound_end ] ):

			# if the oscillator does not have any neighbours that means it is independent of all neighoburs
			if osc.get_Nneighbors() == 0:
				updated_phase.append( osc.get_phase() + osc.get_intrinsic_frequency() * self.dt )

				# there is no need to compute the rest of the expression for an independent oscillator
				continue


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

		if self.size > 1:
			# MPI COMMANDS TO COMMUNICATE WITH OTHER PROCESSES
			if self.rank == 0:
				updated_phase = [ 0.0 for i in range( self.N ) ]
				for proc_id in range( 1, self.size ):
					received_data = self.comm.recv( source = proc_id, tag = (100 + proc_id) )
					local_bound_start = (proc_id - 1) * self.share
					updated_phase[ local_bound_start : local_bound_start + len(received_data) ] = received_data

				# after finishing one step rk4, we update all phases
				for up, osc in zip(updated_phase, self.Oscillator):
					osc.set_frequency( ( up - osc.get_phase() ) / self.dt )
					osc.set_phase( phase = up )
					pass

			else:
				# every process sends the data to the perocess with rank 0
				self.comm.send( updated_phase, dest = 0, tag = (100 + self.rank) )
				pass
		else:
			# after finishing one step rk4, we update all phases
			for up, osc in zip(updated_phase, self.Oscillator):
				osc.set_frequency( ( up - osc.get_phase() ) / self.dt )
				osc.set_phase( phase = up )
				pass
			pass
		pass


	# ---------------------------------------------------------------------------------------------

	def set_dump(self, filename: str = None, period: int = None, overwrite: bool = None) -> None:

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
		self.dump_overwrite = overwrite
		self.dump = True

		if self.dump_overwrite == None or self.dump_overwrite == False:
			self.snap_dumper = open( self.output_name, 'at' )
		elif self.dump_overwrite == True:
			self.snap_dumper = open( self.output_name, 'wt' )
		else:
			print( "***ERROR***Undefined overwrite mode", file = sys.stderr )
			exit( 0 )
			pass
		pass

	def dump_data(self, current_step : int ) -> None:

		self.snap_dumper.write( "#time_step id phase frequency\n" )

		for i, osc in enumerate( self.Oscillator ):
			print( current_step, i+1 , osc.get_phase(), osc.get_frequency(), sep=' ', file = self.snap_dumper )
			pass

		print("", file = self.snap_dumper, flush = True)
		pass

	# ---------------------------------------------------------------------------------------------

	def set_compute_sync(self, filename: str = None, period: int = None, overwrite: bool = None) -> None:
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
		self.sync_overwrite = overwrite

		if self.sync_overwrite == None or self.sync_overwrite == True:
			self.sync_dumper = open( self.output_name_sync, 'wt' )
		elif self.sync_overwrite == False:
			self.sync_dumper = open( self.output_name_sync, 'wt' )
		else:
			print("***ERROR***Undefined overwrite mode", file = sys.stderr )
			exit( 0 )
			pass
		pass

	def dump_sync(self, current_step: int ):

		ave_cosine = 0.0
		ave_sine   = 0.0
		for osc in self.Oscillator:
			ave_cosine += math.cos( osc.get_phase() )
			ave_sine   += math.sin( osc.get_phase() )
			pass

		ave_cosine /= self.N
		ave_sine   /= self.N

		ave_phase = math.atan2( ave_sine, ave_cosine )

		self.sync_dumper.write( f"{current_step} {(ave_cosine*ave_cosine + ave_sine*ave_sine)} {ave_phase}\n" )
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

		steps = int( steps )

		i_step = 0
		while i_step <= steps:

			# to dump data every N steps
			if self.rank == 0 and self.dump == True and i_step % self.dump_lag_time == 0:
				self.dump_data( self.timestep )
				pass

			# to dump sync data every N steps
			if self.rank == 0 and self.sync == True and i_step % self.sync_lag_time == 0:
				self.dump_sync( self.timestep )
				pass

			if self.rank == 0 and self.log == True and i_step % self.log_lag_time == 0:
				print( f"{i_step}/{steps} : {self.timestep}" )
				pass

			MPI.Barrier()

			if self.rk4_integrator == True:
				self.rk4_one_step()
				pass

			# we just update all oscillator and phases and local frequencies
			self.Oscillator = self.comm.bcast( self.Oscillator, root=0 )

			i_step += 1
			self.timestep += 1
			pass
