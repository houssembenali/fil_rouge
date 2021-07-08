#!/usr/bin/env bash
apt-get update
# install python
apt-get install python3 python3-dev python3-pip -q -y
# install git for later GitPython module
apt-get install -y -q git
# remove python to keep only python 3
apt remove -y python
# install all needed python modules for the project (markdown to convert .m files to .html, GitPython to communicate with GitHub, pylint for code quality testing, flask for web server dev)
pip3 install flask markdown pylint GitPython