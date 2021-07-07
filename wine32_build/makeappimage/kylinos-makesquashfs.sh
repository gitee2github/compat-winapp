#!/bin/bash
if [ $(id -u) -ne 0 ]; then
    echo "必须在 sudo 模式运行。"
    exit 1
fi
if [[ $1 == "" ]]; then
    echo "e.g: $0 kylin-wine_i386.deb"
    exit 1
fi

if [ ! -f $1 ]; then
    echo "$1 not found!"
    exit 1
fi
winedebpath=$(readlink -f $1)
# Pre install
dpkg --add-architecture i386
apt update
apt install -y aptitude wget file bzip2

wineworkdir=$PWD/WineWorkdir
pkgcachedir=$PWD/winedeploycache
mkdir -p $wineworkdir
if [ ! -d $pkgcachedir ]; then
    mkdir -p $pkgcachedir
    aptitude -y -d -o dir::cache::archives="$pkgcachedir" install libwine:i386
fi
cd $wineworkdir
find $pkgcachedir -name '*deb' ! -name 'libwine*' -exec dpkg -x {} . \;
dpkg -x $winedebpath .
cp ../resource/AppRun ./
cp ../resource/wine.png ./
cp ../resource/wine.desktop ./
chmod +x AppRun

cd -

if [ ! -f appimagetool.AppImage ]; then
    wget -nv -c "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" -O  appimagetool.AppImage
fi
chmod +x appimagetool.AppImage

if [ ! -d squashfs-root ]; then
    ./appimagetool.AppImage --appimage-extract
fi
echo "===============制作 wine.squashfs==============="
mksquashfs $wineworkdir wine.squashfs -b 256K -comp xz -no-xattrs
echo "===============制作 wine.appimage==============="
#export ARCH=x86_64; squashfs-root/AppRun $wineworkdir
rm -rf $wineworkdir
# rm -rf $pkgcachedir
