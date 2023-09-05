## trackrl

An OpenAI Gym environment to conduct reinforcement learning experiments in RCT2 track construction.

Run trackrl.py to train a model. Then run tracknn.py after specifying the model checkpoint path on line 28.

Python library requirements:
* pyobjc-framework-Quartz (for screenshots \- Mac only)
* pyzmq
* gym (OpenAI)
* numpy
* dill
* tabulate
* dm\_tree
* ray\[rllib\]
* tensorflow
* tqdm
* matplotlib

OpenRCT2: 
* Must use my modified version at https://github.com/campbelljc/OpenRCT2. 
* Building requires installing the ZMQ library (https://zeromq.org). There may be some issues getting it recognized by the OpenRCT2 build process... 
* To run, cd to the OpenRCT2 build directory, then run the command to launch the game (e.g., `./OpenRCT2.app/Contents/MacOS/OpenRCT2`), and start a blank scenario (e.g., one of the two in the scenarios folder from this repo).
