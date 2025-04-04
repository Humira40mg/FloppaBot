from random import randint, sample
from PIL import Image, ImageChops
import tempfile
import discord
import datetime

def get_user_data(user_id):
    with open(f"users/{user_id}.txt","r") as usersave:
        return usersave.readlines()
    
def save_user_data(user_id, data):
    with open(f"users/{user_id}.txt","w") as usersave:
        usersave.writelines(data)
        
mythicaldico={
    1: {
        False: {
            "path": "./images/floppas/mythobscur.png",
            "name": "Maître des Arts Sombres",
            "category": "red"
        },
        True: {
            "path": "./images/shinyfloppa/mythobscur.png",
            "name": "✨Maître des Arts Sombres✨",
            "category": "red"
        }
    },
    2: {
        False: {
            "path": "./images/floppas/mythbatman.png",
            "name": "BatFloppa",
            "category": "red"
        },
        True: {
            "path": "./images/shinyfloppa/mythbatman.png",
            "name": "✨BatFloppa✨",
            "category": "red"
        }
    },
    3: {
        False: {
            "path": "./images/floppas/mythdieu.png",
            "name": "Dieu Floppa",
            "category": "red"
        },
        True: {
            "path": "./images/shinyfloppa/mythdieu.png",
            "name": "✨Dieu Floppa✨",
            "category": "red"
        }
    },
    4: {
        False: {
            "path": "./images/floppas/mythfloppasupremacy.png",
            "name": "Floppa Supremacy",
            "category": "red"
        },
        True: {
            "path": "./images/shinyfloppa/mythfloppasupremacy.png",
            "name": "✨Floppa Supremacy✨",
            "category": "red"
        }
    },
    5: {
        False: {
            "path": "./images/floppas/mythogfloppa.png",
            "name": "Original Big Floppa",
            "category": "red"
        },
        True: {
            "path": "./images/shinyfloppa/mythogfloppa.png",
            "name": "✨Original Big Floppa✨",
            "category": "red"
        }
    }
}
legendarydico = {
    6: {
        False: {
            "path": "./images/floppas/legboplarbear.png",
            "name": "Polar Floppa",
            "category": "gold"
        },
        True: {
            "path": "./images/shinyfloppa/legboplarbear.png",
            "name": "✨Polar Floppa✨",
            "category": "gold"
        }
    },
    7: {
        False: {
            "path": "./images/floppas/leglicorne.png",
            "name": "Flomas",
            "category": "gold"
        },
        True: {
            "path": "./images/shinyfloppa/leglicorne.png",
            "name": "✨Flomas✨",
            "category": "gold"
        }
    },
    8: {
        False: {
            "path": "./images/floppas/legnezuko.png",
            "name": "Libeloul Arc en ciel",
            "category": "gold"
        },
        True: {
            "path": "./images/shinyfloppa/legnezuko.png",
            "name": "✨Libeloul Arc en ciel✨",
            "category": "gold"
        }
    },
    9: {
        False: {
            "path": "./images/floppas/legroi.png",
            "name": "King Floppa",
            "category": "gold"
        },
        True: {
            "path": "./images/shinyfloppa/legroi.png",
            "name": "✨King Floppa✨",
            "category": "gold"
        }
    },
    10: {
        False: {
            "path": "./images/floppas/legsukuna.png",
            "name": "SukuFloppa",
            "category": "gold"
        },
        True: {
            "path": "./images/shinyfloppa/legsukuna.png",
            "name": "✨SukuFloppa✨",
            "category": "gold"
        }
    },
    11: {
        False: {
            "path": "./images/floppas/legbragi.png",
            "name": "Flobbragi",
            "category": "gold"
        },
        True: {
            "path": "./images/shinyfloppa/legbragi.png",
            "name": "✨Flobbragi✨",
            "category": "gold"
        }
    }
}
epicdico = {
    12: {
        False: {
            "path": "./images/floppas/epiccurrency.png",
            "name": "Floppa Coin",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epiccurrency.png",
            "name": "✨Floppa Coin✨",
            "category": "purple"
        }
    },
    13: {
        False: {
            "path": "./images/floppas/epicdiego.png",
            "name": "Diego, The Floppa World",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epicdiego.png",
            "name": "✨Diego, The Floppa World✨",
            "category": "purple"
        }
    },
    14: {
        False: {
            "path": "./images/floppas/epichoga.png",
            "name": "FloppHoga",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epichoga.png",
            "name": "✨FloppHoga✨",
            "category": "purple"
        }
    },
    15: {
        False: {
            "path": "./images/floppas/epicjodio.png",
            "name": "Jodio Floppestar",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epicjodio.png",
            "name": "✨Jodio Floppestar✨",
            "category": "purple"
        }
    },
    16: {
        False: {
            "path": "./images/floppas/epicoasis.png",
            "name": "The Floppa of the Oasis",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epicoasis.png",
            "name": "✨The Floppa of the Oasis✨",
            "category": "purple"
        }
    },
    17: {
        False: {
            "path": "./images/floppas/epicsabo.png",
            "name": "Floppa Sabo",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epicsabo.png",
            "name": "✨Floppa Sabo✨",
            "category": "purple"
        }
    },
    18: {
        False: {
            "path": "./images/floppas/epicspaceodity.png",
            "name": "Floppa Oddity",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epicspaceodity.png",
            "name": "✨Floppa Oddity✨",
            "category": "purple"
        }
    },
    19: {
        False: {
            "path": "./images/floppas/epicswimpgod.png",
            "name": "Swimp Floppa",
            "category": "purple"
        },
        True: {
            "path": "./images/shinyfloppa/epicswimpgod.png",
            "name": "✨Swimp Floppa✨",
            "category": "purple"
        }
    }
}
raredico = {
    20: {
        False: {
            "path": "./images/floppas/raredark.png",
            "name": "Dark Floppa",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/raredark.png",
            "name": "✨Dark Floppa✨",
            "category": "blue"
        }
    },
    36: {
        False: {
            "path": "./images/floppas/comdorime.png",
            "name": "Floppa Dorime",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/comdorime.png",
            "name": "✨Floppa Dorime✨",
            "category": "blue"
        }
    },
    21: {
        False: {
            "path": "./images/floppas/raregun.png",
            "name": "Floppa Gun",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/raregun.png",
            "name": "✨Floppa Gun✨",
            "category": "blue"
        }
    },
    22: {
        False: {
            "path": "./images/floppas/rareleo.png",
            "name": "Fleksoppa",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/rareleo.png",
            "name": "✨Fleksoppa✨",
            "category": "blue"
        }
    },
    23: {
        False: {
            "path": "./images/floppas/rarerhum.png",
            "name": "Floppa Zacapa",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/rarerhum.png",
            "name": "✨Floppa Zacapa✨",
            "category": "blue"
        }
    },
    24: {
        False: {
            "path": "./images/floppas/raretopgun.png",
            "name": "Top Gun Floppa",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/raretopgun.png",
            "name": "✨Top Gun Floppa✨",
            "category": "blue"
        }
    },
    25: {
        False: {
            "path": "./images/floppas/raretrot.png",
            "name": "Floppa Trot.",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/raretrot.png",
            "name": "✨Floppa Trot.✨",
            "category": "blue"
        }
    },
    26: {
        False: {
            "path": "./images/floppas/raretw.png",
            "name": "The Floppa World",
            "category": "blue"
        },
        True: {
            "path": "./images/shinyfloppa/raretw.png",
            "name": "✨The Floppa World✨",
            "category": "blue"
        }
    }
}
uncomdico = {
    27: {
        False: {
            "path": "./images/floppas/uncomamerica.png",
            "name": "FloppAmericaaaaaa",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncomamerica.png",
            "name": "✨FloppAmericaaaaaa✨",
            "category": "green"
        }
    },
    28: {
        False: {
            "path": "./images/floppas/uncomnone.png",
            "name": "None Floppa",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncomnone.png",
            "name": "✨None Floppa✨",
            "category": "green"
        }
    },
    29: {
        False: {
            "path": "./images/floppas/uncompizza.png",
            "name": "FlopPizza",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncompizza.png",
            "name": "✨FlopPizza✨",
            "category": "green"
        }
    },
    30: {
        False: {
            "path": "./images/floppas/uncomrpg.png",
            "name": "FloppAsta la Floppista Baby",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncomrpg.png",
            "name": "✨FloppAsta la Floppista Baby✨",
            "category": "green"
        }
    },
    31: {
        False: {
            "path": "./images/floppas/uncomsacoche.png",
            "name": "Floppa in the Pocket",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncomsacoche.png",
            "name": "✨Floppa in the Pocket✨",
            "category": "green"
        }
    },
    32: {
        False: {
            "path": "./images/floppas/uncomsherif.png",
            "name": "Floppa Shérif",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncomsherif.png",
            "name": "✨Floppa Shérif✨",
            "category": "green"
        }
    },
    33: {
        False: {
            "path": "./images/floppas/uncomwut.png",
            "name": "FloWHAT",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncomwut.png",
            "name": "✨FloWHAT✨",
            "category": "green"
        }
    },
    34: {
        False: {
            "path": "./images/floppas/uncomstare.png",
            "name": "Floppa stare at you",
            "category": "green"
        },
        True: {
            "path": "./images/shinyfloppa/uncomstare.png",
            "name": "✨Floppa stare at you✨",
            "category": "green"
        }
    }
}
commondico = {
    35: {
        False: {
            "path": "./images/floppas/comdead.png",
            "name": "Dead Floppa",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comdead.png",
            "name": "✨Dead Floppa✨",
            "category": "gray"
        }
    },
    37: {
        False: {
            "path": "./images/floppas/comfloppa.png",
            "name": "Floppa",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comfloppa.png",
            "name": "✨Floppa✨",
            "category": "gray"
        }
    },
    38: {
        False: {
            "path": "./images/floppas/comhauparleur.png",
            "name": "FloParleur",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comhauparleur.png",
            "name": "✨FloParleur✨",
            "category": "gray"
        }
    },
    39: {
        False: {
            "path": "./images/floppas/comknife.png",
            "name": "FloMad",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comknife.png",
            "name": "✨FloMad✨",
            "category": "gray"
        }
    },
    40: {
        False: {
            "path": "./images/floppas/comlaugh.png",
            "name": "Flaughppa",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comlaugh.png",
            "name": "✨Flaughppa✨",
            "category": "gray"
        }
    },
    41: {
        False: {
            "path": "./images/floppas/comperdu.png",
            "name": "Floppa ???",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comperdu.png",
            "name": "✨Floppa ???✨",
            "category": "gray"
        }
    },
    42: {
        False: {
            "path": "./images/floppas/compleur.png",
            "name": "Floppa Sad",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/compleur.png",
            "name": "✨Floppa Sad✨",
            "category": "gray"
        }
    },
    43: {
        False: {
            "path": "./images/floppas/comright.png",
            "name": "Floppa Right!",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comright.png",
            "name": "✨Floppa Right!✨",
            "category": "gray"
        }
    },
    44: {
        False: {
            "path": "./images/floppas/comscript.png",
            "name": "Floppa Script",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comscript.png",
            "name": "✨Floppa Script✨",
            "category": "gray"
        }
    },
    45: {
        False: {
            "path": "./images/floppas/comuwu.png",
            "name": "Floppa UwU",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comuwu.png",
            "name": "✨Floppa UwU✨",
            "category": "gray"
        }
    },
    46: {
        False: {
            "path": "./images/floppas/comsuicide.png",
            "name": "Floppa Will Die",
            "category": "gray"
        },
        True: {
            "path": "./images/shinyfloppa/comsuicide.png",
            "name": "✨Floppa Will Die✨",
            "category": "gray"
        }
    }
}
fullfloppedia = {None:"Aucun"}
fullfloppedia.update(mythicaldico)
fullfloppedia.update(legendarydico)
fullfloppedia.update(epicdico)
fullfloppedia.update(raredico)
fullfloppedia.update(uncomdico)
fullfloppedia.update(commondico)

#________________________________________
def floppa_generation():
    luck = randint(1,100)
    if luck == 100:
        image = sample(list(mythicaldico.keys()), 1)
        color = discord.Color.red()
    elif luck <100 and luck > 92 :
        image = sample(list(legendarydico.keys()), 1)
        color = discord.Color.gold()
    elif luck < 93 and luck > 81 :
        image = sample(list(epicdico.keys()), 1)
        color = discord.Color.purple()
    elif luck < 82 and luck > 62 :
        image = sample(list(raredico.keys()), 1)
        color = discord.Color.dark_blue()
    elif luck < 62 and luck > 36 :
        image = sample(list(uncomdico.keys()), 1)
        color = discord.Color.green()
    else:
        image = sample(list(commondico.keys()), 1)
        color = discord.Color.darker_grey()
    return image[0], color

#________________________________________
def generate_shinyfloppa():
    if randint(1, 50) == 50:
        return True
    else :
        return False

def make_floppashiny(image_path: str):
    nc_in_a_nutshell= image_path.split('/')[-1]
    return f"./images/shinyfloppa/{nc_in_a_nutshell}"

def randompackadd(probamax = 4):
    a = randint(1, int(probamax))
    return a == 1


#------------------------------jeux
def jeushifumi(choice):
    dico = {"🪨":"✂️","🧻":"🪨","✂️":"🧻"}
    ia = "".join(sample(['🪨', '🧻', '✂️'],1))
    if dico[str(choice)] == ia:
        return True, ia
    elif str(choice) == ia:
        return None, ia
    else :
        return False, ia


#------------------------------
def get_floppacks(user):
    with open(f"users/{user.id}.txt","r") as usersave:
        data = usersave.readlines()
        return int("".join(data[5].split("packs : ")).strip())

def add_floppacks(user, num = 1):
    with open(f"users/{user.id}.txt","r") as usersaveread:
        data = usersaveread.readlines()
        packs = int("".join(data[5].split("packs : ")).strip()) + num
        data[5] = f"packs : {packs}\n"
    with open(f"users/{user.id}.txt","w") as usersavewrite:
        usersavewrite.writelines(data)
    usersaveread.close()
    usersavewrite.close()

def suppr_floppacks(user):
    with open(f"users/{user.id}.txt","r") as usersaveread:
        data = usersaveread.readlines()
        packs = int("".join(data[5].split("packs : ")).strip())
        if packs == 0:
            return False
        else:
            packs -= 1
            data[5] = f"packs : {packs}\n"
            with open(f"users/{user.id}.txt","w") as usersavewrite:
                usersavewrite.writelines(data)
            usersaveread.close()
            usersavewrite.close()
            return True

def get_equipedfloppa(user):
    with open(f"users/{user.id}.txt","r") as usersave:
        data = usersave.readlines()
        path = "".join((data[6].split(" "))[1]).strip()
        shiny = "".join((data[6].split(" "))[2]).strip()
        if path != "None":
            if shiny == "True":
                shiny = True
            else:
                shiny = False
            return path, shiny
        return None, None

class Storage:


    def __init__(self, user, users_data:dict):
        self.par_cat= None
        self.in_order= None
        self.user= user
        self.users_data= users_data

    def trier(self):

        liste_tried= [[],[],[],[],[],[]]
        stored_floppas_in_order= []
        for stored_floppa in self.users_data[str(self.user.id)]["storage"]:
            if fullfloppedia[stored_floppa[0]][stored_floppa[1]]['category']== "red":
                liste_tried[0].append(stored_floppa)
                
            elif fullfloppedia[stored_floppa[0]][stored_floppa[1]]['category']== "gold":
                liste_tried[1].append(stored_floppa)
                
            elif fullfloppedia[stored_floppa[0]][stored_floppa[1]]['category']== "purple":
                liste_tried[2].append(stored_floppa)
                
            elif fullfloppedia[stored_floppa[0]][stored_floppa[1]]['category']== "blue":
                liste_tried[3].append(stored_floppa)
                
            elif fullfloppedia[stored_floppa[0]][stored_floppa[1]]['category']== "green":
                liste_tried[4].append(stored_floppa)
                
            elif fullfloppedia[stored_floppa[0]][stored_floppa[1]]['category']== "gray":
                liste_tried[5].append(stored_floppa)
        
        for cat in liste_tried:
            stored_floppas_in_order.extend(cat)

        self.par_cat= liste_tried
        self.in_order= stored_floppas_in_order
        self.users_data[str(self.user.id)]['storage']= stored_floppas_in_order


#---------------------------------------------------------dates
def is_friday():
    today = datetime.datetime.now().weekday()
    return today == 4

def get_last_claim(user):
    with open(f"users/{user.id}.txt","r") as usersave:
        data = usersave.readlines()
        return "".join(data[9].split("lastdaily: ")).strip()

def update_last_claim(user, date):
    with open(f"users/{user.id}.txt","r") as usersave:
        data = usersave.readlines()
        data[9]= f"lastdaily: {date}\n"
    with open(f"users/{user.id}.txt","w") as save:
        save.writelines(data)
    usersave.close()
    save.close()

#-------------------------------------
def dailypack():
    luck= randint(1, 10)
    if luck == 1:
        return 3
    if luck <1 and luck > 4:
        return 2
    else :
        return 1

def fridaypack():
    luck= randint(1, 10)
    if luck == 1:
        return 7
    if luck <1 and luck > 4:
        return 6
    else :
        return 5