#!/bin/sh

# Generate a private key
openssl genpkey -algorithm RSA -out /certs/key.pem

# Generate a certificate signing request (CSR)
openssl req -new -key /certs/key.pem -out /certs/cert.csr -subj "/CN=localhost"

# Generate a self-signed certificate
openssl x509 -req -days 365 -in /certs/cert.csr -signkey /certs/key.pem -out /certs/cert.pem

# Execute the main application (replace with your actual command)
exec "$@"