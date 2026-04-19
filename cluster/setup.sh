#!/bin/bash

echo "Starting Minikube..."
minikube start --driver=docker

echo "Enabling metrics..."
minikube addons enable metrics-server

echo "Deploying app..."
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/microservices-demo/main/release/kubernetes-manifests.yaml

echo "Checking pods..."
kubectl get pods
