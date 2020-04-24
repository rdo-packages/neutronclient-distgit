%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global cname neutron
%global sname %{cname}client

%global common_desc \
Client library and command line utility for interacting with OpenStack \
Neutron's API.

Name:       python-neutronclient
Version:    7.1.1
Release:    1%{?dist}
Summary:    Python API and CLI for OpenStack Neutron

License:    ASL 2.0
URL:        http://launchpad.net/%{name}/
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:  noarch

Obsoletes:  python-%{sname}-tests <= 4.1.1-3

%description
%{common_desc}

%package -n python3-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python3-%{sname}}
Obsoletes: python2-%{sname} < %{version}-%{release}

BuildRequires: git
BuildRequires: openstack-macros
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
# Required for unit tests
BuildRequires: python3-osc-lib-tests
BuildRequires: python3-oslotest
BuildRequires: python3-testtools
BuildRequires: python3-testrepository
BuildRequires: python3-testscenarios
BuildRequires: python3-keystoneauth1
BuildRequires: python3-keystoneclient
BuildRequires: python3-os-client-config
BuildRequires: python3-osc-lib
BuildRequires: python3-oslo-log
BuildRequires: python3-oslo-serialization
BuildRequires: python3-oslo-utils
BuildRequires: python3-cliff

Requires: python3-babel >= 2.3.4
Requires: python3-iso8601 >= 0.1.11
Requires: python3-os-client-config >= 1.28.0
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-pbr
Requires: python3-requests >= 2.14.2
Requires: python3-six >= 1.10.0
Requires: python3-debtcollector >= 1.2.0
Requires: python3-osc-lib >= 1.10.0
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-keystoneclient >= 1:3.8.0
Requires: python3-cliff >= 2.8.0
Requires: python3-netaddr >= 0.7.18

Requires: python3-simplejson >= 3.5.1

%description -n python3-%{sname}
%{common_desc}

%package -n python3-%{sname}-tests
Summary:    Python API and CLI for OpenStack Neutron - Unit tests
%{?python_provide:%python_provide python3-%{sname}-tests}
Requires: python3-%{sname} == %{version}-%{release}
Requires: python3-osc-lib-tests
Requires: python3-oslotest
Requires: python3-testtools
Requires: python3-testrepository
Requires: python3-testscenarios

%description -n python3-%{sname}-tests
%{common_desc}

This package containts the unit tests.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Neutron API Client

BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-reno

%description      doc
%{common_desc}
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# Build HTML docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cname} %{buildroot}%{_bindir}/%{cname}-3

%check
# (TODO) Ignore unit tests results until https://bugs.launchpad.net/python-neutronclient/+bug/1783789
# is fixed.
%{__python3} setup.py testr || true

%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/%{cname}
%{_bindir}/%{cname}-3
%exclude %{python3_sitelib}/%{sname}/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Apr 24 2020 RDO <dev@lists.rdoproject.org> 7.1.1-1
- Update to 7.1.1

