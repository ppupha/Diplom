from PetriNet import  *
import const

USER_STATUS_OUTDOOR = 0
USER_STATUS_WRONG = -1
USER_STATUS_INHOME = 1
USER_STATUS_IN_KITCHEN = 2
USER_STATUS_IN_BEDROOM = 3
USER_STATUS_IN_LIVINGROOM = 4
USER_STATUS_IN_WORKROOM = 5
USER_STATUS_IN_TOILET = 6
USER_STATUS_COOKING = 7


def settingTempWhenOutDoor(PN, params = None):
    const.GLOBAL_T_SETTING = 30

def settingTempWhenInDoor(PN, perams = None):
    const.GLOBAL_T_SETTING = 25

class User(BaseObject):
    def __init__(self, name):
        BaseObject.__init__(self,name)
        self.status = []
        self.time = []

        #place
        self.unknownPlace = Place(tokens = [SimpleToken()], name =' unknown')
        self.outDoor = Place(tokens=[], name = 'outDoor')
        self.CheckPlace = Place(tokens=[], name = 'Checking')
        self.checkOKPlace = Place(tokens=[], name = 'checkOK')
        self.checkFailPlace = Place(tokens=[], name =  'CheckFail')
        self.wrongPerson = Place(tokens=[], name = 'WrongPerson')
        self.countCheckAgainPlace = Place(name='Again', tokens=[SimpleToken() for i in range(3)])

        #Place Home
        self.inHome = Place(tokens=[], name='InHome')
        self.inWorkRoomPlace = Place(tokens=[], name = 'InWorkRoom')
        self.inKitchenPlace = Place(tokens=[], name = 'InKitchen')
        self.cookingPlace = Place(name='Cooking')
        self.usingGasStorePlace = Place(name='GasStore')
        self.eatingPlace = Place(name='eating')
        self.inBedRoomPlace = Place(tokens=[], name='InBedRoom')
        self.sleepingPlace = Place(name='sleeping')
        self.inToiletPlace = Place(tokens=[], name='InToilet')
        self.inLivingRoomPlace = Place(name='InLivingRoom')
        self.meetingPlace = Place(name='meetting')
        self.watchingPlace = Place(name='watching')
        #transition
        self.gotoDoorTran = Transition(name = 'startCheck' ,
                                         arcIn=[ArcIn(place=self.unknownPlace)],
                                         arcOut=[ArcOut(place=self.outDoor)])

        self.Input = Transition(name = 'Input',
                                       arcIn=[ArcIn(place=self.outDoor)],
                                       arcOut=[ArcOut(place=self.CheckPlace)])

        self.vetifyTran = Transition(name = 'vetify',
                                     arcIn=[ArcIn(place=self.CheckPlace)],
                                     arcOut=[ArcOut(place=self.checkOKPlace)])

        self.notvetifyTran = Transition(name = 'notvetify',
                                        arcIn=[ArcIn(place=self.CheckPlace)],
                                        arcOut=[ArcOut(place=self.checkFailPlace)])
        self.repeatTran = Transition(name = 'repeat',
                                     arcIn=[ArcIn(place=self.checkFailPlace), ArcIn(self.countCheckAgainPlace)],
                                     arcOut=[ArcOut(place=self.outDoor)])
        self.wrongPersonTran = Transition(name = 'WrongPerson',
                                          arcIn=[ArcIn(place=self.checkFailPlace), ArcEmpty(place=self.countCheckAgainPlace)],
                                          arcOut=[ArcOut(place=self.wrongPerson)])

        #Transiton in Home
        self.comeInTran = Transition(name = 'comeIN',
                                     arcIn=[ArcIn(place=self.checkOKPlace,func=settingTempWhenInDoor)],
                                     arcOut=[ArcOut(place=self.inHome)],)
        self.comeOutTran = Transition(name='comeOut',
                                      arcIn=[ArcIn(place=self.inHome, func=settingTempWhenOutDoor)],
                                      arcOut=[ArcOut(place=self.checkOKPlace)])
        self.goInToiletTran = Transition(name = 'goinToilet',
                                     arcIn=[ArcIn(place=self.inHome)],
                                     arcOut=[ArcOut(place=self.inToiletPlace)])
        self.goOutToiletTran = Transition(name='goOutToilet',
                                      arcIn=[ArcIn(place=self.inToiletPlace)],
                                      arcOut=[ArcOut(place=self.inHome)])
        self.goInWorkTran = Transition(name='goInWork',
                                   arcIn=[ArcIn(place=self.inHome)],
                                   arcOut=[ArcOut(place=self.inWorkRoomPlace)])
        self.goOutWorkTran = Transition(name = 'goOUtWork',
                                    arcIn=[ArcIn(place=self.inWorkRoomPlace)],
                                    arcOut=[ArcOut(place=self.inHome)])

        self.goInBedRoomTran = Transition(name = 'goInBed',
                                      arcIn=[ArcIn(place=self.inHome)],
                                      arcOut=[ArcOut(place=self.inBedRoomPlace)])
        self.goSleepTran = Transition(name='goSleep',
                                  arcIn=[ArcIn(place=self.inBedRoomPlace)],
                                  arcOut=[ArcOut(place=self.sleepingPlace)])
        self.getUPTran = Transition(name='getUp',
                                arcIn=[ArcIn(place=self.sleepingPlace)],
                                arcOut=[ArcOut(place=self.inBedRoomPlace)])
        self.goOutBedRoomTran = Transition(name='goOutBedRoom',
                                       arcIn=[ArcIn(place=self.inBedRoomPlace)],
                                       arcOut=[ArcOut(place=self.inHome)])

        self.goInKitchenTran = Transition(name='goInKitchen',
                                      arcIn=[ArcIn(place=self.inHome)],
                                      arcOut=[ArcOut(place=self.inKitchenPlace)])
        self.startCookingTran = Transition(name='startCooking',
                                       arcIn=[ArcIn(place=self.inKitchenPlace)],
                                       arcOut=[ArcOut(place=self.cookingPlace)])
        self.turnOnGasTran = Transition(name='turnONGas',
                                    arcIn=[ArcIn(place=self.cookingPlace)],
                                    arcOut=[ArcOut(place=self.usingGasStorePlace)])
        self.turnOffGasTran = Transition(name='turnOffGas',
                                     arcIn=[ArcIn(place=self.usingGasStorePlace)],
                                     arcOut=[ArcOut(place=self.cookingPlace)])
        self.finishCookingTran = Transition(name='finishCooking',
                                        arcIn=[ArcIn(place=self.cookingPlace)],
                                        arcOut=[ArcOut(place=self.inKitchenPlace)])
        self.startEatingTran = Transition(name='startEating',
                                      arcIn=[ArcIn(place=self.inKitchenPlace)],
                                      arcOut=[ArcOut(place=self.eatingPlace)])
        self.finishEatingTran = Transition(name='finishEating',
                                       arcIn=[ArcIn(place=self.eatingPlace)],
                                       arcOut=[ArcOut(place=self.inKitchenPlace)])
        self.goOutKitchenTran = Transition(name='goOutKitchen',
                                       arcIn=[ArcIn(place=self.inKitchenPlace)],
                                       arcOut=[ArcOut(place=self.inHome)])
        self.goInLivingRoomTran = Transition(name='goInLivingRoom',
                                         arcIn=[ArcIn(place=self.inHome)],
                                         arcOut=[ArcOut(place=self.inLivingRoomPlace)])
        self.startWatchingTran = Transition(name='startWatching',
                                        arcIn=[ArcIn(place=self.inLivingRoomPlace)],
                                        arcOut=[ArcOut(place=self.watchingPlace)])
        self.finishWatchingTran = Transition(name='finishWatching',
                                         arcIn=[ArcIn(place=self.watchingPlace)],
                                         arcOut=[ArcOut(place=self.inLivingRoomPlace)])
        self.startMeetingTran = Transition(name = 'startMeeting',
                                       arcIn=[ArcIn(place=self.inLivingRoomPlace)],
                                       arcOut=[ArcOut(place=self.meetingPlace)])
        self.finishMeetingTran = Transition(name='finishMeeting',
                                        arcIn=[ArcIn(place=self.meetingPlace)],
                                        arcOut=[ArcOut(place=self.inLivingRoomPlace)])
        self.goOutLivingRoomTran = Transition(name='goOutLivingRoom',
                                          arcIn=[ArcIn(place=self.inLivingRoomPlace)],
                                          arcOut=[ArcOut(place=self.inHome)])

        self.PN = PetriNet([self.gotoDoorTran, self.Input, self.vetifyTran, self.notvetifyTran, self.repeatTran,
                            self.wrongPersonTran,
                            self.comeInTran, self.comeOutTran,
                            self.goInToiletTran, self.goOutToiletTran,
                            self.goInWorkTran, self.goOutWorkTran,
                            self.goInBedRoomTran, self.goSleepTran, self.getUPTran, self.goOutBedRoomTran,
                            self.goInLivingRoomTran, self.startWatchingTran, self.finishWatchingTran,
                            self.startMeetingTran, self.finishMeetingTran,self.goOutLivingRoomTran,
                            self.goInKitchenTran, self.startEatingTran, self.finishEatingTran,
                            self.startCookingTran, self.turnOnGasTran, self.turnOffGasTran, self.finishCookingTran,
                            self.startEatingTran, self.finishCookingTran, self.goOutKitchenTran])

    def addStatus(self):
        status = self.getPositon()
        self.status.append(status)
        self.time.append(GLOBAL_TIME)
        return

    def showStatus(self):
        self.PN.showStatus()

    def getName(self, ):
        return self.name

    def inputPass(self):
        return 'password'

    def checkPass(self, password):
        return password == 'password'

    def getPositon(self):
        allPlace = self.PN.getAllPlaces()
        for p in allPlace:
            if p.countTokens() > 0 and p.name != self.countCheckAgainPlace.name:
                return p.name
        return 'unknowPosition'

    def goInKitchen(self):
        return self.PN.run([self.goInKitchenTran])

    def startCooking(self):
        return self.PN.run([self.startCookingTran])

    def finishCooking(self):
        return self.PN.run([self.finishCookingTran])

    def startEating(self):
        return self.PN.run([self.startEatingTran])

    def finishEating(self):
        return self.PN.run([self.finishEatingTran])


    def goOutKitchen(self):
        return self.PN.run([self.goOutKitchenTran])

    def comeIN(self):
        return self.PN.run([self.comeInTran])

    def comeOut(self):
        return self.PN.run([self.comeOutTran])

    def sleep(self):
        return self.PN.run([self.goInBedRoomTran, self.goSleepTran]) == 2

    def goInBedRoom(self):
        return self.PN.run([self.goInBedRoomTran])

    def goSleep(self):
        return self.PN.run([self.goSleepTran])

    def getUp(self):
        return self.PN.run([self.getUPTran])

    def goOutBedRoom(self):
        return self.PN.run([self.goOutBedRoomTran])

    def goInToilet(self):
        return self.PN.run([self.goInToiletTran]) == 1

    def goOutToilet(self):
        return self.PN.run([self.goOutToiletTran]) == 1

    def goInWorkRoom(self):
        return self.PN.run([self.goInWorkTran])

    def goOutWorkRoom(self):
        return self.PN.run([self.goOutWorkTran])

    def goInLivingRoom(self):
        return self.PN.run([self.goInLivingRoomTran])
    def goOutLingRoom(self):
        return self.PN.run([self.goOutLivingRoomTran])





