#!/usr/bin/env python

from fabric.api import *

env.use_ssh_config = True
		
#### Install NRPE #####
def ubuntu_nrpe():
	sudo('apt-get -y update && apt-get -y install nagios-nrpe-server nagios-plugins sed')

def centos_nrpe():
	sudo('yum -y update && yum -y install nrpe nagios-plugins-all sed')
	
	
#### Configure NRPE
def configure_nrpe():
	sudo("sudo cp /etc/nagios/nrpe.cfg /etc/nagios/nrpe.old && sudo sed -i 's/allowed_hosts=127.0.0.1/allowed_hosts=127.0.0.1, 54.72.182.50/g' /etc/nagios/nrpe.cfg && sudo sed -i 's/hda1/xvda1/g' /etc/nagios/nrpe.cfg && sudo sed -i 's/check_xvda1/check_root_partition/g' /etc/nagios/nrpe.cfg")
	

#### Restart NRPE
@task
def restart_nrpe(env):
	env = env.lower()
	if env == 'ubuntu':
		sudo('/etc/init.d/nagios-nrpe-server restart')
	if env == 'centos':
		sudo('service nrpe restart')

#### Deploy
def deploy_nrpe_centos():
		centos_nrpe()
		configure_nrpe()
		restart_nrpe("centos")
	
def deploy_nrpe_ubuntu():
		ubuntu_nrpe()
		configure_nrpe()
		restart_nrpe("ubuntu")

@task
def deploy(env):
	env = env.lower()
	#### Deploys to either ubuntu or centos
	if env == 'ubuntu':
		deploy_nrpe_ubuntu()	
	if env == 'centos':
		deploy_nrpe_centos()	
	else:
		local('echo Please enter centos or ubuntu')
	
	
	
	
	
	
