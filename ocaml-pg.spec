%define		ocaml_ver	1:3.10.0
Summary:	PostgreSQL binding for OCaml
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla
Name:		ocaml-pg
Version:	1.0
Release:	0.1
License:	LGPL + OCaml linking exception
Group:		Libraries
URL:		http://merjis.com/developers/pgocaml/
Source0:	http://merjis.com/_file/pgocaml-%{version}.tar.gz
# Source0-md5:	4f12ab37e75cc863560600e458e202d5
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-calendar
BuildRequires:	ocaml-csv
BuildRequires:	ocaml-extlib
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-pcre
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml.
It lets you embed SQL statements directly into OCaml code.

%package devel
Summary:	PostgreSQL binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml.
It lets you embed SQL statements directly into OCaml code.

%prep
%setup -q -n pgocaml-%{version}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{postgres,stublibs}

install *.cm[ixa]* *.a $RPM_BUILD_ROOT%{_libdir}/ocaml/postgres
install dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r tests/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# META for findlib
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/postgres
echo 'directory = "+postgres"' >> META
install META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/postgres

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dll*.so

%files devel
%defattr(644,root,root,755)
%doc README *.mli
%dir %{_libdir}/ocaml/postgres
%{_libdir}/ocaml/postgres/*.cm[ixa]*
%{_libdir}/ocaml/postgres/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/postgres
