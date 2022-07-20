

from  PetriNet import *
from  SecuritySystem import *
from User import *

door = Door(name='D')
user = User(name='U')
speaker = Speaker(name='S')
speaker.showStatus()
door.showStatus()
user.showStatus()

#syns

user.vetifyTran.setLabel('userVetified')
door.unlockTran.setLabel('notuserVetified')

user.comeInTran.setLabel('userComeIn')
door.openTran.setLabel('notuserComeIn')

user.wrongPersonTran.setLabel('wrongPersion')
speaker.turnOn.setLabel('notwrongPersion')


#action
user.PN.run([user.gotoDoorTran])
user.PN.run([user.Input])
if 0:
    user.PN.run([user.notvetifyTran])
    user.PN.run([user.repeatTran])
    user.PN.run([user.Input])
    user.PN.run([user.notvetifyTran])
    user.PN.run([user.repeatTran])
    user.PN.run([user.Input])
    user.PN.run([user.notvetifyTran])

    user.PN.run([user.repeatTran])
    user.PN.run([user.Input])
    user.PN.run([user.notvetifyTran])

    user.PN.run([user.wrongPersonTran])
else:
    user.PN.run([user.vetifyTran])
    user.PN.run([user.comeInTran])
    door.PN.run([door.closeTran])



#status
speaker.showStatus()
door.showStatus()
user.showStatus()

