import argparse
import os
import time
from Deploy.vmwarevm import VMwareMod
from Deploy.vmwarevlan import VMwareVlan

def get_args():

	parser = argparse.ArgumentParser()

	parser.add_argument('-a', '--all',
                            action='store_true',
                            help='All the deploy')


	args = parser.parse_args()

	return args

def deployweb():
	deploy1 = VMwareMod("web1","a")
	deploy2 = VMwareMod("web2","b")
	os.system('ansible-playbook Ansible/newvmweb.yml')
#	vlan1 = VMwareVlan("web1")
#	vlan1 = VMwareVlan("web2")

def deploydns():
	deploy1 = VMwareMod("dns1","c")
	deploy2 = VMwareMod("dns2","d")
	os.system('chmod 400 Cert/id_rsa-pa')
	os.system('ansible-playbook Ansible/newvmdns.yml')

def appweb
	time.sleep(70)
	os.system('ansible-playbook Ansible/infra_web_docker.yml')

def appdns():
	time.sleep(70)
	os.system('ansible-playbook Ansible/infra_web_docker.yml')

def main():

	args = get_args()
	if args.all:
		os.system('cp Ansible/conf/hosts /etc/ansible/hosts')
		deployweb()
		deploydns()
		appweb()
		appdns()

if __name__ == "__main__":
    main()
