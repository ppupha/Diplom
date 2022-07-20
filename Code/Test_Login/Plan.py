ACTION_CODE_COME_IN = 0
ACTION_CODE_COME_OUT = 1
ACTION_CODE_TO_KITCHEN = 2
ACTION_CODE_COOKING_BREAKFAST = 16
ACTION_CODE_OUT_KITCHEN = 3
ACTION_CODE_SLEEP = 12
ACTION_CODE_GETUP = 13
ACTION_CODE_TO_TOILET_1 = 14
ACTION_CODE_TO_TOILET_2 = 15
ACTION_CODE_EAT_BREAKFAST = 17
ACTION_CODE_TO_LIVINGROOM = 18
ACTION_CODE_COOKING_DINNER = 19
ACTION_CODE_EAT_DINNER = 20
ACTION_CODE_WORK = 21

ACTION_CODE_SUNSET = 10
ACTION_CODE_NIGHT = 11

import datetime

from  const import *
import numpy.random as nr
import const as Const



def getNormal(M, sigma):
    rc = nr.normal(M, sigma)
    if rc < 0:
        return 0
    return rc

class Action:
    # durations in Mins
    def __init__(self, startTime = None, duration = 0, work = [], name = 'UnknowAction', code = None):
        self.startTime = startTime
        if not self.startTime:
            self.endTime = None
        else:
            self.endTime = self.startTime + datetime.timedelta(minutes=duration)
        self.work = work
        self.duration = duration
        self.name = name
        self.code = code

    def run(self):
        print(self.name, 'at ', Const.GLOBAL_TIME)
        for w in self.work:
            #print(w)
            rc = -1
            func = w[0]
            params = w[1]
            if (params == None):
                rc = func()
            else:
                rc = func(params)
            if (rc != 1):

                print(rc, "*" * 100)

class BasePlan:
    def __init__(self, startTime, queue = []):
        self.time = startTime
        self.queue = queue

    def addAction(self, action):
        if action.startTime == None:
            lastAction = self.getLastAction()
            action.startTime = lastAction.endTime
            action.endTime = action.startTime + datetime.timedelta(hours=action.duration)
        self.queue.append(action)
        return

    def popAction(self):
        return self.queue.pop(0)

    def getAction(self):
        if len(self.queue) > 0:
            return self.queue[0]
        return None

    def getLastAction(self):
        if len(self.queue) > 0:
            return self.queue[-1]
        return None

    def nextAction(self):
        return None

class UserPlan(BasePlan):
    def __init__(self, user, startTime, queue = []):
        BasePlan.__init__(self, startTime, queue)
        self.user = user

    def nextAction(self):
        lastAction = self.getLastAction()
        code = lastAction.code
        lastTime = lastAction.endTime
        new_action = None
        date = lastAction.startTime.date()
        time = lastAction.endTime.time()

        #getUp
        if code == ACTION_CODE_SLEEP:
            time = datetime.datetime.strptime('7:00:00', TIME_FORMAT).time()
            startTime = datetime.datetime.combine(date + datetime.timedelta(days=1), time)
            new_action = Action(name='getUp', code=ACTION_CODE_GETUP,
                                startTime=startTime, duration=getNormal(5, 3),
                                work=[[self.user.getUp, None],
                                      [self.user.goOutBedRoom, None]])

        if code == ACTION_CODE_GETUP:
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='gotoToilet', code=ACTION_CODE_TO_TOILET_1,
                                startTime=startTime, duration= getNormal(10, 5),
                                work=[[self.user.goInToilet, None]])

        if code == ACTION_CODE_TO_TOILET_1:
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='Cook Bref', code=ACTION_CODE_COOKING_BREAKFAST,
                                startTime=startTime, duration=getNormal(30, 10),
                                work=[[self.user.goOutToilet, None],
                                      [self.user.goInKitchen, None],
                                      [self.user.startCooking, None]])
        if code ==  ACTION_CODE_COOKING_BREAKFAST:
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='HaveBref', code=ACTION_CODE_EAT_BREAKFAST,
                                startTime=startTime, duration=getNormal(15, 5),
                                work=[[self.user.finishCooking, None],
                                      [self.user.startEating, None]])

        if code == ACTION_CODE_EAT_BREAKFAST:
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='ComeOut', code=ACTION_CODE_COME_OUT,
                                startTime=startTime, duration=getNormal(8 * 60, 30),
                                work=[[self.user.finishEating, None],
                                      [self.user.goOutKitchen, None],
                                      [self.user.comeOut, None]])

        if code == ACTION_CODE_COME_OUT:
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='ComeIn', code= ACTION_CODE_COME_IN,
                                               startTime= startTime,
                                               duration=getNormal(5, 3),work=[[self.user.comeIN, None]])

        if (code == ACTION_CODE_COME_IN):
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='gotoLivingRoom', code=ACTION_CODE_TO_LIVINGROOM,
                                startTime=startTime, duration=getNormal(60, 30),
                                work=[[self.user.goInLivingRoom, None]])

        if (code == ACTION_CODE_TO_LIVINGROOM):
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='Cook', code=ACTION_CODE_COOKING_DINNER,
                                startTime=startTime, duration=getNormal(60, 30),
                                work=[[self.user.goOutLingRoom, None],
                                      [self.user.goInKitchen, None],
                                      [self.user.startCooking, None]])

        if (code == ACTION_CODE_COOKING_DINNER):
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='HaveDinner', code=ACTION_CODE_EAT_DINNER,
                                startTime=startTime, duration=getNormal(30, 10),
                                work=[[self.user.finishCooking, None],
                                      [self.user.startEating, None]])

        if (code == ACTION_CODE_EAT_DINNER):
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='Work', code=ACTION_CODE_WORK,
                                startTime=startTime, duration=getNormal(4 * 60, 30),
                                work=[[self.user.finishEating, None],
                                      [self.user.goOutKitchen, None],
                                      [self.user.goInWorkRoom, None]])

        if (code == ACTION_CODE_WORK):
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='GotoToilet', code=ACTION_CODE_TO_TOILET_2,
                                startTime=startTime, duration=getNormal(20, 10),
                                work=[[self.user.goOutWorkRoom, None],
                                      [self.user.goInToilet, None],])

        if (code == ACTION_CODE_TO_TOILET_2):
            time = (datetime.datetime.strptime('23:00:00', TIME_FORMAT) + datetime.timedelta(minutes= getNormal(10, 5))).time()
            startTime = datetime.datetime.combine(date, time)
            new_action = Action(name='Sleep', code=ACTION_CODE_SLEEP,
                                startTime=startTime, duration=getNormal(8 * 60, 60),
                                work=[[self.user.goOutToilet, None],
                                      [self.user.goInBedRoom, None],
                                      [self.user.goSleep, None]])


        if (new_action):
            self.addAction(new_action)
        return new_action

class LightSystemPlan(BasePlan):
    def __init__(self, lightSys, startTime, queue = []):
        BasePlan.__init__(self, startTime, queue)
        self.lightSys = lightSys
        self.matrix = None

    def nextAction(self):
        lastAction = self.getLastAction()
        code = lastAction.code
        new_Action = None
        date = lastAction.startTime.date()
        if code == ACTION_CODE_SUNSET:
            time = datetime.datetime.strptime('22:00:00', '%H:%M:%S').time()
            new_Action = Action(name='Night', startTime=datetime.datetime.combine(date, time),
                                duration=0, work=[[self.lightSys.night, None]], code=ACTION_CODE_NIGHT)
        elif code == ACTION_CODE_NIGHT:
            time = datetime.datetime.strptime('17:00:00', '%H:%M:%S').time()
            new_Action = Action(name='Sunset', startTime=datetime.datetime.combine(date + datetime.timedelta(days=1), time),
                                duration=0, work=[[self.lightSys.sunset, None]], code=ACTION_CODE_SUNSET)
        self.addAction(new_Action)


#print(getNormal(5, 3))