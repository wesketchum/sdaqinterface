import subprocess
import select
import sys
import threading
from threading import Thread

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
        self.state = "Existing"
        self.status_period = 3 #in seconds
        
        #self.cmd_init = "SDAQ_Initialize.sh"
        #self.cmd_start = "SDAQ_Start.sh"
        #self.cmd_stop = "SDAQ_Stop.sh"
        #self.cmd_pause = "SDAQ_Pause.sh"
        #self.cmd_resume = "SDAQ_Resume.sh"
        #self.cmd_terminate = "SDAQ_Terminate.sh"
        #self.cmd_status = "SDAQ_Status.sh"
        self.cmd_init = "echo INIT; sleep 15"
        self.cmd_run = "echo RUN; sleep 2"
        self.cmd_stop = "echo STOP; sleep 2"
        self.cmd_pause = "echo PAUSE; sleep 2"
        self.cmd_resume = "echo RESUME; sleep 2"
        self.cmd_terminate = "echo TERMINATE"
        self.cmd_reset = "sleep 2; echo RESET"
        self.cmd_status = "echo STATUS COMPLETE"
                    
    def initialize(self):
        self.state = "Initializing"
        shell_cmd(self.cmd_init)
        self.state = "Initialized"

    def start_running(self):
        self.state = "Starting run"
        shell_cmd(self.cmd_run)
        self.state = "Running"

    def stop_running(self):
        self.state = "Stopping"
        shell_cmd(self.cmd_stop)
        self.state = "Stopped"

    def pause_running(self):
        self.state = "Pausing"
        shell_cmd(self.cmd_pause)
        self.state = "Paused"

    def resume_running(self):
        self.state = "Resuming"
        shell_cmd(self.cmd_resume)
        self.state = "Running"

    def terminate(self):
        self.state = "Terminating"
        shell_cmd(self.cmd_terminate)

    def reset(self):
        self.state = "Resetting"
        shell_cmd(self.cmd_reset)
        self.state = "Existing"

    def get_status(self):
        print "Current SDAQInterface state is %s. %d TransitionWorker(s) running." % (self.state, threading.active_count()-1)
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
            self.terminate()
            return 1

        #if(self.user_input == 'reset'):
         #   self.terminate()
          #  return 1

        if(threading.active_count()>1):
            print "\n\nCANNOT ISSUE COMMAND! Ongoing transition process!"
            #print "Issue 'reset' to return to ground state if processes unresponsive."
            print "Issue 'terminate' to exit out.\n\n"
            return 0
        
        if(self.user_input == 'init'):
            worker = TransitionWorker(self.initialize)
            worker.start()
            return 0
        elif(self.user_input == 'run'):
            worker = TransitionWorker(self.start_running)
            worker.start()
            return 0
        elif(self.user_input == 'stop'):
            worker = TransitionWorker(self.stop_running)
            worker.start()
            return 0
        elif(self.user_input == 'pause'):
            worker = TransitionWorker(self.pause_running)
            worker.start()
            return 0
        elif(self.user_input == 'resume'):
            worker = TransitionWorker(self.resume_running)
            worker.start()
            return 0
        else:
            print "Unknown command %s." % self.user_input

    def run(self):
        while True:
            if(self.process_input()==1):
                break
