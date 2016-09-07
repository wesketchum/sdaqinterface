# sdaqinterface

This is a very simple, basic, DAQ interface intended for artdaq processes. It's based in python.
At time of initial commit (Sep 7, 2016), there are three python modules to care about:

** daqstate: This contains a simple FSM handler for the DAQ states.
   A list of ValidStates (dictionary with state name key and list of allowed transition commands as value) and
   a list of ValidTransitions (dictionary with transition command name as key and value with 'transitioning' state and 'target' state)
   are declared at the get go. StartTransition is used to call a command, where there is some handling of preventing commands from
   piling up. FinalizeTransition must be called externally at the conclusion of transition.
   
** sdaqinterface: This is the real thing interacting with the user and pushing things through the state.
  When "run()" is called, transition commands are requested from command line (with status periodically printed). Available transition
  commands are 'init', 'boot', 'shutdown', 'config', 'run', 'pause', 'resume', 'stop', 'status', and 'terminate'. 'terminate' is special 
  in that it does not respect/wait for current state transitions to finish: it's mean to be an emergency release to kill the daq. All
  others have rudimentary waiting. (Well, except 'status', which just prints status again.)
  
  Each transition has a command in which subprocess POpen commands to call shell scripts are invoked. The 
  shell scripts are declared in sdaqinterface initialization, and are all located in the current directory. sdaqinterface is simply an
  interface for calling those scripts, which should be more portable. 'config' offers an example where a series of scripts could be 
  specified. In general, scripts should aim to accomplish a very specific purpose that cannot be logically broken up, allowing any 
  interface to use the same scripts (or, if needed, not use a script if it's not needed in that interface). There is no guarantee that 
  the set of scripts defined is what we want. Also, those scripts right now only issue an echo command and a sleep. There is also 
  no current input args for those scripts, and that will need to be defined.
  
** rundaq: This just runs it all. From terminal, simply do 'python rundaq.py' to run.

