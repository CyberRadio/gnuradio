Name: RPM_PKG_NAME
Version: RPM_PKG_VERSION
Release: RPM_PKG_OSRPM_PKG_OS_VER
Summary: Software defined radio framework
Group: Applications/Engineering
License: GPLv3
URL: http://www.gnuradio.org
Source: RPM_PKG_NAME-RPM_PKG_VERSION.tar.gz

Requires(pre):	shadow-utils
BuildRequires:	cmake, fftw-devel, cppunit-devel, wxPython-devel, xmlto
BuildRequires:	graphviz, boost-devel, python-devel, swig, doxygen
BuildRequires:	libusbx-devel, alsa-lib-devel, SDL-devel, guile-devel
BuildRequires:	portaudio-devel, libtool, gsm-devel
BuildRequires:	gsl-devel, numpy, PyQt4-devel, python-cheetah
BuildRequires:	xdg-utils, python-lxml, pygtk2-devel, orc-devel
BuildRequires:	desktop-file-utils, make, python-six
BuildRequires:  qwt-devel, python-mako, gcc, gcc-c++
BuildRequires:  zeromq-devel
BuildRequires:  uhd-devel
BuildRequires:  python2-sphinx
Requires:	numpy, wxPython, scipy, portaudio, python-lxml
Requires:	pygtk2, python-cheetah, PyQt4
Requires:	PyQwt, PyOpenGL, uhd

%description
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

%package devel
Summary:	GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	cmake, boost169-devel

%description devel
GNU Radio Headers

%package doc
Summary:	GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
GNU Radio Documentation

%package examples
Summary:	GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description examples
GNU Radio examples

%prep
%setup -q -n %{name}-%{version}

#force regeneration of cached moc output files
find . -name "*_moc.cc" -exec rm {} \;

%build
if [ -d ./build ]; then rm -rf build; fi
mkdir build
cd build
cmake -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
      -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
      -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \
      -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
      -DCMAKE_INSTALL_PREFIX:PATH=/usr \
      -DINCLUDE_INSTALL_DIR:PATH=/usr/include \
      -DLIB_INSTALL_DIR:PATH=/usr/lib64 \
      -DSYSCONF_INSTALL_DIR:PATH=/etc \
      -DSHARE_INSTALL_PREFIX:PATH=/usr/share \
      -DLIB_SUFFIX=64 \
..
make -j 4


%install
# remove atsc example (bytecompilation problem)
# the examples shouldn't be probably bytecompiled,
# but selective bytecompilation would take a lot of time,
# thus letting it as is
cd build
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_datadir}/%{name}/examples/atsc

# install desktop file, icons, and MIME configuration to right locations
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/%{name}/grc/freedesktop/gnuradio-grc.desktop
mkdir -p %{buildroot}%{_datadir}/mime/packages
mv %{buildroot}%{_datadir}/%{name}/grc/freedesktop/gnuradio-grc.xml %{buildroot}%{_datadir}/mime/packages
for x in 16 24 32 48 64 128 256
do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${x}x${x}/apps
  mv %{buildroot}%{_datadir}/%{name}/grc/freedesktop/grc-icon-${x}.png %{buildroot}%{_datadir}/icons/hicolor/${x}x${x}/apps/gnuradio-grc.png
done
rm -f %{buildroot}%{_datadir}/%{name}/grc/freedesktop/*
rmdir %{buildroot}%{_datadir}/%{name}/grc/freedesktop

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    /bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%license COPYING
%{python_sitearch}/*
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libexecdir}/*
%{_datadir}/gnuradio
%{_datadir}/applications/gnuradio-grc.desktop
%{_datadir}/mime/packages/gnuradio-grc.xml
%{_datadir}/icons/hicolor/*/apps/gnuradio-grc.png
%config(noreplace) %{_sysconfdir}/gnuradio
%exclude %{_datadir}/gnuradio/examples
%exclude %{_docdir}/%{name}/html
%exclude %{_docdir}/%{name}/xml
%doc %{_docdir}/%{name}

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/gnuradio

%files doc
%doc %{_docdir}/%{name}-%{version}/html
%doc %{_docdir}/%{name}-%{version}/xml

%files examples
%{_datadir}/gnuradio/examples
