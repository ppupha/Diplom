from PetriNet import *
import matplotlib.pyplot as plt
from weather import *

def testUser():
    user = User('ABC')
    user.showStatus()


def testDoor():
    d = Door('D')
    d.showStatus()
    d.unlock()
    d.open()
    d.close()
    d.showStatus()

def testCurtain():
    c = Curtain(name= ' C')
    c.open()
    c.showStatus()

def testAuten():
    a = Auten(name='Test')
    a.showStatus()
    a.PN.run([a.inputTran, a.checkFailTran])
    a.PN.run([a.repeatTran])
    a.PN.run([a.inputTran, a.checkFailTran])
    a.PN.run([a.repeatTran])
    a.PN.run([a.inputTran, a.checkFailTran])
    print(a.PN.run([a.repeatTran]))
    a.PN.run([a.inputTran, a.checkFailTran])
    print(a.PN.run([a.wrongPerTran]))

    a.showStatus()

def testGasStore():
    gs = GasStore(name='GS')
    gs.showStatus()
    gs.PN.run([gs.turnOn, gs.turnOff, gs.turnOn])
    gs.showStatus()

#testDoor()
#testCurtain()
#testAuten()
#testGasStore()
testUser()



