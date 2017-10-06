# UPI - Universal Post Install
Your best friend in post installation!

Author: Mirko Brombin

This script allows you to perform actions that are normally performed after installing a Linux distribution. The system automatically detects the distribution and language you are using and executes the appropriate script.

## How to use it?
Download the updated zip [here](https://github.com/mirkobrombin/Universal-Post-Install/archive/master.zip), or clone from GitHub:  
	```git clone https://github.com/mirkobrombin/Universal-Post-Install.git```  
If you downloaded the archive, extract it. Now choose one of the following methods:

### CLI mode (recommended)
Enter in folder **Universal-Post-Install** and run: **main.py**:
	```./main.py```

### GUI mode
Enter in folder **Universal-Post-Install** and run: **main.py** with **-gtk** flag:
	```sudo python main.py -gtk```

## Translations:
Scripts for each distribution are not necessarily written by the same creator of UPI, so it may happen that it is not available in the language of your system. If the script did not find a version that corresponds to your language, it will load it in English.

## Supported Distributions:
- ElementaryOS
- Deepin
- Ubuntu
- Debian (under development, not tested)

## Custom configurations for UPI?
On certain situations, it is useful to provide your **collaborators** with a tool for installing/removing/updating packages and performing various types of operations.  
UPI is an easy-to-use tool, if you're interested in creating a custom post-installation script, just fork the project and create your script in the **scripts** folder.
At the moment I am working on a detailed **Wiki** where to step by step how to create a custom script.

## Your distribution is not supported?
Ask for integration in the [Issues](https://github.com/mirkobrombin/Universal-Post-Install/issues) section.
