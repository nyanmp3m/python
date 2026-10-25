#!/usr/bin/env venv/bin/python

import threading
import requests
from flask import Flask, jsonify, request


def create_master_app(initial: list[str], replicas: list[str]) -> Flask:
    app = Flask('master')


    products: list[str] = list(initial)


    @app.get("/products")
    def get_products():
        return jsonify(products=products)


    @app.post("/products")
    def add_product():
        data = request.get_json(silent=True) or {}
        name = data.get("name")

        if not isinstance(name, str) or not name.strip():
            return jsonify(error='Поле "name" обязательно и должно быть непустой строкой'), 400

        name = name.strip()

        if name in products:
            return jsonify(error=f"Такой продукт уже есть в списке, продукты: {products}"), 409

        products.append(name)
        return jsonify(product=name, products=products), 201


    @app.post("/sync")
    def sync():
        return jsonify(
            error="Я ЕСТЬ ИСТОЧНИК ПРАВДЫ!"
        ), 405

    return app


def create_slave_app(name: str, initial: list[str]) -> Flask:

    app = Flask(name)


    products: list[str] = list(initial)


    @app.get("/products")
    def get_products():
        return jsonify(products=products)


    @app.post("/products")
    def add_product():
        return jsonify(
            error='Добавление продуктов на сервер раба запрещено'
        ), 403


    @app.post("/sync")
    def sync():
        return jsonify(
            error='Синхронизация на сервере раба запрещена'
        ), 403

    @app.post("/replicate")
    def replicate():
        data = request.get_json(silent=True) or {}
        new_products = data.get("products")

        if not isinstance(new_products, list) or not all(isinstance(x, str) for x in new_products):
            return jsonify(error='Поле "products" должно быть массивом строк'), 400

        products.clear()
        products.extend(new_products)
        return jsonify(ok=True, products=products)


    return app


def run_server(app: Flask, port: int) -> None:
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    REPLICA_1 = "http://127.0.0.1:5001"
    REPLICA_2 = "http://127.0.0.1:5002"

    master  = create_master_app(initial=["Хлеб", "Молоко"], replicas=[REPLICA_1, REPLICA_2])
    replica1 = create_slave_app("replica1", initial=["Хлеб", "Молоко"])
    replica2 = create_slave_app("replica2", initial=["Хлеб", "Молоко"])

    threads = [
        threading.Thread(target=run_server, args=(master,   5000), daemon=True),
        threading.Thread(target=run_server, args=(replica1, 5001), daemon=True),
        threading.Thread(target=run_server, args=(replica2, 5002), daemon=True),
    ]
    for t in threads:
        t.start()

    print("Мастер:  http://127.0.0.1:5000")
    print("Реплика: http://127.0.0.1:5001")
    print("Реплика: http://127.0.0.1:5002")

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\nОстановка серверов")