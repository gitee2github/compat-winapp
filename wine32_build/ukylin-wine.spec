Name: ukylin-wine
Version: 6.3.0
Release: 1
Summary: from wine

Group: Unspecified
License: GPLv3
BuildArch: noarch
Packager: linchaochao <linchaochao@kylinos.cn>
Vendor: kylinos
BuildRequires: coreutils gzip
Requires: coreutils

source0: run-wine.mount
Source3: run-wine.conf
Source6: wine.squashfs

%description
Wine （“Wine Is Not an Emulator” 的首字母缩写）是一个能够在多种 POSIX-compliant 操作系统（诸如 Linux，macOS 及 BSD 等）上运行 Windows 应用的兼容层。

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system
mkdir -p $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/
mkdir -p $RPM_BUILD_ROOT/usr/share/wine

install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/etc/systemd/system/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/usr/share/wine/

%post
systemctl enable /etc/systemd/system/run-wine.mount
systemd-tmpfiles --create /usr/lib/tmpfiles.d/run-wine.conf 2>/dev/null
# systemd-mount /etc/systemd/system/run-wine.mount
mount /usr/share/wine/wine.squashfs /run/wine
ln -s /run/wine/AppRun /usr/bin/ukylin-wine
if [ ! -f /lib/ld-linux.so.2 ]; then
	rm -rf /lib/ld-linux.so.2
fi
if [ ! -L /lib/ld-linux.so.2 ]; then
	ln -s /run/wine/lib/ld-linux.so.2 /lib/ld-linux.so.2
fi

%preun
lsof /run/wine 2>/dev/null | cut -d ' ' -f 2 | uniq | xargs -i kill -9 {}
umount /run/wine
systemctl disable run-wine.mount

%postun
rm -rf /usr/bin/ukylin-wine
if [ -L /lib/ld-linux.so.2 ] && [ ! -f /lib/ld-linux.so.2 ]; then
	rm -rf /lib/ld-linux.so.2
fi

%files
%defattr(-,root,root)
/etc/systemd/system/run-wine.mount
/usr/lib/tmpfiles.d/run-wine.conf
/usr/share/wine/wine.squashfs

%changelog
* Mon Jun 28 2021 linchaochao<linchaochao@kylinos.cn> ukylin-wine-6.3.0
- Packing for the first time

