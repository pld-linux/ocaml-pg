#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	PostgreSQL binding for OCaml
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla
Name:		ocaml-pg
Version:	4.3.0
Release:	1
License:	LGPL v2 + OCaml linking exception
Group:		Libraries
#Source0Download: https://github.com/darioteixeira/pgocaml/tags
Source0:	https://github.com/darioteixeira/pgocaml/archive/%{version}/pgocaml-%{version}.tar.gz
# Source0-md5:	1f97480892969d3ab371be4b95a0a5bb
Patch0:		%{name}-defaults.patch
URL:		https://github.com/darioteixeira/pgocaml
BuildRequires:	ocaml >= 1:4.07
BuildRequires:	ocaml-calendar-devel
BuildRequires:	ocaml-csv-devel
BuildRequires:	ocaml-dune >= 1.10
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-hex-devel
BuildRequires:	ocaml-ppx_deriving-devel >= 4.0
BuildRequires:	ocaml-ppx_optcomp-devel
BuildRequires:	ocaml-ppx_sexp_conv-devel
BuildRequires:	ocaml-ppxlib-devel >= 0.16.0
BuildRequires:	ocaml-re-devel
BuildRequires:	ocaml-rresult-devel
BuildRequires:	ocaml-sexplib-devel
%requires_eq	ocaml-runtime
Conflicts:	ocaml-pg < 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml.
It lets you embed SQL statements directly into OCaml code.

This package contains files needed to run bytecode executables using
PGOcaml library.

%description -l pl.UTF-8
PG'OCaml to prosty, bezpieczny pod względem typów interfejs do
PostgreSQL-a dla OCamla. Pozwala osadzać instrukcje SQL bezpośrednio
w kodzie w OCamlu.

Ten pakiet zawiera binaria potrzebne do uruchamiania programów
używających biblioteki PGOcaml.

%package devel
Summary:	PostgreSQL binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-calendar-devel
Requires:	ocaml-csv-devel
Requires:	ocaml-hex-devel
Requires:	ocaml-ppx_deriving-devel >= 4.0
Requires:	ocaml-ppx_sexp_conv-devel
Requires:	ocaml-re-devel
Requires:	ocaml-rresult-devel
Requires:	ocaml-sexplib-devel
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
PGOcaml library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki PGOcaml.

%package ppx
Summary:	PPX extension for PGOcaml
Summary(pl.UTF-8):	Rozszerzenie PPX do modułu PGOcaml
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ppx
PGOCaml provides an interface to PostgreSQL databases for OCaml
applications. This PPX syntax extension enables one to directly embed
SQL statements inside the OCaml code. The extension uses the
'describe' feature of PostgreSQL to obtain type information about the
database. This allows PGOCaml to check at compile-time if the program
is indeed consistent with the database structure.

%description ppx -l pl.UTF-8
PGOcaml udostępnia interfejs do baz danych PostgreSQL dla aplikacji w
OCamlu. To rozszerzenie składni PPX pozwala bezpośrednio osadzać
instrukcje SQL wewnątrz kodu w OCamlu. Rozszerzenie wykorzystuje
funkcję 'describe' PostgreSQL-a, aby uzyskać informacje o typach w
bazie. Pozwala to modułowi sprawdzić w czasie kompilacji, czy program
jest spójny ze strukturą bazy.

%package ppx-devel
Summary:	PPX extension for PGOcaml - development part
Summary(pl.UTF-8):	Rozszerzenie PPX do modułu PGOcaml - część programistyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-ppx = %{version}-%{release}
Requires:	ocaml-ppx_optcomp-devel
Requires:	ocaml-ppxlib-devel >= 0.16.0

%description ppx-devel
This package contains files needed to develop OCaml programs using
pgocaml_ppx library.

%description ppx-devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki pgocaml_ppx.

%prep
%setup -q -n pgocaml-%{version}
%patch0 -p1

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr tests/*.ml utils/pgocaml_prof.ml $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/pgocaml/PGOCaml{,_aux,_generic}.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/pgocaml_ppx/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/{pgocaml,pgocaml_ppx}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt LICENSE.txt README.md doc/*.txt
%dir %{_libdir}/ocaml/pgocaml
%{_libdir}/ocaml/pgocaml/META
%{_libdir}/ocaml/pgocaml/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/pgocaml/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/pgocaml/PGOCaml_config.ml
%{_libdir}/ocaml/pgocaml/*.cmi
%{_libdir}/ocaml/pgocaml/*.cmt
%{_libdir}/ocaml/pgocaml/*.cmti
%{_libdir}/ocaml/pgocaml/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/pgocaml/*.a
%{_libdir}/ocaml/pgocaml/*.cmx
%{_libdir}/ocaml/pgocaml/*.cmxa
%endif
%{_libdir}/ocaml/pgocaml/dune-package
%{_libdir}/ocaml/pgocaml/opam
%{_examplesdir}/%{name}-%{version}

%files ppx
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/pgocaml_ppx
%attr(755,root,root) %{_libdir}/ocaml/pgocaml_ppx/ppx.exe
%{_libdir}/ocaml/pgocaml_ppx/META
%{_libdir}/ocaml/pgocaml_ppx/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/pgocaml_ppx/*.cmxs
%endif

%files ppx-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/pgocaml_ppx/*.cmi
%{_libdir}/ocaml/pgocaml_ppx/*.cmt
%if %{with ocaml_opt}
%{_libdir}/ocaml/pgocaml_ppx/*.a
%{_libdir}/ocaml/pgocaml_ppx/*.cmx
%{_libdir}/ocaml/pgocaml_ppx/*.cmxa
%endif
%{_libdir}/ocaml/pgocaml_ppx/dune-package
%{_libdir}/ocaml/pgocaml_ppx/opam
