FROM ubuntu:20.04



WORKDIR /tmp
ENV \
    VERSION=n4.3.2 \
    TARGET=/usr \
    TZ=Asia/Shanghai \
    SOURCE=https://gitee.com/mirrors/ffmpeg.git


RUN \
    sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone && \
    apt-get update && \
    apt-get install --no-install-recommends --fix-missing -y \
        build-essential autoconf automake cmake libtool git checkinstall pkg-config \
        apt-transport-https ca-certificates \
        libx264-dev \
        libx265-dev \
        libvorbis-dev \
        libvpx-dev \
        libopus-dev \
        libnuma-dev \
        libfdk-aac-dev \
        libmp3lame-dev \
        libspeex-dev \
        libssl-dev && \
    git clone -b ${VERSION} ${SOURCE} && cd ffmpeg/ && \
    ./configure --prefix=${TARGET} \
        --enable-shared \
        --disable-static \
        --disable-x86asm \
        --enable-libfdk-aac \
        --enable-libmp3lame \
        --enable-libopus \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libspeex \
        --enable-openssl \
        --enable-gpl \
        --enable-nonfree \
        --enable-version3 && \
    make -j$(nproc) && \
    make install && \
    apt-get clean -y && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


CMD [ "ffmpeg", "-version" ]
