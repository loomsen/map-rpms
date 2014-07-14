%define name MapProxy
%define version 1.7.1
%define unmangled_version 1.7.1
%define unmangled_version 1.7.1
%define release 1%{?dist}cm
%define _unitdir /usr/lib/systemd/system
%define lowname mapproxy

Summary: An accelerating proxy for web map services
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
Source1: mapproxy.upstream.uwsgi.ini
Source2: mapproxy.upstream.README
Source3: mapproxy.upstream.examples.tar.bz2
Source4: mapproxy.upstream.nginx.conf
Patch0:  mapproxy.upstream.smooth-transition-in-demo.patch
License: Apache Software License 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Oliver Tonnhofer <olt@omniscale.de>
Url: http://mapproxy.org
Requires: python-lxml PyYAML libyaml proj proj-epsg geos gdal python-shapely  python-pillow 
BuildRequires: proj-devel geos-devel gdal-devel python-devel zlib-devel libjpeg-turbo-devel freetype-devel python-setuptools python-pillow-devel

%description
MapProxy is an open source proxy for geospatial data. It caches, accelerates and transforms data from existing map services and serves any desktop or web GIS client.

MapProxy is a tile cache, but also offers many new and innovative features like full support for WMS clients.

MapProxy is actively developed and supported by `Omniscale <http://omniscale.com>`_, it is released under the Apache Software License 2.0, runs on Unix/Linux and Windows and is easy to install and to configure.

Go to http://mapproxy.org/ for more information.

The documentation is available at: http://mapproxy.org/docs/latest/

Changes:
See https://raw.github.com/mapproxy/mapproxy/master/CHANGES.txt


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}
%patch0 -p1

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/var/log/mapproxy
mkdir -p $RPM_BUILD_ROOT/var/cache/mapproxy
mkdir -p $RPM_BUILD_ROOT%{_datarootdir}/%{name}
install -m 0644 %{SOURCE1} %{buildroot}%{_datarootdir}/%{name}/uwsgi.mapproxy.ini
install -m 0644 %{SOURCE2} %{buildroot}%{_datarootdir}/%{name}/README
tar -xjf %{SOURCE3} -C $RPM_BUILD_ROOT%{_datarootdir}/%{name}
cp %{SOURCE4} $RPM_BUILD_ROOT%{_datarootdir}/%{name}/nginx.mapproxy.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ $1 -eq 1 ]; then
        if ! getent passwd %{lowname}; then
                useradd -r -d /var/cache/%{lowname} -s /sbin/nologin -U %{lowname}
        fi
fi

%postun
if ! [ $1 -eq 1 ]; then
        userdel %{lowname}
fi

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc
%attr(0755, mapproxy, mapproxy) %{_var}/log/mapproxy/
%attr(0755, mapproxy, mapproxy) %{_var}/cache/mapproxy/
%{_datarootdir}/%{name}/*

%changelog
* Mon Jul 14 2014 Norbert Varzariu <root@loomsen.org> - 1.7.1-1cm
- initial build


