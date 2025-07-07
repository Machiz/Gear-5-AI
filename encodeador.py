# encodeador.py

def encode_state(player, enemy):
    carta_vocab = [
        "OP09-001", "OP03-013", "OP09-002", "OP09-009", "ST03-004",
        "OP01-060", "OP01-077", "ST17-005", "ST17-002"
    ]
    zonas = ["hand", "battle", "trash", "life", "leader"]
    estados = ["active", "rested", "none"]

    def one_hot(value, options):
        return [1 if value == opt else 0 for opt in options]

    encoded = []

    # Cartas propias
    for carta in player["leader"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("leader", zonas)
        estado = "rested" if carta["isRested"] else "active"
        encoded += one_hot(estado, estados)

    for carta in player["characters"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("battle", zonas)
        estado = "rested" if carta["isRested"] else "active"
        encoded += one_hot(estado, estados)

    for carta in player["hand"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("hand", zonas)
        encoded += one_hot("none", estados)

    for carta in player["trash"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("trash", zonas)
        encoded += one_hot("none", estados)

    # Cartas del enemigo
    for carta in enemy["leader"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("leader", zonas)
        estado = "rested" if carta["isRested"] else "active"
        encoded += one_hot(estado, estados)

    for carta in enemy["characters"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("battle", zonas)
        estado = "rested" if carta["isRested"] else "active"
        encoded += one_hot(estado, estados)

    for carta in enemy["trash"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("trash", zonas)
        encoded += one_hot("none", estados)

    # Recursos
    encoded.append(player["don"] / 10)
    encoded.append((player["don"] + player["rested_don"]) / 10)
    encoded.append(player["life"] / 5)
    encoded.append(enemy["life"] / 5)

    return encoded
