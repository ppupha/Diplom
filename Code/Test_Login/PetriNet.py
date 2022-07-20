from const import *

define = {}
NONE = 'Default'
TRUE = 'True'
FALSE = 'False'

DEBUG = False


TransLabels = {}

class SimpleToken:
    def __init__(self, type = NONE, value = None):
        self.type = type
        self.value = value
        
    def showStatus(self,):
        print("This is Default")

class Place:
    def __init__(self, tokens = [] ,  name = ''):
        self.name = name
        self.tokens = tokens
        self.holds = self.typeCount()
        self.hold = sum(self.holds.values())
        
    def countTokens(self,):
        return self.hold
    
    def typeCount(self,):
        res = {NONE: 0,
               LIGHT_TYPE:0}
        
        for i in self.tokens:
            if str(i.type) in res:
                res[str(i.type)] += 1
            else:
                res[str(i.type)] = 1
        return res
            
    def update(self,):
        self.holds = self.typeCount()
        self.hold = sum(self.holds.values())

    '''
    @count - number of token, need pop
    count = -1 - pop all tokens
    
    '''
    def pop(self, type = 0, count = 1):
        c = count
        tokens = []
        if (DEBUG and type == LIGHT_TYPE):
            print("POP function")
            print(self.tokens)
            print(c)
        index = 0
        #for index, value in enumerate(self.tokens):
        while (index < len(self.tokens) and (c > 0 or c == -1)):
            value = self.tokens[index]
            if (c == -1 or c > 0) and value.type == type:
                tokens.append(self.tokens[index])
                self.tokens.pop(index)
                if (c > 0):
                    c -= 1
            else:
                index += 1
        self.update()
        return tokens
        
    def append(self, list = []):
        for i in list:
            self.tokens.append(i)
            # TODO
        self.update()
        return 
                       
class ArcBase:
    def __init__(self, place : Place, hold = 1, label = None, allowType = NONE, name = '', func = None, params = None):
        self.place = place
        self.hold = hold
        if (label == None):
            self.label = NONE
        else:
            self.label = label
        self.allowType = allowType
        self.name = name
        self.func = func
        self.func_params = params
    
    def isNotBlocking(self,):
        rc = str(self.allowType) in self.place.holds and self.place.holds[str(self.allowType)] >= self.hold
        return rc

class ArcIn(ArcBase):
    def trigger(self):
        tokens = []
        self.place.holds[str(self.allowType)] -= self.hold
        if 0 and self.allowType == LIGHT_TYPE:
            print(self.hold, self.place.holds, '\n',tokens)
        tokens = self.place.pop(type = self.allowType, count = self.hold)
        if 0 and self.allowType == LIGHT_TYPE:
            print(self.hold, self.place.holds, '\n',tokens)

        if self.func:
            for t in tokens:
                self.func(t, self.func_params)
        return tokens
        
class ArcOut(ArcBase):
    def trigger(self, tokens, func = None, params = None ):
        append_tokens = []
        c = 0
        for i in tokens:
            if (c < self.hold or self.hold == -1):
                if i.type == self.allowType:
                    append_tokens.append(i)
                    c += 1
        self.place.holds[str(self.allowType)] += self.hold

        if func != None:
            func(append_tokens, params)
        self.place.append(append_tokens)
        return 
        
class ArcEmpty(ArcBase):
    def __init__(self, place, hold = 0, label = None, allowType = NONE, name = ''):
        ArcBase.__init__(self,place, hold = 0, label = None, allowType = NONE, name = '')

    def isNotBlocking(self,):
        print("From ArcEmpty")
        return self.place.countTokens() == 0

    def trigger(self,):
        return []
        
class Transition:
    def __init__(self, arcIn, arcOut, name = '', isAuto = False, label = '', priority = 100,):
        self.name = name
        self.arcIn = arcIn
        self.arcOut = arcOut
        self.priority = priority
        self.isAuto = isAuto
        if label == '':
            label = NONE
        self.label = label
        self.addtoTransLabel()
            
        
        for i in arcIn:
            i.name = "[{} -> {}]".format(i.place.name, name)
            
        for i in arcOut:
            i.name = "[{} -> {}]".format(name, i.place.name)
      
    def addtoTransLabel(self,):
        global TransLabels
        if self.getLabel() not in TransLabels:
            TransLabels[self.getLabel()] = {'main':[], '*': []}
        if self.label.startswith('*'):
            TransLabels[self.getLabel()]['*'].append(self)
        else:
            TransLabels[self.getLabel()]['main'].append(self)
            
    def removeFromTransLabel(self,):
        trans = TransLabels[self.getLabel()]
        if self in trans['main']:
            trans['main'].remove(self)
        if self in trans['*']:
            trans['*'].remove(self)
      
    def getLabel(self):
        if self.label.startswith("*"):
            return self.label
        if self.label.startswith('not'):
            return self.label[3:]
        return self.label
    def setLabel(self, newLabel):
        self.removeFromTransLabel()
        self.label = newLabel
        self.addtoTransLabel()
        
        self.label = newLabel
      
    def needFireWith(self, T):
        return self.label == "not" + T.label or "not" + self.label == T.label
        
    def needFireIf(self, T):
        return self.label == "*" + T.label
        
    def isActive(self, ):
        for i in self.arcIn:
            if not i.isNotBlocking():
                return False
             
        return True
    
    def getInPlaces(self):
        res = []
        for i in self.arcIn:
            res.append(i.place)
        return set(res)
    
    def isConflictWith(self, T):
        # TODO
        return False
        #print(self.isActive, T.isActive)
        '''
        if not self.isActive() or not T.isActive():
            return False
        for i in self.arcIn:
            p = i.place
            for j in T.arcIn:
                pT = j.place
                if p == pT and i.hold + j.hold > p.hold:
                    return True
        '''
        return False
                    
        
    def fire(self, ):
        # TODO
        #print(" {} ia Activated\n".format(self.name))
        isActive = 1#self.isActive()
        popTokens = {}
        if (isActive):
            for i in self.arcIn:
                tokens = i.trigger()
                if (i.label not in popTokens):
                    popTokens[i.label] = []
                popTokens[i.label].extend(tokens)
            #print(popTokens)
            for i in self.arcOut:
                if i.label in popTokens:
                    i.trigger(popTokens[i.label])
                
        return isActive
    
    
class PetriNet:
    def __init__(self, transitions = [], name = '', type = None):
        self.name = name
        self.transitions = transitions
        self.relNet = []
        if type == None:
            self.type = self.name
        else:
            self.type = type
        '''
        {label : [[main,], [if]]}
        '''
        self.relLabel = {}
    

    def createTrans(self, arcIn, arcOut, name = '', isAuto = False, label = None, priority = 100,):
        t = Transition(arcIn, arcOut, name, isAuto, label, priority)
        self.transitions.append(t)

    def addWithLabel(self,Tmain, TWith):
        label = Tmain.getLabel()
        if label not in self.relLabel:
            self.relLabel[label] = [[Tmain], []]
        
        self.relLabel[label][0].append(TWith)
        
    def addIfLabel(self, Tmain, Tif):
        label = Tmain.getLabel()
        if label not in self.relLabel:
            self.relLabel[label] = [[Tmain], []]
        
        self.relLabel[label][1].append(Tif)
        
    def addRelTrans(self, pn):
        for t in self.transitions:
            for tpn in pn.transitions:
                if tpn.needFireWith(t):
                    self.addWithLabel(t, tpn)
                if tpn.needFireIf(t):
                    self.addIfLabel(t, tpn)
    
    def addRelateNet(self, pn):
        self.relNet.append(pn)
        self.addRelTrans(pn)
        return
        
    def getAllPlaces(self, ):
        place = []
        for i in self.transitions:
            for j in i.arcIn + i.arcOut:
                place.append(j.place)
        
        place = list(set(place))
        place.sort(key = lambda x: x.name)
        return place
        
    def showStatus(self, placeList = None):
        if placeList == None:
            placeList = self.getAllPlaces()
        print("\n\n")
        print(self.name)
        for i in placeList:
            print("{:^10}".format(i.name), end = '')
        print("\n")
        for i in placeList:
            print("{:^10}".format(i.hold), end = '')
        print("\n\n")
        
        #for i in self.relNet:
        #    i.showStatus()
        
    def getTransitionByName(self, name):
        for i in self.transitions:
            if i.name == name:
                return i
        return None
    def getPlaceByName(self, name):
        places = self.getAllPlaces()
        for i in places:
            if i.name == name:
                return i
    
    def isConflictWithAny(self, T):
        res = []
        for t in self.transitions:
            if t != T and T.isConflictWith(t):
                continue

    def runByName(self, name):
        tran = self.getTransitionByName(name)
        #print("from Run By Name")
        #print(tran.name)
        return self.run([tran])

    def run(self, sequence = None):
        count = 0
        global TransLabels
        if (sequence == None):
            return count
        
        for i in sequence:
            if (i.label == NONE):
                relatedTrans = [i,]
            else:
                relatedTrans = TransLabels[i.getLabel()]['main']
            isActives = [t.isActive() for t in relatedTrans]

            if (False in isActives):
                continue
                print("{} cant be fired".format(i.name))
                print(i.label)
                print(isActives)
                print("\n")
                continue

            
            for t in relatedTrans:
                t.fire()
            count += 1
            #self.showStatus(self.getAllPlaces())
        return count
    
    def autorun(self):
        res = 0
        print("Status at Begin\n")
        self.showStatus()
        while True:
            print("#"*20)
            count_Active = 0
            
            for i in self.transitions:
                if i.isAuto:
                    rc = self.run([i,])
                    if (rc == 1):
                        count_Active += 1
                        res += 1
                        self.showStatus()
                        break
            if count_Active == 0:
                return

'''
class SH:
    def __init__(self,):
        self.PN = []
    
    def getPNByName(self, name):
        for i in self.PN:
            if i.name == name:
                return i
                
    def addNet(self, pn):
        self.PN.append(pn)
        
        
    def addRelated(self, PN1, PN2):
        PN1.addRelateNet(PN2)
        PN2.addRelateNet(PN1)
    
    
    def getNewLight(self,):
        P4 = Place(tokens = [SimpleToken() for _ in range(1)], name = "P4")
        P5 = Place(tokens = [], name = "P5")

        T3 = Transition(name = "T3", arcIn = [ArcIn(place = P4, ), ], 
                             arcOut = [ArcOut(place = P5),], label = "notl1")

        T4 = Transition(name = "T4", arcIn = [ArcIn(place = P5, ), ], 
                             arcOut = [ArcOut(place = P4),], label = "notl2")   

        PN2 = PetriNet([T3, T4], name = "PN2", type = NONE)
        return PN2

'''

class BaseObject:
    def __init__(self, name):
        self.name = name
        self.status = []
        self.time = []
        self.energy = []
        self.PN = None

    def showStatus(self):
        if (self.PN):
            self.PN.showStatus()

    def addStatus(self):
        pass






'''
class House:
    def __init__(self, name):
        self.name = name
        self.beforeCheck = Place(name = self.name + ' beforeCheck', tokens=[User()])
        self.afterCheck = Place(name = self.name + ' afterCheck', tokens=[])
        self.inHome = Place(name = self.name + ' inHome', tokens = [])
        self.inBedroom = Place(name = self.name + ' InBedroom', tokens=[])
        self.inKitchen = Place(name = self.name + ' InKitchen', tokens=[])
        self.inToilet = Place(name = self.name + ' InToilet', tokens=[])
        self.inWorkingroom = Place(name = self.name + 'InWorkingRoom', tokens=[])
        self.inLivingroom = Place(name = self.name + ' InLingvingroom', tokens=[])

        self.checkTran = Transition(name = 'check' + self.name,
                                    arcIn=[ArcIn(place= self.beforeCheck)],
                                    arcOut=[ArcOut(place=self.afterCheck)])

        self.uncheckTran = Transition(name = 'uncheck' + self.name,
                                      arcIn=[ArcIn(place=self.afterCheck)],
                                      arcOut=[ArcOut(place=self.beforeCheck)])

        self.comeInTran = Transition(name = 'comeIn ' + self.name,
                                 arcIn=[ArcIn(place=self.afterCheck)],
                                 arcOut=[ArcOut(place=self.inHome)])

        self.comeOutTran = Transition(name = 'comeOut ' + self.name,
                                  arcIn=[ArcIn(place=self.inHome)],
                                  arcOut=[ArcOut(place=self.afterCheck)])

        self.toKitchenTran = Transition(name = 'toKitchen ' + self.name,
                                    arcIn=[ArcIn(place=self.inHome)],
                                    arcOut=[ArcOut(place=self.inKitchen)])

        self.outKitchenTran = Transition(name = 'outKitchen' + self.name,
                                     arcIn=[ArcIn(place=self.inKitchen)],
                                     arcOut=[ArcOut(place=self.inHome)])

        self.toBedroomTran = Transition(name = 'toBedroom ' + self.name,
                                    arcIn=[ArcIn(place=self.inHome)],
                                    arcOut=[ArcOut(place=self.inBedroom)])

        self.PN = PetriNet([self.checkTran, self.uncheckTran, self.comeInTran, self.comeOutTran,
                            self.toBedroomTran, self.toKitchenTran,])
'''


