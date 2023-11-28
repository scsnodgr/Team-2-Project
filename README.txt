Project Collaborators:
- scsnodgr - Sebastian Snodgrass
- leowilliams03 - Leo Williams
- ShaunBobbitt - Shaun Bobbitt
- LinkedUp07 - Ben Edens

To run the project:
- Run on a Windows machine (MacOS has responsiveness issues with tkinter that make the program difficult to use)
- Enter a terminal in the project directory (should contain laser-tag.py, python_trafficgenerator_v2.py, Audio folder, and photon.jpg)
- Run "python laser-tag.py" first, then run "python python_trafficgenerator_v2.py" in a separate terminal
  - laser-tag.py will not open any window until python_trafficgenerator_v2.py has been run and prompts answered

Note:
- This code requires you to have Pillow and Supabase installed
  - To install these dependencies, go into a terminal and "pip install Pillow supabase"
- This code also requires a specific version of playsound (the most current version will not work properly)
  - To install this dependency, go into a terminal and "pip install playsound==1.2.2"
- The return to player_entry screen button will appear when the timer runs out
