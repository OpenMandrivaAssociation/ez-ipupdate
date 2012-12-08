%define name ez-ipupdate
%define version 3.0.11b8
%define release %mkrel 14

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


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.11b8-13mdv2011.0
+ Revision: 664173
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.11b8-12mdv2011.0
+ Revision: 605116
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.11b8-11mdv2010.1
+ Revision: 520106
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.0.11b8-10mdv2010.0
+ Revision: 424396
- rebuild

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.11b8-9mdv2009.1
+ Revision: 316635
- added a bunch of patches from debian

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 3.0.11b8-8mdv2009.0
+ Revision: 220739
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Oct 23 2007 GÃ¶tz Waschk <waschk@mandriva.org> 3.0.11b8-7mdv2008.1
+ Revision: 101612
- add missing header to fix crash on x86_64 (bug #35001)

* Mon May 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 3.0.11b8-6mdv2008.0
+ Revision: 26634
- Import ez-ipupdate



* Mon May 14 2007 Götz Waschk <waschk@mandriva.org> 3.0.11b8-6mdv2008.0
- fix permissions
- create config file owned by nobody (bug #29258)

* Mon Aug 28 2006 Götz Waschk <waschk@mandriva.org> 3.0.11b8-6mdv2007.0
- pinit
- new url

* Sun May 14 2006 Stefan van der Eijk <stefan@eijk.nu> 3.0.11b8-5mdk
- rebuild for sparc

* Fri Sep 09 2005 Raphaël Gertz <rapsys@free.fr> 3.0.11b8-4mdk
- run ez-ipupdate as nobody instead of root
- fix startup script
- make rpmlint happy
- add README.urpmi and default config file

* Wed Mar 09 2005 Laurent Culioli <laurent@zarb.org> 3.0.11b8-3mdk
- rebuild
- make rpmlint more happy

* Mon Nov 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.0.11b8-2mdk
- use /var/cache for the cache file rather than /tmp in example configs

* Sun May 11 2003 Laurent Culioli <laurent@pschit.net> 3.0.11b8-1mdk
- 3.0.11b8
- drop patch0 ( merged upstream )

* Fri Feb 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0.11b7-3mdk
- Patch0: don't assume errno to be a global variable.

* Tue Aug 13 2002 Laurent Culioli <laurent@pschit.net> 3.0.11b7-2mdk
- update init

* Tue Jun 18 2002 Laurent Culioli <laurent@mandrakesoft.com> 3.0.11b7-1mdk
- 3.0.11b7

* Tue Feb 26 2002 Laurent Culioli <laurent@mandrakesoft.com> 3.0.11b6-2mdk
- fix init

* Mon Feb 25 2002 Laurent Culioli <laurent@mandrakesoft.com> 3.0.11b6-1mdk
- add init-script
- 3.0.11b6

* Fri Jan 11 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.11b5-2mdk
- Clean specfile
- Fix config files

* Mon Aug 27 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.11b5-1mdk
- updated to 3.0.11b5

* Fri Jul 06 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.11b-2mdk
- fix description, thx to Mordy Ovits

* Fri Jul 06 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.11b-1mdk
- updated to 3.011b

* Tue Jan 09 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.4-1mdk
- updated to 3.0.4

* Tue Dec 12 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.0.1-1mdk
- updated to 3.0.1
- updated list of supported services

* Sun Nov 12 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.9.5-1mdk
- updated to 2.9.5
- provide all configuration example files

* Wed Aug 30 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.8.1-1mdk
- v2.8.1
- BM

* Tue Jul 04 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.4.2-2mdk
- rebuild

* Wed Jun 21 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.4.2-1mdk
- new in contribs
