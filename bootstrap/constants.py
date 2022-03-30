"""Web project initialization CLI constants."""

# Env vars

GITLAB_TOKEN_ENV_VAR = "GITLAB_PRIVATE_TOKEN"

# Media storage

MEDIA_STORAGE_DEFAULT = "s3-digitalocean"

MEDIA_STORAGE_CHOICES = ["local", MEDIA_STORAGE_DEFAULT, "none"]
