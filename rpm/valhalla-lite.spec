# Define Sailfish as it is absent
%if !0%{?fedora}
%define sailfishos 1
%endif

Summary: Open Source Routing Engine for OpenStreetMap
Name: valhalla-lite
Version: 3.4.0
Release: 1%{?dist}
License: MIT
Group: Development/Libraries
URL: https://github.com/valhalla/valhalla

Source: %{name}-%{version}.tar.gz
Patch0: 0001-drop-cmake-required-version-to-3.8.patch
Patch1: 0002-Set-boost-version-to-1.66.patch
Patch2: 0003-cpp-statsd-client-older-cmake.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++ libtool vim-enhanced
BuildRequires: cmake lua lua-devel
BuildRequires: jq, protobuf-devel, libcurl-devel >= 7.22.0
BuildRequires: boost-devel >= 1.51, boost-date-time >= 1.51, boost-filesystem >= 1.51
BuildRequires: boost-iostreams >= 1.51, boost-regex >= 1.51
BuildRequires: boost-system >= 1.51
BuildRequires: lz4-devel >= 1.7.3, zlib-devel >= 1.2.8
Requires: protobuf
Requires: boost-date-time >= 1.51, boost-filesystem >= 1.51
Requires: boost-iostreams >= 1.51, boost-regex >= 1.51
Requires: boost-system >= 1.51
Requires: lz4 >= 1.7.3, zlib >= 1.2.8
Conflicts: valhalla-devel

%description
Valhalla Libraries - Open Source Routing Engine for OpenStreetMap

PackageName: Valhalla Library
Categories:
  - Maps
  - Science
  - Library

%package devel
Summary: Valhalla development package
Group: Development/Libraries/Other
Requires: %{name} = %{version}

%description devel
%summary

PackageName: Valhalla Library Development
Categories:
  - Maps
  - Science
  - Library

%package tools
Summary: valhalla tools
Group: Libraries/Location
Requires: %{name} = %{version}
Conflicts: valhalla-tools

%description tools
Tools for valhalla

PackageName: Valhalla Tools
Type: console-application
Categories:
  - Maps
  - Science

%prep
%setup -q -n %{name}-%{version}/valhalla
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} clean || true
mkdir build-rpm || true
cd build-rpm

%if 0%{?sailfishos}

CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"
%cmake .. -DCMAKE_INSTALL_PREFIX:PATH=/usr \
       -DBUILD_SHARED_LIBS=OFF \
       -DENABLE_DATA_TOOLS=OFF -DENABLE_PYTHON_BINDINGS=OFF \
       -DENABLE_SERVICES=OFF \
       -DENABLE_TESTS=OFF -DENABLE_WERROR=OFF -DENABLE_SINGLE_FILES_WERROR=OFF

%else

%cmake .. -DCMAKE_INSTALL_PREFIX:PATH=/usr \
       -DBUILD_SHARED_LIBS=ON -DENABLE_DATA_TOOLS=OFF \
       -DENABLE_PYTHON_BINDINGS=OFF -DENABLE_SERVICES=OFF \
       -DENABLE_TESTS=OFF -DENABLE_WERROR=OFF -DENABLE_SINGLE_FILES_WERROR=OFF

%endif

%{__make} %{?_smp_mflags}
cd ..

%install
cd build-rpm
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
cd ..

# remove thirdparty files
rm -rf %{buildroot}%{_includedir}/include/cpp-statsd-client
rm -rf %{buildroot}%{_includedir}/robin_hood.h
rm -rf %{buildroot}%{_libdir}/cmake/robin_hood
rm -rf %{buildroot}%{_datadir}/cpp-statsd-client

%clean
%{__rm} -rf %{buildroot}

%pre

%post -n valhalla-lite -p /sbin/ldconfig

%postun -n valhalla-lite -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_docdir}/valhalla/*
%if !0%{?sailfishos}
%{_libdir}/libvalhalla.so*
%{_docdir}/libvalhalla0/*
%endif

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/valhalla
%{_libdir}/pkgconfig/libvalhalla.pc
%{_docdir}/libvalhalla-dev/*
%if 0%{?sailfishos}
%{_libdir}/libvalhalla.a
%endif

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/valhalla_*

%changelog

