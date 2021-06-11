#!/usr/bin/env bash

set -euo pipefail

kubectl config set-cluster my-cluster --server=$KUBE_URL --certificate-authority="$KUBE_CA_PEM_FILE"
kubectl config set-credentials admin --token=$KUBE_TOKEN
kubectl config set-context my-context --cluster=my-cluster --user=admin --namespace=default
kubectl config use-context my-context
cp -r /app/k8s/$CI_ENVIRONMENT_SLUG /tmp/k8s
sed -i "s/__IMAGE_TAG__/$DEPLOY_VERSION/" /tmp/k8s/1_backend.yaml
kubectl apply -f /tmp/k8s
