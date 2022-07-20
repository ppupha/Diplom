point_type = {
'NONE' : 0,
'TRUE' : 1,
'FALSE' : 2,}


class SimpleToken:
    def __init__(self, type):
        self.type = type
        self.value = None

class Place:
    def __init__(self, hold, tokens = [],  name = ''):
        self.name = name
        self.tokens = tokens
        self.holds = self.typeCount()
        self.hold = hold

    def typeCount(self,):
        res = {}
        for i in self.tokens:
            if i.type in hold:
                res[str(i.type)] += 1
            else:
                res[str(i.type)] = 1
        return res
                
                
    
class ArcBase:
    def __init__(self, place, hold = 1, value = None, allowType = []):
        self.place = place
        self.hold = hold
        self.value = value
        self.allowType = allowType
    
    def isNotBlocking(self,):
        return self.place.hold >= self.hold

class ArcIn(ArcBase):
    def trigger(self, ):
        self.place.hold -= self.hold

class ArcOut(ArcBase):
    def trigger(self,):
        self.place.hold += self.hold
        
class ArcEmpty(ArcBase):
    def isNotBlocking(self,):
        return self.hold == 0

    def trigger(self,):
        pass
        
class Transition:
    def __init__(self, arcIn, arcOut, name = '', priority = 100):
        self.name = name
        self.arcIn = arcIn
        self.arcOut = arcOut
        self.priority = priority
        
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
        #print(self.isActive, T.isActive)
        if not self.isActive() or not T.isActive():
            return False
        for i in self.arcIn:
            p = i.place
            for j in T.arcIn:
                pT = j.place
                if p == pT and i.hold + j.hold > p.hold:
                    return True
        return False
                    
        
    def active(self, ):
        isActive = self.isActive()
        if (isActive):
            for i in self.arcIn:
                i.trigger()
            for i in self.arcOut:
                i.trigger()
                
        return isActive
    
    
class PetriNet:
    def __init__(self, transittions, name = ''):
        self.name = name
        self.transittions = transittions
        
    def getAllPlaces(self, ):
        place = []
        for i in self.transittions:
            for j in i.arcIn + i.arcOut:
                place.append(j.place)
        
        place = list(set(place))
        place.sort(key = lambda x: x.name)
        return place
        
    def showStatus(self, placeList = None):
        if placeList == None:
            placeList = self.getAllPlaces()
        print("\n\n")
        for i in placeList:
            print("{:^10}".format(i.name), end = '')
        print("\n")
        for i in placeList:
            print("{:^10}".format(i.hold), end = '')
        print("\n\n")
        
    def getTransitionByName(self, name):
        for i in self.transittions:
            if i.name == name:
                return i
        return None
    
    def isConflictWithAny(self, T):
        res = []
        for t in self.transittions:
            if t != T and T.isConflictWith(t):
                continue
                
    
    def autorun(self):
        print("Status at Begin\n")
        self.showStatus()
        while True:
            count_Active = 0
            for i in self.transittions:
                if i.isActive():
                    i.active()
                    count_Active += 1
                    print(" {} ia Activated\n".format(i.name))
                    self.showStatus()
                    pass
            if count_Active == 0:
                return 
        
    def run(self, sequence = None):
        if (sequence == None):
            return
        for i in sequence:
            rc = i.active()
            if (not rc):   
                print("Transition {} not active".format(i.name))
            
            print("\n\nAfter Active {}".format(i.name))
            self.showStatus(self.getAllPlaces())
     
                
                
                
                
        
    
        

P1 = Place(hold = 3, name = "P1")
P2 = Place(hold = 0, name = "P2")
P3 = Place(hold = 1, name = "P3")
P = [P1, P2, P3]

T1 = Transition(name = "T1", arcIn = [ArcIn(P1), ArcIn(P3)], arcOut = [ArcOut(P2),])
T2 = Transition(name = "T2", arcIn = [ArcIn(P2), ], arcOut = [ArcOut(P3),])

T = [T1, T2]

PN = PetriNet([T1, T2], name = "PN")


print(T1.isConflictWith(T2))

#PN.run([T1])
PN.autorun()

print("Output");
for i in P:
    print("{}   {}".format(i.name, i.hold))
    



