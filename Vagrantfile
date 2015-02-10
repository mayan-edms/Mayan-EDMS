# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty32"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.synced_folder ".", "/mayan-edms-repository"
  config.vm.provision :shell, :path => "contrib/scripts/install/development.sh", privileged: false

  config.vm.provision "file", destination: "/home/vagrant/mayan-edms/mayan/settings/celery_redis.py", source: "contrib/configs/celery_redis.py"
  config.vm.provision "file", destination: "/home/vagrant/mayan-edms/mayan_edms_worker.sh", source: "contrib/misc/mayan_edms_worker.sh"
end
