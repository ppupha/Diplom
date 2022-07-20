from PetriNet import  *
from User import *


class Door:
    def __init__(self,name):
        self.name = name
        self.status = []
        self.time = []

        #place
        self.lockedPlace = Place(name = self.name + ' locked', tokens=[SimpleToken()])
        self.unlockedPlace = Place(name = self.name + ' unlocked', tokens=[])
        self.openPlace = Place(name = self.name + ' open', tokens=[])
        self.closePlace = Place(name = self.name + ' close', tokens = [SimpleToken()])

        self.lockTran = Transition(name = 'lock ' + self.name,
                                   arcIn=[ArcIn(place=self.unlockedPlace,),
                                          ArcIn(place=self.closePlace,)],
                                   arcOut=[ArcOut(place=self.closePlace),
                                           ArcOut(place=self.lockedPlace)])

        self.unlockTran = Transition(name = 'unlock '+ self.name,
                                     arcIn=[ArcIn(place=self.lockedPlace)],
                                     arcOut=[ArcOut(place=self.unlockedPlace)])

        self.openTran = Transition(name = 'open ' + self.name,
                                   arcIn=[ArcIn(place=self.unlockedPlace),
                                          ArcIn(place=self.closePlace)],
                                   arcOut=[ArcOut(place=self.openPlace),
                                           ArcOut(place=self.unlockedPlace)])

        self.closeTran = Transition(name = 'close' + self.name,
                                    arcIn=[ArcIn(place=self.openPlace)],
                                    arcOut=[ArcOut(place=self.closePlace),])
        self.PN = PetriNet(transitions=[self.closeTran, self.openTran, self.lockTran, self.unlockTran], name = self.name)


    def addStatus(self):
        pass
        status  = 1 #locked
        if not self.isLocked():
            if self.isOpen():
                status = 3
            if self.isCLoce():
                status = 2
        self.status.append(status)
        self.time.append(GLOBAL_TIME)

    def isOpen(self):
        rc = self.openPlace.countTokens() > 0
        return rc

    def isCLoce(self):
        rc = self.closePlace.countTokens() > 0
        return rc

    def isLocked(self):
        rc = self.lockedPlace.countTokens() > 0
        return rc

    def inUnlock(self):
        rc = self.unlockedPlace.countTokens() > 0
        return rc

    def lock(self):
        self.PN.run([self.lockTran])

    def unlock(self):
        self.PN.run([self.unlockTran])

    def open(self):
        self.PN.run([self.openTran])

    def close(self):
        self.PN.run([self.closeTran])

    def showStatus(self):
        self.PN.showStatus()


class Auten(BaseObject):
    def __init__(self, name):
        BaseObject.__init__(self, name)

        #Place
        self.startPlace = Place(name = 'Start', tokens=[SimpleToken()])
        self.checkPassPlace = Place(name = 'Checking', tokens=[])
        self.checkOKPlace = Place(name = 'OK', tokens=[])
        self.checkPassFalsePlace = Place(name = 'Fail', tokens=[])
        self.countCheckAgainPlace = Place(name='Again', tokens=[SimpleToken() for i in range(3)])
        self.wrongPersion = Place(name = 'WrongPer', tokens=[])

        #Transitions
        self.inputTran = Transition(name = 'input' + self.name,
                                    arcIn=[ArcIn(place=self.startPlace)],
                                    arcOut=[ArcOut(place=self.checkPassPlace)],)

        self.checkOKTran = Transition(name = 'checkOK',
                                      arcIn=[ArcIn(place=self.checkPassPlace)],
                                      arcOut=[ArcOut(place=self.checkOKPlace)])

        self.checkFailTran = Transition(name = 'checkFail',
                                        arcIn=[ArcIn(place=self.checkPassPlace)],
                                        arcOut= [ArcOut(place=self.checkPassFalsePlace)])

        self.repeatTran = Transition(name='repeat',
                                     arcIn=[ArcIn(place=self.checkPassFalsePlace), ArcIn(place=self.countCheckAgainPlace)],
                                     arcOut=[ArcOut(place=self.startPlace)])

        self.wrongPerTran = Transition(name='WrongPersion',
                                       arcIn=[ArcIn(place=self.checkPassFalsePlace), ArcEmpty(place=self.countCheckAgainPlace)],
                                       arcOut=[ArcOut(place=self.wrongPersion)])

        self.PN = PetriNet(name= self.name, transitions=[self.inputTran, self.repeatTran, self.checkOKTran,
                                                         self.checkFailTran, self.repeatTran, self.wrongPerTran])


class Speaker(BaseObject):
    def __init__(self, name):
        BaseObject.__init__(self, name)
        self.onPlace = Place(name='on')
        self.offPlace = Place(name='off', tokens=[SimpleToken()])
        self.turnOn = Transition(name='turnOn',
                                 arcIn=[ArcIn(place=self.offPlace)],
                                 arcOut=[ArcOut(place=self.onPlace)])
        self.turnOff = Transition(name='turnOff',
                                  arcIn=[ArcIn(place=self.onPlace)],
                                  arcOut=[ArcOut(place=self.offPlace)])
        self.PN = PetriNet([self.turnOn, self.turnOff])