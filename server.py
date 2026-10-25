#!/usr/bin/env venv/bin/python

import threading
import requests
from flask import Flask, jsonify, request


def create_app(name: str, initial: list[str], peer_url: str) -> Flask:
    app = Flask(name)


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
            return jsonify(error="Такой продукт уже есть в списке"), 409

        products.append(name)
        return jsonify(product=name, products=products), 201


    @app.post("/sync")
    def sync():
        try:
            response = requests.get(f"{peer_url}/products", timeout=5)
            response.raise_for_status()
        except requests.RequestException as err:
            return jsonify(error=f"Не удалось получить данные от второго сервера: {err}"), 502

        peer_products = response.json().get("products", [])
        if not isinstance(peer_products, list):
            peer_products = []

        added = []
        for item in peer_products:
            if item not in products:
                products.append(item)
                added.append(item)

        return jsonify(added=added, products=products)

    return app


def run_server(app: Flask, port: int) -> None:
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    app1 = create_app(
        "server1",
        initial=["Хлеб", "Молоко"],
        peer_url="http://127.0.0.1:5002",
    )

    app2 = create_app(
        "server2",
        initial=["Молоко", "Сыр", "Яблоко"],
        peer_url="http://127.0.0.1:5001",
    )

    t1 = threading.Thread(target=run_server, args=(app1, 5001), daemon=True)
    t2 = threading.Thread(target=run_server, args=(app2, 5002), daemon=True)

    t1.start()
    t2.start()

    print("Сервер 1: http://127.0.0.1:5001")
    print("Сервер 2: http://127.0.0.1:5002")

    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("\nОстановка серверов")