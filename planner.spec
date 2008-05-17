%define lib_major 0
%define lib_name %mklibname planner-1_ %{lib_major}
%define build_gda 1
%define title Planner
%define longtitle Project management tool
%define Summary Planner is a project management application for GNOME

Summary: 	%Summary
Name: 		planner
Version:	0.14.3
Release:	%mkrel 1
License: 	GPL
Group: 		Office
Url:		http://live.gnome.org/Planner

Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/planner/%{name}-%{version}.tar.bz2

Patch1:		planner-0.14.2-evolution.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libglade2.0-devel
BuildRequires:	libgsf-devel
BuildRequires:	libgnomeprintui-devel >= 2.2
BuildRequires:	libgnomeui2-devel
BuildRequires:	libxslt-devel
BuildRequires:	perl-XML-Parser
%if %{build_gda}
BuildRequires:	gda2.0-devel > 3.0.0
%endif
BuildRequires:	rarian
Buildrequires:	python-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	gtk-doc
BuildRequires:	evolution-devel
BuildRequires:	intltool
BuildRequires:	evolution-data-server-devel
BuildRequires:	mono-devel
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

%package -n	%{lib_name}
Summary:	%{Summary}
Group:		System/Libraries

%description -n	%{lib_name}
A support library for accessing Planner data.
 
%package -n	%{lib_name}-devel
Summary:	The files needed for Planner application development
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	lib%{name}-1-devel

%description -n	%{lib_name}-devel
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

%package        evolution
Summary:        Planner evolution support
Group:          Office
Requires:       %{name} = %{version}-%{release}

%description    evolution
Evolution support for Planner, this plugin can be used with evolution.
 

%prep
%setup -q
%patch1 -p1 -b .evolution

#fix build
intltoolize --force
aclocal
automake -f -i
autoconf

%build

%configure2_5x --enable-gtk-doc --enable-python --enable-python-plugin --enable-eds --enable-eds-backend --disable-update-mimedb \
	%if %{build_gda}
		--enable-database=yes
	%endif

# FIXME: pygtk-codegen-2.0 creates code, which breaks strict aliasing
sed -i 's/^CFLAGS =/& -fno-strict-aliasing/' python/Makefile.in

make

%install
rm -fr $RPM_BUILD_ROOT

%makeinstall_std

sed -i -e 's/^\(Icon=.*\).png$/\1/g' $RPM_BUILD_ROOT%{_datadir}/applications/planner.desktop 

#duplicate comments to GenericName for KDE (Mdv bug #33406)
sed -i -e 's/^Comment\(.*\)$/GenericName\1\nComment\1/g' $RPM_BUILD_ROOT%{_datadir}/applications/planner.desktop 

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="GNOME" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%find_lang %{name} --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/planner/views/*.la \
   $RPM_BUILD_ROOT%{_libdir}/planner/plugins/*.la \
   $RPM_BUILD_ROOT%{_libdir}/planner/file-modules/*.la \
   $RPM_BUILD_ROOT%{_libdir}/planner/storage-modules/*.la \
   $RPM_BUILD_ROOT%{_libdir}/planner/*.la \
   $RPM_BUILD_ROOT%{_libdir}/evolution-data-server-1.2/extensions/*.la \
   $RPM_BUILD_ROOT%{_libdir}/evolution/2.4/plugins/*.la \
   $RPM_BUILD_ROOT%{_datadir}/doc/planner \
   $RPM_BUILD_ROOT%{_datadir}/mime/{globs,XMLnamespaces,application,magic,aliases,subclasses}

%post
%update_scrollkeeper
%update_menus
%{update_desktop_database}
%update_mime_database
%post_install_gconf_schemas planner
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas planner

%postun
%clean_scrollkeeper
%{clean_desktop_database}
%clean_mime_database
%clean_icon_cache hicolor
%clean_menus


%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -fr %buildroot

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog README examples/sample-1.planner
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

%files -n %{lib_name}-devel
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

%files evolution
%defattr(-,root,root)
%{_libdir}/evolution-data-server-1.2/extensions/*
%{_libdir}/evolution/*/plugins/*
%{_libdir}/planner/plugins/libeds-plugin.so


