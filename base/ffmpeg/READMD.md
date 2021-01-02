# FFmpeg

- 基础镜像：ubuntu20.04
- ffmpeg版本：n4.3.1

---
编译选项
~~~sh
./configure --prefix=/usr \
    --enable-shared \
    --disable-static \
    --disable-x86asm \
    --disable-doc \
    --enable-libfdk-aac \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-libvorbis \
    --enable-libvpx \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libspeex \
    --enable-gpl \
    --enable-nonfree \
    --enable-version3
~~~

---
使用
~~~sh
$ docker run -d -v /tmp:/tmp ggdream/ffmpeg ffmpeg -i test.mp4 test.flv
~~~