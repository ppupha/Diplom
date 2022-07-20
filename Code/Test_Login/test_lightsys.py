from LightSystem import *

def test_lightsys():
    ls = LightSystem(name='LSYS', Lights=[SimpleLight(name='L{}'.format(i)) for i in range(3)])
    print("@" * 20)
    print("Before:")
    ls.showStatus()
    for l in ls.Lights:
        print(l.getStatus())
    ls.PN.run([ls.SunsetTran])
    ls.PN.run([ls.Time22hTran])
    #ls.PN.run([ls.SleepTran])
    #ls.PN.run([ls.getupPlaceTran])

    print("*"*20)
    print("After:")
    ls.showStatus()
    for l in ls.Lights:
        print(l.getStatus())



test_lightsys()
