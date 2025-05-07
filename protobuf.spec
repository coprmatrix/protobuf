Name:           protobuf-source
Version:        30.2

%define _name protobuf
# Enablde tests
%bcond_with check

# Build -java subpackage
%bcond_without java
%bcond_with java_tests

# Library names
%define libname         %{_name}
%define liblite         %{_name}-lite
%define libcompiler     libprotoc
%define develname       %{_name}-devel
%define javaname        %{_name}-java
%define javalite        %{_name}-javalite
%define javautil        %{_name}-java-util
%define libutf8         utf8_range
%define devutf8         utf8_range-devel
%define libvim          %{_name}-vim
%define libjavadoc      %{_name}-javadoc
%define bompom          %{_name}-pom
%define parentpom       %{_name}-parent
%define compiler        %{_name}-compiler

%define major           %{uversion}
%define majorutf8       %{major}

%define uversion              %{version}
%define protobuf_java_ver     4.%{version}
%define protobuf_cpp_ver      6.%{version}

# Major
%define freeze() %{lua:
for key, value in ipairs(arg)
do
  rpm.define(value .. ' ' .. rpm.expand('%' .. value))
end
}

%freeze protobuf_cpp_ver protobuf_java_ver uversion majorutf8 major

Summary:        Protocol Buffers - Google's data interchange format
Release:        2%{?autorelease}
License:        BSD
Group:          System/Libraries
URL:            https://github.com/protocolbuffers/protobuf
Source0:        https://github.com/protocolbuffers/protobuf/archive/v%{version}%{?rcver}/%{_name}-%{version}%{?rcver}-all.tar.gz
Source1:        ftdetect-proto.vim
Source10:       https://repo1.maven.org/maven2/com/google/protobuf/%{_name}-java/%{protobuf_java_ver}/%{_name}-java-%{protobuf_java_ver}.pom
Source11:       https://repo1.maven.org/maven2/com/google/protobuf/%{_name}-javalite/%{protobuf_java_ver}/%{_name}-javalite-%{protobuf_java_ver}.pom
Source12:       https://repo1.maven.org/maven2/com/google/protobuf/%{_name}-java-util/%{protobuf_java_ver}/%{_name}-java-util-%{protobuf_java_ver}.pom
Patch100:       protobuf-SOVERSION.patch
BuildRequires:  cmake
BuildRequires:  cmake(absl)
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(zlib)
BuildRequires:  g++

%define _description %{expand:
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages.
}

%description %{_description}

%package -n     %{libname}
Summary:        %{summary}
Group:          Development/Other
Version:        %{protobuf_cpp_ver}

%description -n %{libname} %{_description}

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

%package -n     %{compiler}
Summary:        Protocol Buffers compiler
Group:          Development/Other
Version:        %{protobuf_cpp_ver}
Recommends:     %{libname} = %{protobuf_cpp_ver}-%{release}
Recommends:     %{liblite} = %{protobuf_cpp_ver}-%{release}

%description -n %{compiler}
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
Requires:       %{compiler} = %{protobuf_cpp_ver}-%{release}
Provides:       lib%{_name}-devel = %{protobuf_cpp_ver}-%{release}

%description -n %{develname}
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries.

%package -n     %{libvim}
Summary:        Vim syntax highlighting for Google Protocol Buffers descriptions
Group:          Development/Other
Version:        %{protobuf_cpp_ver}
BuildArch:      noarch
Requires:       vim-enhanced

%description -n %{libvim}
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor.

%if %{with java}
%package -n     %{javaname}
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

%description -n %{javaname}
This package contains Java Protocol Buffers runtime library.

%package -n     %{javalite}
Summary:        Java Protocol Buffers lite runtime library
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description -n %{javalite}
This package contains Java Protocol Buffers lite runtime library.

%package -n     %{javautil}
Summary:        Utilities for Protocol Buffers
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description -n %{javautil}
Utilities to work with protos. It contains JSON support
as well as utilities to work with proto3 well-known types.

%package -n     %{bompom}
Summary:        Protocol Buffer BOM POM
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description -n %{bompom}
Protocol Buffer BOM POM.

%package -n     %{libjavadoc}
Summary:        Javadoc for %{_name}-java
Group:          Documentation
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description -n %{libjavadoc}
This package contains the API documentation for %{_name}-java.

%package -n     %{parentpom}
Summary:        Protocol Buffer Parent POM
Group:          Development/Java
Version:        %{protobuf_java_ver}
BuildArch:      noarch

%description -n %{parentpom}
Protocol Buffer Parent POM.

%endif

%prep
%autosetup -p1 -n %{_name}-%{uversion}

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
%mvn_file :protobuf-java:jar: %{_name}/%{_name}-java %{_name}

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

%files -n %{libname}
%doc CONTRIBUTORS.txt README.md
%license LICENSE
%{_libdir}/lib%{_name}.so.%{major}{,.*}

%files -n %{liblite}
%doc README.md
%license LICENSE
%{_libdir}/lib%{_name}-lite.so.%{major}{,.*}

%files -n %{libutf8}
%doc third_party/utf8_range/README.md
%license third_party/utf8_range/LICENSE
%{_libdir}/libutf8_{range,validity}.so.%{major}
%{_libdir}/libutf8_{range,validity}.so.%{uversion}.*

%files -n %{compiler}
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
%{_includedir}/google/%{_name}/
%{_libdir}/lib%{_name}.so
%{_libdir}/lib%{_name}-lite.so
%{_libdir}/libprotoc.so
%{_libdir}/cmake/protobuf/
%{_libdir}/pkgconfig/%{_name}.pc
%{_libdir}/pkgconfig/%{_name}-lite.pc

%{_libdir}/pkgconfig/upb.pc
%{_libdir}/libupb.a
%{_includedir}/upb/

%{_libdir}/cmake/utf8_range/
%{_libdir}/pkgconfig/utf8_range.pc
%{_includedir}/utf8_range.h
%{_includedir}/utf8_validity.h
%{_libdir}/libutf8_range.so
%{_libdir}/libutf8_validity.so

%files -n %{libvim}
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
%files -n %{javaname} -f .mfiles-protobuf-java
%doc examples/AddPerson.java examples/ListPeople.java
%doc java/README.md
%license LICENSE

%files -n %{javautil} -f .mfiles-protobuf-java-util

%files -n %{libjavadoc} -f .mfiles-javadoc
%license LICENSE

%files -n %{parentpom} -f .mfiles-protobuf-parent
%license LICENSE

%files -n %{bompom} -f .mfiles-protobuf-bom
%license LICENSE

%files -n %{javalite} -f .mfiles-protobuf-javalite
%license LICENSE
%endif

