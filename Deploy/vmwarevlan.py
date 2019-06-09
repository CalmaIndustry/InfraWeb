from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
from pyVmomi import vim
from pyVim.task import WaitForTask
import atexit
import ssl
import vmutils

class VMwareVlan:

	def __init__(self,vm_name):

		self.vcenter = "192.168.100.10"
		self.user="administrator@cloud.projet"
		self.passwd="Pr@jet2019"
		self.content = ""
		self.vm_name = vm_name
		self.uuid = ""
		self.network_name = "DMZ PUBLIQUE"
		self.VsphereVlan()

	def Get_Obj(self, vimtype, name):

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

	def Vm_Info(self):

		container  = self.content.rootFolder
		viewType = [vim.VirtualMachine]
		recursive = True
		containerView = self.content.viewManager.CreateContainerView(container, viewType, recursive)
		children = containerView.view
		for child in children:
			summary = child.summary
			vmname = summary.config.name
			if self.vm_name == vmname:
				self.uuid = summary.config.uuid


	def VsphereCo(self):

		cssl=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		cssl.verify_mode=ssl.CERT_NONE
		covsphere = SmartConnect(host=self.vcenter, user=self.user, pwd=self.passwd, sslContext=cssl)
		atexit.register(Disconnect, covsphere)
		self.content = covsphere.RetrieveContent()

	def VsphereVlan(self):

		self.VsphereCo()
		self.Vm_Info()
		vm = self.content.searchIndex.FindByUuid(None, self.uuid, True)
		device_change = []
		for device in vm.config.hardware.device:
			if isinstance(device, vim.vm.device.VirtualEthernetCard):
				nicspec = vim.vm.device.VirtualDeviceSpec()
				nicspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
				nicspec.device = device
				nicspec.device.wakeOnLanEnabled = True
				nicspec.device.deviceInfo = vim.Description()
				nicspec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
				nicspec.device.backing.network = self.Get_Obj([vim.Network],self.network_name)
				nicspec.device.backing.deviceName = self.network_name

				nicspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
				nicspec.device.connectable.startConnected = True

#				nicspec.device.connectable.connected = True
				nicspec.device.connectable.allowGuestControl = True
				device_change.append(nicspec)

				config_spec = vim.vm.ConfigSpec(deviceChange=device_change)
				taskvlan = vm.ReconfigVM_Task(config_spec)
				WaitForTask(taskvlan)

				VMs = self.content.searchIndex.FindByDnsName(None, self.vm_name, True)
				print(vm)
				TASK = VMs.ResetVM_Task()
#				WaitForTask(TASK)

