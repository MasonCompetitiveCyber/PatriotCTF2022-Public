// CaptSHA
// PatriotCTF 2022
// Author: Andy Smith
// Category: Programming

package main

import (
	"bufio"
	"bytes"
	"crypto/sha1"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

func main() {
	fmt.Println("--------------------------------------------------------------")
	fmt.Println("Welcome to the CaptSHA flag service!")
	fmt.Println("To limit spam, we are now requiring a captcha to be completed.")
	fmt.Println("To do this, we use a hashing proof-of-work system.")
	fmt.Println("You must enter a string. We will hash it using SHA1.")
	fmt.Println("The hash must end with the specified bytes.")
	fmt.Println("You have 5 seconds for each of the 25 questions. Let's begin!")
	fmt.Println("--------------------------------------------------------------")

	in := bufio.NewReader(os.Stdin)

	rand.Seed(time.Now().UnixNano())

	for i := 0; i < 25; i++ {

		// Random bytes we'll ask for
		randomBytes := []byte{byte(rand.Intn(256)), byte(rand.Intn(256))}

		// Get starting time
		startTime := time.Now().UnixMilli()

		// Ask the user to enter a string
		fmt.Printf("[Question %d] ", i+1)
		fmt.Printf("Please enter a string whose SHA1 hash ends with %x: ", randomBytes)
		userHash, err := in.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input")
			return
		}

		// If userHash is empty, return
		userHash = strings.TrimSpace(userHash)
		if len(userHash) == 0 {
			fmt.Println("You must enter a string")
			return
		}

		// Create the hash
		h := sha1.New()
		h.Write([]byte(userHash))
		hash := h.Sum(nil)
		fmt.Printf("Your string's hash is: %x\n", hash)

		// Check the if the hash ends with the requested byte
		if !bytes.HasSuffix(hash, randomBytes) {
			fmt.Println("Sorry, that's not correct.")
			return
		}

		// Get ending time
		endTime := time.Now().UnixMilli()

		if (endTime - startTime) > 5000 {
			fmt.Println("Sorry, you took too long.")
			return
		}
	}

	fmt.Println("You completed the captcha! Here's your reward: PCTF{y0u_c4ptur3d_th3_c4ptcha}")
}
