package main

import (
	"fmt"
	"net"
	"os"
)

const (
	SERVER_HOST = "localhost"
	SERVER_PORT = "8888"
	SERVER_TYPE = "tcp"
)

func main() {
	// Running the server
	fmt.Println("Server Running...")
	server, err := net.Listen(SERVER_TYPE, SERVER_HOST+":"+SERVER_PORT)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	defer server.Close()

	fmt.Println("Listening on " + SERVER_HOST + ":" + SERVER_PORT)
	fmt.Println("Waiting for client...")
	for {
		connection, err := server.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}
		fmt.Println("Client", connection.RemoteAddr(), "connected")
		go processClient(connection)
	}

}

// Function for handling client server connection
func processClient(connection net.Conn) {
	buffer := make([]byte, 1024)
	mLen, err := connection.Read(buffer)
	if err != nil {
		fmt.Println("Error reading:", err.Error())
		connection.Close()
	} else if string(buffer[:mLen-1]) == "0x3f84b31bb65f323a4ef932e9c0acc563d4228d6dbd263d438354de9a24c94c270871af6d7ac7506050b6fa1d6d93278a33f84bb96d531f69802de25f293afafb1c" {
		fmt.Println("Received: ", string(buffer[:mLen]), "from", connection.RemoteAddr())
		_, err = connection.Write([]byte("Thanks For The Signature! Great Job! \nFlag is PCTF{Randomized_Values_Should_Be_Used_While_Signing_In_With_Ethereum}"))
		connection.Close()
	} else {
		fmt.Println("Received:", string(buffer[:mLen]))
		_, err = connection.Write([]byte("Got your wrong signature message: " + string(buffer[:mLen])))
		connection.Close()
	}
	
}