Install Latest Python on CentOS 7
=================================

This repo accompanies the blog post
`Install Latest Python on CentOS 7 <http://www.codeghar.com/blog/install-latest-python-on-centos-7.html>`_.
While the blog details manual steps this repo is more a clone-and-play type of
deal.

How?
----

Install `Vagrant <https://www.vagrantup.com/>`_ (tested with v1.9.1),
`VirtualBox <https://www.virtualbox.org/>`_ (tested with v5.0.30), and
`Ansible <https://pypi.python.org/pypi/ansible>`_ (tested with v2.2.1.0 with
Python 3.5).

Clone this repo. Optionally, edit *Vagrantfile* or *playbook.yml* to fit your
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

Updates
-------

To update the Vagrant box you can either update OS packages with ``yum`` or
you can destroy this box, download a newer Vagrant box, and provision it.
Be warned that with the latter option you will lose all data.

Option 1

::

    vagrant@centos7$ sudo yum upgrade

Option 2

::

    user@host$ vagrant destroy -f
    user@host$ vagrant box update
    user@host$ vagrant up
