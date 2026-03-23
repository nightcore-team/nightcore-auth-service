



## Generate public and private keys
```bash
# private
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048

# public
openssl rsa -pubout -in private.pem -out public.pem
```

### Convert .pem keys to base64 string:
```bash
base64 -w 0 private.pem
base64 -w 0 public.pem
```

### Pass base64 string to .env file:
```bash
JWT_PUBLIC_KEY=...
JWT_PRIVATE_KEY=...
```