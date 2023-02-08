# Define Sailfish as it is absent
%if !0%{?fedora}
%define sailfishos 1
%define keepstatic 1
%endif

%define _sover 3
%define _soname libvalhalla%{_sover}

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
BuildRequires: boost-program-options
BuildRequires: lz4-devel >= 1.7.3, zlib-devel >= 1.2.8
BuildRequires: pkgconfig(sqlite3)
BuildRequires: fdupes
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
%{description}

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

%package doc
Summary: Valhalla documentation

%description doc
%summary

%prep
%autosetup -p1 -n %{name}-%{version}/valhalla

%build
mkdir -p build-rpm
cd build-rpm

CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"

#Reason for ENABLE_DATA_TOOLS=OFF: sorry no one has packaged LuaJIT
#Reason for ENABLE_{SERVICES,TOOLS,BENCHMARKS,TESTS}=OFF: not linking to GEOS properly
%cmake .. \
       -DENABLE_TOOLS=OFF \
       -DENABLE_DATA_TOOLS=OFF \
       -DENABLE_SERVICES=OFF \
       -DENABLE_HTTP=ON \
       -DENABLE_PYTHON_BINDINGS=OFF \
       -DENABLE_CCACHE=OFF \
       -DENABLE_COVERAGE=OFF \
       -DENABLE_COMPILER_WARNINGS=OFF \
       -DENABLE_SANITIZERS=OFF \
       -DENABLE_ADDRESS_SANITIZER=OFF \
       -DENABLE_UNDEFINED_SANITIZER=OFF \
       -DENABLE_TESTS=OFF \
       -DENABLE_WERROR=OFF \
       -DENABLE_BENCHMARKS=OFF \
       -DENABLE_THREAD_SAFE_TILE_REF_COUNT=OFF

%cmake_build

cd ..

%install
%{__make} -C  build-rpm install DESTDIR=%{buildroot}

# remove thirdparty files
rm -rf %{buildroot}%{_includedir}/include/cpp-statsd-client
rm -rf %{buildroot}%{_includedir}/robin_hood.h
rm -rf %{buildroot}%{_libdir}/cmake/robin_hood
rm -rf %{buildroot}%{_datadir}/cpp-statsd-client

%fdupes %{buildroot}%{_prefix}

%pre

%post -n valhalla-lite -p /sbin/ldconfig

%postun -n valhalla-lite -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_libdir}/libvalhalla.so.%{_sover}*

%files doc
%{_datadir}/doc/libvalhalla0/
%{_datadir}/doc/valhalla/
%{_datadir}/doc/libvalhalla-dev/

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/valhalla/
%{_libdir}/libvalhalla.so
%{_libdir}/pkgconfig/libvalhalla.pc
%dir %{_includedir}/include
%if 0%{?sailfishos}
#%{_libdir}/libvalhalla.a
%endif

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/valhalla_*

%changelog

