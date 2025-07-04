import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import pprint
MY_KEY = "tx7I4BVTJr13AyXuOGfU"
img_path = "./Roboflow/img_1753.jpg"

def add_card(prd, agent, type):
    isRested = prd["height"] < 120

    agent[type].append({
        "class":prd["class"],
        "position": pos_in_table(prd),
        "x": prd["x"],
        "y": prd["y"],
        "confidence":prd["confidence"],
        "isRested":isRested,
        "attached_don":0
    })

def pos_in_table(prd):
    pos = 0
    if(prd["y"] > 800 or prd["y"] < 430):
        # attached don pertenece al leader
        pos = -1
    else:
        # attached don pertenece a algun character del tablero
        startX = 780
        pos = round((prd["x"] - startX)/CARD_WIDTH) + 1
    return pos

def format_main_cards_player(prd, agent):
    if(prd["y"] > 740 and prd["y"] < 780): # LEADER
        if(prd["x"] > 960 and prd["x"] < 1040):
            add_card(prd, agent, "leader")

    elif(prd["x"] < 600 and prd["y"] < 950): # HAND
        add_card(prd, agent, "hand")

    elif(prd["y"] > 600 and prd["y"] < 640): # CHARACTER
        if(prd["x"] > 760 and prd["x"] < 1400):
            add_card(prd, agent, "characters")
            
    elif(prd["x"] > 1200 and prd["y"] > 900): # TRASH
        agent["trash"].append(prd)


def format_main_cards_enemy(prd, agent):
    if(prd["y"] > 290 and prd["y"] < 360): # LEADER
        if(prd["x"] > 900 and prd["x"] < 940):
            add_card(prd, agent, "leader")

    elif(prd["x"] < 300 and prd["y"] < 170): # TRASH
        agent["trash"].append(prd)

    elif(prd["y"] > 430 and prd["y"] < 470): # CHARACTER
        if(prd["x"] > 680 and prd["x"] < 1200):
            add_card(prd, agent, "characters")
    

CARD_WIDTH = 95 #aprox
RESTED_cARD_WIDTH = 125 #aprox

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=MY_KEY,
    
)

configuration = InferenceConfiguration(
    confidence_threshold=0.5
)

# CLIENT.configure(configuration)

# result = CLIENT.infer(img_path, model_id="card-detection-hbgys/4")

## RESULTADO PRECOMPILADO DE LA IMAGEN 1486
result = {'inference_id': '263f6070-cdf2-4b1e-a0bb-db36f4108bb5', 'time': 0.5239047300001403, 'image': {'width': 1938, 'height': 1048}, 'predictions': [{'x': 1043.721923828125, 'y': 455.5909423828125, 'width': 92.154541015625, 'height': 129.5579833984375, 'confidence': 0.9733846187591553, 'class': 'OP09-009', 'class_id': 22, 'detection_id': 'bfa4d334-a7c4-4982-ab3f-7ef271756ed8'}, {'x': 783.3965148925781, 'y': 621.9437255859375, 'width': 91.34820556640625, 'height': 129.4576416015625, 'confidence': 
0.9602342247962952, 'class': 'ST17-005', 'class_id': 54, 'detection_id': '01db0b11-b225-4ed6-9db2-62817400cd3f'}, {'x': 924.0099487304688, 'y': 306.2315216064453, 'width': 125.7576904296875, 'height': 93.28829956054688, 'confidence': 0.956625759601593, 'class': 'OP09-001', 'class_id': 18, 'detection_id': '7a3eb37b-9b56-4aeb-89f9-7d8e8fe4bc70'}, {'x': 1273.1693725585938, 'y': 340.3908157348633, 'width': 91.9339599609375, 'height': 176.5775604248047, 'confidence': 0.9553887844085693, 'class': 'life', 'class_id': 58, 'detection_id': 'fe96d44d-ddb5-4a92-a9bb-57c966537a3c'}, {'x': 921.3798522949219, 'y': 160.43902587890625, 'width': 91.96551513671875, 'height': 128.72247314453125, 'confidence': 0.9543513655662537, 'class': 'don', 'class_id': 57, 'detection_id': '722abfe1-ded6-4e77-8fde-2314e511afa2'}, {'x': 1232.4838256835938, 'y': 913.6309814453125, 'width': 91.6295166015625, 'height': 128.7930908203125, 'confidence': 0.951657772064209, 'class': 'ST03-004', 'class_id': 48, 'detection_id': '069d5399-212b-433d-9810-29b1b8645da9'}, {'x': 907.6569213867188, 'y': 915.8786315917969, 'width': 207.900634765625, 'height': 132.45904541015625, 'confidence': 0.9491488337516785, 'class': 'don', 'class_id': 57, 'detection_id': 'a3fb424f-8289-4f86-9e61-c5287f5c9dc5'}, {'x': 665.6507568359375, 'y': 713.8352355957031, 'width': 92.293212890625, 'height': 222.20587158203125, 'confidence': 0.9474508762359619, 'class': 'life', 'class_id': 58, 'detection_id': 'c6373a8c-dee8-495d-8bc2-7319662e8554'}, {'x': 1014.0761108398438, 'y': 770.2548522949219, 'width': 95.1300048828125, 'height': 128.28033447265625, 'confidence': 0.940378725528717, 'class': 'OP01-060', 'class_id': 3, 'detection_id': 'f1f53c2d-814f-487e-8476-859f1a64830e'}, {'x': 1076.8697814941406, 'y': 160.9900665283203, 'width': 216.26263427734375, 'height': 93.51129150390625, 'confidence': 0.9384208917617798, 'class': 'don', 'class_id': 57, 'detection_id': '2eefdf02-debc-4c8a-a2a6-1890ff16253a'}, {'x': 1154.4879760742188, 'y': 455.4802551269531, 'width': 96.8245849609375, 'height': 130.33599853515625, 'confidence': 0.938327968120575, 'class': 'OP09-002', 'class_id': 19, 'detection_id': '42b8954f-21e6-49ab-9f7f-62c2fbf2fe49'}, {'x': 1005.3205871582031, 'y': 622.0296325683594, 'width': 96.61614990234375, 'height': 132.43243408203125, 'confidence': 0.9369170665740967, 'class': 'OP01-077', 'class_id': 4, 'detection_id': '926e791d-4ca1-4472-97bd-68db3198c6fe'}, {'x': 881.1202697753906, 'y': 699.3377990722656, 'width': 98.86517333984375, 'height': 65.92376708984375, 'confidence': 0.9050725698471069, 'class': 'attached_don', 'class_id': 56, 'detection_id': '5c1d89ea-8e23-4b4d-ac56-478c4b01b9e8'}, {'x': 894.3143615722656, 'y': 621.7731323242188, 'width': 126.62091064453125, 'height': 96.1878662109375, 'confidence': 0.9019573926925659, 'class': 'ST17-002', 'class_id': 51, 'detection_id': '92b29124-e9e3-4e17-88af-a113e9103fd7'}, {'x': 778.2003784179688, 'y': 916.7565612792969, 'width': 49.74462890625, 'height': 90.75775146484375, 'confidence': 0.8882855176925659, 'class': 'don', 'class_id': 57, 'detection_id': 'a11660e9-757e-49ee-80a4-07b8830e575b'}, {'x': 931.2197570800781, 'y': 454.40618896484375, 'width': 124.79473876953125, 'height': 95.8408203125, 'confidence': 0.5032228827476501, 'class': 'OP03-013', 'class_id': 6, 'detection_id': '4c980742-604d-48bd-9f1a-4f695ae5d87c'}]}

## RESULTADO PRECOMPILADO DE LA IMAGEN 1753
# result = {'inference_id': 'e243b78f-7278-41c5-95ec-c56fb45733df', 'time': 0.7144953329998316, 'image': {'width': 1938, 'height': 1048}, 'predictions': [{'x': 1232.1525268554688, 'y': 912.1881408691406, 'width': 93.2762451171875, 'height': 130.63482666015625, 'confidence': 0.9753414988517761, 'class': 'OP01-077', 'class_id': 4, 'detection_id': '4c594424-508a-4da2-9779-889e9809124f'}, {'x': 820.7540283203125, 'y': 455.8093719482422, 'width': 91.5162353515625, 'height': 129.55508422851562, 'confidence': 0.9678700566291809, 'class': 'OP06-007', 'class_id': 9, 'detection_id': '19f3ac70-beda-4a56-a651-2c742138009e'}, {'x': 784.5562133789062, 'y': 621.7583312988281, 'width': 
# 94.104736328125, 'height': 128.37371826171875, 'confidence': 0.9631971120834351, 'class': 'EB01-023', 'class_id': 0, 'detection_id': '60f8744d-1963-4c4f-bbe7-b302ef226474'}, {'x': 1047.8402709960938, 'y': 454.4803924560547, 'width': 109.4320068359375, 'height': 92.22317504882812, 'confidence': 0.9590116143226624, 'class': 'OP09-009', 'class_id': 22, 'detection_id': '5927a37f-bb49-4849-b4a5-e3ad64e94374'}, {'x': 665.3798217773438, 'y': 725.5673522949219, 'width': 93.138671875, 'height': 199.49896240234375, 'confidence': 0.9585884809494019, 'class': 'life', 'class_id': 58, 'detection_id': '5f3cdfd6-aeb9-48ad-9122-b7fffa906cb1'}, {'x': 158.05708694458008, 'y': 937.0823974609375, 'width': 90.52776336669922, 'height': 127.6749267578125, 'confidence': 0.9578992128372192, 'class': 'OP07-040', 'class_id': 13, 'detection_id': 'c53ba784-5c80-42be-8cd4-20db215d9deb'}, {'x': 924.1362609863281, 'y': 306.2118225097656, 'width': 126.03302001953125, 'height': 92.63916015625, 'confidence': 0.9572929739952087, 'class': 'OP09-001', 'class_id': 18, 'detection_id': '126e8a4f-1059-4b5f-a7c1-985a30000e17'}, {'x': 1272.8953247070312, 'y': 329.24095153808594, 'width': 91.7303466796875, 'height': 153.42837524414062, 'confidence': 0.9571518301963806, 'class': 'life', 'class_id': 58, 'detection_id': '0b9e628f-1f38-4d8c-b11d-62d7174b6ca2'}, {'x': 931.7891235351562, 'y': 455.1832275390625, 'width': 126.6734619140625, 'height': 94.38433837890625, 'confidence': 0.9554445147514343, 'class': 'OP03-013', 'class_id': 6, 'detection_id': 'e72dbf6d-08bb-494b-94b4-0f44248c0dad'}, {'x': 992.6255493164062, 'y': 160.7342071533203, 'width': 375.9632568359375, 'height': 94.329345703125, 'confidence': 0.9400933384895325, 'class': 'don', 'class_id': 57, 'detection_id': '83986c74-2a04-49b2-bf78-f842b37fef5b'}, {'x': 1013.7852783203125, 'y': 767.9011840820312, 'width': 100.12939453125, 'height': 128.307373046875, 'confidence': 0.9362618923187256, 'class': 'OP01-060', 'class_id': 3, 'detection_id': 'd5a47bb7-5fcf-4cb8-af20-6cbd754845b7'}, {'x': 1154.3466186523438, 'y': 455.5942840576172, 'width': 95.6029052734375, 'height': 130.14163208007812, 'confidence': 0.9300102591514587, 'class': 'OP09-002', 'class_id': 19, 'detection_id': '9c01d5e2-a9c2-4098-a34c-5a34cf1800ba'}, {'x': 821.2439575195312, 'y': 916.466552734375, 'width': 126.5791015625, 'height': 94.268798828125, 'confidence': 0.9299609661102295, 'class': 'don', 'class_id': 57, 'detection_id': 'c2e08f8f-2d34-42ac-ae96-cc325a7e5a8f'}, {'x': 250.98523712158203, 'y': 936.9953918457031, 'width': 89.74015808105469, 'height': 128.58331298828125, 'confidence': 0.9237920045852661, 'class': 'OP07-040', 'class_id': 13, 'detection_id': 'a18c102a-d45f-4fb0-b625-50ee59c47e0b'}, {'x': 947.2006225585938, 'y': 916.17431640625, 'width': 121.9598388671875, 'height': 129.3787841796875, 'confidence': 0.9034671783447266, 'class': 'don', 'class_id': 57, 'detection_id': '30c3f6e2-d166-4294-ab56-4cf8b51dafe0'}, {'x': 1006.0836486816406, 'y': 859.7289733886719, 'width': 96.94671630859375, 'height': 57.81927490234375, 'confidence': 0.8922500014305115, 'class': 'attached_don', 'class_id': 56, 'detection_id': '536df635-7bf4-4fb7-94bc-05764397ce05'}]}

player = {
    "leader": [],
    "hand": [],
    "characters":[],
    "don" : 0,
    "rested_don": 0,
    "attached_don": [],
    "trash" : [],
    "life": 0 
}
enemy = {
    "leader": [],
    "hand": [],
    "characters":[],
    "don" : 0,
    "rested_don": 0,
    "attached_don": [],
    "trash" : [],
    "life": 0 
}



for prd in result["predictions"]:
    if (prd["y"] > 600): # Si su "y" es mayor a 600, es una carta del jugador.
        
        format_main_cards_player(prd, player)

        if(prd["class"] == "don"): # RESTED DON Y DON
            if(prd["height"] > 110): # Se determina si no es rested por su altura.
                don_count = round(((prd["width"] - 95.7) / 28) + 1)
                player["don"] = don_count
            else:
                don_count = round(((prd["width"] - 50) / 28) + 1)
                player["rested_don"] = don_count

        elif(prd["class"] == "attached_don"):
            don_count = round(((prd["height"] - 44) / 11) + 1)
            player["attached_don"].append({
                "x":prd["x"],
                "y":prd["y"],
                "witdh":prd["width"],
                "height":prd["height"],
                "position": pos_in_table(prd),
                "count":don_count
                })
            continue

        elif(prd["class"] == "life"):
            life_count = round(((prd["height"] - 131) / 26) + 1)
            player["life"] = life_count

    else: # MAZO DEL ENEMIGO
        format_main_cards_enemy(prd, enemy)

        if(prd["class"] == "don"): # RESTED DON Y DON
            if(prd["height"] > 110): # Se determina si no es rested por su altura.
                don_count = round(((prd["width"] - 95.7) / 28) + 1)
                enemy["don"] = don_count
                continue
            else:
                don_count = round(((prd["width"] - 50) / 28) + 1)
                enemy["rested_don"] = don_count
                continue

        if(prd["class"] == "attached_don"): # ATTACHED DON
            don_count = round(((prd["height"] - 44) / 11) + 1)
            enemy["attached_don"].append({
                "x":prd["x"],
                "y":prd["y"],
                "witdh":prd["width"],
                "height":prd["height"],
                "position": pos_in_table(prd),
                "count":don_count
                })
            continue

        if(prd["class"] == "life"): # LIFE
            life_count = round(((prd["height"] - 131) / 26) + 1)
            enemy["life"] = life_count
            continue

# Se asigna a cada carta su cantidad de attached don, en caso tenga.
# Se evalua la posición actual del don y del character para revisar si le pertenece el attached don
# Este chequeo se hace despues de leer todas las predicciones para esperar a leer todos los attached don.
for dones in enemy["attached_don"]:
    if(dones["position"] == -1):
        enemy["leader"][0]["attached_don"] = dones["count"]
        continue
    for character in enemy["characters"]:
        if(character["position"] == dones["position"]):
            character["attached_don"] = dones["count"]
            continue
    
for dones in player["attached_don"]:
    if(dones["position"] == -1):
        player["leader"][0]["attached_don"] = dones["count"]
        continue
    for character in player["characters"]:
        if(character["position"] == dones["position"]):
            character["attached_don"] = dones["count"]
            continue

# print("\n")
# print("\n")
# print("---🔵 JUGADOR---")
# pprint.pprint(player)

# print("\n")
# print("---🔴 ENEMIGO---")
# pprint.pprint(enemy)

state = {
    "propias": [
        {"nombre": "Luffy", "zona": "battle", "estado": "active", "poder": 5000},
        {"nombre": "Zoro", "zona": "battle", "estado": "rested", "poder": 5000},
        {"nombre": "Sanji", "zona": "hand", "estado": "none", "poder": 4000},
    ],
    "rival": [
        {"nombre": "Robin", "zona": "battle", "estado": "rested", "poder": 3000},
        {"nombre": "Usopp", "zona": "battle", "estado": "active", "poder": 2000},
    ],
    "recursos": {
        "don_activo": 5,
        "don_total": 7,
        "vidas": 3
    },
    "rival_recursos": {
        "vidas": 2
    }
}
    
def encode_ref(state):
    # Ejemplo con vocabulario limitado
    carta_vocab = ["OP09-001", "OP03-013", "OP09-002", "OP09-009", "ST03-004", "OP01-060", "OP01-077", "ST17-005", "ST17-002", "ST03-004", ]
    zonas = ["hand", "battle", "trash", "life", "leader"]
    estados = ["active", "rested", "none"]

    def one_hot(value, options):
        return [1 if value == opt else 0 for opt in options]

    encoded = []

    # Codificar cartas propias
    for carta in state["propias"]:
        encoded += one_hot(carta["nombre"], carta_vocab)
        encoded += one_hot(carta["zona"], zonas)
        encoded += one_hot(carta["estado"], estados)
        # encoded.append(carta["poder"] / 10000)  # Normalizado

    # Igual con cartas del rival
    for carta in state["rival"]:
        encoded += one_hot(carta["nombre"], carta_vocab)
        encoded += one_hot(carta["zona"], zonas)
        encoded += one_hot(carta["estado"], estados)
        # encoded.append(carta["poder"] / 10000)

    # Recursos
    encoded.append(state["recursos"]["don_activo"] / 10)
    encoded.append(state["recursos"]["don_total"] / 10)
    encoded.append(state["recursos"]["vidas"] / 5)
    encoded.append(state["rival_recursos"]["vidas"] / 5)

    # return torch.tensor([encoded], dtype=torch.float32)
    return encoded

def encode_state(player, enemy):
    # Ejemplo con vocabulario limitado
    carta_vocab = ["OP09-001", "OP03-013", "OP09-002", "OP09-009", "ST03-004", "OP01-060", "OP01-077", "ST17-005", "ST17-002", "ST03-004", ]
    zonas = ["hand", "battle", "trash", "life", "leader"]
    estados = ["active", "rested", "none"]

    def one_hot(value, options):
        return [1 if value == opt else 0 for opt in options]

    encoded = []

    # Codificar cartas propias
    
    for carta in enemy["leader"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("leader", zonas)
        
        estado = "rested" if(carta["isRested"]) else "active"
        encoded += one_hot(estado, estados)
    for carta in player["characters"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("battle", zonas)
        estado = "rested" if(carta["isRested"]) else "active"
        encoded += one_hot(estado, estados)
        # encoded.append(carta["poder"] / 10000)  # Normalizado
    for carta in player["hand"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("hand", zonas)
        encoded += one_hot("none", estados)
    for carta in player["trash"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("trash", zonas)
        encoded += one_hot("none", estados)

    # Igual con cartas del rival
    for carta in enemy["leader"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("leader", zonas)
        estado = "rested" if(carta["isRested"]) else "active"
        encoded += one_hot(estado, estados)
    for carta in enemy["characters"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("battle", zonas)
        estado = "rested" if(carta["isRested"]) else "active"
        encoded += one_hot(estado, estados)
        # encoded.append(carta["poder"] / 10000)
    for carta in enemy["trash"]:
        encoded += one_hot(carta["class"], carta_vocab)
        encoded += one_hot("trash", zonas)
        encoded += one_hot("none", estados)

    # Recursos
    encoded.append(player["don"] / 10)
    encoded.append((player["don"] + player["rested_don"]) / 10)
    encoded.append(player["life"] / 5)
    encoded.append(enemy["life"] / 5)

    # return torch.tensor([encoded], dtype=torch.float32)
    return encoded

print(encode_state(player, enemy))
