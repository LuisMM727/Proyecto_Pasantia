# supongamos que cada elemento es un dict, y la columna clave se llama "id"
a = [
    {"id": 1, "valor": "foo"},
    {"id": 2, "valor": "bar"},
    {"id": 3, "valor": "baz"},
]
b = [
    {"id": 2, "otro": 100},
    {"id": 3, "otro": 200},
]

# 1) construir un set de los ids en b
ids_b = {d["id"] for d in b}

# 2) filtrar a
a_filtrado = [d for d in a if d["id"] in ids_b]

print(a_filtrado)
# → [{'id': 2, 'valor': 'bar'}, {'id': 3, 'valor': 'baz'}]
