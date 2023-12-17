%global build_ldflags %{build_ldflags} -Wl,--undefined-version

%define api 1
%define major 0
%define libname %mklibname planner %{api} %{major}
%define devname %mklibname -d planner

#gw planner 0.14.4 does not build with evo 2.31.6
%define build_evolution 0
%define title Planner
%define longtitle Project management tool
%define Summary Planner is a project management application for GNOME
%define debug_package %{nil}

Summary: 	%Summary
Name: 		planner
Version:	0.14.92
Release:	1
License: 	GPLv2+
Group: 		Office
Url:		https://live.gnome.org/Planner
Source0: 	https://download.gnome.org/sources/planner/0.14/planner-%{version}.tar.xz

BuildRequires:	meson
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libgda-5.0)
BuildRequires: pkgconfig(gail-3.0)
BuildRequires:	rarian
BuildRequires:	gnome-common
BuildRequires:	pkgconfig(python)
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:  desktop-file-utils
Requires:	rarian
Obsoletes:	mrproject
Provides:	mrproject = %{version}-%{release}


%description
Planner is a project management application for GNOME.

It was formely known as MrProject.

%package	python
Summary:	Python binding for Planner library
Group:		Development/GNOME and GTK+

%description	python
Python binding for Planner library

%package -n	%{libname}
Summary:	%{Summary}
Group:		System/Libraries

%description -n	%{libname}
A support library for accessing Planner data.
 
%package -n	%{devname}
Summary:	The files needed for Planner application development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the necessary include files
for developing applications that access Planner data.


%package	database
Summary:        Planner database support
Group:          Office
Requires:       %{name} = %{version}-%{release}
 
%description	database
Database support for Planner, this plugin can be used to store projects
in a PostgreSQL database.



%if %build_evolution
%package        evolution
Summary:        Planner evolution support
Group:          Office
Requires:       %{name} = %{version}-%{release}
Requires:	evolution
BuildRequires:	pkgconfig(evolution-data-server-1.2)
BuildRequires:	evolution-devel
BuildRequires:	mono-devel

%description    evolution
Evolution support for Planner, this plugin can be used with evolution.
%endif 

%prep
%setup -q

%build
%meson
%meson_build

%install
%meson_install

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc NEWS README examples/sample-1.planner
%{_sysconfdir}/gconf/schemas/planner.schemas
%{_bindir}/%{name}
%dir %{_libdir}/planner
%dir %{_libdir}/planner/plugins
#%{_libdir}/planner/libgantt-task.so
%{_libdir}/planner/file-modules
%{_libdir}/planner/plugins/libhtml-plugin.so
%{_libdir}/planner/plugins/libxmlplanner-plugin.so
%{_libdir}/planner/plugins/libmsp-plugin.so
%dir %{_libdir}/planner/storage-modules
%{_libdir}/planner/storage-modules/libstorage-mrproject-1.so
%{_datadir}/applications/*
%dir %{_datadir}/planner
%dir %{_datadir}/planner/glade
%{_datadir}/planner/glade/*-*.glade
%{_datadir}/planner/glade/eds.glade
%dir %{_datadir}/planner/ui
%{_datadir}/planner/ui/eds-plugin.ui
%{_datadir}/planner/ui/gantt-view.ui
%{_datadir}/planner/ui/resource-view.ui
%{_datadir}/planner/ui/time-table-view.ui
%{_datadir}/planner/ui/html-plugin.ui
%{_datadir}/planner/ui/xml-planner-plugin.ui
%{_datadir}/planner/ui/main-window.ui
%{_datadir}/planner/ui/msp-plugin.ui
%{_datadir}/planner/ui/task-view.ui
%{_datadir}/planner/dtd
%{_datadir}/planner/stylesheets
%dir %{_datadir}/planner/images/
%{_datadir}/planner/images/*
%{_datadir}/mime/packages/*
%{_iconsdir}/hicolor/48x48/mimetypes/*
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/planner.*

%files -n %{libname}
%{_libdir}/libplanner-%{api}.so.%{major}*

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/libplanner
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files python
%{py2_platsitedir}/*
%{_libdir}/planner/plugins/libpython-plugin.so

%files database
%doc docs/sql/README.sql
%{_libdir}/planner/storage-modules/libstorage-sql.so
%{_libdir}/planner/plugins/libsql-plugin.so
%{_datadir}/planner/glade/sql.glade
%{_datadir}/planner/ui/sql-plugin.ui
%{_datadir}/planner/sql

%if %build_evolution
%files evolution
%{_libdir}/evolution-data-server-1.2/extensions/*
%{_libdir}/evolution/*/plugins/*
%{_libdir}/planner/plugins/libeds-plugin.so
%endif

