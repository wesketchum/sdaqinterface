class DAQState():
    #Valid state key is the state. Value is allowed transitions
    ValidStates = { "Existing":["Initialize","Terminate"],
                    "Initialized":["Initialize","Boot","Terminate"],
                    "Booted":["Shutdown","Configure","Terminate"],
                    "Configured":["Shutdown","Configure","Run","Terminate"],
                    "Running":["Stop","Pause","Terminate"],
                    "Paused":["Stop","Resume","Terminate"],
                    "Stopped":["Run","Configure","Shutdown","Terminate"],
                    "Initializing":["Terminate"],
                    "Booting":["Terminate"],
                    "ShuttingDown":["Terminate"],
                    "Configuring":["Terminate"],
                    "Starting":["Terminate"],
                    "Pausing":["Terminate"],
                    "Resuming":["Terminate"],
                    "Stopping":["Terminate"],
                    "Terminated":[] }
    #Valid transition key is transition name. Value is transitionining state, then end state
    ValidTransitions = { "Initialize":["Initializing","Initialized"],
                         "Boot":["Booting","Booted"],
                         "Shutdown":["ShuttingDown","Initialized"],
                         "Configure":["Configuring","Configured"],
                         "Run":["Starting","Running"],
                         "Pause":["Pausing","Paused"],
                         "Resume":["Resuming","Running"],
                         "Stop":["Stopping","Stopped"],
                         "Terminate":["Terminating","Terminated"] }    
    """
    DAQState: A simple class for controlling state machine.
    We should really implement a full FSM, but this is a rough start.
    
    """

    def __init__(self):
        self.state = "Existing"
        self.target = "None"

    def State(self):
        return self.state

    def StartTransition(self,transition):
        my_transition = self.ValidTransitions.get(transition,"Invalid")
        if(my_transition=='Invalid'):
            print "INVALID TRANSITION COMMAND: %s" % transition
            return False
        if(self.target != 'None' and transition!='Terminate'):
            print "INVALID TRANSITION: Currently in transition state %s." % self.state
            return False
        if(transition in self.ValidStates.get(self.state)):
            self.state = my_transition[0]
            self.target = my_transition[1]
            return True
        else:
            print "INVALID TRANSITION: Cannot issue %s while in %s state." % (transition,self.state)
            return False

    def FinalizeTransition(self):
        self.state = self.target
        self.target = "None"
        return True
