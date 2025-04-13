#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (few failing as of 6.1.1)

%define	module	rdflib

Summary:	Python 3 library for working with RDF
Summary(pl.UTF-8):	Biblioteka Pythona 3 do pracy z RDF
Name:		python3-%{module}
Version:	7.1.4
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/RDFLib/rdflib/releases
Source0:	https://github.com/RDFLib/rdflib/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	19d7da77b48922dc2cc15467141d7ecf
URL:		https://rdflib.dev/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-poetry-core >= 1.4.0
BuildRequires:	python3-wheel >= 0.42
%if %{with tests}
BuildRequires:	python3-berkeleydb >= 18.1
BuildRequires:	python3-html5lib
%if "%{_ver_lt '%{py3_ver}' '3.8'}" == "1"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-isodate
# >= 0.7.2
BuildRequires:	python3-lxml >= 4.3
BuildRequires:	python3-networkx >= 2
BuildRequires:	python3-pyparsing >= 2.1.0
BuildRequires:	python3-pytest >= 7.1.3
BuildRequires:	python3-pytest-cov >= 4
# TODO: html5rdf>=1.2, orjson>=3.9.14
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.045
%if %{with doc}
BuildRequires:	python3-isodate
BuildRequires:	python3-myst_parser >= 2
BuildRequires:	python3-sphinx_autodoc_typehints >= 1.25.3
BuildRequires:	python3-sphinxcontrib-apidoc >= 0.3
BuildRequires:	python3-typing_extensions >= 4.5.0
BuildRequires:	sphinx-pdg >= 7.1.2
%endif
Requires:	python3-modules >= 1:3.8
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
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-tests

# many berkeleydb related tests fail with "TypeError: cannot unpack non-iterable builtin_function_or_method object" after cursor.set_range()
# test_example[secure_with_audit.py] fails with "AttributeError: \'int\' object has no attribute \'endswith\'\n'" in audit function

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
PYTHONPATH=$(pwd)/build-3-tests \
%{__python3} -m pytest test -k 'not berkeleydb and not secure_with_audit.py and not test_graph_context'
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc

PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTORS LICENSE README.md
%{py3_sitescriptdir}/rdflib
%{py3_sitescriptdir}/rdflib-%{version}.dist-info
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
