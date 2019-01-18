Derived from [sblaisot/certbot-dns-01-authenticators]

This fork fixes a few issues we met for our use-case:
- compatibility with python 2 for use with the [certbot/certbot] Docker image
- works with multiple domains (e.g. base domain AND wildcard subdomains)

[sblaisot/certbot-dns-01-authenticators]: https://github.com/sblaisot/certbot-dns-01-authenticators]
[certbot/certbot]: https://hub.docker.com/r/certbot/certbot

## Example usage

```bash
docker run -it --rm \
    --name certbot \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --volume "$(pwd)/gandi-livedns:/gandi-livedns" \
  certbot/certbot certonly \
    --manual \
    --manual-auth-hook /gandi-livedns/auth.py \
    --manual-cleanup-hook /gandi-livedns/cleanup.py \
    --domains example.com,*.example.com
```
