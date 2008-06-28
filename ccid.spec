Summary:	A generic USB CCID (Chip/Smart Card Interface Devices) driver
Name:		ccid
Version:	1.3.8
Release:	%mkrel 2
# RSA_SecurID_getpasswd and Kobil_mIDentity_switch are GPLv2+
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://pcsclite.alioth.debian.org/
Source0:	https://alioth.debian.org/download.php/1474/ccid-%{version}.tar.bz2
Source1:	https://alioth.debian.org/download.php/1475/ccid-%{version}.tar.bz2.asc
Patch0:		ccid-libtool_fixes.diff
BuildRequires:	flex
BuildRequires:	libpcsclite-devel >= 1.3.3
BuildRequires:	libusb-devel
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	libtool
# update-reader.conf is called in %%post
Requires(post): pcsc-lite
Requires(postun): pcsc-lite
Requires:	pcsc-lite
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package provides a generic USB CCID (Chip/Smart Card Interface Devices)
driver.

%prep

%setup -q
%patch0 -p0

%build
autoreconf -fis

%configure2_5x \
    --enable-twinserial \
    --enable-udev

%make

%install
rm -rf %{buildroot}

%makeinstall_std

# serial driver is installed separately
%makeinstall_std -C src install_ccidtwin

# conf file should be placed inside reader.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/reader.conf.d
mv -f %{buildroot}%{_sysconfdir}/reader.conf %{buildroot}%{_sysconfdir}/reader.conf.d/GemPCTwin-serial.conf

# udev
install -m 0644 -D src/pcscd_ccid.rules %{buildroot}%{_sysconfdir}/udev/rules.d/70-pcscd_ccid.rules

rm -rf %{buildroot}%{_docdir}/*
cp -f src/towitoko/README README.towitoko

%post
%{_sbindir}/update-reader.conf

%postun
if [ "$1" = "0" ]; then
    %{_sbindir}/update-reader.conf
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL README COPYING
%doc readers contrib/Kobil_mIDentity_switch/README_Kobil_mIDentity_switch.txt
%doc README.towitoko
%config(noreplace) %{_sysconfdir}/reader.conf.d/*.conf
%config(noreplace) %{_sysconfdir}/udev/rules.d/70-pcscd_ccid.rules
%{_libdir}/pcsc/drivers/ifd-ccid.bundle
%{_libdir}/pcsc/drivers/serial
%{_bindir}/RSA_SecurID_getpasswd
%{_sbindir}/Kobil_mIDentity_switch
%{_mandir}/man1/RSA_SecurID_getpasswd.1*
%{_mandir}/man8/Kobil_mIDentity_switch.8*
