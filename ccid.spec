Summary:	A generic USB CCID (Chip/Smart Card Interface Devices) driver
Name:		ccid
Version:	1.4.31
Release:	3
# RSA_SecurID_getpasswd and Kobil_mIDentity_switch are GPLv2+
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://pcsclite.alioth.debian.org/
# ccid svn contains symlinks to files pcsc svn. To create a working
# source tarball from svn:
# mkdir -p ccid/Drivers
# cd ccid
# svn co svn://svn.debian.org/pcsclite/trunk/PCSC
# cd Drivers
# svn co svn://svn.debian.org/pcsclite/trunk/Drivers/ccid
#Source0:	https://alioth.debian.org/download.php/3897/%{name}-%{version}.tar.bz2
#New source:
Source0:    https://github.com/LudovicRousseau/CCID/archive/%{name}-%{verson}/CCID-%{name}-%{verson}.tar.gz
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
%autosetup -p1 CCID-%{name}-%{verson}

%build
autoreconf -fis
%configure \
    --enable-twinserial \
    --enable-udev

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
%doc AUTHORS README COPYING
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
