import subprocess
import select
import sys
import threading
from threading import Thread
from daqstate import DAQState

class TransitionWorker(Thread):
    def __init__(self,function):
        Thread.__init__(self)
        self.function = function
    def run(self):
        self.function()
        
def shell_cmd(cmd):
    stat = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).stdout.read()
    print stat        
                
class SDAQInterface():
    """
    SDAQInterface: A simple control process.
    
    """
    def __init__(self):
        self.daqstate = DAQState()
        self.status_period = 3 #in seconds
        
        self.cmd_init = "./SDAQ_Initialize.sh"
        self.cmd_terminate = "./SDAQ_Terminate.sh"

        self.cmd_boot = "./SDAQ_Boot.sh"
        self.cmd_shutdown = "./SDAQ_Shutdown.sh"

        self.cmd_getconfig = "./SDAQ_GetConfigs.sh"
        self.cmd_configp = "./SDAQ_ConfigProcesses.sh"
        self.cmd_configh = "./SDAQ_ConfigHardware.sh"

        self.cmd_startrun = "./SDAQ_StartRun.sh"
        self.cmd_stoprun = "./SDAQ_StopRun.sh"
        self.cmd_pauserun = "./SDAQ_PauseRun.sh"
        self.cmd_resumerun = "./SDAQ_ResumeRun.sh"

        self.cmd_status = "./SDAQ_Status.sh"
                    
    def initialize(self):
        shell_cmd(self.cmd_init)
        self.daqstate.FinalizeTransition()

    def boot(self):
        shell_cmd(self.cmd_boot)
        self.daqstate.FinalizeTransition()

    def shutdown(self):
        shell_cmd(self.cmd_shutdown)
        self.daqstate.FinalizeTransition()

    def config(self):
        shell_cmd(self.cmd_getconfig)
        shell_cmd(self.cmd_configp)
        shell_cmd(self.cmd_configh)
        self.daqstate.FinalizeTransition()

    def start_running(self):
        shell_cmd(self.cmd_startrun)
        self.daqstate.FinalizeTransition()

    def stop_running(self):
        shell_cmd(self.cmd_stoprun)
        self.daqstate.FinalizeTransition()

    def pause_running(self):
        shell_cmd(self.cmd_pauserun)
        self.daqstate.FinalizeTransition()

    def resume_running(self):
        shell_cmd(self.cmd_resumerun)
        self.daqstate.FinalizeTransition()

    def terminate(self):
        shell_cmd(self.cmd_terminate)
        self.daqstate.FinalizeTransition()

    def reset(self):
        shell_cmd(self.cmd_reset)
        self.daqstate.FinalizeTransition()

    def get_status(self):
        current_state = self.daqstate.State()
        print "Current SDAQInterface state is %s. %d TransitionWorker(s) running." % (current_state, threading.active_count()-1)
        shell_cmd(self.cmd_status)
    
    def process_input(self):
        while True:
            self.get_status()
            try:
                if select.select( [sys.stdin], [], [], self.status_period) == ([sys.stdin], [], []):
                    self.user_input = sys.stdin.readline().rstrip('\r\n')
                    break
            except:
                pass
        print "Received message %s from user." % self.user_input
        return self.issue_command()
        
    def issue_command(self):
        if(self.user_input == 'terminate'):
            if(self.daqstate.StartTransition("Terminate")):                
                self.terminate()
                return 1
            return 0

        if(self.user_input == 'status'):
            self.get_status()
            return 0

        #if(self.user_input == 'reset'):
         #   self.terminate()
          #  return 1

        if(threading.active_count()>1):
            print "\n\nCANNOT ISSUE COMMAND! Ongoing transition process!"
            #print "Issue 'reset' to return to ground state if processes unresponsive."
            print "Issue 'terminate' to exit out.\n\n"
            return 0
        
        if(self.user_input == 'init'):
            if(self.daqstate.StartTransition("Initialize")):                
                worker = TransitionWorker(self.initialize)
                worker.start()
            return 0
        elif(self.user_input == 'boot'):
            if(self.daqstate.StartTransition("Boot")):                
                worker = TransitionWorker(self.boot)
                worker.start()
            return 0
        elif(self.user_input == 'shutdown'):
            if(self.daqstate.StartTransition("Shutdown")):                
                worker = TransitionWorker(self.shutdown)
                worker.start()
            return 0
        elif(self.user_input == 'config'):
            if(self.daqstate.StartTransition("Configure")):                
                worker = TransitionWorker(self.config)
                worker.start()
            return 0
        elif(self.user_input == 'run'):
            if(self.daqstate.StartTransition("Run")):                
                worker = TransitionWorker(self.start_running)
                worker.start()
            return 0
        elif(self.user_input == 'stop'):
            if(self.daqstate.StartTransition("Stop")):                
                worker = TransitionWorker(self.stop_running)
                worker.start()
            return 0        
        elif(self.user_input == 'pause'):
            if(self.daqstate.StartTransition("Pause")):                
                worker = TransitionWorker(self.pause_running)
                worker.start()
            return 0
        elif(self.user_input == 'resume'):
            if(self.daqstate.StartTransition("Resume")):                
                worker = TransitionWorker(self.resume_running)
                worker.start()
            return 0
        else:
            print "Unknown command %s." % self.user_input

    def run(self):
        while True:
            if(self.process_input()==1):
                break
