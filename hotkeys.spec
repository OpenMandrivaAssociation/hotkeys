Summary:	A program to use the special keys on internet/multimedia keyboards
Name:		hotkeys
Version:	0.5.7.1
Release:	%mkrel 17
License:	GPL
Group:		System/Kernel and hardware
URL:		http://alioth.debian.org/projects/%{name}/
Source0:	%{url}%{name}_%{version}.tar.bz2
Source1:	vaio.def.bz2
Source2:	FCSAmilo.def.bz2
Source3:	samsungx30.def.bz2
Source4:	precision.def.bz2
Source5:	dellinspiron.def.bz2
Source6:	samsungx10.def.bz2
Source10:	%{name}.sysconfig
Source11:	%{name}.xinit
Patch1:		hotkeys-0.5.7.1_mutefix.patch
Patch2:		hotkeys-0.5.7.1-db4.patch
Patch3:		hotkeys-0.5.7.1-gcc43.diff
BuildRequires:	db4-devel >= 4.2.0
BuildRequires:	libxml2-devel >= 2.2.8
BuildRequires:	libxosd-devel
BuildRequires:	gtk2-devel
BuildRequires:	gettext-devel
BuildRequires:	libxkbfile-devel
BuildRequires:	libxmu-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The HotKeys daemon listens for the "special" hotkeys that you won't
normally use on your Internet/Multimedia keyboards. The buttons perform
their intended behaviors, such as volume up and down, mute the speaker,
or launch applications. It has On-screen display (OSD) to show the
volume, program that's being started, etc. It features an XML-based
keycode configuration file format, which makes it possible to define the
hotkeys to launch any programs you want.

%prep

%setup -q
%patch1 -p0
%patch2 -p1
%patch3 -p0

%build
rm -f configure
libtoolize --copy --force
aclocal
autoconf
%configure --with-xosd
make CC="gcc -I%{_includedir}/libxml2 -I%{_includedir}/libxml2/libxml"
cat > README.mdk <<EOF
Adding a new keyboard
----------------------
If you have a keyboard not supported by this package, you can create 
your own file, by using xev, and writing the xml config files based 
on the examples provided.

Then, you can send them to the author, Anthony Wong <ypwong@ypwong.org>, 
in order to have them included in the tarball. I will also take 
contribution, send them to <misc@mandriva.org>, or fill a bugreport
on qa.mandriva.com ( i prefer bug report as i may forget mail ).

Keyboard for owner of Samsung X10
----------------------------------
For people owning a Samsung X10, the provided keymap requires 2 commands
to activate all keys. Place a script in /etc/X11/xinit.d/ that contains :

#!/bin/bash
setkeycodes 0x74 122
setkeycodes 0x75 123

and use the samsungX10.def file.
See http://www.samsungpc.com/products/x10_x10plus/x10.htm if your are not sure this is
yours.
EOF

echo "WebBrowser=www-browser">> src/%{name}.conf
echo "Shell=xvt">> src/%{name}.conf

%install
rm -rf %{buildroot}

%makeinstall

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 src/%{name}.conf %{buildroot}/%{_sysconfdir}
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -d %{buildroot}%{_sysconfdir}/X11/xinit.d/
install -m 755 %{SOURCE11} %{buildroot}%{_sysconfdir}/X11/xinit.d/%{name}

bzcat %{SOURCE1} > %{buildroot}/%{_datadir}/%{name}/vaio.def
bzcat %{SOURCE2} > %{buildroot}/%{_datadir}/%{name}/FCSAmilo.def
bzcat %{SOURCE3} > %{buildroot}/%{_datadir}/%{name}/samsungx30.def
bzcat %{SOURCE4} > %{buildroot}/%{_datadir}/%{name}/precision.def
bzcat %{SOURCE5} > %{buildroot}/%{_datadir}/%{name}/dellinspiron.def
bzcat %{SOURCE6} > %{buildroot}/%{_datadir}/%{name}/samsungX10.def

chmod 644 AUTHORS BUGS COPYING INSTALL TODO def/sample.xml

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS BUGS COPYING INSTALL TODO def/sample.xml README.mdk
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/X11/xinit.d/%{name}
