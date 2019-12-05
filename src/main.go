package main

import (
	"bufio"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/csv"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

func storeCertificate(cert *x509.Certificate, writer *csv.Writer, domain string) {

	if v := cert.PublicKeyAlgorithm.String(); v == "RSA" {
		if w := cert.Issuer.Organization[0]; w != "Digital Signature Trust Co." {
			var data []string
			// Get Issuer Organization
			data = append(data, domain[:len(domain)-4])
			data = append(data, cert.Issuer.Organization[0])
			rsaPublicKey := cert.PublicKey.(*rsa.PublicKey)
			data = append(data, rsaPublicKey.N.String())
			data = append(data, strconv.Itoa(rsaPublicKey.E))
			data = append(data, strconv.Itoa(rsaPublicKey.Size()))
			writer.Write(data)
			writer.Flush()
		}
	}

	//}
}

func analyzeDomain(domain string, writer *csv.Writer) {
	fmt.Println("analyzing", domain)
	dialer := net.Dialer{}
	dialer.Timeout = 10 * time.Second
	conn, err := tls.DialWithDialer(&dialer, "tcp", domain, &tls.Config{
		InsecureSkipVerify: true,
	})
	if err != nil {
		fmt.Println(fmt.Sprintf("\x1b[31;1mfailed to connect to %s", domain), err, "\x1b[0m")
		return
	}
	defer conn.Close()
	for _, cert := range conn.ConnectionState().PeerCertificates {
		storeCertificate(cert, writer, domain)
	}
}

func analyzeDomains(queue chan string, writer *csv.Writer) {
	for {
		domain := <-queue
		analyzeDomain(domain, writer)
	}
}

func main() {
	// Creates a channel
	cs := make(chan string)

	// Creates result.csv
	file, err := os.Create("result.csv")

	//Verifies that the file has been created
	checkError("Cannot create file", err)
	defer file.Close()
	writer := csv.NewWriter(file)
	defer writer.Flush()
	for i := 0; i < 80; i++ {
		go analyzeDomains(cs, writer)
	}

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if !strings.Contains(line, ":") {
			line = line + ":443"
		}
		cs <- line
	}
	time.Sleep(2 * time.Second)
}

func checkError(message string, err error) {
	if err != nil {
		log.Fatal(message, err)
	}
}
