Summary:	A generic USB CCID (Chip/Smart Card Interface Devices) driver
Name:		ccid
Version:	1.4.34
Release:	1
# RSA_SecurID_getpasswd and Kobil_mIDentity_switch are GPLv2+
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://pcsclite.alioth.debian.org/
Source0:  https://ccid.apdu.fr/files/%{name}-%{version}.tar.bz2
Patch0:		ccid-libtool_fixes.diff

BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(libusb-1.0)
Requires:	pcsc-lite >= 1.8.23

%description
This package provides a generic USB CCID (Chip/Smart Card Interface Devices)
driver.

%prep
%setup -qn %{name}-%{version}
%autopatch -p1

%build
./bootstrap
%configure --enable-twinserial

%make_build

%install
%make_install

# serial driver is installed separately
%make_install -C src install_ccidtwin

# conf file should be placed inside reader.conf.d
mv -f %{buildroot}%{_sysconfdir}/reader.conf.d/libccidtwin %{buildroot}%{_sysconfdir}/reader.conf.d/GemPCTwin-serial.conf

# udev
install -m 0644 -D src/92_pcscd_ccid.rules %{buildroot}/lib/udev/rules.d/92_pcscd_ccid.rules

rm -rf %{buildroot}%{_docdir}/*
rm -f readers/Makefile*
cp -f src/towitoko/README README.towitoko
# wipe broken symlink
rm -f INSTALL

%files
%doc AUTHORS COPYING
%doc readers contrib/Kobil_mIDentity_switch/README_Kobil_mIDentity_switch.txt
%doc README.towitoko
%config(noreplace) %{_sysconfdir}/reader.conf.d/*.conf
%config /lib/udev/rules.d/92_pcscd_ccid.rules
%{_libdir}/pcsc/drivers/ifd-ccid.bundle
%{_libdir}/pcsc/drivers/serial
#%{_bindir}/RSA_SecurID_getpasswd
#%{_sbindir}/Kobil_mIDentity_switch
#%{_mandir}/man1/RSA_SecurID_getpasswd.1*
#%{_mandir}/man8/Kobil_mIDentity_switch.8*
