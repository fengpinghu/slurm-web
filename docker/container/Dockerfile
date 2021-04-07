# Copyright (C) 2017 Kilian Cavalotti <kilian@stanford.edu>
#
# This file is part of slurm-web.
#
# slurm-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# slurm-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with slurm-web.  If not, see <http://www.gnu.org/licenses/>.

# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.

FROM phusion/baseimage:0.9.19
#FROM phusion/baseimage:18.04-1.0.0
#FROM ubuntu:18.04
#kFROM phusion/baseimage
MAINTAINER Kilian Cavalotti <kilian@stanford.edu>

# Set correct environment variables.
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Use baseimage-docker's init system
CMD ["/sbin/my_init"]

# Install locales
#RUN locale-gen en_US.UTF-8

#ENV BUILD_DEPS="git devscripts equivs apt-utils apache2-dev libslurm-dev python-setuptools cython python-dev libslurmdb-dev libslurm-dev ca-certificates"
ENV BUILD_DEPS="python-pip git wget iputils-ping tcpdump telnet sssd libmunge-dev libmariadb-client-lgpl-dev libmysqlclient-dev ruby ruby-dev devscripts equivs apt-utils apache2-dev  python-setuptools cython python-dev  ca-certificates node-async"

#ENV RUN_DEPS="apache2 libapache2-mod-wsgi javascript-common python-flask clustershell libjs-bootstrap libjs-jquery-flot libjs-jquery-tablesorter munge slurm-llnl node-uglify fonts-dejavu-core python-ldap python-redis libjs-requirejs libjs-requirejs-text libjs-three libjs-d3 libjs-handlebars"
ENV RUN_DEPS="apache2 libapache2-mod-wsgi javascript-common python-flask clustershell libjs-async libjs-bootstrap libjs-jquery-flot libjs-jquery-tablesorter munge  node-uglify fonts-dejavu-core python-ldap python-redis libjs-requirejs libjs-requirejs-text libjs-three libjs-d3 libjs-handlebars"

# Enable universe and multiverse
#RUN cat /etc/apt/sources.list && \
#    sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list && \
#    sed -i 's/^#\s*\(deb.*multiverse\)$/\1/g' /etc/apt/sources.list

# Install system dependencies
RUN apt-get update -q && \
    apt-get -y install $BUILD_DEPS $RUN_DEPS && \
    ln -s /usr/lib/x86_64-linux-gnu/ /usr/lib64 && \
    gem install fpm

RUN a2enmod wsgi && \
    a2enconf javascript-common

RUN cd /usr/src  && \
    wget https://download.schedmd.com/slurm/slurm-20.02.5.tar.bz2 && \
    tar --bzip -x -f slurm-20.02.5.tar.bz2 && \
    cd slurm-20.02.5  && \
    ./configure --prefix=/tmp/slurm-build --sysconfdir=/etc/slurm --enable-pam --with-pam_dir=/lib/x86_64-linux-gnu/security/ && \
    make && \
    make contrib && \
    # a workaround for undefined symbled issue, 01/22/2019
    #gcc -shared  -fPIC -DPIC  /usr/src/slurm-20.02.5/src/plugins/accounting_storage/slurmdbd/.libs/accounting_storage_slurmdbd.o /usr/src/slurm-20.02.5/src/plugins/accounting_storage/slurmdbd/.libs/slurmdbd_agent.o   /usr/src/slurm-20.02.5/src/common/.libs/*.o   -g -O2 -pthread -ggdb3 -g -O1   -pthread -Wl,-soname -Wl,accounting_storage_slurmdbd.so -o /usr/src/slurm-20.02.5/src/plugins/accounting_storage/slurmdbd/.libs/accounting_storage_slurmdbd.so && \
    make install  && \
    cd .. && \
    fpm -s dir -t deb -v 1.0 -n slurm-20.02.5  --prefix=/usr -C /tmp/slurm-build . && \
    dpkg -i slurm-20.02.5_1.0_amd64.deb 

# Build and install specific deps
#ENV SLURM_VER=15.08.2
ENV SLURM_VER=20.02.5
RUN cd /usr/src && \
    #git clone https://github.com/PySlurm/pyslurm.git && \
    git clone https://github.com/bikerdanny/pyslurm.git && \
    cd pyslurm && \
    git checkout remotes/origin/$SLURM_VER && \
    #debian directory is removed, so let's checkout the version before that, 01/14/2019
    #git checkout 9477102dbcdd31d1fe674ff83b2131dccead7f9c  && \
    #sed -i 's/__max_slurm_hex_version__ = "0x0f0803"/__max_slurm_hex_version__ = "0x0f0807"/' setup.py && \
    #sed -i 's/\<libslurm-dev\>//g' debian/control     && \
    #echo "override_dh_shlibdeps:" >> debian/rules     && \
    #echo "	dh_shlibdeps --dpkg-shlibdeps-params=--ignore-missing-info" >> debian/rules && \
    #tar cvfj ../python-pyslurm_$SLURM_VER.orig.tar.bz2 --exclude .git .  && \
    #mk-build-deps -ri -t "apt-get -y --no-install-recommends" && \
    #dch -v $SLURM_VER-1 -D testing "New upstream release" && \
    #debuild -us -uc && \
    #dpkg -i ../python-pyslurm_$SLURM_VER-1_amd64.deb
#    python setup.py build && \
#    python setup.py install
    pip install autopxd2 && \
    cd /usr/include       && \
    autopxd --include-dir /usr/include slurm/slurm.h /usr/src/pyslurm/pyslurm/slurm.h.pxd && \
    autopxd --include-dir /usr/include slurm/slurmdb.h /usr/src/pyslurm/pyslurm/slurmdb.h.pxd && \
    autopxd --include-dir /usr/include slurm/slurm_errno.h /usr/src/pyslurm/pyslurm/slurm_errno.h.pxd && \
    cd /usr/src/pyslurm/pyslurm && \
    patch -p0 < slurm.h.pxd.patch && \
    patch -p0 < slurmdb.h.pxd.patch && \
    sed -i "s/slurm_addr_t control_addr/#slurm_addr_t control_addr/g" slurmdb.h.pxd && \
    sed -i "s/pthread_mutex_t lock/#pthread_mutex_t lock/g" slurmdb.h.pxd && \
    patch -p0 < slurm_errno.h.pxd.patch 

RUN pip install j2cli && \
    cd /usr/src/pyslurm/pyslurm &&\
    j2 slurm.j2 > slurm.pxd && \

    pip install Cython && \
    cd /usr/src/pyslurm/ &&\
    python setup.py build && \
    python setup.py install 

RUN cd /usr/src && \
    git clone https://github.com/edf-hpc/opentypejs.git && \
    cd opentypejs && \
    git checkout debian/0.4.3-2 && \
        tar cvfj ../opentypejs_0.4.3.orig.tar.bz2 --exclude .git . && \
        mk-build-deps -ri -t "apt-get -y --no-install-recommends" && \
        debuild -us -uc && \
        dpkg -i ../node-opentypejs_0.4.3-2_all.deb

RUN cd /usr/src && \
        git clone https://github.com/edf-hpc/libjs-bootstrap-typeahead.git && \
        cd libjs-bootstrap-typeahead/ && \
    git checkout debian/0.11.1-1 && \
        tar cvfj ../libjs-bootstrap-typeahead_0.11.1.orig.tar.bz2 --exclude .git . && \
        debuild -us -uc && \
        dpkg -i ../libjs-bootstrap-typeahead_0.11.1-1_all.deb

RUN cd /usr/src && \
        git clone https://github.com/edf-hpc/libjs-bootstrap-tagsinput.git && \
        cd libjs-bootstrap-tagsinput/ && \
    git checkout debian/0.8.0-1 && \
        tar cvfj ../libjs-bootstrap-tagsinput_0.8.0.orig.tar.bz2 --exclude .git . && \
        debuild -us -uc && \
        dpkg -i ../libjs-bootstrap-tagsinput_0.8.0-1_all.deb


RUN cd /usr/src && \
    pip install ClusterShell && \
    git clone https://github.com/fengpinghu/slurm-web.git && \
    cd slurm-web && \
    git checkout unc && \
    # build fails without package.json file
    #cp /usr/lib/nodejs/async/package.json  /usr/lib/nodejs/ && \
    debuild -us -uc && \
    dpkg -i ../slurm-web-*deb

# Create apache2 service file and start it
RUN rm /etc/apache2/sites-available/default-ssl.conf && \
    echo www-data > /etc/container_environment/APACHE_RUN_USER && \
    echo www-data > /etc/container_environment/APACHE_RUN_GROUP && \
    echo /var/log/apache2 > /etc/container_environment/APACHE_LOG_DIR && \
    echo /var/lock/apache2 > /etc/container_environment/APACHE_LOCK_DIR && \
    echo /var/run/apache2.pid > /etc/container_environment/APACHE_PID_FILE && \
    echo /var/run/apache2 > /etc/container_environment/APACHE_RUN_DIR && \
    chown -R www-data:www-data /var/log/apache2 && \
    chown -R 57386:57386 /var/www/
RUN mkdir -p /etc/service/apache2
COPY apache2.sh /etc/service/apache2/run
RUN chmod +x /etc/service/apache2/run

# Create munge service file and start it
RUN chown munge: /var/log/munge /var/lib/munge && \
    mkdir -p /etc/service/munge
COPY munge.sh /etc/service/munge/run
RUN chmod +x /etc/service/munge/run


# Cleanup
RUN apt-get clean

EXPOSE 80/tcp

VOLUME ["/etc/slurm-web"]


