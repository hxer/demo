# Docker for shadowsocks-libev


## build docker image

```
curl -sSL https://github.com/hxer/docker/raw/master/shadowsocks/Dockerfile > Dockerfile
docker build -t shadowsocks .
```

## run docker container

```
docker run -d -e PASSWORD=socks -p 1188:1188 --restart always shadowsocks
```

## shadowsocks client

```
{
    "server": "your-vps-ip",
    "server_port": 1188,
    "local_address": "0.0.0.0",
    "local_port": 1080,
    "password": "socks",
    "timeout": 600,
    "method": "aes-256-cfb"
}
```

## note

使用过程中，连接速度没有vps使用shdowsocks快，可能和使用的是 shadowsocks-libdev 有关，不确定
