%define debug_package %{nil}
# Main preamble
Summary: Slurm Web Python REST API
Name: slurm-web
Version: 3.9.6
Release:  1%{?dist}.edf
Source0: %{name}-%{version}.tar.gz
License: GPLv3
Group: Application/System
Prefix: %{_prefix}
Vendor: EDF CCN HPC <dsp-cspito-ccn-hpc@edf.fr>
Url: https://github.com/scibian/%{__name}

BuildRequires: python36 python3-setuptools
Requires: slurm-web-dashboard slurm-web-dashboard-backend slurm-web-restapi

%description
Slurm Web backend  REST API developed in Python using Flask web framework.

#########################################
# Prep, Setup, Build, Install & clean   #
#########################################

%prep
%setup -q

# Build Section
%build
cd %{_builddir}/%{name}-%{version}/rest
python3 setup.py build
cd %{_builddir}/%{name}-%{version}/conf_dashboard
python3 setup.py build
cd %{_builddir}/%{name}-%{version}

# Install & clean sections
%install
install -d %{buildroot}/etc/slurm-web/dashboard
install conf/dashboard/* %{buildroot}/etc/slurm-web/dashboard
install -d %{buildroot}/usr/share/slurm-web/dashboard
cp -dr --no-preserve=ownership dashboard %{buildroot}/usr/share/slurm-web/
cd %{_builddir}/%{name}-%{version}/rest
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
cd %{_builddir}/%{name}-%{version}
install -d %{buildroot}/usr/share/slurm-web/conf-server
install -m 644 conf_dashboard/slurmconfdashboard/slurm-web-conf.wsgi %{buildroot}/usr/share/slurm-web/conf-server/slurm-web-conf.wsgi
cd %{_builddir}/%{name}-%{version}/conf_dashboard
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
cd %{_builddir}/%{name}-%{version}
install -d %{buildroot}/usr/share/slurm-web/restapi
install -m 644 rest/slurmrestapi/slurm-web-restapi.wsgi %{buildroot}/usr/share/slurm-web/restapi/slurm-web-restapi.wsgi
install -d %{buildroot}/etc/slurm-web/
install conf/restapi.conf %{buildroot}/etc/slurm-web/restapi.conf
install conf/racks.xml %{buildroot}/etc/slurm-web/racks.xml
install schema/racks.dtd %{buildroot}/usr/share/slurm-web/restapi/schema/dtd

%clean
rm -rf %{buildroot}

#############
# Preambles #
#############

%package dashboard
Summary: Slurm Web HTML+JS dashboard
Group: Application/System
%description dashboard
The dashboard in HTML and Javascript that runs in a browser.

%package dashboard-backend
Summary: Slurm Web conf dashboard
Requires: python36 python3-flask
%description dashboard-backend
Static Flask server to supply config files for the dashboard

%package restapi
Summary: Slurm Web Python REST API
Requires: python36 python3-flask python3-redis python3-ldap python3-pyslurm python3-Cython
%description restapi
Slurm Web backend  REST API developed in Python using Flask web framework.

##################
# Files Sections #
##################

# Main meta-package
%files

# core
%files dashboard
/usr/share/slurm-web/dashboard

%files dashboard-backend
%config /etc/slurm-web/dashboard/*
/usr/share/slurm-web/conf-server
%{python3_sitelib}/slurm_web_dashboard_backend/*
%{python3_sitelib}/slurm_web_dashboard_backend*.egg-info

%files restapi
%config /etc/slurm-web/restapi.conf
%config /etc/slurm-web/racks.xml
/usr/share/slurm-web/restapi
%{python3_sitelib}/slurm_web_restapi/*
%{python3_sitelib}/slurm_web_restapi*.egg-info

%changelog
* Mon Mar 22 2021 Guillaume Ranquet <guillaume-externe.ranquet@edf.fr> 3.9.6-1el8.edf
- Initial RPM release
