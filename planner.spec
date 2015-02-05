%define api 1
%define major 0
%define libname %mklibname planner %{api} %{major}
%define devname %mklibname -d planner

%define build_gda 0
#gw planner 0.14.4 does not build with evo 2.31.6
%define build_evolution 0
%define title Planner
%define longtitle Project management tool
%define Summary Planner is a project management application for GNOME
%define debug_package %{nil}

%define git 20141226
%define rel 1

%if %{git}
%define srcname %{name}-%{version}-%{git}.tar.xz
%define release 10.%{git}.%{rel}
%else
%define srcname %{name}-%{version}.tar.xz
%define release %{rel}
%endif

Summary: 	%Summary
Name: 		planner
Version:	0.14.6
Release:	%{release}
License: 	GPLv2+
Group: 		Office
Url:		http://live.gnome.org/Planner
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/planner/%{srcname}
Patch1:		planner-0.14.6-format-strings.patch
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libgnomecanvas-2.0)
BuildRequires:  pkgconfig(gconf-2.0)

BuildRequires:	pkgconfig(libxslt)
%if %{build_gda}
BuildRequires:	pkgconfig(libgda-3.0)
%endif
BuildRequires:	rarian
BuildRequires:	gnome-common
BuildRequires:	pkgconfig(python2)
BuildRequires:	pygtk2.0-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:  desktop-file-utils
Requires:	rarian
Obsoletes:	mrproject
Provides:	mrproject = %{version}-%{release}
Requires(post): desktop-file-utils shared-mime-info scrollkeeper
Requires(postun): desktop-file-utils shared-mime-info scrollkeeper

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

%if %{build_gda}

%package	database
Summary:        Planner database support
Group:          Office
Requires:       %{name} = %{version}-%{release}
 
%description	database
Database support for Planner, this plugin can be used to store projects
in a PostgreSQL database.

%endif

%if %build_evolution
%package        evolution
Summary:        Planner evolution support
Group:          Office
Requires:       %{name} = %{version}-%{release}
Requires:	evolution
BuildRequires:	evolution-data-server-devel
BuildRequires:	evolution-devel
BuildRequires:	mono-devel

%description    evolution
Evolution support for Planner, this plugin can be used with evolution.
%endif 

%prep
%setup -q
%patch1 -p1 -b .format-strings
touch xmldocs.make

%build
NOCONFIGURE=yes gnome-autogen.sh
export CFLAGS=-Wno-error
%configure --enable-gtk-doc --enable-python --enable-python-plugin \
%if %build_evolution
	--enable-eds \
	--enable-eds-backend \
%endif
	--disable-update-mimedb \
	--disable-schemas-install \
%if %{build_gda}
	--with-database \
%endif
        PYTHON=%__python2

# FIXME: pygtk-codegen-2.0 creates code, which breaks strict aliasing
sed -i 's/^CFLAGS =/& -fno-strict-aliasing/' python/Makefile.in

%make

%install
%makeinstall_std

desktop-file-install --vendor="" \
	--add-category="GTK" \
	--add-category="GNOME" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%find_lang %{name} --with-gnome

# remove unpackaged files
#rm -rf %{buildroot}%{_libdir}/planner/views/*.la \
#   %{buildroot}%{_libdir}/planner/plugins/*.la \
#   %{buildroot}%{_libdir}/planner/file-modules/*.la \
#   %{buildroot}%{_libdir}/planner/storage-modules/*.la \
#   %{buildroot}%{_libdir}/planner/*.la \
#   %{buildroot}%{_libdir}/evolution-data-server-1.2/extensions/*.la \
#   %{buildroot}%{_libdir}/evolution/2.4/plugins/*.la \
#   %{buildroot}%{_datadir}/doc/planner \
#   %{buildroot}%{_datadir}/mime/{globs,XMLnamespaces,application,magic,aliases,subclasses}

%if !%build_gda
rm -rf %{buildroot}%{_datadir}/planner/sql %{buildroot}%{_datadir}/planner/glade/sql.glade %{buildroot}%{_datadir}/planner/ui/sql-plugin.ui
%endif

%preun
%preun_uninstall_gconf_schemas planner

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

%if %{build_gda}
%files database
%doc docs/sql/README.sql
%{_libdir}/planner/storage-modules/libstorage-sql.so
%{_libdir}/planner/plugins/libsql-plugin.so
%{_datadir}/planner/glade/sql.glade
%{_datadir}/planner/ui/sql-plugin.ui
%{_datadir}/planner/sql
%endif

%if %build_evolution
%files evolution
%{_libdir}/evolution-data-server-1.2/extensions/*
%{_libdir}/evolution/*/plugins/*
%{_libdir}/planner/plugins/libeds-plugin.so
%endif

