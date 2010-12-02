%define name ez-ipupdate
%define version 3.0.11b8
%define release %mkrel 12

Name: %{name}
Summary: Client for Dynamic DNS Services
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Source1: ez-ipupdate.init
# add missing include for 64 bit (bug #35001)
Patch0: ez-ipupdate-3.0.11b8-64-bit.patch
Patch1: 000_missing_headers.diff
Patch2: 001_automake_syntax.diff
Patch3: 002_am_maintainer_mode.diff
Patch4: 010_rebootstrap.diff
Patch5: 100_portability.diff
Patch6: 101_syslog_crashes.diff
Patch7: 102_misc_crashes.diff
Patch8: 103_protocol.diff
Patch9: 104_misc_crashes.diff
Patch10: 150_cosmetic.diff
Patch11: 200_default_config.diff
Patch12: 201_upstream_changelog.diff
Group: Networking/Other
URL: http://ez-ipupdate.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
License: GPL
Requires(post): rpm-helper
Requires(postun): rpm-helper

%description
ez-ipupdate is a small utility for updating your host name for any of the
dynamic DNS service offered at: 

    * http://www.ez-ip.net
    * http://www.justlinux.com
    * http://www.dhs.org
    * http://www.dyndns.org
    * http://www.ods.org
    * http://gnudip.cheapnet.net (GNUDip)
    * http://www.dyn.ca (GNUDip)
    * http://www.tzo.com
    * http://www.easydns.com
    * http://www.dyns.cx
    * http://www.hn.org
    * http://www.zoneedit.com

it is pure C and works on Linux, *BSD and Solaris.  

Don't forget to create your own config file ( in /etc/ez-ipupdate.conf )
You can find some example in /usr/share/doc/%{name}-%{version}

%prep

%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p0
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
%configure

%make 

%install
rm -rf $RPM_BUILD_ROOT 

chmod 644 *.conf
%makeinstall_std
perl -pi -e "s|\/usr\/local\/bin|\/usr\/bin|" *.conf
install -D -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/%{name}

cat > README.urpmi << EOF
To configure the ez-ipupdate deamon, edit and set the corrects
parameters in /etc/ez-ipupdate.conf config file.
Then you can start the deamon with service ez-ipupdate start
EOF

%clean
rm -rf $RPM_BUILD_ROOT 

%files 
%defattr(-,root,root)
%doc COPYING INSTALL README README.urpmi
%doc *.conf
%{_bindir}/*
%{_initrddir}/%{name}

%post
%create_ghostfile %{_sysconfdir}/%{name}.conf nobody root 600
if [ ! -s %{_sysconfdir}/%{name}.conf ]; then
cat > %{_sysconfdir}/%{name}.conf << EOF
# example config file for ez-ipupdate
#service-type=dyndns-static
service-type=dyndns
user=login:password
host=somedomain.dyndns.org
interface=eth1
max-interval=2073600

# cache file in the temp directory
cache-file=/tmp/.ez-ipupdate.cache
EOF
fi
%_post_service ez-ipupdate

%preun
%_preun_service ez-ipupdate
