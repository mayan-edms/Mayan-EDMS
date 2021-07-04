help:
	@echo
	@echo "start - Start and provision the vagrant box."
	@echo "destroy - Stop and delete the vagrant box."
	@echo "test - Execute the Mayan EDMS test runner inside the vagrant box."
	@echo

start:
	vagrant up advanced-deploy

destroy:
	vagrant destroy advanced-deploy

test:
	vagrant ssh -c "sudo -u www-data /usr/share/mayan-edms/bin/mayan-edms.py test --mayan-apps --no-input"



