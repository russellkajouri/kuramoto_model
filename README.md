## KURAMOTO Model
A single process implementation of the Kuramoto model by the 4th-order Runge-Kutta method.

The famous Kuramoto model exhibits phase synchronization among coupled self-sustained oscillators. I here implemented the Kuramoto model by the 4th-order Runge-Kutta discretisation method. The mathematical formula of time evolution of an oscillator's phase is presented

$$\dot{\varphi}_i = \omega_i + \frac{ 1 }{ N_i } \sum^{ N_i }_{ j=1 } \kappa_{ij} \sin( \varphi_j - \varphi_i )  , $$

where $\varphi$ and $\omega$ are the phase and intrinsic frequency of the $i^{th}$ oscillator, respectively. Oscillators are coupled to each other and has been inserted in the formula by $\kappa_{ij}$, while $N_i$ illustrates the number of neigbours of the $i^{th}$ oscillator.
