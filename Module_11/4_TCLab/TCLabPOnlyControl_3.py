import numpy as np
import matplotlib.pyplot as plt
import tclab
import time

# -----------------------------
# Adjust controller gain (Kc)
#  from ITAE tuning correlation
# -----------------------------
Kc = 4.45

n = 600  # Number of second time points (10 min)
tm = np.linspace(0,n-1,n) # Time values
lab = tclab.TCLab()
T1 = np.zeros(n)
Q1 = np.zeros(n)
# step setpoint from 23.0 to 60.0 degC
SP1 = np.ones(n)*23.0
SP1[10:] = 60.0
Q1_bias = 0.0
for i in range(n):
    # record measurement
    T1[i] = lab.T1

    # --------------------------------------------------
    # fill-in P-only controller equation to change Q1[i]
    # --------------------------------------------------
    Q1[i] = Q1_bias + Kc * (SP1[i]-T1[i])

    # implement new heater value
    Q1[i] = max(0,min(100,Q1[i])) # clip to 0-100%
    lab.Q1(Q1[i])
    if i%20==0:
        print(' Heater,   Temp,  Setpoint')
    print(f'{Q1[i]:7.2f},{T1[i]:7.2f},{SP1[i]:7.2f}')
    # wait for 1 sec
    time.sleep(1)
lab.close()
# Save data file
data = np.vstack((tm,Q1,T1,SP1)).T
np.savetxt('P-only.csv',data,delimiter=',',\
           header='Time,Q1,T1,SP1',comments='')

# Create Figure
plt.figure(figsize=(10,7))
ax = plt.subplot(2,1,1)
ax.grid()
plt.plot(tm/60.0,SP1,'k-',label=r'$T_1$ SP')
plt.plot(tm/60.0,T1,'r.',label=r'$T_1$ PV')
plt.text(6.1,30,'Measured Offset: ' + str(np.round(SP1[-1]-T1[-1],2)))
offset = 60 - (23+0.9*Kc*60)/(1+0.9*Kc)
plt.text(6.1,26,'Calculated Offset: ' + str(np.round(offset,2)))
plt.text(6.1,22,r'$K_c$: ' + str(np.round(Kc,2)))  
plt.plot([tm[-1]/60.0,tm[-1]/60.0],[SP1[-1],T1[-1]],\
         'b-',lw=3,alpha=0.5)
plt.ylabel(r'Temp ($^oC$)')
plt.xlim([0,10])
plt.legend(loc=2)
ax = plt.subplot(2,1,2)
ax.grid()
plt.plot(tm/60.0,Q1,'b-',label=r'$Q_1$')
plt.ylabel(r'Heater (%)')
plt.xlabel('Time (min)')
plt.legend(loc=1)
plt.savefig('P-only_Control.png')
plt.show()