from PetriNet import *
import matplotlib.pyplot as plt
from weather import *
from ClimateSys import *

C = Conđition('Condition')
C.turnOn()
C.setLevel(100)
C.showStatus()
print(C.calc_W())

coef_Tout = 0.3
delta_in = 2
T_setting = 25
T_sigma = 1
m = 1000
c = 600
timeStep = 20
Total_Time = 24 * 3600 * 2
tempDataDay = getWeatherDay()
tempDataHour = getWeatherHour()
Time = [i / 3600 for i in range(0, Total_Time, timeStep)]

T_outDoor = [float(tempDataHour[int(i)]) for i in Time]
T_inDoor = []
C_energy = []
T_fromOutDoor = []
Sum_E = [0, ]
T_inside = 35

for i in range(len(Time)):
    T_inDoor.append(T_inside)
    C_E = C.calc_W()
    C_energy.append(C_E)
    Sum_E.append(C_E + Sum_E[-1])

    if T_inside > T_setting + T_sigma:
        rc = C.turnOn()
        if not rc:
            print('cant turn on')
            # break
    if T_inside < T_setting - T_sigma:
        rc = C.turnOff()
        if not rc:
            print("Cant turn off")
            # break
    # update
    delta_T_fromOutDoor = T_outDoor[i] * (T_outDoor[i] - T_inside) * coef_Tout * timeStep
    T_fromOutDoor.append(delta_T_fromOutDoor)
    W_fromInDoor = delta_in * timeStep
    W_fromCondition = C.calc_W_Temp(timeStep)
    sumWatt = delta_T_fromOutDoor + W_fromInDoor - W_fromCondition * int(C.isOn())
    deltaTemp = sumWatt / (m * c)
    if 0:
        print(deltaTemp, sumWatt, T_inside)
        print(delta_T_fromOutDoor, W_fromInDoor, W_fromCondition)
    T_inside += deltaTemp

plot1 = plt.figure(1)
plt.plot(Time, T_outDoor, label = "внешняя")
plt.plot(Time, T_inDoor, label = "внутренняя (Вкл./выкл.)")
plt.xlabel("время (ч)")
plt.ylabel("температура (oC)")
plt.legend()


plot2 = plt.figure(2)
plt.plot(Time, C_energy, label = 'Вкл./выкл.')
plt.xlabel("время (ч)")
plt.ylabel("мощность (W)")
plt.legend()

plot3 = plt.figure(3)
plt.plot(Time, Sum_E[1:], label = 'Вкл./выкл.')
plt.xlabel("время (ч)")
plt.ylabel("общая мощность(W)")
plt.legend()



T_inDoor2 = []
C_energy2 = []
Sum_E2 = [0, ]
Level = []
Kp = 1
Ki = 1
Kd = 1
I_ = 0
D_ = 0
error_before = 0
print("Start")
C.setLevel(50)
T_inside = 35
for i in range(len(Time)):
    T_inDoor2.append(T_inside)
    C_E = C.calc_W()
    C_energy2.append(C_E)
    Sum_E2.append(C_E + Sum_E2[-1])
    Level.append(C.getLevel())

    error = T_setting - T_inside
    P = Kp * error
    I_ += error * timeStep
    I = Ki * I_
    D_ = (error - error_before) / timeStep
    D = Kd * D_
    u_t = P  # + I + D

    error_before = error
    if (u_t < 0):
        C.incLevel(1)
    if (u_t > 0):
        C.decLevel(1)
    # update
    delta_T_fromOutDoor = (T_outDoor[i] * (T_outDoor[i] - T_inside) * coef_Tout) * timeStep
    W_fromInDoor = delta_in * timeStep
    W_fromCondition = C.calc_W_Temp(timeStep)
    sumWatt = delta_T_fromOutDoor + W_fromInDoor - W_fromCondition * int(C.isOn())
    deltaTemp = sumWatt / (m * c)
    if 0:
        print(u_t, T_inside, C.getLevel())
        # print(deltaTemp, sumWatt, T_inside)
        # print(delta_T_fromOutDoor, W_fromInDoor, W_fromCondition)
    T_inside += deltaTemp

plot1 = plt.figure(1)
plt.plot(Time, T_inDoor2, label="внутренняя (ПИД)")
plt.legend()

plot2 = plt.figure(2)
plt.plot(Time, C_energy2, label='ПИД-регулятор')
plt.legend()

plot3 = plt.figure(3)
plt.plot(Time, Sum_E2[1:], label='ПИД-регулятор')
plt.legend()


plot3 = plt.figure(4)
plt.plot(Time, Level)


plt.show()
