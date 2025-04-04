from discord.ext import commands
from floppagames import get_floppacks

#fonctions utiles

#------------------------------ vérifications
def checkadmin(floppa, slash= False):
    if slash is False:
        try:
            if floppa.author.guild_permissions.administrator:
                return True
        except Exception as e :
            print(e)
    else:
        if floppa.user.guild_permissions.administrator:
            return True

def ismp(floppa):
    if floppa.guild is None :
        return True
    else :
        return False
    
def checkuser(floppa, user):
    if floppa.author == user.user :
        return True
    else:
        return False
    

#------------------------------ Divers
    
def redimentiondicon(url):
    return "".join(url.split("size=")[0])+"width=90&height=90"

#______________________________gestion données serveur___________________________________
#----------------------------------------------------------------------------------------  
def get_préfix(floppa):
    try:
        with open(f"servers/{floppa.guild.id}.txt", "r") as file:
            lines = file.readlines()
            préfix = str(lines[1]).strip()
    except Exception as e:
        print(e)
        préfix = ";"
    return préfix

def get_serverpinglvl(floppa):
    try:
        with open(f"servers/{floppa.guild.id}.txt","r") as file:
            lines = file.readlines()
            if str(lines[2]).strip() == "1":
                return True
            else:
                return False
    except FileNotFoundError :
        print(f"ALERTE OMG : FICHIé NON TROUVé POUR {floppa.guild} !!!")
        return True

def custom_prefix(floppa):
    if ismp(floppa) is False :
        if floppa.guild:
            try:
                with open(f"servers/{floppa.guild.id}.txt", "r") as file:
                    lines = file.readlines()
                    préfix = str(lines[1]).strip()
                    return commands.when_mentioned_or(préfix)
            except FileNotFoundError:
                print(f"ALERTE OMG : FICHIé NON TROUVé POUR {floppa.guild}") 
                return commands.when_mentioned_or(";")   
    return commands.when_mentioned_or(";")
        
#______________________________gestion données utilisateur___________________________________
#--------------------------------------------------------------------------------------------  

def get_user_data(user_id):
    with open(f"users/{user_id}.txt","r") as usersave:
        return usersave.readlines()
    
def save_user_data(user_id, data):
    with open(f"users/{user_id}.txt","w") as usersave:
        usersave.writelines(data)

#------------------------------

def get_msgcount(floppa):
    try :
        with open(f"users/{floppa.id}.txt","r") as usersave:
            userdata = usersave.readlines()
            return int(userdata[3].replace("msg count : ","").strip()), True
    except Exception as e : 
        print(e)
        return 0, False

#------------------------------
def get_userlvl(user):
    try :
        with open(f"users/{user.id}.txt","r") as usersave:
            userdata = usersave.readlines()
            return int(userdata[4].replace("lvl : ","").strip()), True
    except Exception as e : 
        print(e)
        return 0, False
    
#------------------------------
def get_lvlpourcent(count, lvl):
    if lvl != 0:
        niv = lvl
        for i in range(lvl):
            count -= 50*(1.2**(niv-1))
            niv -= 1
    return int((count/(50*(1.2**lvl)))*100)

#------------------------------  
def newuserfile(floppa):
        newusersave = open(f"users/{floppa.author.id}.txt","w", encoding='utf-8')
        newusersave.write(f"{floppa.author}\n{floppa.author.id}\nping : True\nmsg count : 0\nlvl : 0\npacks : 0\nFloppa: None None\nStorage :\n--ligne libre--\nlastdaily: 2023-08-02\npray_count: 0\ndark_mode: False\nfidelite: 0\ncompte_pray_today: 0\nlast_pray: 2023-08-02\nlast_friday: 2023-08-02\n")
        return

def userpinglvl(user):
    with open(f"users/{user.id}.txt","r") as usersave:
        userdata = usersave.readlines()
        if userdata[2].replace("ping : ","").strip() == "True":
            return True
        else :
            return False
    
def messagecompteplus1(msgcount):
        msgcount += 1
        return f"msg count : {msgcount}\n"

def calcullvl(count, lvl):
    if lvl != 0:
        niv = lvl
        for i in range(lvl):
            count -= 50*(1.2**(niv-1))
            niv -= 1
    if count/(50*(1.2**lvl)) >= 1 :
        return True
    else:
        return False