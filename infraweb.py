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

def main():

	args = get_args()
	if args.all:
		deploy1 = VMwareMod("web1","a")
		deploy2 = VMwareMod("web2","b")
		os.system('chmod 400 Cert/id_rsa-pa')
		os.system('ansible-playbook Ansible/newvmweb.yml')
		deploy3 = VMwareMod("dns1","c")
		deploy4 = VMwareMod("dns2","d")
		os.system('ansible-playbook Ansible/newvmdns.yml')
#		vlan1 = VMwareVlan("web1")
#		vlan1 = VMwareVlan("web2")
#		os.system('cp Ansible/conf/hosts /etc/ansible/hosts')
#		time.sleep(70)
#		os.system('ansible-playbook Ansible/infra_web_docker.yml')

if __name__ == "__main__":
    main()
