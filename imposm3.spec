%global commit 0807c33eaaa5146d3f8088bf23e058524055c4fd
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		imposm3	
Version:	3.0.0.%{shortcommit}
Release:	1%{?dist}
Summary:	Imposm is an importer for OpenStreetMap data. It reads PBF files and imports the data into PostgreSQL/PostGIS. 

Group:		Development/Libraries
License:	Apache Software License 2.0
URL:		http://imposm.org/
#Source0:        https://github.com/omniscale/imposm3/archive/%{commit}/imposm3-%{commit}.tar.gz
Source0:	.
Source1:	%{name}.psql-setup.sh
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	hyperleveldb golang-pkg-bin-linux-amd64 golang-src golang golang-pkg-linux-amd64 geos-devel protobuf-devel protobuf-compiler sqlite-devel git mercurial
Requires:	postgresql-server postgresql geos sqlite hyperleveldb postgis proj-epsg

%description
Imposm is an importer for OpenStreetMap data. It reads PBF files and imports the data into PostgreSQL/PostGIS. It can also update the DB from diff files.

It is designed to create databases that are optimized for rendering (i.e. generating tiles or for WMS services).

Imposm 3 is written in Go and it is a complete rewrite of the previous Python implementation. Configurations/mappings and cache files are not compatible with Imposm 2, but they share a similar architecture.

It is released as open source under the Apache License 2.0.

The development of Imposm 3 was sponsored by Omniscale and development will continue as resources permit. Please get in touch if you need commercial support or if you need specific features.

%prep

%build

%install
mkdir -p %{name}
cd %{name}
export GOPATH=`pwd`
git clone https://github.com/omniscale/imposm3 src/imposm3
pushd src/imposm3
git checkout %{commit}
popd
go get imposm3
go install %{name}
mkdir -p %{buildroot}/usr/bin
install -m 0755 bin/%{name} %{buildroot}/usr/bin/%{name}
mkdir -p %{buildroot}/usr/share/%{name}
install -m 0644 %{SOURCE1} %{buildroot}%{_datarootdir}/%{name}/psql-setup.sh
install -m 0644 src/imposm3/example-mapping.json %{buildroot}%{_datarootdir}/%{name}/example-mapping.json

%clean
rm -rf %{buildroot}

%pre
if [ $1 -eq 1 ]; then
	if ! getent passwd osm; then
		useradd -rm -d /var/cache/%{name} -s /sbin/nologin -U osm
		chown osm.osm /var/cache/%{name}
	fi
fi

%postun
if ! [ $1 -eq 1 ];then
	userdel -r osm
fi

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/%{name}
%{_datarootdir}/%{name}/*

%changelog
* Mon Jul 14 2014 Norbert Varzariu <root@loomsen.org> - 3.0.0.0807c33-1
- initial build

