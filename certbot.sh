#!/bin/bash

# Can be used to override the source of the mounted volumes.
# e.g. to use the current directory as certbot's working directory, run:
# ```
#     CERTBOT_WORK_DIR=$(pwd) ./certbot.sh
# ```
config_dir="${CERTBOT_CONFIG_DIR-/etc/letsencrypt}"
work_dir="${CERTBOT_WORK_DIR-/var/lib/letsencrypt}"
log_dir="${CERTBOT_LOGS_DIR-/var/log/letsencrypt}"
script_dir="${SCRIPT_DIR-$(dirname "$(readlink -f "$BASH_SOURCE")")/gandi-livedns}"

function authentication_options {
  case $1 in
    certonly)
      echo \
        --preferred-challenges dns \
        --manual \
        --manual-auth-hook    /gandi-livedns/auth.py \
        --manual-cleanup-hook /gandi-livedns/cleanup.py
      ;;

    *)
      ;;
  esac
}

docker run \
    -it --rm \
    --name certbot \
    --volume "$config_dir:/etc/letsencrypt" \
    --volume "$work_dir:/var/lib/letsencrypt" \
    --volume "$log_dir:/var/log/letsencrypt" \
    --volume "$script_dir:/gandi-livedns" \
  certbot/certbot \
    "$@" \
    $(authentication_options $1)
