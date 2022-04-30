package main

import (
	"crypto/ecdsa"
	"fmt"
	"io/ioutil"
	"log"

	"github.com/ethereum/go-ethereum/accounts/keystore"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/spruceid/siwe-go"
)

// Defining constant values and variables
const (
	domain    = "https://pctf.competitivecyber.club"
	uri       = "https://pctf.competitivecyber.club"
	version   = "1"
	statement = ""
	chainId   = "5"
	requestId = "2113853211"
)

const addressStr = "0x19EDFEa51785C878973628ECb8bBDDC669bf41d8"

//const addressStr = "0xe8076002401e345A50a6c91B6254396A24822322"

var address = common.HexToAddress(addressStr)

var (
	issuedAt       = "2022-04-04T20:06:19Z"
	nonce          = "13371337"
	expirationTime = ""
	notBefore      = ""
	resources      = []string{"https://pctf.competitivecyber.club/gimmeflag"}
)

//var issuedAt = time.Now().UTC().Format(time.RFC3339)
//var issuedAt = ""
//var expirationTime = time.Now().UTC().Add(48 * time.Hour).Format(time.RFC3339)
//var notBefore = time.Now().UTC().Add(-24 * time.Hour).Format(time.RFC3339)

var options = map[string]interface{}{
	"statement":      statement,
	"nonce":          nonce,
	"chainId":        chainId,
	"issuedAt":       issuedAt,
	"expirationTime": expirationTime,
	"notBefore":      notBefore,
	"requestId":      requestId,
	"resources":      resources,
}

// The SIWE Message
var message, _ = siwe.InitMessage(
	domain,
	addressStr,
	uri,
	version,
	options,
)

// Returns Keccak256 Hash
func signHash(data []byte) common.Hash {
	msg := fmt.Sprintf("\x19Ethereum Signed Message:\n%d%s", len(data), data)
	return crypto.Keccak256Hash([]byte(msg))
}

// Signs message and returns signature
func signMessage(message string, privateKey *ecdsa.PrivateKey) ([]byte, error) {

	sign := signHash([]byte(message))

	signature, err := crypto.Sign(sign.Bytes(), privateKey)

	if err != nil {
		return nil, err
	}

	signature[64] += 27
	return signature, nil
}

// Main Function
func main() {

	// Reads Bytes From The Keystore File
	b, err := ioutil.ReadFile("./block_one")
	if err != nil {
		log.Fatal(err)
	}

	// Password For it
	password := "precious"

	// Decrypts the key
	key, err := keystore.DecryptKey(b, password)
	if err != nil {
		log.Fatal(err)
	}

	// Extracts Private Key
	pvkey := crypto.FromECDSA(key.PrivateKey)
	pvtkey := hexutil.Encode(pvkey)
	fmt.Println("Private Key =", pvtkey)

	// Extracts Public Key
	//pbkey := crypto.FromECDSAPub(&key.PrivateKey.PublicKey)
	//pubkey := hexutil.Encode(pbkey)
	//fmt.Println("Public Key =", pubkey)

	// Extracts Address of the Wallet
	addr := crypto.PubkeyToAddress(key.PrivateKey.PublicKey).Hex()
	fmt.Println("Address =", addr)

	// Signs the message with private key
	sgn, err := signMessage(message.String(), key.PrivateKey)
	if err != nil {
		log.Fatal(err)
	}

	// Prints Original Message and Also the Corresponding Generated Signature
	fmt.Println("===================================================================================================================")
	fmt.Println(message)

	fmt.Println("===================================================================================================================")
	fmt.Println("Signature =", hexutil.Encode(sgn))

	signed := hexutil.Encode(sgn)

	// Used to Verify the Signature
	pbKey, err := message.VerifyEIP191(signed)
	if err != nil {
		log.Fatal(err)
	}

	//fmt.Println(pbKey.Params())
	/*
		var sth time.Time
		sth = time.Now()

		some, err := message.Verify(signed, &nonce, &sth)
		if err != nil {
			log.Fatal(err)
		}

		fmt.Println(some)
	*/

	//If the signature is valid, Original Public Key can be extracted

	finalPbKey := hexutil.Encode(crypto.FromECDSAPub(pbKey))

	fmt.Println("===================================================================================================================")

	fmt.Println("Extracted Public Key =", finalPbKey)

	fmt.Println("===================================================================================================================")

}
