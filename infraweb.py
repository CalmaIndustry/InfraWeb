import argparse
import os
import time
from Deploy.vmwarevm import VMwareMod


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
		deploy1 = VMwareMod("web2","b")
		os.system('chmod 400 Cert/id_rsa-pa')
		os.system('ansible-playbook Ansible/newvm.yml')
		os.system('cp Ansible/conf/hosts /etc/ansible/hosts')
		time.sleep(70)
		os.system('ansible-playbook Ansible/infra_web_docker.yml')

if __name__ == "__main__":
    main()
