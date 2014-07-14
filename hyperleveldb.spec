%global commit 9198d6fa2216125b656091dd998e0162deec2595
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%define upname HyperLevelDB

Name:		hyperleveldb
Version:	1.0.0
Release:	4%{?dist}
Summary:	A fork of LevelDB intended to meet the needs of HyperDex while remaining compatible with LevelDB.

Group:		Development/Libraries
License:	https://github.com/rescrv/%{upname}/blob/master/LICENSE
URL:		https://github.com/rescrv/%{upname}
Source0:        https://github.com/rescrv/%{upname}/archive/%{commit}/%{upname}-%{commit}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc autoconf automake libtool
Obsoletes:	leveldb leveldb-devel


%description
A fork of LevelDB intended to meet the needs of HyperDex while remaining compatible with LevelDB.

%package -n %{name}-devel
Summary:        A fork of LevelDB intended to meet the needs of HyperDex while remaining compatible with LevelDB.
Group:          Development/Libraries
License:	https://github.com/rescrv/%{upname}/blob/master/LICENSE
BuildRequires:	gcc autoconf automake libtool
%description -n %{name}-devel
A fork of LevelDB intended to meet the needs of HyperDex while remaining compatible with LevelDB.


%prep
%setup -qn %{upname}-%{commit} 


%build
autoreconf -i

%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
ln -s %{_includedir}/%{name} 			%{buildroot}%{_includedir}/leveldb
ln -s %{_libdir}/libhyperleveldb.a 		%{buildroot}%{_libdir}/libleveldb.a
ln -s %{_libdir}/libhyperleveldb.la 		%{buildroot}%{_libdir}/libleveldb.la
ln -s %{_libdir}/libhyperleveldb.so 		%{buildroot}%{_libdir}/libleveldb.so
ln -s %{_libdir}/libhyperleveldb.so.0 		%{buildroot}%{_libdir}/libleveldb.so.0
ln -s %{_libdir}/libhyperleveldb.so.0.0.0 	%{buildroot}%{_libdir}/libleveldb.so.0.0.0
ln -s %{_libdir}/pkgconfig/libhyperleveldb.pc  	%{buildroot}%{_libdir}/pkgconfig/libleveldb.pc

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc
%{_libdir}/libhyperleveldb.so.0
%{_libdir}/libhyperleveldb.so.0.0.0
%{_libdir}/libleveldb.so.0
%{_libdir}/libleveldb.so.0.0.0
%{_libdir}/*.a
%{_libdir}/*.la

%files -n %{name}-devel
%defattr(-,root,root,-)
%doc
%{_includedir}/%{name}/*
%{_includedir}/leveldb
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%changelog
* Mon Jul 14 2014 Norbert Varzariu <root@loomsen.org> - 1.0.0-4
- split package into self and devel

* Thu Jul 10 2014 Norbert Varzariu <root@loomsen.org> - 1.0.0-3
- create symlinks for leveldb

* Thu Jul 10 2014 Norbert Varzariu <root@loomsen.org> - 1.0.0-2
- initial build


