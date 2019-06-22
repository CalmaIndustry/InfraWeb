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

        parser.add_argument('-vw', '--vmweb',
                            action='store_true',
                            help='Deploy VM & App web')

        parser.add_argument('-vd', '--vmdns',
                            action='store_true',
                            help='Deploy VM & DNS web')

        parser.add_argument('-w', '--web',
                            action='store_true',
                            help='Deploy web app')

        parser.add_argument('-d', '--dns',
                            action='store_true',
                            help='Deploy Dns app')

        args = parser.parse_args()

        return args

def deployweb():
        deploy1 = VMwareMod("web1","a")
        deploy2 = VMwareMod("web2","b")
        os.system('ansible-playbook Ansible/newvmweb.yml')
        time.sleep(70)
        vlan1 = VMwareVlan("web1")
        vlan2 = VMwareVlan("web2")

def deploydns():
        deploy1 = VMwareMod("dns1","c")
        deploy2 = VMwareMod("dns2","d")
        os.system('ansible-playbook Ansible/newvmdns.yml')
        time.sleep(70)

def appweb():
        os.system('ansible-playbook Ansible/infra_web_docker.yml')

def appdns():
        os.system('ansible-playbook Ansible/infra_dns.yml')

def main():
	args = get_args()
	os.system('chmod 400 Cert/id_rsa-pa')
	os.system('cp Ansible/conf/hosts /etc/ansible/hosts')
	if args.all:
		deployweb()
		deploydns()
		appweb()
		appdns()
	elif args.vmweb:
		deployweb()
		appweb()
	elif args.vmdns:
		deploydns()
		appdns()
	elif args.web:
		appweb()
	elif args.dns:
		appdns()
	else:
		print("No Argument")


if __name__ == "__main__":
    main()

