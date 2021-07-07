# 制作依赖自包含的wine32 rpm包方法

## 前言
  由于OpenEuler系统没有 i386 的架构和相关依赖包，wine 32 位的程序就无法在OpenEuler系统编译和执行；所以为了在OpenEuler上跑32位的wine和 Windows程序，我们采用了app-image的打包方法，先在其他有32位依赖的linux 系统上把wine32 位的依赖下载下来，并以AppImage的格式对文件进行组织，然后打包成rpm包。在OpenEuler 系统上安装此rpm包，验证可以安装并启动微信。

## 文件介绍
 - wine-i386.deb 是制作原生 wine.deb 包的模板
 - ukylin-wine   是制作 ukylin-wine deb包模板文件
 - makeappimage  是制作 wine.squashfs 的模板工具

## 制作 ukylin-wine deb包流程

### (1) 编译 wine 源码

	$ cd wine-source-dir
	$ mkdir wine32
	$ cd wine32
	$ ../configure --prefix=$PWD/../deb-package/debwine-i386.deb/usr
	$ make && make install
	```

### (2) 制作 wine.deb 包

	$ cd ../deb-package/
	$ dpkg -b debwine-i386.deb wine.deb
	```

### (3) 制作 wine.squashfs
	*注意：* 由于制作 squashfs 自依赖包需要先将wine的相关依赖包都下载到本地，如果系统中已经安装过wine的相关包或依赖包会导致依赖下载不全，所以制作环境最好是新安装的操作系统。

	$ cd makeappimage
	$ sudo ./kylinos-makesquashfs.sh ../wine.deb
	$ cd ..

	制作完成后生成 wine.squashfs 文件。

### (4) 编辑 ukylin-wine.spec 文件，生成rpm

	rpm -bb SPEC/ukylin-wine.spec
	

至此，ukylin-wine rpm包制作完成。


## ukylin-wine rpm包安装和使用
### 下载地址：
    链接：https://pan.baidu.com/s/1XWWSF7QCzV2zdCTlXRio_A 
    提取码：3vtl

### 安装方法 
    1. 先安装ukui 桌面环境
    2. 执行下面命令安装 wine 包
    sudo rpm -i ukylin-wine-6.3.0-3.noarch.rpm

### wine 使用指南
    wine --version 
    查看wine的版本

    wine WeChatSetup.exe
    wine 安装微信安装包 

    启动微信，点击桌面微信图标可以启动微信。
