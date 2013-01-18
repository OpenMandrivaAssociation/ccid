Summary:	A generic USB CCID (Chip/Smart Card Interface Devices) driver
Name:		ccid
Version:	1.4.9
Release:	1
# RSA_SecurID_getpasswd and Kobil_mIDentity_switch are GPLv2+
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://pcsclite.alioth.debian.org/
# ccid svn contains symlinks to files pcsc svn. To create a working
# source tarball from svn:
# mkdir -p ccid/Drivers
# cd ccid
# svn co svn://svn.debian.org/pcsclite/trunk/PCSC
# cd Drivers
# svn co svn://svn.debian.org/pcsclite/trunk/Drivers/ccid
Source0:	https://alioth.debian.org/download.php/1474/ccid-%{version}.tar.bz2
Source1:	https://alioth.debian.org/download.php/1475/ccid-%{version}.tar.bz2.asc
Patch0:		ccid-libtool_fixes.diff
BuildRequires:	flex
BuildRequires:	libpcsclite-devel >= 1.6.5
BuildRequires:	libusb-devel
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	libtool
# update-reader.conf is called in %%post
Requires(post): pcsc-lite
Requires(postun): pcsc-lite
Requires:	pcsc-lite

%description
This package provides a generic USB CCID (Chip/Smart Card Interface Devices)
driver.

%prep
%setup -q 
%patch0 -p1

%build
autoreconf -fis
%configure2_5x \
    --enable-twinserial \
    --enable-udev

%make

%install
%makeinstall_std

# serial driver is installed separately
%makeinstall_std -C src install_ccidtwin

# conf file should be placed inside reader.conf.d
mv -f %{buildroot}%{_sysconfdir}/reader.conf.d/libccidtwin %{buildroot}%{_sysconfdir}/reader.conf.d/GemPCTwin-serial.conf

# udev
install -m 0644 -D src/92_pcscd_ccid.rules %{buildroot}/lib/udev/rules.d/92_pcscd_ccid.rules

rm -rf %{buildroot}%{_docdir}/*
rm -f readers/Makefile*
cp -f src/towitoko/README README.towitoko

%post
%{_sbindir}/update-reader.conf

%postun
if [ "$1" = "0" ]; then
    %{_sbindir}/update-reader.conf
fi

%files
%doc AUTHORS INSTALL README COPYING
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
