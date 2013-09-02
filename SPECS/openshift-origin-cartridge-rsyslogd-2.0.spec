%global cartridgedir %{_libexecdir}/openshift/cartridges/v2/rsyslogd

Name: openshift-origin-cartridge-rsyslogd
Version: 2.0
Release: 2%{?dist}
Summary: Embedded rsyslogd support for OpenShift

Group: Network/Daemons
License: ASL 2.0
URL: http://openshift.redhat.com
#Source0: http://mirror.openshift.com/pub/origin-server/source/%{name}/%{name}-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

#Requires: openshift-origin-cartridge-abstract
Requires: rubygem(openshift-origin-node)
Requires: rsyslog
Obsoletes: cartridge-rsyslogd-2.0

%description
Provides rhc rsyslogd cartridge support to OpenShift in a number of user scenarios and rsyslogd modes. (Cartridge Format V2)

%prep
%setup -q


%build
%__rm %{name}.spec

%install
%__rm -rf %{buildroot}
%__mkdir -p %{buildroot}%{cartridgedir}
%__cp -r * %{buildroot}%{cartridgedir}

%post
%{_sbindir}/oo-admin-cartridge --action install --source %{cartridgedir}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{cartridgedir}
%attr(0755,-,-) %{cartridgedir}/bin/
%{cartridgedir}
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Wed Aug 14 2013 Miguel Pérez Colino <mperez@redhat.com> 2.0-2
- Modified manifest.yml to add missing vars

* Wed Aug 14 2013 Miguel Pérez Colino <mperez@redhat.com> 2.0-1
- First attempt to create a v2 format cartridge

* Wed Aug 14 2013 Miguel Pérez Colino <mperez@redhat.com> 1.0-3
- modified "rsyslog" daemon stop

* Wed Aug 14 2013 Miguel Pérez Colino <mperez@redhat.com> 1.0-2
- removed openshift-origin-cartridge-abstract dependency

* Wed Jun 5 2013 Rog Nunn <rnunn@redhat.com> 1.0.0-1
- experimental package built
