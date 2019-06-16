from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
from pyVmomi import vim
from pyVim.task import WaitForTask
import ssl
import atexit
import getpass
import time

class VMwareMod:


	def __init__(self,vm_name,i):
		self.vcenter = "192.168.100.10"
		self.user="administrator@cloud.projet"
		self.passwd="Pr@jet2019"
		self.template_name="Template"
		self.content = ""
		self.datastore_name = "datastore2"
		self.resource_pool_name ="Cluster ESX"
		self.datacenter_name = ""
		self.vm_name=vm_name
		self.vm_folder=""
		self.ip=""
		self.i = i
		self.VsphereClone()

	#Get Vcenter Info
	def getobj(self,vimtype,name):

		obj = None

		container = self.content.viewManager.CreateContainerView(
			self.content.rootFolder, vimtype, True)
		for c in container.view:
			if name:
				if c.name == name:
					obj = c
					break
			else:
				obj = c
				break
		return obj

	#Get InfoVM
	def PrintVmInfo(self, vm, depth=1):

		ch1 = "a"
		ch2 = "b"
		ch3 = "c"


		maxdepth = 10

		if hasattr(vm, 'childEntity'):
			if depth > maxdepth:
				return
			vmList = vm.childEntity
			for c in vmList:
				PrintVmInfo(c, depth+1)
			return
		if isinstance(vm, vim.VirtualApp):
			mList = vm.vm
			for c in vmList:
				PrintVmInfo(c, depth + 1)
			return
		summary = vm.summary
		if summary.config.name == self.vm_name:
			print("Name       : ", summary.config.name)
			print("Path       : ", summary.config.vmPathName)
			print("Guest      : ", summary.config.guestFullName)
			annotation = summary.config.annotation
			if annotation != None and annotation != "":
				print("Annotation : ", annotation)
			print("State      : ", summary.runtime.powerState)
			if summary.guest != None:
				self.ip = summary.guest.ipAddress
				print(self.i)
				if self.i == ch1:
					if self.ip != None and self.ip != "":
						print("IP         : ", self.ip)
						fichier = open("/etc/ansible/hosts", "a")
						fichier.write("[web1postip]\n{} env=prod ansible_ssh_user=root ansible_ssh_private_key_file=/root/InfraWeb/Cert/id_rsa-pa\n".format(self.ip))
						fichier.close()
				elif self.i == ch2:
					if self.ip != None and self.ip != "":
						print("IP         : ", self.ip)
						fichier = open("/etc/ansible/hosts", "a")
						fichier.write("[web2postip]\n{} env=prod ansible_ssh_user=root ansible_ssh_private_key_file=/root/InfraWeb/Cert/id_rsa-pa\n".format(self.ip))
						fichier.close()
				elif self.i == ch3:
					if self.ip != None and self.ip != "":
						print("IP         : ", self.ip)
						fichier = open("/etc/ansible/hosts", "a")
						fichier.write("[dns1postip]\n{} env=prod ansible_ssh_user=root ansible_ssh_private_key_file=/root/InfraWeb/Cert/id_rsa-pa\n".format(self.ip))
						fichier.close()
				else:
					if self.ip != None and self.ip != "":
						print("IP         : ", self.ip)
						fichier = open("/etc/ansible/hosts", "a")
						fichier.write("[dns2postip]\n{} env=prod ansible_ssh_user=root ansible_ssh_private_key_file=/root/InfraWeb/Cert/id_rsa-pa\n".format(self.ip))
						fichier.close()


	#Connexion to VCenter
	def VsphereCo(self):

		self.cssl=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		self.cssl.verify_mode=ssl.CERT_NONE
		self.co = SmartConnect(host=self.vcenter, user=self.user, pwd=self.passwd, sslContext=self.cssl)
		atexit.register(Disconnect, self.co)
		self.content = self.co.RetrieveContent()

	#Clone VM
	def VsphereClone(self):

		self.VsphereCo()
		power_on = True
		datacenter = self.getobj([vim.Datacenter], self.datacenter_name)#
		template = self.getobj([vim.VirtualMachine], self.template_name)
		datastore = self.getobj([vim.Datastore], self.datastore_name)
		resource_pool = self.getobj([vim.ResourcePool], self.resource_pool_name)
		destfolder = self.getobj([vim.Folder],self.vm_folder)

		relospec = vim.vm.RelocateSpec()
		relospec.datastore = datastore
		relospec.pool = resource_pool

		clonespec = vim.vm.CloneSpec()
		clonespec.location = relospec
		clonespec.powerOn = power_on

		task = template.Clone(folder=destfolder, name=self.vm_name, spec=clonespec)
		WaitForTask(task)
		time.sleep(70)
		self.VsphereVmInfo()


	#Get VM Info
	def VsphereVmInfo(self):

		for child in self.content.rootFolder.childEntity:
			if hasattr(child, 'vmFolder'):
				datacenter = child
				vmFolder = datacenter.vmFolder
				vmList = vmFolder.childEntity
				for vm in vmList:
					self.PrintVmInfo(vm)




