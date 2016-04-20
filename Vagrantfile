# -*- mode: ruby -*-
# vi: set ft=ruby :
required_plugins = %w(vagrant-vbguest)
required_plugins.each do |plugin|
  system "vagrant plugin install #{plugin}" unless Vagrant.has_plugin? plugin
end

Vagrant.configure(2) do |config|

  config.vm.provider 'virtualbox' do |v|
    v.memory = 2048
    v.cpus = 2
  end

  config.vm.define 'centos7' do |centos|

    centos.vm.box = "centos/7"

    centos.vm.box_check_update = true

    centos.vm.guest = :linux

    # When uncommented in Vagrant 1.8.1
    # ``vagrant up`` throws this error
    # Vagrant attempted to execute the capability 'change_host_name'
    # on the detect guest OS 'linux', but the guest doesn't
    # support that capability. This capability is required for your
    # configuration of Vagrant. Please either reconfigure Vagrant to
    # avoid this capability or fix the issue by creating the capability.
    # centos.vm.hostname = "centos7"

    # When uncommented in Vagrant 1.8.1
    # ``vagrant up`` throws this error
    # Vagrant attempted to execute the capability 'configure_networks'
    # on the detect guest OS 'linux', but the guest doesn't
    # support that capability. This capability is required for your
    # configuration of Vagrant. Please either reconfigure Vagrant to
    # avoid this capability or fix the issue by creating the capability.
    # centos.vm.network "private_network", type: "dhcp"

    centos.vm.synced_folder ".", "/vagrant_data", disabled: true

    centos.ssh.shell = "/bin/bash"

    centos.vm.provision "ansible" do |ansible|
      ansible.verbose = "v"
      ansible.playbook = "playbook.yaml"
    end
  end
end
