from  PetriNet import *

class GasStore(BaseObject):
    def __init__(self, name):
        BaseObject.__init__(self, name)
        self.onPlace = Place(name = 'on')
        self.offPlace = Place(name = 'off', tokens=[SimpleToken()])
        self.turnOn = Transition(name='turnOn',
                                 arcIn=[ArcIn(place=self.offPlace)],
                                 arcOut=[ArcOut(place=self.onPlace)])
        self.turnOff = Transition(name='turnOff',
                                  arcIn=[ArcIn(place=self.onPlace)],
                                  arcOut=[ArcOut(place=self.offPlace)])
        self.PN = PetriNet([self.turnOn, self.turnOff])

class AirPurifier(BaseObject):
    def __init__(self, name):
        BaseObject.__init__(self, name)
        self.onPlace = Place(name = 'on')
        self.offPlace = Place(name = 'off', tokens=[SimpleToken()])
        self.turnOn = Transition(name='turnOn',
                                 arcIn=[ArcIn(place=self.offPlace)],
                                 arcOut=[ArcOut(place=self.onPlace)])
        self.turnOff = Transition(name='turnOff',
                                  arcIn=[ArcIn(place=self.onPlace)],
                                  arcOut=[ArcOut(place=self.offPlace)])
        self.PN = PetriNet([self.turnOn, self.turnOff])