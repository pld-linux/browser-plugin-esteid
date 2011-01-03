# TODO
# - new dir for gecko extensions
%define		firebreath_version 1.3.0
Summary:	Estonian ID card digital signing browser plugin
Name:		browser-plugin-esteid
Version:	1.2.0
Release:	0.1
License:	LGPL v2+
Group:		Applications/Networking
URL:		http://code.google.com/p/esteid/
Source0:	http://firebreath.googlecode.com/files/firebreath-%{firebreath_version}.tar.bz2
# Source0-md5:	704bd0183407a166d105277b13763d01
Source1:	http://esteid.googlecode.com/files/esteid-browser-plugin-%{version}.tar.bz2
# Source1-md5:	4a26435087b8578c5727b144e5870ae6
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	gtkmm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	smartcardpp-devel
BuildRequires:	unzip
BuildRequires:	zip
# obsolete package name upstream uses
Obsoletes:	esteid-browser-plugin
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# this comes from install.rdf
%define		extension_id	\{aa84ce40-4253-11da-8cd6-0800200c9a66\}

%description
Esteid Browser Plugin is cross-browser plugin that exposes Estonian
eID card functions via JavaScript.

The plugin is used by web pages to obtain users digital signature. To
protect privacy, only web pages in "whitelist" can use the card. For
unlisted pages, a yellow notification bar appears. The plugin also
implements a compatibility mode to support existing web pages that use
old signature API-s.

%prep
# Extract firebreath
%setup -q -n firebreath-%{firebreath_version}
# Extract esteid-browser-plugin into firebreath's projects/ subdir
install -d projects
tar -xf %{SOURCE1} -C projects

%build
install -d build
cd build
export CXXFLAGS="%{rpmcxxflags} -fno-strict-aliasing"
export CFLAGS="$CXXFLAGS"
%cmake .. \
	-DCMAKE_BUILD_WITH_INSTALL_RPATH=FALSE \
	-DCMAKE_SKIP_RPATH=TRUE \
	-DDOCDIR=%{_docdir} \
	-DWITH_SYSTEM_BOOST:BOOL=YES

%{__make}


%install
rm -rf $RPM_BUILD_ROOT
cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

%find_lang esteid-browser-plugin

install -d $RPM_BUILD_ROOT%{_libdir}/browser-plugins
mv $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/npesteid.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins

# Install Gecko extension
install -d $RPM_BUILD_ROOT%{_libdir}/firefox/extensions/%{extension_id}
unzip build/esteid-*.xpi \
      -d $RPM_BUILD_ROOT%{_libdir}/firefox/extensions/%{extension_id}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f esteid-browser-plugin.lang
%defattr(644,root,root,755)
%doc projects/esteid-browser-plugin-%{version}/AUTHORS
%attr(755,root,root) %{_libdir}/browser-plugins/npesteid.so
%{_datadir}/esteid-browser-plugin
%{_libdir}/firefox/extensions/%{extension_id}
