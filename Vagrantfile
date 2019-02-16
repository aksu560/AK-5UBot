Vagrant.configure("2") do |config|

  config.vm.box = "beanbox"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
  config.vm.provision :shell, path: "provision/python.sh"
  config.vm.provision "shell", inline: <<-SHELL
    python3 /vagrant/main.py
  SHELL

end
