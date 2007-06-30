%define eclipse_base %{_datadir}/eclipse
%define cs_ver 4.3
%define eclipse_ver 3.2
%define gcj_support 1

Summary:   Checkstyle plugin for Eclipse
Name:      eclipse-checkstyle
Version:   4.0.1
Release:   %mkrel 6.1
License:   LGPL
Group:     Development/Java
URL:       http://eclipse-cs.sourceforge.net
Buildroot: {_tmppath}/%{name}-%{version}-%{release}-root

Source0: CheckstylePlugin-v4_0_1.tar.bz2
Source10: checkout_and_build_tarball.sh

# remove problematic getEclipseClasspath call and checkstyle jar inclusion
Patch0: %{name}-%{version}.patch
# remove problematic eclipse 3.0 backwards compatibility
Patch1: %{name}-%{version}-tabwidth.patch

Requires: eclipse-platform >= 1:%{eclipse_ver}
Requires: checkstyle = 0:%{cs_ver}
Requires: checkstyle-optional = 0:%{cs_ver}

BuildRequires: jpackage-utils >= 0:1.5
BuildRequires: ant >= 0:1.6
BuildRequires: eclipse-pde >= 1:%{eclipse_ver}
BuildRequires: checkstyle = 0:%{cs_ver}
BuildRequires: checkstyle-optional = 0:%{cs_ver}
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel >= 1.0.33
Requires(post):         java-gcj-compat >= 1.0.33
Requires(postun):       java-gcj-compat >= 1.0.33
%else
BuildRequires:          java-devel >= 1.4.2
%endif

%description
The Eclipse Checkstyle plugin integrates the Checkstyle Java code
auditor into the Eclipse IDE. The plugin provides real-time feedback
to the user about violations of rules that check for coding style and
possible error prone code constructs. 

%prep
%setup -q -c
%patch0
%patch1

# rewrite classpath
perl -p -i -e "s/checkstyle-all-%{cs_ver}.jar/[checkstyle-%{cs_ver}].jar,\
[checkstyle-optional-%{cs_ver}].jar,[commons-beanutils-core].jar,\
[commons-logging].jar,[antlr].jar/g" CheckstylePlugin/META-INF/MANIFEST.MF

%build
# make target directory for build.plugin.docs
mkdir -p target/docs

# remove any precompiled bits (also done in checkout_and_build_tarball.sh)
find . -regextype posix-egrep -regex '.*.jar|.*.zip|.*.class' -type f -print \
    | xargs rm -f

# create build classpath
export CLASSPATH=$(build-classpath checkstyle \
                          checkstyle-optional xerces-j2 xalan-j2)
for jar in \
%{_jnidir}/swt-gtk-%{eclipse_ver}*.jar \
%{eclipse_base}/plugins/org.eclipse.core.commands_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.filebuffers_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.resources_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.runtime_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.jdt.core_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.jdt.ui_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.jface_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.jface.text_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.osgi_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.swt_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.team.core_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.team.cvs.core_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.text_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.editors_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.ide_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.workbench_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.ui.workbench.texteditor_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.equinox.common_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.equinox.registry_%{eclipse_ver}*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.jobs_%{eclipse_ver}*.*.jar
do
  test -f  ${jar} || exit 1
  CLASSPATH=$CLASSPATH:${jar}
done

pushd CheckstylePlugin/build

%{ant} -Dbuild.sysclasspath=only \
    -Dcheckstyle.docs.dir=../target/docs \
    -Declipse.plugin.dir=%{eclipse_base}/plugins \
    -Dworkspace=.. \
    -Declipse.version=%{eclipse_ver} \
    -Dproject.name=CheckstylePlugin_4.0.1 \
    build.bindist

popd

%install
rm -rf %{buildroot}
install -d -m755 %{buildroot}/%{eclipse_base}/features/com.atlassw.tools.eclipse.checkstyle_%{version}
BUILD_DIR=`pwd`/CheckstylePlugin

# install feature
pushd %{buildroot}/%{eclipse_base}/features/com.atlassw.tools.eclipse.checkstyle_%{version}
   %{jar} xvf ${BUILD_DIR}/dist/com.atlassw.tools.eclipse.checkstyle_%{version}-feature.jar
popd

# install plugin
pushd %{buildroot}/%{eclipse_base}
    %{jar} xvf ${BUILD_DIR}/dist/com.atlassw.tools.eclipse.checkstyle_%{version}-bin.zip
    find . -type f -name '*src.zip' -print | xargs -t rm -f
    build-jar-repository \
    %{buildroot}/%{eclipse_base}/plugins/com.atlassw.tools.eclipse.checkstyle_%{version} \
    checkstyle-%{cs_ver} \
    checkstyle-optional-%{cs_ver} \
    commons-beanutils-core \
    commons-logging antlr
popd

%if %{gcj_support}
  %{_bindir}/aot-compile-rpm
%endif

%clean 
rm -rf %{buildroot}

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root)
%doc CheckstylePlugin/license/LICENSE.*
%{eclipse_base}/features/*
%{eclipse_base}/plugins/*

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif
