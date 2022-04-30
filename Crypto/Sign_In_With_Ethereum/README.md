# Sign In With Ethereum

### Description
::::::::: Part Two:::::::::

You did it. You recovered the secret key.  
As it's been a long time, and cool new tech is being developed every day we also decided to try one.  
We were feeling bored seeing sign in with google, so we decided to try  
the new amazing "Sign In With Ethereum" feature.   

We've heard `EIP - 4361` and `EIP - 191` are helpful.

Also, we have some requirements here:
Domain should be https://pctf.competitivecyber.club  
Chain Id should be 5  
Date Issued should be 2022-04-04T20:06:19Z  
Request Id should be 2113853211  
Nonce should be 13371337  
Resource should be https://pctf.competitivecyber.club/gimmeflag  

You must create a valid signature to access the hidden secret.  
Can you generate the signature and submit it to server?

`nc someserverip 8888`

Flag Format: PCTF{}

### Difficulty 
6/10 ?

### Flag
PCTF{Randomized_Values_Should_Be_Used_While_Signing_In_With_Ethereum}

### Hints
`siwe` implementations from `spruceid` is pretty cool and easy to use

### Author
Biplav

### Tester
None yet

### Writeup
```
Same given encrypted ethereum keystore file from Eetthheerr challenge should be used.
The password for the wallet file is "precious".  

The goal here is to create a valid EIP - 4361 Signature.

From the wallet, private key can be extracted, which can be used to sign message.  

Verification is performed via EIP - 191 using the address field of the message as the expected signer.  

If verification succeeds, the original public key is recovered, and flag is sent

Solution code is included in solution.go file

Server can be started with go run server.go  
```
