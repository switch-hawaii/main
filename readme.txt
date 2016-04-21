This contains files to run SWITCH for the standard SWITCH-Hawaii scenarios.

To install this repository:

1. install python, git and a solver (glpk, cplex, gurobi). See "INSTALL PYTHON AND PYOMO" and "INSTALL A SOLVER" at https://github.com/switch-model/switch-hawaii-studies/blob/master/README.md for more information. To solve the larger models in a reasonable time, it is recommended that you obtain a copy of cplex or gurobi (free for academics).

3. execute the following commands in a terminal window (command prompt) to install this model and a matching copy of SWITCH:

cd <location to store model>
git clone --recursive https://github.com/switch-hawaii/main.git
cd main/switch
python setup.py develop
cd ..

4. Change settings in options.txt to reflect the solver you are using (e.g., cplex or glpk) and to choose the standard or tiny version of the model (tiny version is recommended for testing, standard version reproduces one of the standard switch-hawaii scenarios)

5. After this, you can solve the model by cd'ing into the 'main' directory and then running one of these commands to solve the default scenario or all scenarios:

switch solve
switch solve-scenarios

You can add --help to these commands to see more options.

6. Edit scenarios.txt, options.txt and modules.txt to configure the model as needed. You can also create new python modules in the local directory and then add their name to modules.txt. These modules should define some or all of the same callback functions as the modules inside switch/switch_mod (e.g., define_arguments(), define_components(), load_data(), post_solve()).
