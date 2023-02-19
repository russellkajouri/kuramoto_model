from simulator import kuramoto

def main():


	# to initialise the kuramoto system
	Kuramoto = kuramoto( Noscillators = 100 )

	# to set a random phases for all oscillators
	Kuramoto.set_uniform_phase()

	# to set the intrisic frequencies of all oscillators
	Kuramoto.set_guassin_frequency( mean = 0, std_dev = 1)

	# to set the interval time
	Kuramoto.integrator_rk4( dt = 0.005 )

	# to define the output of snapshot
	Kuramoto.set_dump( filename= "out.dat", period = 1e4 , overwrite = False )

	# to define the output of the synchroziation order
	Kuramoto.set_compute_sync( filename= "sync.dat", period = 5e3, overwrite = False )

	# to define the period of log and trun it on as well
	Kuramoto.set_log( period = 1e4 )

	init_kappa = 0.00
	ultm_kappa = 4.00
	itvl_kappa = 0.50

	while init_kappa <= ultm_kappa:

		# we would like to specify the new coupling every cycle
		Kuramoto.set_coupling( coupling = init_kappa )

		# this is the number of repeatitive cycle
		Kuramoto.run( steps = 1e5 )

		init_kappa += itvl_kappa
		pass

if __name__ == "__main__":
	main()
