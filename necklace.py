#Solving the necklace problem
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
from scipy.stats import linregress
#from scipy.constants import g

# set random seed
np.random.seed(4132)

# define initial state
state_0 = np.random.randint(0,21,size=20)

# lock end beads in the middle
state_0[0]  = 10
state_0[19] = 10
initial = np.copy(state_0)

# define mass of beads, spring constant, gravitational acceleration
#this is what affects the shape of the graph (ratio)
m = 2.5*2 #*4 for .666
#k = 15*2
k = 15
g = 9.81
#change m/k ratio to change eqiulibrium
# print(m/k)

# define move function
# the argument is the indexed state array not the entire array
def move(state):
    # random move up or down by 1
    randval = np.random.random()
    if randval < 0.5:
        new_state = state + 1
    else:
        new_state = state - 1

    return new_state

# define cost function
# total energy of the system of hanging masses and springs
def E(state):
    # grav potential energy
    Egrav = m * g * state.sum()

    # elastic potential energy
    Eelastic = 0
    for i in range(state.size-1):
        Eelastic += 0.5 * k * (np.abs(state[i]-state[i+1]))**2

    return Egrav + Eelastic

# define function for simulated annealing
def anneal(state, T0, Tf):
    # set temperature for each iteration of moves
    T = T0
    # initialize temperature and total energy lists
    T_list = []
    E_list = []
    while T > Tf:
        T_list.append(T)
        E_list.append(E(state))
        # move beads ***NOT THE FIXED ENDS***
        for i in range(1, len(state)-1):
            # calculate initial energy of state
            E_0 = E(state)

            # copy state array to check energy of new possible state
            copy_state = np.copy(state)

            # get new state
            new_state = move(state[i])
            copy_state[i] = new_state

            # determine acceptance of the move
            # calculate energy of new_state
            E_f = E(copy_state)

            if E_f < E_0:
                state[i] = new_state

            else:
                prob = np.random.random()
                if prob < np.exp(-abs(E_f - E_0)/T):
                    state[i] = new_state
                else:
                    state[i] = state[i]

        # decrease T
        T = 0.995*T

    return state, T_list, E_list

# do the annealing starting with a random state
state_f, T_list, E_list = anneal(state_0, 500, .1)


'''
fit the positions of the necklace with an actual catenary
using the cosh function
'''

def catenary(x, a, b):
    return a * np.cosh((x-9.5)*b/a)-100

x_data = np.zeros(20)

for i in range(x_data.size):
    x_data[i] = i

popt, pcov = curve_fit(catenary, x_data, state_f, [.03, .05], maxfev=4000)

y_catenary = catenary(x_data, *popt)

ss, iii, R, ppp, stderr = linregress(y_catenary, state_f)

ratio = round(m/k, 5)

print("&^&^&^&^")
print(R)

# plot necklace
# cs = {'fontname':'Times New Roman'}
plt.plot(initial, color='r', label = 'initial state')
plt.plot(state_f, color='b', label = 'final state')
plt.title('Free-hanging necklace with \nmass/spring constant ratio = ' + str(ratio))
plt.legend()
plt.xlabel('x position of beads')
plt.ylabel('Discrete Energy Level')
# plt.show()
plt.savefig('necklace')
plt.close()


# plot necklace with catenary fit
plt.plot(state_f, color='r', label='free-hanging necklace')
plt.plot(y_catenary, color='b', label = 'catenary curve')
plt.title('Catenary Fit to the hanging necklace with \nmass/spring constant ratio = ' + str(ratio))
plt.legend()
# plt.show()
plt.savefig('fit_necklace')
plt.close()


# plot energy vs temperature
fig, ax = plt.subplots()
plt.plot(T_list, E_list, color='r')
plt.title('Total Energy vs. Temperature with \nmass/spring constant ratio = ' + str(ratio))
plt.xlabel('Temperature')
plt.ylabel('Total Energy')
ax.invert_xaxis()

# plt.show()
plt.savefig('EnergyVtemp')
plt.close()
