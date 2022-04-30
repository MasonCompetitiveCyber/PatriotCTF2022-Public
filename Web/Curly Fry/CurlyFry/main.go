package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func rootHandler(w http.ResponseWriter, r *http.Request) {
	path := "." + r.URL.String()

	if path == "./" {
		http.ServeFile(w, r, "./index.html")
		return
	}

	if _, err := os.Stat(path); err != nil {
		fmt.Fprintf(w, "The path provided is not a file or does not exist.")
		return
	}

	f, err := os.Open(path)
	if err != nil {
		http.Error(w, r.RequestURI, http.StatusNotFound)
		return
	}
	defer f.Close()

	fi, err := f.Stat()
	if err != nil {
		http.Error(w, r.RequestURI, http.StatusNotFound)
		return
	}
	modTime := fi.ModTime()

	http.ServeContent(w, r, path, modTime, f)
}

func main() {
	http.HandleFunc("/", rootHandler)

	fmt.Printf("Starting server at port 8080\n")
	if err := http.ListenAndServe(":80", nil); err != nil {
		log.Fatal(err)
	}
}
