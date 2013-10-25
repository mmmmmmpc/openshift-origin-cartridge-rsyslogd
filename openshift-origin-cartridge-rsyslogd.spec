%global cartridgedir %{_libexecdir}/openshift/cartridges/v2/rsyslog

Name: openshift-origin-cartridge-rsyslogd
Version: 2.13
Release: 1%{?dist}
Summary: Embedded rsyslogd support for OpenShift

Group: Network/Daemons
License: ASL 2.0
URL: http://openshift.redhat.com
Source0: %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

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
%doc %{cartridgedir}/LICENSE

%changelog
* Thu Oct 24 2013 Roger Nunn <rnunn@redhat.com> 2.0.7
- Fixed multi-gear scaling challenge
- Fixed a lot of annoying bugs including double slashes
- Fixed some significant points including killall
- Fixed 516 -> 514 ports for remote targets in rsyslog.conf
- Fixed ruby parser on rsyslog.conf and a lot of other simple errors

* Fri Oct 18 2013 Roger Nunn <rnunn@redhat.com> 2.0.6
- Modified manifest file and added README.md
- Significant re-structure of /bin V2 control scripts
- Updated to dynamic configs using ruby parser

* Fri Sep 05 2013 Miguel Pérez Colino <mperez@redhat.com> 2.0-5
- Modified setup and control scripts
- Removed symlinks and replaced it with files

* Thu Sep 04 2013 Miguel Pérez Colino <mperez@redhat.com> 2.0-4
- Modified categories in manifest.yml

* Thu Sep 04 2013 Miguel Pérez Colino <mperez@redhat.com> 2.0-3
- Modified manifest.yml
- Changes to contro script

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
