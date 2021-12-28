#!make
include config.env

HOST_IP = `/sbin/ip route get 1.0.0.0|cut --delimiter=" " --fields=7`
APT_PROXY ?= $(HOST_IP):3142
PIP_INDEX_URL ?= http://$(HOST_IP):3141/root/pypi/+simple/
PIP_TRUSTED_HOST ?= $(HOST_IP)

vagrant-destroy: ## Destroy the machine.
vagrant-destroy:
	@VAGRANT_CWD=vagrant vagrant destroy --force

vagrant-ssh: ## Connect to the machine via SSH.
vagrant-ssh:
	@VAGRANT_CWD=vagrant vagrant ssh

vagrant-up: ## Starts and provisions the machine.
vagrant-up:
	@VAGRANT_CWD=vagrant vagrant up

vagrant-up-with-proxy: ## Starts and provisions the machine using an APT proxy as APT_PROXY.
vagrant-up-with-proxy: devpi-start
	@APT_PROXY=$(APT_PROXY) PIP_INDEX_URL=$(PIP_INDEX_URL) PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) VAGRANT_CWD=vagrant vagrant up
	$(MAKE) devpi-stop
