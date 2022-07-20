import datetime
import matplotlib.pyplot as plt

ACTION_CODE = {
    'comeIn' : 0,
    'comeOut': 1,
    'toKitchen' : 2,
    'outKitchen' : 3,
}



from PetriNet import *
from LightSystem import *
from User import *
from SecuritySystem import *
from ClimateSys import  *
from HouseHoldSys import *
from weather import *
import const
from  Plan import *

DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
DATE_FORMAT = '%d/%m/%Y'
TIME_FORMAT = '%H:%M:%S'



class Modeling:
    def __init__(self, PID = 0):
        self.PID = PID

        #user
        self.user = User(name='myuser')
        #Door
        self.door = Door(name='D')

        #Light
        self.DoorLight = SimpleLight(name="DoorLight")
        self.KitchenLight = SimpleLight(name='KitchenLight')
        self.BedRoomLight = SimpleLight(name='BedRoomLight')
        self.LivingRoomLight = SimpleLight(name='LivingRoomLight')
        self.ToiletLight = SimpleLight(name='ToiletLight')
        self.WorkRoomLight = SimpleLight(name='WorkRoomLight')

        self.BedRoomCurtain = Curtain(name='BedRoomCurtain')

        self.LightSysObjs = [self.DoorLight, self.KitchenLight,
                             self.BedRoomLight, self.LivingRoomLight,
                             self.ToiletLight, self.WorkRoomLight]
        self.LightSys = LightSystem(name='LSys', Lights= self.LightSysObjs)

        #Security
        self.Speaker = Speaker(name='Speaker')
        self.SecuritySysObjects = [self.Speaker]

        #Weather
        self.Condition = Conđition(name='Condition')
        self.ClimateSysObjs = [self.Condition]

        #Kitchen
        self.Store = GasStore(name='GasStore')
        self.AirPurifier = AirPurifier(name='AirPurifier')

        self.KitchenObjs = [self.Store, self.AirPurifier]

        #All Objects
        self.allObject = []
        self.allObject.extend(self.LightSysObjs)
        self.allObject.extend(self.KitchenObjs)
        self.allObject.extend(self.ClimateSysObjs)
        self.allObject.append(self.user)
        #params

        #time
        self.TimeArr = []
        #temperature
        self.TinDoorArr  = []
        self.ToutDoorArr = []
        self.TsettingArr = []
        self.T_setting = const.GLOBAL_T_SETTING
        self.TinsideNow = 30

        #wattage
        self.WattageArr = []
        self.WattageSumArr = []

        #PID
        self.errorBefore = 0
        self.I_ = 0

        #asyn
        self.asyn()
        self.actionInit()

        #tmp

        self.error = []

    def actionInit(self):
        user = self.user
        self.userAction = {
            'comeIn': [user.comeIN, None],
            'comeOut': [user.comeOut, None]
        }
        self.lightSysAction = {
            'sunset': [[self.LightSys.sunset, None]],
            'night': [[self.LightSys.night, None]],
            'sleep': [[self.LightSys.sleep, None]],
            'getup': [[self.LightSys.getup, None]],
        }


    def asyn(self):
        self.checkUser()

        self.user.goSleepTran.setLabel('goSleep')
        self.LightSys.SleepTran.setLabel('notgoSleep')

        self.user.getUPTran.setLabel('getUp')
        self.LightSys.getupTran.setLabel('notgetUp')


    def checkUser(self):
        self.user.PN.run([self.user.gotoDoorTran])
        passwork = '123'#input("Input PassWork")
        if passwork == '123' or 1:

            self.user.PN.run([self.user.Input])
            self.user.PN.run([self.user.vetifyTran])

    def weatherDay(self, fromDate, toDate):
        startDate = datetime.date(year=2021, month=7, day=21)
        fromIndex = (fromDate - startDate).days
        toIndex = (toDate - fromDate).days + fromIndex + 1
        weatherData = getWeatherDay()
        return weatherData[fromIndex:toIndex]

    def weatherHour(self, fromDatetime, toDatetime = None):
        if toDatetime == None:
            toDatetime = fromDatetime
        startDatetime = datetime.datetime.strptime('24/07/2021 00:00:00', DATETIME_FORMAT)
        fromIndex = int((fromDatetime - startDatetime).total_seconds() / 3600)
        toIndex = int((toDatetime - fromDatetime).total_seconds() / 3600 + fromIndex + 1)
        weatherData = getWeatherHour()
        rc = weatherData[fromIndex:toIndex]
        return [float(i) for i in rc]

    def lightShow(self, index, Lights = None):
        label = "ПИД-регулятор"
        if (not self.PID):
            label = 'вкл/выкл-регулятора'
        if Lights == None:
            Lights = self.LightSys.Lights
        pl = plt.figure(index)
        for i in Lights:

            plt.plot(self.TimeArr,i.status)
        plt.xlabel("время")
        plt.ylabel("яркость (% Макс.)")
        plt.legend()
        #plt.title("LightSystem")

    def conditionShow(self, index):
        label = "ПИД-регулятор"
        if (not self.PID):
            label = 'вкл/выкл-регулятора'
        pl = plt.figure(index)
        plt.plot(self.TimeArr, self.Condition.status, label=label)
        plt.xlabel("время")
        plt.ylabel("мощность (% Макс.)")
        plt.legend()
        #plt.title("Condition")

    def conditionEnergy(self, index):
        label = "ПИД-регулятор"
        if (not self.PID):
            label = 'вкл/выкл-регулятора'
        pl = plt.figure(index)
        plt.plot(self.TimeArr, self.Condition.energy, label=label)
        plt.xlabel("время")
        plt.ylabel("мощность (W)")
        plt.legend()
        #plt.title("Condition")

    def eneryShow(self, index):
        pl = plt.figure(index)
        SumE = []
        allObj = [self.Condition,]
        #allObj.extend(self.LightSysObjs)
        for i in range(len(allObj[0].energy)):
            tmp = 0
            for k in allObj:
                tmp += k.energy[i]
            SumE.append(tmp)

        ESum = [sum(SumE[0:i]) * self.timeStep / 3600 / 100 for i in range(len(SumE))]
        label = "ПИД-регулятор"
        if (not self.PID):
            label = 'вкл/выкл-регулятора'
        plt.plot(self.TimeArr, ESum, label= label)
        plt.xlabel("время")
        plt.ylabel("общая мощность (кВтч)")
        plt.legend()

    def tempseShow(self, index):
        label = "ПИД-регулятор"
        if (not self.PID):
            label = 'вкл/выкл-регулятора'
        plot1 = plt.figure(index)
        if (self.PID):
            plt.plot(self.TimeArr, self.ToutDoorArr,  'g--', label="внешняя",)
            plt.plot(self.TimeArr, self.TsettingArr, 'r-.', label="установленная")
        plt.plot(self.TimeArr, self.TinDoorArr, label="внутренняя " + label)

        plt.xlabel("время")
        plt.ylabel("температура")
        plt.legend()

    def userShow(self):
        for i in range(len(self.user.status)):
            print(self.TimeArr[i], self.user.status[i])

    def show(self):
        self.tempseShow(1)
        #self.lightShow(2, None)
        #print(self.user.status)
        #self.userShow()
        self.conditionShow(3)
        self.eneryShow(4)
        self.conditionEnergy(5)
        #plt.show()

    def addStatus(self):
        for i in self.allObject:
            i.addStatus()

    def updateTempInside(self, condition, ToutsideNow):
        delta_T_fromOutDoor = ToutsideNow * (ToutsideNow - self.TinsideNow) * 0.05 / 3600 * self.timeStep
        W_fromInDoor = 0
        for i in self.LightSysObjs:
            W_fromInDoor += i.get_WTemp() #for 1 second
        W_fromInDoor *= self.timeStep
        W_fromCondition = condition.calc_W_Temp(self.timeStep)
        sumWatt = W_fromInDoor - W_fromCondition * int(condition.isOn())
        deltaTemp = sumWatt / (1000 * 1005) + delta_T_fromOutDoor
        #if deltaTemp < -30:
            #print(self.TinsideNow,delta_T_fromOutDoor,W_fromInDoor, W_fromCondition,int(condition.isOn()), deltaTemp)
        #print(condition.getLevel(), self.timeStep)
        self.TinsideNow += deltaTemp

    def control_condition_onOff(self, condition):
        #print(GLOBAL_TIME)
        ToutsideNow = float(self.weatherHour(const.GLOBAL_TIME)[0])
        self.ToutDoorArr.append(ToutsideNow)
        self.TinDoorArr.append(self.TinsideNow)
        self.TsettingArr.append(self.T_setting)

        T_sigma = 2
        if self.TinsideNow > self.T_setting + T_sigma and not condition.isOn():
            rc = condition.turnOn()
            if not rc:
                print('cant turn on condition')
                # break
        if self.TinsideNow < self.T_setting - T_sigma and not condition.isOff():
            rc = condition.turnOff()
            if not rc:
                print("Cant turn off condition")
                # break
        self.updateTempInside(condition, ToutsideNow)

    def control_condition_PID(self, condition):
        ToutsideNow = float(self.weatherHour(const.GLOBAL_TIME)[0])
        self.ToutDoorArr.append(ToutsideNow)
        self.TinDoorArr.append(self.TinsideNow)
        self.TsettingArr.append(self.T_setting)
        Kp = 0.5
        Ki = 1
        Kd = 1
        error = self.T_setting - self.TinsideNow
        P = Kp * error
        self.I_ += error
        I = Ki * self.I_
        D_ = (error - self.errorBefore) / self.timeStep
        D = Kd * D_
        u_t = P + D  #+ I# + D
        self.error.append(u_t)
        step = min(abs(int(u_t / (745 * self.timeStep / (1005 * 1005)))), 20)
        if self.Condition.isOff():
            self.Condition.turnOn()
        if (u_t < 0):
            self.Condition.incLevel(step)
        if (u_t > 0):
            self.Condition.decLevel(step)

        self.updateTempInside(self.Condition, ToutsideNow)
        self.errorBefore = error

    def runAction(self, func, params = None):
        if params == None:
            func()
        else:
            func(params)
    #duration in Hours
    '''
    def getActionArr(self, startDateTime, duration):
        
        #[[Time1, [Action11, Action12]], [Timw2], [Action21, Action22], ...]
        
        user_action = [[startDateTime + datetime.timedelta(hours=18), [self.userAction['comeIn']]],
                       [startDateTime + datetime.timedelta(hours= 24 + 8), [self.userAction['comeOut']]],
                       ]
        res = []
        #startDate = datetime.datetime.now()
        endDate = startDateTime + datetime.timedelta(hours=duration)

        light_action = [[startDateTime + datetime.timedelta(hours=7), [self.lightSysAction['getup']]],
                        [startDateTime + datetime.timedelta(hours=17), [self.lightSysAction['sunset']]],
                        [startDateTime + datetime.timedelta(hours=22), [self.lightSysAction['night']]],
                        [startDateTime + datetime.timedelta(hours=25), [self.lightSysAction['sleep']]]
                        ]
        res.extend(light_action)
        res.extend(user_action)
        res.sort(key= lambda X: X[0])
        return res
    '''

    def getNextAction(self):
        planArray = [self.userPlan, self.LightSysPlan]
        #planArray = [self.LightSysPlan]
        minAction = None
        minPlan = None
        for p in planArray:
            act = p.getAction()
            if act == None:
                continue
            #print(act, act.name)
            if minAction == None:
                minAction = act
                minPlan = p
            elif minAction.startTime > act.startTime:
                minAction = act
                minPlan = p
        if (minPlan):
            minPlan.nextAction()
            return minPlan.popAction()
        return None

    # duration in Hour
    def run(self, startTime, duration):
        endTime = startTime + datetime.timedelta(hours=duration)
        self.timeStep = 10  #second
        const.GLOBAL_TIME = startTime
        date = startTime.date()
        sunsetTime = datetime.datetime.strptime('17:00:00', '%H:%M:%S').time()

        self.userPlan = UserPlan(user=self.user, startTime= startTime,
                                 queue=[Action(name='ComeIn', code= 0,
                                               startTime= startTime + datetime.timedelta(hours=6),
                                               duration=0,work=[[self.user.comeIN, None]]),
                                        ]
                                 )
        '''
        self.userPlan.addAction(Action(name='toKitchen', code = ACTION_CODE_TO_KITCHEN,
                                       startTime=None, duration=2, work=[self.user.goInKitchen, None]))
        self.userPlan.addAction(Action(name='outKitchen', code=ACTION_CODE_OUT_KITCHEN,
                                       startTime=None, duration=1, work=[self.user.goOutKitchen, None]))
        self.userPlan.addAction(Action(name='ComeOut', code= ACTION_CODE_COME_OUT,
                                       startTime=None, duration=3, work=[self.user.comeOut, None]))
        '''
        self.LightSysPlan = LightSystemPlan(lightSys = self.LightSys, startTime=startTime,
                                            queue=[Action(name='Sunset',
                                                          startTime=datetime.datetime.combine(date , sunsetTime),
                                                          duration=0, work=[[self.LightSys.sunset, None]], code=ACTION_CODE_SUNSET)])


        nextAction = self.getNextAction()
        self.Condition.turnOn()
        self.Condition.setLevel(newLevel=90)
        print("Start While")
        while (const.GLOBAL_TIME < endTime):
            self.T_setting = const.GLOBAL_T_SETTING
            self.TimeArr.append(const.GLOBAL_TIME)
            if self.PID == 1:
                self.control_condition_PID(self.Condition)
            else:
                self.control_condition_onOff(self.Condition)
            self.addStatus()

            while (nextAction and const.GLOBAL_TIME >= nextAction.startTime):
                #print(nextAction.name, nextAction.startTime, const.GLOBAL_TIME)
                #self.runAction(nextAction.work[0], nextAction.work[1])
                nextAction.run()
                nextAction = self.getNextAction()


            const.GLOBAL_TIME += datetime.timedelta(seconds=self.timeStep)





duration = 1 * 24
m = Modeling(PID = 0)
#startTime = datetime.datetime(year=2021, month=7, day=24, hour=0,minute=0, second=0)
startTime = datetime.datetime.strptime('25/07/2021 12:0:0', DATETIME_FORMAT)
print("Start Run")
m.run(startTime=startTime, duration=duration,)
m2 = Modeling(PID = 1)
startTime = datetime.datetime.strptime('25/07/2021 12:0:0', DATETIME_FORMAT)
print("Start Run")
m2.run(startTime=startTime, duration=duration,)
#print(m.LivingRoomLight.status)
print("Start Show")



label = "ПИД-регулятор"
a = sum([abs(i) for i in m2.error]) / len(m2.error)
sigma = sum([(a - i) * (a - i) for i in m2.error]) / len(m2.error)
print(a, ' +- ', sigma)
m.show()
m2.show()


plt.show()


