Summary:	multiple host monitoring tool
Name:		icmpmonitor
Version:	1.2
Release:	0.1
License:	BSD
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/icmpmonitor/%{name}-%{version}.tar.gz
# Source0-md5:	c6c9bfc14f914604232945185be387b3
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
URL:		http://www.crocodile.org/software.html
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Using the InterNet Control Message Protocol (ICMP) "ECHO" facility,
monitors several hosts, and notify admin if some of them are down.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -D icmpmonitor		$RPM_BUILD_ROOT/%{_sbindir}/icmpmonitor
install -D icmpmonitor.man	$RPM_BUILD_ROOT/%{_mandir}/man1/icmpmonitor.1
install -D %{SOURCE1}		$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE2}		$RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -D %{SOURCE3}		$RPM_BUILD_ROOT%{_sysconfdir}/icmpmonitor.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README NEWS TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/icmpmonitor.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
