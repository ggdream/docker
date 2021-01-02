FROM golang:1.15.6


ENV GO111MODULE=auto
ENV GORPOXY=https://goproxy.cn,direct

WORKDIR /app
COPY . .

RUN go run main.go