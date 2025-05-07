# Enablde tests
%bcond_with check

# Build -java subpackage
%bcond_without java
%bcond_with java_tests

%define mklibname(d) %{lua: name = arg[1]; if opt.d then name = name .. "-devel" end; print(name) }
%define mkrel() %{lua: print(rpm.expand( arg[1] .. "%{?autorelease}" )) }

# Version
# Check sub pkg versions from version.json
# or from src/google/protobuf/compiler/versions.h
%define uversion          30.0
%define protobuf_cpp_ver  6.%{uversion}
%define protobuf_java_ver 4.%{uversion}

# Major
%define major           %{uversion}

# Library names
%define libname         %mklibname %{name} %{major}
%define liblite         %mklibname %{name}-lite %{major}
%define libcompiler     %mklibname libprotoc %{major}
%define develname       %mklibname %{name} -d

%define majorutf8       %{uversion}
%define libutf8         %mklibname utf8_range %{majorutf8}
%define devutf8         %mklibname utf8_range -d

#define rcver rc2

Summary:        Protocol Buffers - Google's data interchange format
Name:           protobuf
Version:        %{uversion}
Release:        %mkrel 2
License:        BSD
Group:          System/Libraries
URL:            https://github.com/protocolbuffers/protobuf
Source0:        https://github.com/protocolbuffers/protobuf/archive/v%{version}%{?rcver}/%{name}-%{version}%{?rcver}-all.tar.gz
Source1:        ftdetect-proto.vim
Source10:       https://repo1.maven.org/maven2/com/google/protobuf/%{name}-java/%{protobuf_java_ver}/%{name}-java-%{protobuf_java_ver}.pom
Source11:       https://repo1.maven.org/maven2/com/google/protobuf/%{name}-javalite/%{protobuf_java_ver}/%{name}-javalite-%{protobuf_java_ver}.pom
Source12:       https://repo1.maven.org/maven2/com/google/protobuf/%{name}-java-util/%{protobuf_java_ver}/%{name}-java-util-%{protobuf_java_ver}.pom
Patch100:       protobuf-SOVERSION.patch
BuildRequires:  cmake
BuildRequires:  cmake(absl)
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(zlib)
BuildRequires:  g++

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages.

%package -n     %{liblite}
Summary:        Protocol Buffers lite version
Group:          Development/Other
Version:        %{protobuf_cpp_ver}

%description -n %{liblite}
This package contains a compiled with "optimize_for = LITE_RUNTIME"
version of Google's Protocol Buffers library.

The "optimize_for = LITE_RUNTIME" option causes the compiler to
generate code which only depends libprotobuf-lite, which is much
smaller than libprotobuf but lacks descriptors, reflection, and some
other features.

%package -n     %{libutf8}
Summary:        Google's UTF8 Library
Group:          System/Libraries
Version:        %{protobuf_cpp_ver}
License:        MIT

%description -n %{libutf8}
Fast UTF-8 validation with Range algorithm (NEON+SSE4+AVX2).

%package        compiler
Summary:        Protocol Buffers compiler
Group:          Development/Other
Version:        %{protobuf_cpp_ver}
Recommends:     %{libname} = %{protobuf_cpp_ver}-%{release}
Recommends:     %{liblite} = %{protobuf_cpp_ver}-%{release}

%description    compiler
This package contains Protocol Buffers compiler for all programming
languages.

%package -n     %{libcompiler}
Summary:        Protocol Buffers compiler shared library
Group:          System/Libraries
Version:        %{protobuf_cpp_ver}

%description -n %{libcompiler}
This package contains the Protocol Buffers compiler shared library.

%package -n     %{develname}
Summary:        Protocol Buffers C++ headers and libraries
Group:          Development/Other
Version:        %{protobuf_cpp_ver}
Requires:       %{libname} = %{protobuf_cpp_ver}-%{release}
Requires:       %{liblite} = %{protobuf_cpp_ver}-%{release}
Requires:       %{libutf8} = %{protobuf_cpp_ver}-%{release}
Requires:       %{libcompiler} = %{protobuf_cpp_ver}-%{release}
Requires:       %{name}-compiler = %{protobuf_cpp_ver}-%{release}
Provides:       %{name}-devel = %{protobuf_cpp_ver}-%{release}

%description -n %{develname}
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries.

%package        vim
Summary:        Vim syntax highlighting for Google Protocol Buffers descriptions
Group:          Development/Other
Version:        %{protobuf_cpp_ver}
BuildArch:      noarch
Requires:       vim-enhanced

%description    vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor.

%if %{with java}
%package java
Summary:        Java Protocol Buffers runtime library
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.gson:gson)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(com.google.guava:guava-testlib)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.easymock:easymock)
%if %{with java_tests}
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(com.google.truth:truth)
BuildRequires:  mvn(junit:junit)
%endif

%description java
This package contains Java Protocol Buffers runtime library.

%package javalite
Summary:        Java Protocol Buffers lite runtime library
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description javalite
This package contains Java Protocol Buffers lite runtime library.

%package java-util
Summary:        Utilities for Protocol Buffers
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description java-util
Utilities to work with protos. It contains JSON support
as well as utilities to work with proto3 well-known types.

%package bom
Summary:        Protocol Buffer BOM POM
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description bom
Protocol Buffer BOM POM.

%package javadoc
Summary:        Javadoc for %{name}-java
Group:          Documentation
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{name}-java.

%package parent
Summary:        Protocol Buffer Parent POM
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description parent
Protocol Buffer Parent POM.

%endif

%prep
%autosetup -p1 -n %{name}-%{uversion}

find -name \*.cc -o -name \*.h | xargs chmod -x

# https://github.com/protocolbuffers/protobuf/issues/8459
sed \
	-e "/^TEST(ArenaTest, BlockSizeSmallerThanAllocation) {$/a\\  if (sizeof(void*) == 4) {\n    GTEST_SKIP();\n  }" \
	-e "/^TEST(ArenaTest, SpaceAllocated_and_Used) {$/a\\  if (sizeof(void*) == 4) {\n    GTEST_SKIP();\n  }" \
	-i src/google/protobuf/arena_unittest.cc

# https://github.com/protocolbuffers/protobuf/issues/8460
sed -e "/^TEST(AnyTest, TestPackFromSerializationExceedsSizeLimit) {$/a\\  if (sizeof(void*) == 4) {\n    GTEST_SKIP();\n  }" -i src/google/protobuf/any_test.cc

%if %{with java}
cp %{SOURCE10} java/core/pom.xml
cp %{SOURCE11} java/lite/pom.xml
cp %{SOURCE12} java/util/pom.xml

# Remove unnecessary animal sniffer
%pom_remove_plugin org.codehaus.mojo:animal-sniffer-maven-plugin java/pom.xml

%pom_remove_dep com.google.errorprone:error_prone_annotations java/util/pom.xml
%pom_remove_dep com.google.j2objc:j2objc-annotations java/util/pom.xml

# Remove annotation libraries we don't have
annotations=$(
    find -name '*.java' |
      xargs grep -h -e '^import com\.google\.errorprone\.annotation' \
                    -e '^import com\.google\.j2objc\.annotations' |
      sort -u | sed 's/.*\.\([^.]*\);/\1/' | paste -sd\|
)
find -name '*.java' | xargs sed -ri \
    "s/^import .*\.($annotations);//;s/@($annotations)"'\>\s*(\((("[^"]*")|([^)]*))\))?//g'

# These use truth or error_prone_annotations or guava-testlib
rm -r java/util/src/test/java/com/google/protobuf/util
rm -r java/util/src/main/java/com/google/protobuf/util

# Make OSGi dependency on sun.misc package optional
%pom_xpath_inject "pom:configuration/pom:instructions" "<Import-Package>sun.misc;resolution:=optional,*</Import-Package>" java/core/pom_template.xml

# Backward compatibility symlink
%mvn_file :protobuf-java:jar: %{name}/%{name}-java %{name}

# This test is incredibly slow on arm
# https://github.com/google/protobuf/issues/2389
%ifarch %{arm32} s390x
mv java/core/src/test/java/com/google/protobuf/IsValidUtf8Test.java \
   java/core/src/test/java/com/google/protobuf/IsValidUtf8Test.java.slow
mv java/core/src/test/java/com/google/protobuf/DecodeUtf8Test.java \
   java/core/src/test/java/com/google/protobuf/DecodeUtf8Test.java.slow

mv java/core/src/test/java/com/google/protobuf/CheckUtf8Test.java \
   java/core/src/test/java/com/google/protobuf/CheckUtf8Test.java.slow
mv java/core/src/test/java/com/google/protobuf/Proto3SchemaTest.java \
   java/core/src/test/java/com/google/protobuf/Proto3SchemaTest.java.slow
mv java/core/src/test/java/com/google/protobuf/Proto3LiteSchemaTest.java \
   java/core/src/test/java/com/google/protobuf/Proto3LiteSchemaTest.java.slow
%endif
%endif

rm -f src/solaris/libstdc++.la

iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt

%build
# -Wno-error=type-limits:
#     https://bugzilla.redhat.com/show_bug.cgi?id=1838470
#     https://github.com/protocolbuffers/protobuf/issues/7514
#     https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
#  (also set in %%check)
export CXXFLAGS="%{build_cxxflags} -Wno-error=type-limits"
%cmake -GNinja \
  -Dprotobuf_VERBOSE:BOOL=ON \
  -Dprotobuf_BUILD_TESTS:BOOL=OFF \
  -Dprotobuf_BUILD_LIBPROTOC:BOOL=ON \
  -Dprotobuf_LOCAL_DEPENDENCIES_ONLY:BOOL=ON
%cmake_build

%if %{with java}
export B__BUILD_PATH=`realpath %{__cmake_builddir}`
pushd java
LD_LIBRARY_PATH="${B__BUILD_PATH}:%{_libdir}" PATH="${B__BUILD_PATH}:$PATH" env protoc \
  --java_out=core/src/main/java \
  -I../src \
  ../src/google/protobuf/descriptor.proto \
  --proto_path=core/src/main/resources/google/protobuf \
   core/src/main/resources/google/protobuf/java_features.proto
popd
%ifarch %ix86 s390x %{arm32}
export MAVEN_OPTS=-Xmx1024m
%endif
%pom_disable_module kotlin java/pom.xml
%pom_disable_module kotlin-lite java/pom.xml
%mvn_build -s %{!?with_java_tests:--skip-tests} -- -f java/pom.xml
%endif

%if %{with check}
%check
export CXXFLAGS="%{build_cxxflags} -Wno-error=type-limits"
%ctest
%endif

%install
%cmake_install

install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
%mvn_install
%endif

%files
%doc CONTRIBUTORS.txt README.md
%license LICENSE
%{_libdir}/lib%{name}.so.%{major}{,.*}

%files -n %{liblite}
%doc README.md
%license LICENSE
%{_libdir}/lib%{name}-lite.so.%{major}{,.*}

%files -n %{libutf8}
%doc third_party/utf8_range/README.md
%license third_party/utf8_range/LICENSE
%{_libdir}/libutf8_{range,validity}.so.%{major}
%{_libdir}/libutf8_{range,validity}.so.%{uversion}.*

%files compiler
%doc README.md
%license LICENSE
%{_bindir}/protoc{,-%{uversion}.*}
%{_bindir}/protoc-gen-upb{,-%{uversion}.*}
%{_bindir}/protoc-gen-upb_minitable{,-%{uversion}.*}
%{_bindir}/protoc-gen-upbdefs{,-%{uversion}.*}

%files -n %{libcompiler}
%{_libdir}/libprotoc.so.%{major}{,.*}

%files -n %{develname}
%doc examples/add_person.cc examples/addressbook.proto
%doc examples/list_people.cc examples/Makefile examples/README.md
%dir %{_includedir}/google/
%{_includedir}/google/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-lite.so
%{_libdir}/libprotoc.so
%{_libdir}/cmake/protobuf/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-lite.pc

%{_libdir}/pkgconfig/upb.pc
%{_libdir}/libupb.a
%{_includedir}/upb/

%{_libdir}/cmake/utf8_range/
%{_libdir}/pkgconfig/utf8_range.pc
%{_includedir}/utf8_range.h
%{_includedir}/utf8_validity.h
%{_libdir}/libutf8_range.so
%{_libdir}/libutf8_validity.so

%files vim
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
%files java -f .mfiles-protobuf-java
%doc examples/AddPerson.java examples/ListPeople.java
%doc java/README.md
%license LICENSE

%files java-util -f .mfiles-protobuf-java-util

%files javadoc -f .mfiles-javadoc
%license LICENSE

%files parent -f .mfiles-protobuf-parent
%license LICENSE

%files bom -f .mfiles-protobuf-bom
%license LICENSE

%files javalite -f .mfiles-protobuf-javalite
%license LICENSE
%endif

