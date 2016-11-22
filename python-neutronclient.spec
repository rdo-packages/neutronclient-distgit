%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname neutronclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-neutronclient
Version:    XXX
Release:    XXX
Summary:    Python API and CLI for OpenStack Neutron

License:    ASL 2.0
URL:        http://launchpad.net/python-neutronclient/
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:  noarch

# Since RDO Mitaka at GA had python-neutronclient-tests
# We need to obsoletes this test subpackage other it will
# affect while upgrade from Mitaka to Newton
Obsoletes:  python-%{sname}-tests

%description
Client library and command line utility for interacting with OpenStack
Neutron's API.

%package -n python2-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python2-neutronclient}

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr

Requires: python-babel >= 2.3.4
Requires: python-cliff >= 1.15.0
Requires: python-iso8601 >= 0.1.11
Requires: python-netaddr >= 0.7.12
Requires: python-os-client-config >= 1.13.1
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.16.0
Requires: python-pbr
Requires: python-requests >= 2.10.0
Requires: python-simplejson >= 2.2.0
Requires: python-six >= 1.9.0
Requires: python-debtcollector
Requires: python-osc-lib
Requires: python-keystoneauth1 >= 2.10.0

%description -n python2-%{sname}
Client library and command line utility for interacting with OpenStack
Neutron's API.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python3-neutronclient}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires: python3-babel >= 2.3.4
Requires: python3-cliff >= 1.15.0
Requires: python3-iso8601 >= 0.1.11
Requires: python3-netaddr >= 0.7.12
Requires: python3-os-client-config >= 1.13.1
Requires: python3-oslo-i18n >= 2.1.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-utils >= 3.16.0
Requires: python3-pbr
Requires: python3-requests >= 2.10.0
Requires: python3-simplejson >= 2.2.0
Requires: python3-six >= 1.9.0
Requires: python3-debtcollector
Requires: python3-osc-lib
Requires: python3-keystoneauth1 >= 2.10.0

%description -n python3-%{sname}
Client library and command line utility for interacting with OpenStack
Neutron's API.
%endif

%package doc
Summary:          Documentation for OpenStack Neutron API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-reno

%description      doc
Client library and command line utility for interacting with OpenStack
Neutron's API.

%prep
%setup -q -n %{name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/neutron %{buildroot}%{_bindir}/neutron-%{python3_version}
ln -s ./neutron-%{python3_version} %{buildroot}%{_bindir}/neutron-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/neutronclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/neutron %{buildroot}%{_bindir}/neutron-%{python2_version}
ln -s ./neutron-%{python2_version} %{buildroot}%{_bindir}/neutron-2

ln -s ./neutron-2 %{buildroot}%{_bindir}/neutron

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/neutronclient/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html


%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/neutronclient
%{python2_sitelib}/*.egg-info
%{_bindir}/neutron
%{_bindir}/neutron-2
%{_bindir}/neutron-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/neutron-3
%{_bindir}/neutron-%{python3_version}
%endif

%files doc
%doc html
%license LICENSE

%changelog
