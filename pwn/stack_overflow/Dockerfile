FROM alpine:3.20 AS build
RUN apk add --no-cache build-base
WORKDIR /src
COPY vuln.c .
RUN gcc -O0 -g -fno-stack-protector -no-pie -o vuln vuln.c

FROM alpine:3.20
RUN apk add --no-cache socat
WORKDIR /app
COPY --from=build /src/vuln ./vuln
COPY flag.txt ./flag.txt
EXPOSE 31337
CMD socat TCP-LISTEN:31337,reuseaddr,fork EXEC:"/app/vuln",pty,stderr
