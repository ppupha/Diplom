from PetriNet import *
from const import *


class SimpleLight:
    def __init__(self, name, wattage = 15):
        self.name = name
        self.brighness = 50
        self.maxW = wattage
        self.coef_WTemp = 30 / 100
        self.time = []
        self.status = []
        self.energy = []

        #place
        self.onPlace = Place(tokens=[], name='on')
        self.offPlace = Place(tokens=[SimpleToken()], name='off')
        self.incPlace = Place(tokens=[SimpleToken() for i in range(100 - self.brighness)], name="inc")
        self.decPlace = Place(tokens=[SimpleToken() for i in range(self.brighness)], name="dec")

        self.onLightTrans = Transition(name="turn_on", arcIn=[ArcIn(place=self.offPlace), ],
                                       arcOut=[ArcOut(place=self.onPlace), ], label="")
        self.offLightTrans = Transition(name="turn_off", arcIn=[ArcIn(place=self.onPlace, ), ],
                                        arcOut=[ArcOut(place=self.offPlace), ], label="")

        self.decLightTrans = Transition(name="decLight",
                                        arcIn=[ArcIn(place=self.decPlace, ),
                                               ArcIn(place=self.onPlace)],
                                        arcOut=[ArcOut(place=self.onPlace, ),
                                                ArcOut(place=self.incPlace)])
        self.incLightTrans = Transition(name='incLight',
                                        arcIn=[ArcIn(place=self.incPlace, ),
                                               ArcIn(place=self.onPlace)],
                                        arcOut=[ArcOut(place=self.decPlace),
                                                ArcOut(place=self.onPlace)])

        self.PN = PetriNet([self.onLightTrans, self.offLightTrans, self.incLightTrans, self.decLightTrans],
                           name=self.name, type=LIGHT_TYPE)

    def addStatus(self):
        status = -1
        if self.isOn():
            status =self.getBrightness()
        self.status.append(status)
        self.energy.append(self.getW())

    def get_WTemp(self):
        return self.brighness / 100 * self.maxW * self.coef_WTemp

    def getW(self, ):
        return self.maxW * self.brighness

    def getBrightness(self):
        self.brighness = self.decPlace.countTokens()
        return self.brighness

    def showStatus(self):
        self.PN.showStatus()

    def getStatus(self):
        if self.isOff():
            return self.name + " Is OFF"
        return self.name + " Is ON ({})".format(self.getBrightness())

    def setBrightness(self, new):
        old = self.brighness
        if (old < new):
            self.incBright(new - old)
        else:
            self.decBright(old - new)

    def getNet(self, ):
        return self.PN

    def isOn(self, ):
        return self.onPlace.countTokens() > 0

    def isOff(self, ):
        return self.offPlace.countTokens() > 0

    def turnOn(self, ):
        self.PN.run([self.onLightTrans])

    def turnOff(self, ):
        self.PN.run([self.offLightTrans])

    def incBright(self, count=1):
        for i in range(count):
            rc = self.PN.run([self.incLightTrans])
            self.brighness = self.decPlace.countTokens()

    def decBright(self, count=1):
        for i in range(count):
            rc = self.PN.run([self.decLightTrans])
            self.brighness = self.decPlace.countTokens()


class Curtain(BaseObject):
    def __init__(self, name):
        BaseObject.__init__(self,name)
        #self.name = name
        self.openPlace = Place(name='open', tokens=[])
        self.closePlace = Place(name = 'close', tokens=[SimpleToken()])
        self.openTran = Transition(name = 'open ' + self.name,
                                    arcIn=[ArcIn(place=self.closePlace)],
                                    arcOut=[ArcOut(place=self.openPlace)])
        self.closeTran = Transition(name = 'close '+ self.name,
                                    arcIn=[ArcIn(place=self.openPlace),],
                                    arcOut=[ArcOut(place=self.closePlace)])
        self.PN = PetriNet(transitions=[self.openTran, self.closeTran], name = self.name)

    def isOpen(self):
        return self.openPlace.countTokens() > 0

    def isClose(self):
        return self.closePlace.countTokens() > 0

    def open(self):
        self.PN.run([self.openTran,])

    def close(self):
        self.PN.run([self.closeTran,])


def turnonLight(light_PN, params = None):
    l = light_PN
    l.runByName('turn_on')
    return light_PN

def turnOffLight(light_PN, params = None):
    #l = SimpleLight("L").PN
    l = light_PN
    l.runByName('turn_off')
    return light_PN

def dec50Light(light_PN, params = None):
    #PN = SimpleLight(name='').PN
    PN = light_PN
    level = PN.getPlaceByName('dec').countTokens()
    SP = int(level / 2)
    if level > SP:
        for i in range(level - SP):
            PN.runByName('decLight')
    return light_PN

def setDefaultLight(light_PN, params = None):
    PN = SimpleLight(name='').PN
    PN = light_PN
    level = PN.getPlaceByName('dec').countTokens()
    SP = 50
    PN.runByName('turn_on')
    if level > SP:
        for i in range(level - SP):
            PN.runByName('decLight')
    if level < SP:
        for i in range(SP - level):
            PN.runByName('incLight')
    PN.runByName('turn_off')
    return light_PN

class LightSystem(BaseObject):
    def __init__(self, name, Lights):
        BaseObject.__init__(self, name)
        self.Lights = Lights

        #Places
        self.startPlace = Place(name='start', tokens=[i.PN for i in self.Lights])
        self.SunsetPlace = Place(name = 'sunset', tokens=[])
        self.time22hPlace = Place(name='time22h', tokens=[])
        self.sleepPlace = Place(name = 'sleep', tokens=[])
        self.meetingPlace = Place(name = 'meeting', tokens=[])
        self.watchingPlace = Place(name = 'watching', tokens=[])

        #Transitions

        self.SunsetTran = Transition(name='Sunset',
                                 arcIn=[ArcIn(place=self.startPlace, allowType=LIGHT_TYPE, func=turnonLight, hold=-1)],
                                 arcOut=[ArcOut(place=self.SunsetPlace, allowType=LIGHT_TYPE, hold=-1)])

        self.Time22hTran = Transition(name = 'time22h',
                                  arcIn=[ArcIn(place=self.SunsetPlace, allowType=LIGHT_TYPE, func= dec50Light, hold=-1)],
                                  arcOut=[ArcOut(place=self.time22hPlace, allowType=LIGHT_TYPE, hold=-1)])

        self.SleepTran = Transition(name='sleep',
                                arcIn=[ArcIn(place=self.time22hPlace, func=turnOffLight, allowType=LIGHT_TYPE, hold=-1)],
                                arcOut=[ArcOut(place=self.sleepPlace, allowType=LIGHT_TYPE, hold=-1)])

        self.getupTran = Transition(name = 'getUp',
                                     arcIn=[ArcIn(place=self.sleepPlace, allowType=LIGHT_TYPE, hold=-1, func=setDefaultLight)],
                                     arcOut=[ArcOut(place=self.startPlace, allowType=LIGHT_TYPE, hold=-1)])

        self.PN = PetriNet([self.SleepTran, self.Time22hTran, self.SleepTran, self.getupTran])

    def sunset(self):
        return self.PN.run([self.SunsetTran]) == 1

    def night(self):
        return self.PN.run([self.Time22hTran]) == 1

    def sleep(self):
        return self.PN.run([self.SleepTran]) == 1

    def getup(self):
        return self.PN.run([self.getupTran]) == 1