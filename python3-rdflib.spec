#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (few failing as of 6.1.1)

%define	module	rdflib

Summary:	Python 3 library for working with RDF
Summary(pl.UTF-8):	Biblioteka Pythona 3 do pracy z RDF
Name:		python3-%{module}
# 6.3.0+ uses poetry instead of setuptools
Version:	6.2.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/RDFLib/rdflib/releases
Source0:	https://github.com/RDFLib/rdflib/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	8120a87ba4a60b1024906e5328004e87
URL:		https://rdflib.dev/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-berkeleydb
BuildRequires:	python3-html5lib
%if "%{_ver_lt '%{py3_ver}' '3.8'}" == "1"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-isodate
BuildRequires:	python3-networkx
BuildRequires:	python3-pyparsing
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-subtests
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.749
%if %{with doc}
BuildRequires:	python3-myst_parser
BuildRequires:	python3-sphinx_autodoc_typehints
BuildRequires:	python3-sphinxcontrib-apidoc
BuildRequires:	python3-sphinxcontrib-kroki
BuildRequires:	sphinx-pdg >= 4.1.2
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RDFLib is a Python library for working with RDF, a simple yet powerful
language for representing information. The library contains an RDF/XML
parser/serializer, a TripleStore, an InformationStore and various
store backends. It is being developed by Daniel Krech along with the
help of a number of contributors.

%description -l pl.UTF-8
RDFLib to biblioteka Pythona do pracy z RDF - prostym, ale potężnym
językiem do reprezentowania informacji. Biblioteka zawiera
parser/serializer RDF/XML, TripleStore, InformationStore oraz różne
backendy do przechowywania informacji. Jest rozwijana przez Daniela
Krecha z pomocą wielu współpracowników.

%package apidocs
Summary:	API documentation for Python rdflib module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona rdflib
Group:		Documentation

%description apidocs
API documentation for Python rdflib module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona rdflib.

%package -n rdflib-tools
Summary:	Utilities from python-rdflib
Summary(pl.UTF-8):	Narzędzia z pakietu python-rdflib
Group:		Applications/File
Requires:	python3-%{module} = %{version}-%{release}

%description -n rdflib-tools
Utilities from python-rdflib.

%description -n rdflib-tools -l pl.UTF-8
Narzędzia z pakietu python-rdflib.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build %{?with_tests:test}

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTORS LICENSE README.md
%{py3_sitescriptdir}/rdflib
%{py3_sitescriptdir}/rdflib-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,apidocs,*.html,*.js}
%endif

%files -n rdflib-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/csv2rdf
%attr(755,root,root) %{_bindir}/rdf2dot
%attr(755,root,root) %{_bindir}/rdfgraphisomorphism
%attr(755,root,root) %{_bindir}/rdfpipe
%attr(755,root,root) %{_bindir}/rdfs2dot
