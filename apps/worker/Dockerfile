FROM golang:1.22-alpine

WORKDIR /app

RUN apk add --no-cache git

COPY go.mod go.sum* ./
RUN go mod download

COPY . .

RUN go build -o /worker ./cmd/worker

CMD ["/worker"]