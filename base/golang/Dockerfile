FROM golang:1.15.6


ENV GOPROXY=https://goproxy.cn,direct

WORKDIR /app
COPY . .

RUN go run main.go