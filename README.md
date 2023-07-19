## KURAMOTO Model
A single process implementation of the Kuramoto model by the 4th-order Runge-Kutta method.

The famous Kuramoto model exhibits phase synchronization among coupled self-sustained oscillators. I here implemented the Kuramoto model by the 4th-order Runge-Kutta discretisation method. The mathematical formula for the time evolution of an oscillator's phase is presented

$$\dot{\varphi}_i = \omega_i + \frac{ 1 }{ N_i } \sum^{ N_i }_{ j=1 } \kappa_{ij} \sin( \varphi_j - \varphi_i )  , $$

where $\varphi$ and $\omega$ are the phase and intrinsic frequency of the $i^{th}$ oscillator, respectively. Oscillators are coupled to each other and have been inserted in the formula by $\kappa_{ij}$, while $N_i$ illustrates the number of neighbours of the $i^{th}$ oscillator. we can discrete the above equation by the 4th-order Rung-kutta method which consists of a summation of four different sentences as follows

$$ k_1 = f(t_n, \varphi(t_n) ) = \omega_i + \frac{ 1 }{ N_i } \sum^{ N_i }_{ j=1 } \kappa_{ij} \sin( \varphi_j(t_n) - \varphi_i(t_n) ), $$

$$ k_2 = f(t_n+\frac{h}{2}, \varphi(t_n) + h\frac{k_1}{2} ) = \omega_i + \frac{ 1 }{ N_i } \sum^{ N_i }_{ j=1 } \kappa_{ij} \sin( \varphi_j(t_n) - (\varphi_i(t_n) + h\frac{k_1}{2} )) $$

$$ k_3 = f(t_n+\frac{h}{2}, \varphi(t_n) + h\frac{k_2}{2} ) = \omega_i + \frac{ 1 }{ N_i } \sum^{ N_i }_{ j=1 } \kappa_{ij} \sin( \varphi_j(t_n) - (\varphi_i(t_n) + h\frac{k_2}{2} )) $$

$$ k_4 = f(t_n + h, \varphi(t_n) + hk_3 ) = \omega_i + \frac{ 1 }{ N_i } \sum^{ N_i }_{ j=1 } \kappa_{ij} \sin( \varphi_j(t_n) - (\varphi_i(t_n) + hk_3 )) $$

The time $t$ variable is not revealed explicitly in the equation, therefore we should continue our approach with variable $\varphi_i$. To obtain the value of $\varphi_i(t_{n+1})$; we derive the following equation

$$ \varphi_i(t_{n+1}) = \varphi_i(t_n) + \frac{h}{6} ( k_1 + 2 ( k_2 + k_3 ) + k_4 ). $$

-------

## All-to-all coupling
We can couple the oscillators to each other by many diverse approaches one of them is all-to-all which means all oscillators are connected to each other.
We also consider the value of the coupling $\kappa_{ij} = \kappa$ for all connections. On the other hand, we assumed every oscillator has an intrinsic frequency $\omega_i$ which has been selected from a mathematical distribution, i.e. Gaussian distribution $G(\mu, \sigma)$, where $\mu$ and $\sigma$ are the mean and standard deviation of the distribution, respectively. It has been turned out there is a critical coupling strength value for a group of the self-sustained oscillator which are coupled to each other al-to-all, and its value depends on the frequency distribution value on the mean point. 

$$ \kappa_c = \frac{ 2 }{\pi g(\bar{\omega}) } $$

Let us consider a normal dist. as the frequency dits. and then the value of the critical coupling strength will be derived as

$$ \kappa_c = \frac{2}{\pi G(0, 1) } = \frac{2 \sqrt{2\pi} \sigma }{\pi} $$
