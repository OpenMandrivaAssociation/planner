%define lib_api 1
%define lib_major 0
%define lib_name %mklibname planner %{lib_api} %{lib_major}
%define develname %mklibname -d planner
%define build_gda 1
#gw planner 0.14.4 does not build with evo 2.31.6
%define build_evolution 0
%define title Planner
%define longtitle Project management tool
%define Summary Planner is a project management application for GNOME

Summary: 	%Summary
Name: 		planner
Version:	0.14.6
Release:	2
License: 	GPLv2+
Group: 		Office
Url:		http://live.gnome.org/Planner
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/planner/%{name}-%{version}.tar.xz
Patch0:		planner-0.14.6-glib-includes.patch
Patch1:		planner-0.14.6-format-strings.patch
Patch4:		planner-0.14.4-linkage.patch
Patch5:		planner-0.14.6-automake113.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libglade2.0-devel
BuildRequires:	libgsf-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libxslt-devel >= 1.1.23
%if %{build_gda}
BuildRequires:	gda2.0-devel > 3.0.0
%endif
BuildRequires:	rarian
Buildrequires:	python-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:  desktop-file-utils
BuildRequires:	gnome-common
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

%package -n	%{lib_name}
Summary:	%{Summary}
Group:		System/Libraries
Obsoletes:	%mklibname planner- 1 0

%description -n	%{lib_name}
A support library for accessing Planner data.
 
%package -n	%{develname}
Summary:	The files needed for Planner application development
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	lib%{name}-1-devel = %version
Provides:	%name-devel = %version
Obsoletes:	%mklibname -d planner- 1 0

%description -n	%{develname}
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
%patch0 -p1
%patch1 -p1 -b .format-strings
%patch4 -p0 -b .link

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure2_5x --enable-gtk-doc --enable-python --enable-python-plugin \
%if %build_evolution
--enable-eds --enable-eds-backend \
%endif
--disable-update-mimedb --disable-schemas-install \
	%if %{build_gda}
		--with-database
	%endif

# FIXME: pygtk-codegen-2.0 creates code, which breaks strict aliasing
sed -i 's/^CFLAGS =/& -fno-strict-aliasing/' python/Makefile.in

%make

%install
rm -fr %{buildroot}

%makeinstall_std

sed -i -e 's/^\(Icon=.*\).png$/\1/g' %{buildroot}%{_datadir}/applications/planner.desktop 

#duplicate comments to GenericName for KDE (Mdv bug #33406)
sed -i -e 's/^Comment\(.*\)$/GenericName\1\nComment\1/g' %{buildroot}%{_datadir}/applications/planner.desktop 

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="GNOME" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*


%find_lang %{name} --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

# remove unpackaged files
rm -rf %{buildroot}%{_libdir}/planner/views/*.la \
   %{buildroot}%{_libdir}/planner/plugins/*.la \
   %{buildroot}%{_libdir}/planner/file-modules/*.la \
   %{buildroot}%{_libdir}/planner/storage-modules/*.la \
   %{buildroot}%{_libdir}/planner/*.la \
   %{buildroot}%{_libdir}/evolution-data-server-1.2/extensions/*.la \
   %{buildroot}%{_libdir}/evolution/2.4/plugins/*.la \
   %{buildroot}%{_datadir}/doc/planner \
   %{buildroot}%{_datadir}/mime/{globs,XMLnamespaces,application,magic,aliases,subclasses}

%preun
%preun_uninstall_gconf_schemas planner

%clean
rm -fr %buildroot

%files -f %{name}.lang
%defattr(-,root,root)
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
%{_datadir}/pixmaps/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%{_datadir}/mime/packages/*
%{_datadir}/icons/hicolor/48x48/mimetypes/*
%{_mandir}/man1/planner.*

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libplanner
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files python
%defattr(-,root,root)
%{py_platsitedir}/*
%{_libdir}/planner/plugins/libpython-plugin.so

%if %{build_gda}
%files database
%defattr(-,root,root)
%doc docs/sql/README.sql
%{_libdir}/planner/storage-modules/libstorage-sql.so
%{_libdir}/planner/plugins/libsql-plugin.so
%{_datadir}/planner/glade/sql.glade
%{_datadir}/planner/ui/sql-plugin.ui
%{_datadir}/planner/sql
%endif

%if %build_evolution
%files evolution
%defattr(-,root,root)
%{_libdir}/evolution-data-server-1.2/extensions/*
%{_libdir}/evolution/*/plugins/*
%{_libdir}/planner/plugins/libeds-plugin.so
%endif
