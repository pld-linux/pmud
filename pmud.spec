Summary:	Power Manager daemon for Apple PowerBooks.
Name:		pmud
Version:	0.10.1
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tar.gz
Provides:	apmd
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	chkconfig
Obsoletes:	apmd

%description
pmud is a daemon which periodically polls the PMU (power manager) and
performs functions such as enabling or disabling devices appropriately
when the power source changes. It can also be instructed to signal
init(8) that a power- failure has occured.

%prep
%setup -q -n pmud-0.10

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sbindir},usr/X11R6/bin,%{_bindir},%{_mandir}/man8,/etc/sysconfig}
install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,etc/power,usr/X11R6/bin}

install pmud $RPM_BUILD_ROOT/%{_sbindir}
install snooze $RPM_BUILD_ROOT/%{_sbindir}
install wakebay $RPM_BUILD_ROOT/%{_sbindir}
install fblevel $RPM_BUILD_ROOT/%{_sbindir}
install xmouse $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
install Batmon $RPM_BUILD_ROOT/%{_bindir}

install pmud.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install snooze.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install fblevel.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install batmon.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install xmouse.8 $RPM_BUILD_ROOT/%{_mandir}/man8/

install power.conf $RPM_BUILD_ROOT/etc/sysconfig/power
install pmud.rc $RPM_BUILD_ROOT/etc/rc.d/init.d/pmud
install pwrctl $RPM_BUILD_ROOT%{_sysconfdir}/power/pwrctl

%clean
rm -rf $RPM_BUILD_ROOT

%post
ln -s /usr/sbin/snooze /usr/bin/apm
/sbin/chkconfig --add pmud
if [ -f /var/lock/subsys/pmud ]; then
	/etc/rc.d/init.d/pmud stop >&2
	/etc/rc.d/init.d/pmud start >&2
else
	echo "Run \"/etc/rc.d/init.d/pmud start\" to start pmud daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/pmud ]; then
		/etc/rc.d/init.d/pmud stop >&2
	fi
	/sbin/chkconfig --del pmud
fi

%pre
[ -c /dev/pmu ] || {
    echo "creating /dev/pmu"
    mknod /dev/pmu c 10 154
}
[ -c /dev/adb ] || {
    echo "creating /dev/adb"
    mknod /dev/adb c 56 0
}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_prefix}/X11R6/bin/*
%attr(444,root,root) /etc/sysconfig/power
%attr(754,root,root) /etc/rc.d/init.d/pmud
%attr(640,root,root) %{_sysconfdir}/power/pwrctl

%{_mandir}/man8/*
%doc {BUGS,CHANGES,INSTALL,README,THANKS,TODO,pwrctl-local}
