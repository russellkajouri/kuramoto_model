from simulator import kuramoto

def main():

	Kuramoto = kuramoto( Noscillators = 50 )
	Kuramoto.set_uniform_phase()
	Kuramoto.set_guassin_frequency( mean = 0, std_dev = 1)
	Kuramoto.set_coupling( coupling = 1 )
	Kuramoto.integrator_rk4( dt = 0.01 )
	Kuramoto.set_dump( filename= "out.dat", period = 50 )
	Kuramoto.set_compute_sync( filename= "sync.dat", period = 5 )
	Kuramoto.set_log( period = 300 )
	Kuramoto.run( steps = 3000 )

if __name__ == "__main__":
	main()
