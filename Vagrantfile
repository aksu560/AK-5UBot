
Vagrant.configure("2") do |config|

  config.vm.box = "hashicorp/bionic64"
  config.vm.provider = "virtualbox"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
  config.vm.provision :shell, path: "provision/python.sh"
end
