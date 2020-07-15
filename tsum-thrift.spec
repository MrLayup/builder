%define build_timestamp %(date +"%s")

Name:           tsum-thrift
License:        Apache License v2.0
Group:          Development
Summary:        RPC and serialization framework
Version:        0.13.1
Release:        %{build_timestamp}
Provides:	thrift = 0.13.1-1
#Obsoletes:	thrift <= 0.13.1-1
URL:            http://thrift.apache.org
Packager:       Thrift Developers <dev@thrift.apache.org>
Source0:        thrift-%{version}.tar.gz

BuildRequires:  gcc >= 3.4.6, php-devel = 7.4.7
BuildRequires:  gcc-c++, byacc, bison, flex, php-composer-ca-bundle

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%description
Tsum fork from thrift for dev usage

%files
%defattr(-,root,root)
%{_bindir}/thrift

%package lib-cpp
Summary: Thrift C++ library
Group:   Libraries

%description lib-cpp
C++ libraries for Thrift.

%files lib-cpp
%defattr(-,root,root)
%{_libdir}/libthrift*.so.*
%{_libdir}/libthrift*.so

%package lib-cpp-devel
Summary:   Thrift C++ library development files
Group:     Libraries
Requires:  %{name} = %{version}-%{release}
Requires:  boost-devel
%if 0%{!?without_libevent:1}
Requires:  libevent-devel >= 1.2
%endif
%if 0%{!?without_zlib:1}
Requires:  zlib-devel
%endif

%description lib-cpp-devel
C++ static libraries and headers for Thrift.

%files lib-cpp-devel
%defattr(-,root,root)
%{_includedir}/thrift/
%{_libdir}/libthrift*.*a
%{_libdir}/pkgconfig/thrift*.pc

%package lib-php
Summary:	Thrift PHP library
Group:		Libraries
Provides:       thrift-lib-php = 0.13.1-1
#Obsoletes:      thrift-lib-php <= 0.13.1-1

%description lib-php
PHP libraries for Thrift.

%files lib-php
%defattr(-,root,root)
/usr/lib/php/*
/usr/lib64/php/modules/thrift_protocol.so

%prep
%setup -q -n thrift-%{version}

%build
[[ -e Makefile.in ]] || ./bootstrap.sh
%configure \
  PHP_PREFIX=${RPM_BUILD_ROOT}/usr/lib/php \
  %{?without_libevent: --without-libevent } \
  %{?without_zlib:     --without-zlib     } \
  --without-tests \
  --without-java \
  --without-python \
  --without-ruby \
  --without-csharp \
  --without-erlang \
  --without-haskell \

make %{?_smp_mflags}

%install
%makeinstall
ln -s libthrift-%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libthrift.so.0
ln -s libthriftnb-%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libthriftnb.so.0
ln -s libthriftz-%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libthriftz.so.0
mkdir -p ${RPM_BUILD_ROOT}/usr/lib64/php/modules
cp lib/php/src/ext/thrift_protocol/modules/thrift_protocol.so ${RPM_BUILD_ROOT}/usr/lib64/php/modules

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
umask 007
/sbin/ldconfig > /dev/null 2>&1
echo 'extension=thrift_protocol.so' > /etc/php.d/40-thrift_protocol.ini
chmod 644 /etc/php.d/40-thrift_protocol.ini

%postun
umask 007
/sbin/ldconfig > /dev/null 2>&1
