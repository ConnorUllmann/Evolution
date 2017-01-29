class _State:

    @staticmethod
    def CarefulExecute(func, *args):
        if func is not None:
            return func(*args)
        return None

    def update(self):
        return _State.CarefulExecute(self.updateCallback)

    def begin(self, *args):
        return _State.CarefulExecute(self.beginCallback, *args)

    def end(self):
        return _State.CarefulExecute(self.endCallback)

    def __init__(self, ID, name, updateCallback, beginCallback, endCallback):
        self.id = ID
        self.name = name
        self.updateCallback = updateCallback
        self.beginCallback = beginCallback
        self.endCallback = endCallback
        

class StateMachine:

    def StateExists(self, stateName):
        return stateName in self.states

    def RemoveState(self, stateName):
        if self.StateExists(stateName):
            _id = self.states.pop(stateName, None).id
            self.statesById.pop(_id, None)
            return True
        return False

    def AddState(self, stateName, stateUpdateCallback=None, stateBeginCallback=None, stateEndCallback=None):
        if stateName is None:
            return False
        stateId = self._GetNewId()
        self.states[stateName] = self.statesById[stateId] = _State(stateId, stateName, stateUpdateCallback, stateBeginCallback, stateEndCallback)
        return True

    def SetState(self, nextStateName, *args):
        if self.StateExists(nextStateName):
            self.nextStateName = nextStateName
            self.nextStateBeginArgs = args
            #print("next state: {} begin({})".format(self.nextStateName, self.nextStateBeginArgs))
            return True
        return False

    def Update(self):
        if self.nextStateName is not None and self.nextStateName != self.currStateName:
            self.lastStateName = self.currStateName
            self.currStateName = self.nextStateName
            self.nextStateName = None
            if self.lastStateName is not None:
                self.states[self.lastStateName].end()
            if self.currStateName is not None:
                #print("next state begin args:")
                #print(*self.nextStateBeginArgs)
                self.states[self.currStateName].begin(*self.nextStateBeginArgs)
        
        if self.currStateName is not None:
            self.states[self.currStateName].update()

    def _GetNewId(self):
        _id = self.id
        self.id += 1
        return _id

    def StateNameToStateId(self, stateName):
        return self.states[stateName].id if self.StateExists(stateName) else None

    def StateIdToStateName(self, stateId):
        return self.statesById[stateId].name if stateId in self.statesById else None

    def __init__(self):
        self.id = 0
        self.statesById = {}
        self.states = {}
        self.lastStateName = None
        self.currStateName = None
        self.nextStateName = None

    @property
    def state(self):
        return self.currStateName

# -------------------- STATE MACHINE TESTING -------------------- 

class _StateMachineTestObject:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.age = 0
        self.sm = StateMachine()
        self.sm.AddState("active", self.ActiveUpdate, self.ActiveBegin, self.ActiveEnd)
        self.sm.AddState("idle", self.IdleUpdate, self.IdleBegin, self.IdleEnd)
        self.sm.SetState("idle")

        print(", ".join(k for k in self.sm.states))
        input(", ".join(str(k) for k in self.sm.statesById))

        self.sm.AddState("nothing")

        print(", ".join(k for k in self.sm.states))
        input(", ".join(str(k) for k in self.sm.statesById))
        
        self.sm.RemoveState("nothing")

        print(", ".join(k for k in self.sm.states))
        input(", ".join(str(k) for k in self.sm.statesById))
        
        self.sm.AddState("new")

        print(", ".join(k for k in self.sm.states))
        input(", ".join(str(k) for k in self.sm.statesById))
        
        self.sm.RemoveState("active")
        self.sm.RemoveState("nothing")

        print(", ".join(k for k in self.sm.states))
        input(", ".join(str(k) for k in self.sm.statesById))
        

    def Update(self):
        print("Updating State Machine... age: {}".format(self.age))
        self.sm.Update()

    def ActiveBegin(self, phrase=""):
        print("Begin - Active + Phrase: {}".format(phrase))

    def ActiveEnd(self):
        print("End - Active")

    def ActiveUpdate(self):
        print("Update - Active")
        self.x += 1
        self.y -= 1
        self.age += 1
        if self.age % 5 == 0:
            print("State Change Successful: {}".format(self.sm.SetState("idle")))

        if self.age % 20 == 0:
            print("Not changing state")
            self.sm.SetState("active")

    def IdleBegin(self):
        print("Begin - Idle")
        
    def IdleEnd(self):
        print("End - Idle")
        
    def IdleUpdate(self):
        print("Update - Idle")
        self.age += 1
        if self.age % 5 == 0:
            print("State Change Successful: {}".format(self.sm.SetState("active")))

        if self.age % 20 == 0:
            print("Not changing state")
            self.sm.SetState("idle")

def _StartTest():
    smto = _StateMachineTestObject()
    while True:
        smto.Update()

if __name__ == "__main__":
    _StartTest()
