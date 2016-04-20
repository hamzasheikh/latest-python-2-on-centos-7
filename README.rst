Install Latest Python on CentOS 7
=================================

This repo accompanies the blog post
`Install Latest Python on CentOS 7 <http://www.codeghar.com/blog/install-latest-python-on-centos-7.html>`_. While the blog details manual
steps this repo is more a clone-and-play type of deal.

How?
----

Install `Vagrant <https://www.vagrantup.com/>`_,
`VirtualBox <https://www.virtualbox.org/>`_, and
`Ansible <https://pypi.python.org/pypi/ansible>`_.

Clone this repo. Optionally, edit *Vagrantfile* or *playbook.yaml* to fit your
requirements. Run Vagrant.

::

    user@host$ vagrant up

Once the machine is up it has been provisioned with all the repos
and packages required to get going Review *playbook.yaml* for more
information. SSH into the VM.

::

    user@host$ vagrant ssh centos7

Run ``invoke`` to cleanup (not necessary the first time but needed
afterwards), setup (download Python source rpm package and prepare to build),
and build.

::

    vagrant@centos7$ invoke clean setup build

Copy all rpm packages in */home/vagrant/rpmbuild/RPMS/x86_64/* to your own
repo and install them as needed on CentOS 7 boxes.
