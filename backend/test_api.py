#!/usr/bin/env python3
"""
Script de prueba para verificar que el backend funciona correctamente.
Ejecutar después de configurar .env
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000/auth"

def test_register():
    data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "TestPass123!",
        "password_check": "TestPass123!"
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Register: {response.status_code} - {response.json()}")
    return response.json().get("token")

def test_login():
    data = {
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Login: {response.status_code} - {response.json()}")
    return response.json().get("token")

def test_create_task(token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "titulo": "Tarea de prueba",
        "descripcion": "Descripción de prueba",
        "estado": "pendiente"
    }
    response = requests.post(f"{BASE_URL}/tareas", json=data, headers=headers)
    print(f"Create Task: {response.status_code} - {response.json()}")

def test_get_tasks(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/tareas", headers=headers)
    print(f"Get Tasks: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    print("=== PRUEBAS DE BETODO BACKEND ===")
    try:
        token = test_register()
        if token:
            test_create_task(token)
            test_get_tasks(token)
        else:
            token = test_login()
            if token:
                test_create_task(token)
                test_get_tasks(token)
    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de que el servidor esté ejecutándose y .env esté configurado")