%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc 1

%global cname neutron
%global sname %{cname}client

%global common_desc \
Client library and command line utility for interacting with OpenStack \
Neutron's API.

Name:       python-neutronclient
Version:    XXX
Release:    XXX
Summary:    Python API and CLI for OpenStack Neutron

License:    Apache-2.0
URL:        http://launchpad.net/%{name}/
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires: openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{sname}
Summary:    Python API and CLI for OpenStack Neutron

BuildRequires: git-core
BuildRequires: openstack-macros
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: python3-osc-lib-tests

%description -n python3-%{sname}
%{common_desc}

%package -n python3-%{sname}-tests
Summary:    Python API and CLI for OpenStack Neutron - Unit tests
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

%description      doc
%{common_desc}
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# Build HTML docs
%tox -e docs

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%pyproject_install

%check
%tox -e %{default_toxenv}

%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/%{sname}/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
