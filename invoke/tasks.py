#!/usr/bin/env python3.5
import glob
import os
import shutil

from bs4 import BeautifulSoup
from invoke import run, task
from requests import get
import version_utils

koji_base_url = "http://koji.fedoraproject.org/koji/"

# global srpm_from_setup

def create_dirs():
    for dir in {"BUILD", "BUILDROOT", "RPMS", "SOURCES", "SPECS", "SRPMS"}:
        path = os.path.expanduser(os.path.join('~', 'rpmbuild', dir))
        print("Create dir {0}".format(path))
        os.makedirs(path, exist_ok=True)


def new_python_build():
    koji_url_python = koji_base_url + "packageinfo?packageID=130"
    r = get(koji_url_python)
    soup = BeautifulSoup(r.text, 'html.parser')

    last_pkg = None
    last_url = None
    for link in soup.find_all("a", href=True):
        package = link.text
        url = link["href"]
        if "python-" in package:
            try:
                pkg = version_utils.rpm.package(package)
            except version_utils.errors.RpmError:
                continue
            try:
                if version_utils.rpm.compare_packages(package, last_pkg) > 0:
                    last_pkg = package
                    last_url = url
            except TypeError:
                if not last_pkg:
                    last_pkg = package
                    last_url = url
    return last_pkg, koji_base_url + last_url


def new_python_srpm(name, url):
    r = get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    srpm = {}
    for link in soup.find_all("a", href=True):
        url_ = link["href"]
        name_ = url_.split("/")[-1]
        if ".src.rpm" in url_:
            # srpm["url"] = url_
            # srpm["name"] = name_
            if name_.replace(".src.rpm", "") == name:
                break
    print("Newest Python srpm {0} is at {1}".format(name, url_))
    return name_, url_


def get_python_srpm(name, url):
    path = os.path.expanduser(os.path.join('~', 'rpmbuild', "SRPMS", name))
    print("Download {0} to {1}".format(url, path))
    with open(path, 'wb') as srpm_file:
        response = get(url, stream=True)

        if not response.ok:
            print("Could not download {0}".format(url))
            exit

        for block in response.iter_content(1024):
            srpm_file.write(block)
    return path


def install_build_dep(srpm_path):
    # path = os.path.expanduser(os.path.join('~', 'rpmbuild', "SRPMS", name))
    print("Install build dependencies for {0}".format(srpm_path))
    run("sudo yum-builddep -y {0}".format(srpm_path))


@task
def clean(ctx):
    path = os.path.expanduser(os.path.join('~', 'rpmbuild'))
    print("Remove dir {0}".format(path))
    shutil.rmtree(path, ignore_errors=True)


@task
def setup(ctx):
    create_dirs()
    name, url = new_python_build()
    name, url = new_python_srpm(name, url)
    srpm_path = get_python_srpm(name, url)
    install_build_dep(srpm_path)


@task
def build(ctx, runtests=False):
    paths = glob.glob(os.path.expanduser(os.path.join('~', 'rpmbuild', "SRPMS", "*.src.rpm")))
    last_pkg = None
    for path in paths:
        package = path.rstrip(".src.rpm")
        try:
            if version_utils.rpm.compare_packages(package, last_pkg) > 0:
                last_pkg = package
        except TypeError:
            if not last_pkg:
                last_pkg = package
    srpm = ".".join([last_pkg, "src", "rpm"])

    path = os.path.expanduser(os.path.join('~', 'rpmbuild', "SRPMS", srpm))
    print("\"Install\" {0} to ~/rpmbuild".format(path))
    run("rpm -i {0}".format(path))

    if not runtests:
        path = os.path.expanduser(os.path.join('~', 'rpmbuild', "SPECS", "python.spec"))
        print("Disable tests in {0}".format(path))
        run("sed -i -e \"s/^%global run_selftest_suite 1/%global run_selftest_suite 0/g\" {0}".format(path))

    print("Build {0}".format(path))
    run("rpmbuild -ba {0}".format(path))
