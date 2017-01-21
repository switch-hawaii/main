INTRODUCTION

This repository contains files to run SWITCH for the standard SWITCH-Hawaii scenarios.

To solve this model, you will need to install several things: 

- Python (to run all the code)
- a numerical solver, to do the computations needed to solve the model
- git software, to download SWITCH code and model data from github.com
- the data files in this repository
- Python code for SWITCH and Pyomo (used by SWITCH)

These instructions take you through these steps and then show you how to configure and run the model. If you follow the instructions below, the only freestanding binary applications you will need to install are the Anaconda Python distribution (version 2.7) and the cplex or gurobi solver (if you want to solve models other than the "tiny" test version). All the other components will be installed as plugins to Anaconda.

INSTALL PYTHON

We recommend that you use the Anaconda Python distribution. This provides an easy way to install many of the resources that SWITCH needs, and it avoids interfering with your system's built-in Python installation (if present). The instructions below assume you wiil use the Anaconda distribution. If you prefer to use a different distribution, you will need to adjust the instructions accordingly (a few hints are given).

Download and install the Anaconda Python distribution from https://www.continuum.io/downloads. Make sure to select the option to install Python 2.7. (SWITCH is not yet compatible with Python 3.x.) To save some space, you can install Miniconda from http://conda.pydata.org/miniconda.html, and the required components will be installed as needed.

Note that the Anaconda distribution can be installed without administrator rights.

INSTALL A SOLVER

For testing purposes, you can use the open-source glpk solver. This can be installed as follows:

- Open Terminal.app (OS X) or an Anaconda command prompt (Start -> Anaconda -> Anaconda Prompt)
- Type this command and then press Enter or return:

conda install -c conda-forge glpk

Follow the prompts to install glpk.

If you want to solve larger models, you will need to install the cplex or gurobi solvers, which are an order of magnitude faster than glpk. Both of these have free trials available, and are free long-term for academics. You can install one of these now or later. More information on these solvers can be found at the following links:

- cplex: https://www.ibm.com/developerworks/community/blogs/jfp/entry/free_cplex_trials?lang=en
- gurobi: http://www.gurobi.com/downloads/download-center

INSTALL GIT SOFTWARE

Open a Terminal window or Anaconda command prompt, as discussed in the previous section, then run this command and follow the prompts:

conda install git

INSTALL SWITCH-HAWAII DATA AND SWITCH MODEL CODE

Open a Terminal window or Anaconda command prompt. Then use the 'cd' and 'mkdir' commands to create and/or enter the  directory where you would like to store the SWITCH-Hawaii model data. Once you are in that directory, run the following commands (don't type the comments that start with '#'):

# download the SWITCH-Hawaii model and a matching version of the SWITCH model code
git clone --recursive https://github.com/switch-hawaii/main.git

# install the SWITCH model code and required Python packages
cd main
cd switch
python setup.py develop
cd ..
(this will leave you in the "main" directory, which is where you should be to run the model)

SETUP THE MODEL FOR YOUR FIRST RUN

You may need to edit main/options.txt to configure the model for your first run. The following should normally be changed before you get started:

-  Change the --solver flag and solver-related options to match the solver you are using (e.g., cplex or glpk); see notes in options.txt for advice on this.
- Change the --inputs-dir flag to choose the appropriate inputs directory; "inputs_tiny" is a small version recommended for testing; "inputs" is a medium size model which will usually solve within an hour; "inputs_12x24" is a larger model (12 days per period and 24 hours per day), which usually takes too long to solve when using the unit commitment and reserves modules.

RUN THE MODEL

You can solve the model at any time by launching a Terminal window or Anaconda prompt, cd'ing into the 'main' directory and then running one of these commands:

switch solve
switch solve-scenarios

You can add --help to these commands to see more options.

The "switch solve" command solves the default scenario, as defined by settings in options.txt, plus any additional settings you specify on the command line. Normally this will load the modules specified in modules.txt, but you can override that by specifying a different file via a --module-list flag in options.txt or on the command line. 

The "switch solve-scenarios" command solves all scenarios listed in scenarios.txt. This uses settings specified in options.txt, plus options specified scenarios.txt, plus settings specified on the command line. Settings specified on the command line take precedence over those specified in the scenarios file, and both of those take precedence over options.txt. If your scenario definitions are stored in a different file (e.g., scenarios_ev.txt), you can specify that via the --scenario-list flag.

After the model runs, results will be written in tab-separated text files (with extension .tsv or .tab) in the "outputs" directory.

RECONFIGURE THE MODEL

To reconfigure the model, you can edit options.txt, modules.txt and scenarios.txt. If you want to add new constraints or technologies to the model, you should create new python modules in the local directory and then add their names to modules.txt. These modules should define some or all of the same callback functions as the modules inside switch/switch_mod (e.g., define_arguments(), define_components(), load_data(), post_solve()).

You can also inspect or change any of the model's input data by editing the *.tab files in the inputs* directories.

UPDATE MODEL TO LATEST VERSION

You can pull the latest version of the SWITCH-Hawaii data and SWITCH model code from github.com at any time by launching a Terminal window or Anaconda prompt, then cd'ing into the 'main' directory (the same place you run the model from) and running these commands:

git pull
git submodule update

The first command will attempt to merge your local changes with changes in the main repository. If there are any conflicts, you can follow the instructions given by the git command to resolve them.

Alternatively, you could rename your 'main' directory to something else (like 'main_backup') and then repeat the instructions in the 'Install SWITCH-Hawaii Data and SWITCH Model Code' section.
