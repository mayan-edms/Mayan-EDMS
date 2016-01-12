# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider :lxc do |v, override|
    override.vm.box = "fgrehm/trusty64-lxc"
  end

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  # Development box
  config.vm.define "development", autostart: false do |development|
    development.vm.network "forwarded_port", guest: 8000, host: 8000
    development.vm.synced_folder ".", "/mayan-edms-repository"
    development.vm.provision :shell, :path => "contrib/scripts/install/development.sh", privileged: false

    development.vm.provision "file", destination: "/home/vagrant/mayan-edms/mayan/settings/celery_redis.py", source: "contrib/settings/celery_redis.py"
    development.vm.provision "file", destination: "/home/vagrant/mayan-edms/mayan_edms_worker.sh", source: "contrib/misc/mayan_edms_worker.sh"
  end

  # Production box
  config.vm.define "production", autostart: false do |production|
    production.vm.network "forwarded_port", guest: 80, host: 8080
    production.vm.provision :shell, :path => "contrib/scripts/install/production.sh", privileged: true
  end

end
