This contains files to run SWITCH for the standard SWITCH-Hawaii scenarios.

To install this repository:

1. install python, git and a solver (glpk, cplex, gurobi). See "INSTALL PYTHON AND PYOMO" and "INSTALL A SOLVER" at https://github.com/switch-model/switch-hawaii-studies/blob/master/README.md for more information. To solve the larger models in a reasonable time, it is recommended that you obtain a copy of cplex or gurobi (free for academics).

2. execute the following commands in a terminal window (command prompt) to install this model and a matching copy of SWITCH:

cd <location to store model>
git clone --recursive https://github.com/switch-hawaii/main.git
cd main
cd switch
python setup.py develop
cd ..

3. Edit options.txt to configure the model for your first run. The following should normally be changed before you get started:
-  Change the --solver flag and solver-related options to match the solver you are using (e.g., cplex or glpk); see notes in options.txt for advice on this.
- Change the --inputs-dir flag to choose the appropriate inputs directory; "inputs_tiny" is a small version recommended for testing, "inputs" is used for the standard switch-hawaii scenarios.

4. After this, you can solve the model by cd'ing into the 'main' directory and then running one of these commands:

switch solve
switch solve-scenarios

You can add --help to these commands to see more options.

The "switch solve" command solves the default scenario, as defined by settings in options.txt, plus any additional settings you specify on the command line. Normally this will load the modules specified in modules.txt, but you can override that by specifying a --module-list flag in options.txt or on the command line. 

The "switch solve-scenarios" command solves all scenarios listed in scenarios.txt. This uses settings specified in options.txt, plus options specified in the --scenario-list file (usually scenarios.txt), plus settings specified on the command line. Settings specified on the command line take precedence over those specified in the scenarios file, and both of those take precedence over options.txt.

After the model runs, results will be written in text files (with extension .tsv) in the "outputs" directory.

5. To reconfigure the model, you can edit options.txt, modules.txt and scenarios.txt. If you want to add new constraints or technologies to the model, you should create new python modules in the local directory and then add their names to modules.txt. These modules should define some or all of the same callback functions as the modules inside switch/switch_mod (e.g., define_arguments(), define_components(), load_data(), post_solve()).

