%global eclipse_base %{_libdir}/eclipse
%global install_loc %{_datadir}/eclipse/dropins/checkstyle
%global cs_ver 5.1
%global eclipse_ver 3.5

Summary:   Checkstyle plugin for Eclipse
Name:      eclipse-checkstyle
Version:   5.1.0
Release:   3
License:   LGPLv2+
Group:     Development/Java
URL:       http://eclipse-cs.sourceforge.net
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Source0: %{name}-%{version}.tar.xz 
Source10: eclipse-eclipsecs-fetch-src.sh
Patch0:  itext-rtf-remove.patch
Patch1:  unpack-plugins.patch

# remove problematic getEclipseClasspath call and checkstyle jar inclusion
#Patch0: %{name}-%{version}.patch
# remove problematic eclipse 3.0 backwards compatibility
#Patch1: %{name}-%{version}-tabwidth.patch

Requires: eclipse-platform >= 0:%{eclipse_ver}
Requires: eclipse-jdt
Requires: checkstyle >= 0:%{cs_ver}
Requires: guava
Requires: apache-commons-beanutils
Requires: apache-commons-io
Requires: dom4j

BuildRequires: jpackage-utils >= 0:1.5
BuildRequires: ant >= 0:1.6
BuildRequires: eclipse-pde >= 0:%{eclipse_ver}
BuildRequires: checkstyle >= 0:%{cs_ver}
BuildRequires: java-devel >= 1.4.2
BuildRequires: apache-commons-io
BuildRequires: guava
BuildRequires: jfreechart
BuildRequires: dom4j

%description
The Eclipse Checkstyle plugin integrates the Checkstyle Java code
auditor into the Eclipse IDE. The plugin provides real-time feedback
to the user about violations of rules that check for coding style and
possible error prone code constructs. 

%prep
%setup -q 
%patch0 -p0 -R
%patch1 -p0

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

sed -i -e "s|checkstyle-all-5.1.jar|checkstyle-all-5.1.jar,guava.jar,commons-beanutils.jar|g"  net.sf.eclipsecs.checkstyle/META-INF/MANIFEST.MF

ln -s %{_javadir}/checkstyle.jar net.sf.eclipsecs.checkstyle/checkstyle-all-5.1.jar
ln -s %{_javadir}/guava.jar net.sf.eclipsecs.checkstyle/guava.jar
ln -s %{_javadir}/commons-beanutils.jar net.sf.eclipsecs.checkstyle/commons-beanutils.jar
ln -s %{_javadir}/commons-io.jar net.sf.eclipsecs.core/lib/commons-io-1.2.jar
ln -s %{_javadir}/commons-lang.jar net.sf.eclipsecs.core/lib/commons-lang-2.3.jar
ln -s %{_javadir}/dom4j.jar net.sf.eclipsecs.core/lib/dom4j-1.6.1.jar

ln -s %{_javadir}/jcommon.jar net.sf.eclipsecs.ui/lib/jcommon-1.0.9.jar
ln -s %{_javadir}/jfreechart.jar net.sf.eclipsecs.ui/lib/jfreechart-1.0.5.jar
ln -s %{_javadir}/itext.jar net.sf.eclipsecs.ui/lib/itext-2.0.1.jar

rm -fr net.sf.eclipsecs.ui/src/net/sf/eclipsecs/ui/stats/export/internal/RTFStatsExporter.java

%build
%{eclipse_base}/buildscripts/pdebuild

%install
rm -rf %{buildroot}
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}

unzip -q -o -d $RPM_BUILD_ROOT%{install_loc} \
 build/rpmBuild/net.sf.eclipsecs.zip

pushd $RPM_BUILD_ROOT%{install_loc}/eclipse/plugins
rm -fr net.sf.eclipsecs.checkstyle_0.0.0/checkstyle-all-5.1.jar
ln -s %{_javadir}/checkstyle.jar net.sf.eclipsecs.checkstyle_0.0.0/checkstyle-all-5.1.jar
rm -fr net.sf.eclipsecs.checkstyle_0.0.0/guava.jar
ln -s %{_javadir}/guava.jar net.sf.eclipsecs.checkstyle_0.0.0/guava.jar
rm -fr net.sf.eclipsecs.checkstyle_0.0.0/commons-beanutils.jar
ln -s %{_javadir}/commons-beanutils.jar net.sf.eclipsecs.checkstyle_0.0.0/commmons-beanutils.jar
rm -fr net.sf.eclipsecs.core_0.0.0/lib/commons-io-1.2.jar
ln -s %{_javadir}/commons-io.jar net.sf.eclipsecs.core_0.0.0/lib/commons-io-1.2.jar
rm -fr net.sf.eclipsecs.core_0.0.0/lib/commons-lang-2.3.jar
ln -s %{_javadir}/commons-lang.jar net.sf.eclipsecs.core_0.0.0/lib/commons-lang-2.3.jar
rm -fr net.sf.eclipsecs.core_0.0.0/lib/dom4j-1.6.1.jar net.sf.eclipsecs.core_0.0.0/lib/dom4j-1.6.1.jar
ln -s %{_javadir}/dom4j.jar net.sf.eclipsecs.core_0.0.0/lib/dom4j-1.6.1.jar

rm -fr net.sf.eclipsecs.ui_0.0.0/lib/jcommon-1.0.9.jar
ln -s %{_javadir}/jcommon.jar net.sf.eclipsecs.ui_0.0.0/lib/jcommon-1.0.9.jar
rm -fr net.sf.eclipsecs.ui_0.0.0/lib/jfreechart-1.0.5.jar
ln -s %{_javadir}/jfreechart.jar net.sf.eclipsecs.ui_0.0.0/lib/jfreechart-1.0.5.jar
rm -fr net.sf.eclipsecs.ui_0.0.0/lib/itext-2.0.1.jar
ln -s %{_javadir}/itext.jar net.sf.eclipsecs.ui_0.0.0/lib/itext-2.0.1.jar
popd

%clean 
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc net.sf.eclipsecs-feature/license.html
%{install_loc}

