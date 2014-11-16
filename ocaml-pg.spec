%define		ocaml_ver	1:3.10.0
Summary:	PostgreSQL binding for OCaml
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla
Name:		ocaml-pg
Version:	2.1
Release:	1
License:	LGPL + OCaml linking exception
Group:		Libraries
Source0:	http://forge.ocamlcore.org/frs/download.php/1413/pgocaml-%{version}.tgz
# Source0-md5:	a05383cfdb34478eac93d9c84f2f2e77
URL:		http://pgocaml.forge.ocamlcore.org/
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-calendar-devel
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-csv-devel
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-pcre-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml.
It lets you embed SQL statements directly into OCaml code.

%description -l pl.UTF-8
PG'OCaml to prosty, bezpieczny pod względem typów interfejs do
PostgreSQL-a dla OCamla. Pozwala osadzać instrukcje SQL bezpośrednio
w kodzie w OCamlu.

%package devel
Summary:	PostgreSQL binding for OCaml
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla
Group:		Development/Libraries
Requires:	ocaml-calendar-devel
Requires:	ocaml-csv-devel
Requires:	ocaml-pcre-devel
%requires_eq	ocaml

%description devel
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml.
It lets you embed SQL statements directly into OCaml code.

%description devel -l pl.UTF-8
PG'OCaml to prosty, bezpieczny pod względem typów interfejs do
PostgreSQL-a dla OCamla. Pozwala osadzać instrukcje SQL bezpośrednio
w kodzie w OCamlu.

%prep
%setup -q -n pgocaml-%{version}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r tests/*.ml utils/pgocaml_prof.ml $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# META for findlib
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pgocaml
echo 'directory = "+pgocaml"' >> src/META
install src/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pgocaml

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc README* doc/*.txt src/*.mli
%dir %{_libdir}/ocaml/pgocaml
%{_libdir}/ocaml/pgocaml/*.cm[oixa]*
%{_libdir}/ocaml/pgocaml/*.a
%{_libdir}/ocaml/pgocaml/*.mli
%{_libdir}/ocaml/pgocaml/PGOCaml_config.ml
%{_libdir}/ocaml/pgocaml/pa_pgsql.ml
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/pgocaml
