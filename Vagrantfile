# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty32"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.synced_folder ".", "/mayan-edms-repository"
  config.vm.provision :shell, :path => "contrib/scripts/install/development.sh", privileged: false
end

