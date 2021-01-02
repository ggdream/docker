FROM ubuntu:20.04


WORKDIR /tmp
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone && \
    sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt update && \
    apt upgrade -y && \
    # apt install -y ffmpeg && \
    apt install -y zlib1g-dev gcc make build-essential libssl-dev \
        libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
        libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev openssl && \
    wget -c https://npm.taobao.org/mirrors/python/3.8.6/Python-3.8.6.tgz && \
    tar -zxvf Python-3.8.6.tgz && \
    cd Python-3.8.6/ && \
    ./configure --prefix=/usr/local && \
    make -j4 && \
    make install && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com && \
    python -m pip install --upgrade pip && \
    # pip install requests==2.24.0 aiohttp==3.6.2 ffmpy3==0.2.3 && \
    apt install -y autoconf automake cmake libtool git checkinstall \
        nasm yasm pkg-config libspeex-dev && \
    git clone -b n4.3.1 https://hub.fastgit.org/FFmpeg/FFmpeg.git && \
    cd FFmpeg/ && \
    ./configure --prefix=/usr/local \
        --enable-gpl \
        --enable-version3 \
        --enable-libspeex \
        --disable-ffplay \
        --disable-ffprobe && \
    make -j4 && \
    make install && \
    apt clean && \
    apt autoclean && \
    apt autoremove && \
    rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/*


WORKDIR /file
COPY . .
RUN pip install -r requirements.txt
VOLUME [ "/data" ]

ENTRYPOINT [ "python", "/file/bilibili.py" ]
CMD [ "--help" ]