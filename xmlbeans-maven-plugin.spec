Name:          xmlbeans-maven-plugin
Version:       2.3.3
Release:       3%{?dist}
Summary:       Maven XML Beans Plugin
License:       ASL 2.0
Url:           http://mojo.codehaus.org/xmlbeans-maven-plugin/
# svn export https://svn.codehaus.org/mojo/tags/xmlbeans-maven-plugin-2.3.3
# tar cJf xmlbeans-maven-plugin-2.3.3.tar.xz xmlbeans-maven-plugin-2.3.3
Source0:       %{name}-%{version}.tar.xz
# xmlbeans-maven-plugin package don't include the license file
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: java-devel
BuildRequires: mvn(org.codehaus.mojo:mojo-parent:pom:)

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-invoker-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-surefire-provider-junit

BuildRequires: mvn(org.apache.maven:maven-artifact)
BuildRequires: mvn(org.apache.maven:maven-core)
BuildRequires: mvn(org.apache.maven:maven-model)
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
BuildRequires: mvn(org.apache.xmlbeans:xmlbeans)
BuildRequires: mvn(org.codehaus.plexus:plexus-utils)
BuildRequires: mvn(xml-resolver:xml-resolver)

BuildArch:     noarch

%description
Maven XML Beans Plugin provides integration of the
Apache XML Beans for Maven. Runs the xmlbeans
parser/code generator against schemes in files and
dependent jars.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

cp -p %{SOURCE1} .
sed -i 's/\r//' LICENSE-2.0.txt

# these test fails
# [INFO] XMLBeans discrete xsd's in a jar test for MXMLBEANS-21  FAILURE [0.665s]
# Caused by: org.sonatype.aether.transfer.ArtifactNotFoundException: 
# Could not find artifact org.codehaus.mojo:xmlbeans-maven-plugin:pom:latest
# in local.central (file:///..../BUILD/xmlbeans-maven-plugin-2.3.3/.m2)
rm -r src/it/mxmlbeans-21/*

%pom_remove_dep org.apache.maven:maven-project
%pom_add_dep org.apache.maven:maven-core:any:compile

%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :jdepend-maven-plugin
rm -r pom.xml.orig

%build

%mvn_file : %{name}
%mvn_build -- -Dmojo.java.target=1.5

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.3.3-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Jan 09 2013 gil cattaneo <puntogil@libero.it> 2.3.3-1
- initial rpm
