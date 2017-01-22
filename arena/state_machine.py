class _State:

    @staticmethod
    def CarefulExecute(func):
        if func is not None:
            return func()
        return None

    def update(self):
        return _State.CarefulExecute(self.updateCallback)

    def begin(self):
        return _State.CarefulExecute(self.beginCallback)

    def end(self):
        return _State.CarefulExecute(self.endCallback)

    def __init__(self, name, updateCallback, beginCallback, endCallback):
        self.name = name
        self.updateCallback = updateCallback
        self.beginCallback = beginCallback
        self.endCallback = endCallback
        

class StateMachine:

    def StateExists(self, stateName):
        return stateName in self.states

    def RemoveState(self, stateName):
        if self.StateExists(stateName):
            self.states.pop(stateName, None)
            return True
        return False

    def AddState(self, stateName, stateUpdateCallback=None, stateBeginCallback=None, stateEndCallback=None):
        if stateName is None:
            return False
        self.states[stateName] = _State(stateName, stateUpdateCallback, stateBeginCallback, stateEndCallback)
        return True

    def SetState(self, nextStateName):
        if self.StateExists(nextStateName):
            self.nextStateName = nextStateName
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
                self.states[self.currStateName].begin()
        
        if self.currStateName is not None:
            self.states[self.currStateName].update()

    def __init__(self):
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


        self.sm.AddState("nothing")
        print("States exist: {} {} {} = 1 1 1".format(int(self.sm.StateExists("active")), int(self.sm.StateExists("idle")), int(self.sm.StateExists("nothing"))))
        
        self.sm.RemoveState("nothing")
        print("States exist: {} {} {} = 1 1 0".format(int(self.sm.StateExists("active")), int(self.sm.StateExists("idle")), int(self.sm.StateExists("nothing"))))
        

    def Update(self):
        print("Updating State Machine... age: {}".format(self.age))
        self.sm.Update()

    def ActiveBegin(self):
        print("Begin - Active")

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
