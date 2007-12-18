%define		ocaml_ver	1:3.10.0
Summary:	PostgreSQL binding for OCaml
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla
Name:		ocaml-pg
Version:	1.0
Release:	3
License:	LGPL + OCaml linking exception
Group:		Libraries
URL:		http://merjis.com/developers/pgocaml/
Source0:	http://merjis.com/_file/pgocaml-%{version}.tar.gz
# Source0-md5:	4f12ab37e75cc863560600e458e202d5
Patch0:		%{name}-notest.patch
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-calendar-devel
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-csv-devel
BuildRequires:	ocaml-extlib-devel
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-pcre-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml.
It lets you embed SQL statements directly into OCaml code.

%package devel
Summary:	PostgreSQL binding for OCaml
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla
Group:		Development/Libraries
Requires:	ocaml-calendar-devel
Requires:	ocaml-csv-devel
Requires:	ocaml-extlib-devel
Requires:	ocaml-pcre-devel
%requires_eq	ocaml

%description devel
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml.
It lets you embed SQL statements directly into OCaml code.

%prep
%setup -q -n pgocaml-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{pgocaml,stublibs}

install *.cm[ixa]* *.a pa_pgsql.cmo $RPM_BUILD_ROOT%{_libdir}/ocaml/pgocaml

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r test* pgocaml_prof.ml $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# META for findlib
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pgocaml
echo 'directory = "+pgocaml"' >> META
install META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pgocaml

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc README* BUGS.txt CONTRIBUTORS.txt HOW_IT_WORKS.txt *.mli
%dir %{_libdir}/ocaml/pgocaml
%{_libdir}/ocaml/pgocaml/*.cm[oixa]*
%{_libdir}/ocaml/pgocaml/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/pgocaml
