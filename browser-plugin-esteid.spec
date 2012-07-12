# TODO
# - new dir for gecko extensions
%define		firebreath_version 1.5.2
Summary:	Estonian ID card digital signing browser plugin
Summary(pl.UTF-8):	Wtyczka przeglądarki do cyfrowego podpisywania przy użyciu estońskich kart eID
Name:		browser-plugin-esteid
Version:	1.3.3
Release:	0.1
# The source files from esteid-browser-plugin and Firebreath are compiled
# together to the shared object npesteid.so.
# Firebreath is dual-licensed [BSD or LGPLv2+], esteid-browser-plugin is LGPLv2+.
# The resulting npesteid.so binary is: LGPLv2+.
#
# The files in mozilla-esteid subpackage are all from esteid-browser-plugin
# tarball and are LGPLv2+.
License:	LGPL v2+
Group:		Applications/Networking
#Source0Download: http://code.google.com/p/firebreath/downloads/list
Source0:	http://firebreath.googlecode.com/files/firebreath-%{firebreath_version}.7z
# Source0-md5:	7321e1c2157b69faf68e4b64aeb0ab3d
# Source1Download: http://code.google.com/p/esteid/downloads/list
Source1:	http://esteid.googlecode.com/files/esteid-browser-plugin-%{version}.tar.bz2
# Source1-md5:	d9af514fb8fa251e9039340f7063eb12
Patch0:		boost-1.50.patch
URL:		http://code.google.com/p/esteid/
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	gettext-devel
BuildRequires:	gtkmm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	p7zip
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	smartcardpp-devel
BuildRequires:	unzip
BuildRequires:	zip
Requires:	browser-plugins >= 2.0
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
old signature APIs.

%description -l pl.UTF-8
Esteid Browser Plugin to wtyczka dla wielu przeglądarek udostępniająca
funkcje estońskich kart eID z poziomu JavaScriptu.

Wtyczka może być używana na stronach WWW w celu przesłania podpisu
elektronicznego użytkownika. Aby chronić prywatność, podpisu mogą
używać tylko strony z "białej listy". W przypadku stron nie
znajdujących się na liście pojawia się żółty pasek powiadomienia.
Wtyczka ma zaimplementowany także tryb kompatybilności obsługujący
istniejące strony WWW używające stare API do podpisów.

%prep
%setup -qcT
# Extract firebreath
7z x %{SOURCE0} > /dev/null
mv firebreath-%{firebreath_version}/* .

# Extract esteid-browser-plugin into firebreath's projects/ subdir
install -d projects
tar xf %{SOURCE1} -C projects

# Remove bundled libraries
%{__rm} -rv src/3rdParty/boost
%{__rm} -rv src/libs

%patch0 -p1

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
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/browser-plugins
mv $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/npesteid.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins

# Install Gecko extension
install -d $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{extension_id}
cp -a build/projects/esteid-browser-plugin-1/Mozilla/xpi/* \
      $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{extension_id}

%find_lang esteid-browser-plugin

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f esteid-browser-plugin.lang
%defattr(644,root,root,755)
%doc projects/esteid-browser-plugin-%{version}/AUTHORS
%attr(755,root,root) %{_libdir}/browser-plugins/npesteid.so
%{_datadir}/esteid-browser-plugin
%{_libdir}/mozilla/extensions/%{extension_id}
