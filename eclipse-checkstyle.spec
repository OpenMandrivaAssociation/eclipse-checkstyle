%define eclipse_base    %{_datadir}/eclipse
%define eclipse_ver     3.3
%define gcj_support     1

Name:           eclipse-checkstyle
Version:        4.3.2
Release:        %mkrel 0.0.6
Epoch:          0
Summary:        Checkstyle plugin for Eclipse
License:        LGPL
Group:          Development/Java
URL:            http://eclipse-cs.sourceforge.net/
Source0:        CheckstylePlugin-v4_3_2.tar.bz2
Source1:        checkout_and_build_tarball.sh
Patch0:         %{name}-4.3.2.patch
Patch1:         %{name}-4.3.2-manifest.patch
Requires:       eclipse-platform >= 1:%{eclipse_ver}
Requires:       checkstyle
Requires:       checkstyle-optional
Requires:       jakarta-commons-beanutils
Requires:       jakarta-commons-collections
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-io
Requires:       jakarta-commons-lang
Requires:       jakarta-commons-logging
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  checkstyle
BuildRequires:  checkstyle-optional
BuildRequires:  eclipse-cvs-client >= 1:%{eclipse_ver}
BuildRequires:  eclipse-pde >= 1:%{eclipse_ver}
BuildRequires:  jakarta-commons-beanutils
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jakarta-commons-io
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Eclipse Checkstyle plugin integrates the Checkstyle Java code
auditor into the Eclipse IDE. The plugin provides real-time feedback
to the user about violations of rules that check for coding style and
possible error prone code constructs. 

%prep
%setup -q -c
%patch0 -p0
%patch1 -p0
%{__mkdir_p} target/docs

%build
export OPT_JAR_LIST="ant/ant-trax xalan-j2 xalan-j2-serializer xerces-j2"
export CLASSPATH=$(build-classpath checkstyle checkstyle-optional commons-beanutils-core jakarta-commons-collections commons-httpclient commons-io commons-lang)

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
%{eclipse_base}/plugins/org.eclipse.equinox.preferences_3.2*.*.jar \
%{eclipse_base}/plugins/org.eclipse.core.jobs_%{eclipse_ver}*.*.jar
do
  %{_bindir}/test -f  ${jar} || exit 1
  CLASSPATH=$CLASSPATH:${jar}
done

pushd CheckstylePlugin/build

%{ant} -Dbuild.sysclasspath=only \
    -Dcheckstyle.docs.dir=../target/docs \
    -Declipse.plugin.dir=%{eclipse_base}/plugins \
    -Dworkspace=.. \
    -Declipse.version=%{eclipse_ver} \
    -Dproject.name=CheckstylePlugin_%{version} \
    build.bindist build.feature

popd

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}/%{eclipse_base}/features/com.atlassw.tools.eclipse.checkstyle_%{version}

BUILD_DIR=`pwd`/CheckstylePlugin

# install feature
pushd %{buildroot}/%{eclipse_base}/features/com.atlassw.tools.eclipse.checkstyle_%{version}
   %{jar} xvf ${BUILD_DIR}/dist/com.atlassw.tools.eclipse.checkstyle_%{version}-feature.jar
popd

# install plugin
pushd %{buildroot}/%{eclipse_base}
    %{jar} xvf ${BUILD_DIR}/dist/com.atlassw.tools.eclipse.checkstyle_%{version}-bin.zip
    %{_bindir}/build-jar-repository \
    %{buildroot}/%{eclipse_base}/plugins/com.atlassw.tools.eclipse.checkstyle_%{version} \
    checkstyle \
    checkstyle-optional \
    antlr \
    jakarta-commons-logging \
    jakarta-commons-cli \
    jakarta-commons-beanutils-core \
    jakarta-commons-collections \
    commons-httpclient \
    commons-io \
    commons-lang
popd

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean 
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc CheckstylePlugin/license/LICENSE.*
%{eclipse_base}/features/*
%{eclipse_base}/plugins/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
