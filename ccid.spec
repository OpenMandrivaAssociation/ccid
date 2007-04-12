Summary: A generic USB CCID (Chip/Smart Card Interface Devices) driver
Name: ccid
Version: 1.2.1
Release: %mkrel 1
License: LGPL
Group: System/Libraries
Source0: https://alioth.debian.org/download.php/1474/ccid-%{version}.tar.gz
Source1: https://alioth.debian.org/download.php/1475/ccid-%{version}.tar.gz.asc
URL: http://pcsclite.alioth.debian.org/
BuildRequires: pkgconfig >= 0.9.0
BuildRequires: libpcsclite-devel >= 1.3.3
BuildRequires: libusb-devel
# update-reader.conf is called in %%post
Requires(post,postun): pcsc-lite
Requires: pcsc-lite
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a generic USB CCID (Chip/Smart Card Interface Devices)
driver.

%prep
%setup -q

%build
%configure --enable-twinserial --enable-udev

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
# serial driver is installed separately
%makeinstall_std -C src install_ccidtwin

# conf file should be placed inside reader.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/reader.conf.d
mv -f %{buildroot}%{_sysconfdir}/reader.conf %{buildroot}%{_sysconfdir}/reader.conf.d/GemPCTwin-serial.conf

# udev
install -m 0644 -D src/pcscd_ccid.rules %{buildroot}%{_sysconfdir}/udev/rules.d/70-pcscd_ccid.rules

%post
%{_sbindir}/update-reader.conf

%postun
if [ "$1" = "0" ]; then
	%{_sbindir}/update-reader.conf
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL README COPYING
%doc readers
%config(noreplace) %{_sysconfdir}/reader.conf.d/*.conf
%config(noreplace) %{_sysconfdir}/udev/rules.d/70-pcscd_ccid.rules
%{_libdir}/pcsc/drivers/ifd-ccid.bundle
%{_libdir}/pcsc/drivers/serial


