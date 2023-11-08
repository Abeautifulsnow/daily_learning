// https://github.com/antirez/smallchat/blob/main/smallchat.c
package main

import (
	"bufio"
	"fmt"
	"net"
	"strconv"
	"strings"
)

const (
	maxClients = 1000
	port       = 7711
)

type client struct {
	conn net.Conn
	nick string
}

type chatState struct {
	listener net.Listener
	clients  map[int]*client
	nextID   int
}

func main() {
	chat := newChat()
	chat.run()
}

func newChat() *chatState {
	return &chatState{
		clients: make(map[int]*client),
	}
}

func (cs *chatState) run() {
	l, err := net.Listen("tcp", ":"+strconv.Itoa(port))
	if err != nil {
		fmt.Println("Error listening:", err)
		return
	}
	cs.listener = l
	defer l.Close()

	fmt.Println("Chat server running on port", port)

	for {
		conn, err := l.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}
		go cs.handleConn(conn)
	}
}

func (cs *chatState) handleConn(conn net.Conn) {
	id := cs.nextID
	cs.nextID++

	nick := "user" + strconv.Itoa(id)
	c := &client{conn: conn, nick: nick}
	cs.clients[id] = c

	fmt.Println("Client connected:", id)

	r := bufio.NewReader(conn)
	for {
		msg, err := r.ReadString('\n')
		if err != nil {
			break
		}

		if msg[0] == '/' {
			cs.handleCmd(id, msg)
		} else {
			cs.broadcast(id, msg)
		}
	}

	delete(cs.clients, id)
	conn.Close()
	fmt.Println("Client disconnected:", id)
}

func (cs *chatState) handleCmd(id int, msg string) {
	parts := strings.SplitN(strings.TrimSpace(msg), " ", 2)
	cmd := parts[0]
	arg := ""
	if len(parts) > 1 {
		arg = parts[1]
	}

	switch cmd {
	case "/nick":
		cs.clients[id].nick = arg
	default:
		conn := cs.clients[id].conn
		conn.Write([]byte("Unsupported command\n"))
	}
}

func (cs *chatState) broadcast(sender int, msg string) {
	for id, c := range cs.clients {
		if id != sender {
			outMsg := fmt.Sprintf("%s> %s", c.nick, msg)
			c.conn.Write([]byte(outMsg))
		}
	}
}
