from PetriNet import *

class Conđition(BaseObject):
    def __init__(self, name):
        BaseObject.__init__(self, name)
        self.maxW = 1500
        self.level = 50
        self.onPlace = Place(tokens=[], name=self.name + 'on')
        self.offPlace = Place(tokens=[SimpleToken()], name=self.name + 'off')
        self.stdbyPlace = Place(tokens=[], name = self.name + ' stdby')
        self.incPlace = Place(tokens=[SimpleToken() for i in range(100 - self.level)], name=self.name + "inc")
        self.decPlace = Place(tokens=[SimpleToken() for i in range(self.level)], name=self.name + "dec")

        self.onTrans = Transition(name="turn_on" + self.name,
                                  arcIn=[ArcIn(place=self.offPlace, ), ],
                                  arcOut=[ArcOut(place=self.onPlace), ], label="")
        self.offTrans = Transition(name="turn_off" + self.name,
                                   arcIn=[ArcIn(place=self.onPlace, ), ],
                                   arcOut=[ArcOut(place=self.offPlace), ], label="")

        self.stdbyToOffTran = Transition(name = 'stdby to Off '+self.name,
                                         arcIn=[ArcIn(place=self.stdbyPlace)],
                                         arcOut=[ArcOut(place=self.offPlace)])

        self.stdbyToOnTran = Transition(name = 'Stdby to On' + self.name,
                                        arcIn=[ArcIn(place=self.stdbyPlace)],
                                        arcOut=[ArcOut(place=self.onPlace)])

        self.onToStdbyTran = Transition(name = 'On to Stdby '+ self.name,
                                        arcIn=[ArcIn(place=self.onPlace)],
                                        arcOut=[ArcOut(place=self.stdbyPlace)])

        self.decTrans = Transition(name="decLight" + self.name,
                                        arcIn=[ArcIn(place=self.decPlace, ),
                                               ArcIn(place=self.onPlace)],
                                        arcOut=[ArcOut(place=self.onPlace, ),
                                                ArcOut(place=self.incPlace)])
        self.incTrans = Transition(name='incLight' + self.name,
                                        arcIn=[ArcIn(place=self.incPlace, ),
                                               ArcIn(place=self.onPlace)],
                                        arcOut=[ArcOut(place=self.decPlace),
                                                ArcOut(place=self.onPlace)])
        self.PN = PetriNet([self.onTrans, self.offTrans, self.incTrans, self.decTrans,
                            self.onToStdbyTran, self.stdbyToOnTran, self.stdbyToOffTran])


    def cube_func(self, x):
        return x ** 1.5

    def calc_W(self):
        if self.isOn():
            return self.maxW * self.cube_func(self.level / 100)
        return 0

    def calc_W_Temp(self, deltaTime):
        #time in second
        self.W_Temp = 745.6 #W
        rc =  self.level / 100 * (self.W_Temp * 100) * deltaTime
        return rc

    def getLevel(self):
        return self.level

    def addStatus(self):
        status = -1
        if self.isOn():
            status = self.getLevel()
        self.status.append(status)
        self.energy.append(self.calc_W())

    def turnOn(self):
        return self.PN.run([self.onTrans])

    def turnOff(self):
        return self.PN.run([self.offTrans])

    def incLevel(self, count = 1):
        for i in range(count):
            rc = self.PN.run([self.incTrans])
        self.level = self.decPlace.countTokens()


    def decLevel(self, count = 1):
        for i in range(count):
            rc = self.PN.run([self.decTrans])
        self.level = self.decPlace.countTokens()

    def setLevel(self, newLevel = 50):
        old = self.level
        if (old < newLevel):
            self.incLevel(newLevel - old)
        else:
            self.decLevel(old - newLevel)
    def isOn(self):
        return self.onPlace.countTokens() > 0

    def isOff(self):
        return self.offPlace.countTokens() > 0

    def isStandby(self):
        return self.stdbyPlace.countTokens() > 0
