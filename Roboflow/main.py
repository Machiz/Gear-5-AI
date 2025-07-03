from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import pprint
MY_KEY = "tx7I4BVTJr13AyXuOGfU"
img_path = "./Roboflow/img_1249.jpg"

def add_character(prd, agent):
    isRested = prd["height"] < 120

    agent["characters"].append({
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
    startX = 780
    pos = round((prd["x"] - startX)/CARD_WIDTH) + 1

    return pos

def format_main_cards(prd, agent):
    if(prd["y"] > 740 and prd["y"] < 780): # LEADER
        if(prd["x"] > 960 and prd["x"] < 1040):
            agent["leader"].append(prd)

    elif(prd["x"] < 600 and prd["y"] < 900): # HAND
        agent["hand"].append(prd)

    elif(prd["y"] > 600 and prd["y"] < 640): # CHARACTER
        if(prd["x"] > 760 and prd["x"] < 1400):
            add_character(prd, agent)
            
    elif(prd["x"] > 1200 and prd["y"] > 900): # TRASH
        agent["trash"].append(prd)


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

result = {'inference_id': '263f6070-cdf2-4b1e-a0bb-db36f4108bb5', 'time': 0.5239047300001403, 'image': {'width': 1938, 'height': 1048}, 'predictions': [{'x': 1043.721923828125, 'y': 455.5909423828125, 'width': 92.154541015625, 'height': 129.5579833984375, 'confidence': 0.9733846187591553, 'class': 'OP09-009', 'class_id': 22, 'detection_id': 'bfa4d334-a7c4-4982-ab3f-7ef271756ed8'}, {'x': 783.3965148925781, 'y': 621.9437255859375, 'width': 91.34820556640625, 'height': 129.4576416015625, 'confidence': 
0.9602342247962952, 'class': 'ST17-005', 'class_id': 54, 'detection_id': '01db0b11-b225-4ed6-9db2-62817400cd3f'}, {'x': 924.0099487304688, 'y': 306.2315216064453, 'width': 125.7576904296875, 'height': 93.28829956054688, 'confidence': 0.956625759601593, 'class': 'OP09-001', 'class_id': 18, 'detection_id': '7a3eb37b-9b56-4aeb-89f9-7d8e8fe4bc70'}, {'x': 1273.1693725585938, 'y': 340.3908157348633, 'width': 91.9339599609375, 'height': 176.5775604248047, 'confidence': 0.9553887844085693, 'class': 'life', 'class_id': 58, 'detection_id': 'fe96d44d-ddb5-4a92-a9bb-57c966537a3c'}, {'x': 921.3798522949219, 'y': 160.43902587890625, 'width': 91.96551513671875, 'height': 128.72247314453125, 'confidence': 0.9543513655662537, 'class': 'don', 'class_id': 57, 'detection_id': '722abfe1-ded6-4e77-8fde-2314e511afa2'}, {'x': 1232.4838256835938, 'y': 913.6309814453125, 'width': 91.6295166015625, 'height': 128.7930908203125, 'confidence': 0.951657772064209, 'class': 'ST03-004', 'class_id': 48, 'detection_id': '069d5399-212b-433d-9810-29b1b8645da9'}, {'x': 907.6569213867188, 'y': 915.8786315917969, 'width': 207.900634765625, 'height': 132.45904541015625, 'confidence': 0.9491488337516785, 'class': 'don', 'class_id': 57, 'detection_id': 'a3fb424f-8289-4f86-9e61-c5287f5c9dc5'}, {'x': 665.6507568359375, 'y': 713.8352355957031, 'width': 92.293212890625, 'height': 222.20587158203125, 'confidence': 0.9474508762359619, 'class': 'life', 'class_id': 58, 'detection_id': 'c6373a8c-dee8-495d-8bc2-7319662e8554'}, {'x': 1014.0761108398438, 'y': 770.2548522949219, 'width': 95.1300048828125, 'height': 128.28033447265625, 'confidence': 0.940378725528717, 'class': 'OP01-060', 'class_id': 3, 'detection_id': 'f1f53c2d-814f-487e-8476-859f1a64830e'}, {'x': 1076.8697814941406, 'y': 160.9900665283203, 'width': 216.26263427734375, 'height': 93.51129150390625, 'confidence': 0.9384208917617798, 'class': 'don', 'class_id': 57, 'detection_id': '2eefdf02-debc-4c8a-a2a6-1890ff16253a'}, {'x': 1154.4879760742188, 'y': 455.4802551269531, 'width': 96.8245849609375, 'height': 130.33599853515625, 'confidence': 0.938327968120575, 'class': 'OP09-002', 'class_id': 19, 'detection_id': '42b8954f-21e6-49ab-9f7f-62c2fbf2fe49'}, {'x': 1005.3205871582031, 'y': 622.0296325683594, 'width': 96.61614990234375, 'height': 132.43243408203125, 'confidence': 0.9369170665740967, 'class': 'OP01-077', 'class_id': 4, 'detection_id': '926e791d-4ca1-4472-97bd-68db3198c6fe'}, {'x': 881.1202697753906, 'y': 699.3377990722656, 'width': 98.86517333984375, 'height': 65.92376708984375, 'confidence': 0.9050725698471069, 'class': 'attached_don', 'class_id': 56, 'detection_id': '5c1d89ea-8e23-4b4d-ac56-478c4b01b9e8'}, {'x': 894.3143615722656, 'y': 621.7731323242188, 'width': 126.62091064453125, 'height': 96.1878662109375, 'confidence': 0.9019573926925659, 'class': 'ST17-002', 'class_id': 51, 'detection_id': '92b29124-e9e3-4e17-88af-a113e9103fd7'}, {'x': 778.2003784179688, 'y': 916.7565612792969, 'width': 49.74462890625, 'height': 90.75775146484375, 'confidence': 0.8882855176925659, 'class': 'don', 'class_id': 57, 'detection_id': 'a11660e9-757e-49ee-80a4-07b8830e575b'}, {'x': 931.2197570800781, 'y': 454.40618896484375, 'width': 124.79473876953125, 'height': 95.8408203125, 'confidence': 0.5032228827476501, 'class': 'OP03-013', 'class_id': 6, 'detection_id': '4c980742-604d-48bd-9f1a-4f695ae5d87c'}]}

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
        
        format_main_cards(prd, player)

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
        format_main_cards(prd, enemy)

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
    for character in enemy["characters"]:
        if(character["position"] == dones["position"]):
            character["attached_don"] = dones["count"]
            continue
for dones in player["attached_don"]:
    for character in player["characters"]:
        if(character["position"] == dones["position"]):
            character["attached_don"] = dones["count"]
            continue

    
print(result)

print("\n")
print("\n")
print("---🔵 JUGADOR---")
pprint.pprint(player)

print("\n")
print("---🔴 ENEMIGO---")
pprint.pprint(enemy)


    
