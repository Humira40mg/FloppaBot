from random import sample,randint


def floppagif():
    gif = sample(['https://tenor.com/view/floppa-gif-24459715','https://tenor.com/view/floppa-vibing-big-floppa-vibing-gif-22702623','https://tenor.com/view/floppa-gif-26153303','https://tenor.com/view/floppa-big-floppa-lil-floppa-flop-floppa-flop-gif-22883844','https://tenor.com/view/diagnosis-issue-flop-flop-floppa-bingus-gif-22901732','https://tenor.com/view/funni-flop-gif-23713618','https://tenor.com/view/floppy-floppa-gif-21921987','https://tenor.com/view/small-floppa-big-floppa-lynx-sound-of-poggers-big-chungus-gif-20022861','https://tenor.com/view/flop-gif-20244619','https://tenor.com/view/caracal-big-floppa-floppa-prozhony-flop-gif-23506865','https://tenor.com/view/floppa-floppa-cat-flop-gif-26014481','https://tenor.com/view/floppa-big-floppa-caracal-pumba-pumber-gif-23931271','https://tenor.com/view/get-this-gif-to-trending-floppa-floppa-flop-get-this-gif-to-trending-floppa-tube-gif-25093055','https://tenor.com/view/floppa-big-big-floppa-kitty-review-gif-21384663','https://tenor.com/view/floppa-floppy-lssd-lsrp-gta-world-gif-26058402','https://tenor.com/view/floppa-karr-kerr-hiss-fat-gif-25301966','https://tenor.com/view/big-floppa-floppa-nacrocent-shrimp-big-floppa-shrimp-gif-21212407','https://tenor.com/view/flopa-floppa-big-floppa-caracal-prozhony-gif-20185616','https://tenor.com/view/big-floppa-flop-floppa-hi-lusid-gif-24049570','https://tenor.com/view/floppa-big-zabloing-googas-flop-gif-19891236','https://tenor.com/view/floppa-sad-flopper-flip-flops-gucci-flip-flops-gif-25765382','https://tenor.com/view/floppa-exfloppa-anonraid-ex_floppa-gif-22688938','https://tenor.com/view/big-floppa-flag-floppa-bingus-gif-21392215','Manul\nhttps://tenor.com/view/manul-sneak-pallas-gif-5623670','https://tenor.com/view/big-floppa-floppa-knockout-baby-floppa-wwe-ufc-gif-20391349','https://tenor.com/view/big-floppa-floppa-cat-bingus-sogga-gif-23529984','https://tenor.com/view/flop-troll-floppa-milf-gif-23637798','https://tenor.com/view/big-floppa-caracal-gosha-gregory-kerr-gif-27022893','https://tenor.com/view/floppa-caracal-angry-flopping-gif-22573853','https://tenor.com/view/floppa-jakecord-floppacord-sadlynut-sadnut-gif-18885442','https://tenor.com/view/no-floppa-or-flop-flop-floppa-gif-27182839','https://tenor.com/view/floppa-small-floppa-baby-floppa-kitten-gif-17785342143018081133','https://tenor.com/view/flop-pa-gif-2537213760990164220','https://tenor.com/view/floppa-caracal-charlie-murphy-chad-gigachad-gif-22354634','https://tenor.com/view/big-floppa-big-flopa-flop-who-the-fuck-asked-hot-gif-20419810','https://tenor.com/view/floppa-chad-flopped-gif-21642248','https://tenor.com/view/floppasit-floppa-sitting-caracal-gif-24754620','https://tenor.com/view/floppa-based-caracal-sniff-big-floppa-gif-21703719','https://tenor.com/view/floppa-big-floppa-floppa-hat-hat-kimbo-gif-23170772'],1)
    return "".join(gif)

def pingreponse():
    reponse = sample(["Ui ??","C'est moi !","Bonjur. c:","Heeeyy ! Mais c'est moi ! c:","Hey, ça vas ? c:","Tiens, tiens, tiens..."],1)
    return "".join(reponse)

def paslesperms():
    reponse = sample(["T'as cru ?! >:C","Mais t'as cru t'étais ki omg !!! >:C","ptdr t ki ???",">:C","Tu n'as pas la permission de faire ceci. >:C","Error 404 : Floppa permission not found","https://tenor.com/view/floppa-flop-flopping-i-love-to-flop-big-floppa-gif-25588715"],1)
    return "".join(reponse)

def affinite():
    return randint(0, 100)

def bienvenuebackground():
    roll = randint(1, 25)
    if roll == 25 :
        return r"images/bienvenue/mobscur.png"
    elif roll < 25 and roll > 19 :
        return "".join(sample([r"images/bienvenue/ltrot.png", r"images/bienvenue/lroi.png"], 1))
    elif roll < 20 and roll > 11 :
        return "".join(sample([r"images/bienvenue/rdark.png", r"images/bienvenue/rsherif.png"], 1))
    else :
        return "".join(sample([r"images/bienvenue/cnormal.png", r"images/bienvenue/cuwu.png", r"images/bienvenue/ceau.png"], 1))

def reponse_brisee(tracker=1):
    if tracker == 1:
        return sample(["Floppa semble t'avoir déjà oublié.", "Floppa te considère comme un paillasson.", "Comment oses-tu lui adresser la parole ??"], 1)
    elif tracker == 2:
        return sample(["Floppa pourrait te prêter une chaussure.", "Floppa se souvient de ton visage.", "Floppa te considère presque autant que son bonsaï préféré."], 1)
    elif tracker == 3:
        return sample(["Tu es synchronisé avec Floppa.", "Floppa pourrait envisager de partager une barre chocolatée avec toi.", "Floppa se souvient de ton anecdote sur les canards."], 1)
    elif tracker == 4:
        return sample(["Floppa t'aime bien.", "Floppa envisage de te donner une place VIP pour son prochain concert.", "Floppa te donne des bonbons."], 1)
    elif tracker == 5:
        return sample(["Floppa te donne un coup.", "Floppa t'invite à passer un week-end sur son yacht privé.", "Floppa te prête ses chaussures."], 1)
    else:
        return "Floppa te tue."


def random_hacking(user):
    randomlist = sample([
    f"Initiating user data extraction for {user}.\n",
    f"Accessing {user}'s personal files.\n",
    f"Hacking into {user}'s account.\n",
    f"Decrypting {user}'s messages.\n",
    f"Bypassing {user}'s security protocols.\n",
    f"Intercepting {user}'s private information.\n",
    f"Gathering intelligence on {user}.\n",
    f"Initiating a cyber intrusion on {user}.\n",
    f"Uncovering {user}'s deepest secrets.\n",
    f"Breaching {user}'s digital fortress.\n",
    f"Scanning {user}'s online presence.\n",
    f"Infiltrating {user}'s digital world.\n",
    f"Cracking {user}'s encryption.\n",
    f"Compromising {user}'s online identity.\n",
    f"Extracting sensitive data from {user}.\n",
    f"Penetrating {user}'s firewall.\n",
    f"Hacking {user}'s login credentials.\n",
    f"Accessing {user}'s hidden files.\n",
    f"Unmasking {user}'s online activities.\n",
    f"Initiating a takeover of {user}'s account.\n",
    f"Manipulating {user}'s digital footprint.\n",
    f"Dissecting {user}'s online behavior.\n",
    f"Decrypting {user}'s password.\n",
    f"Breaching {user}'s security perimeter.\n",
    f"Interfering with {user}'s online presence.\n",
    f"Extracting confidential data from {user}.\n",
    f"Infiltrating {user}'s virtual world.\n",
    f"Cracking {user}'s access codes.\n",
    f"Compromising {user}'s online security.\n",
    f"Initiating a data breach on {user}.\n",
    f"Uncovering {user}'s hidden secrets.\n",
    f"Hacking {user}'s online activities.\n",
    f"Accessing {user}'s classified information.\n",
    f"Unmasking {user}'s online identity.\n",
    f"Initiating a cyber attack on {user}.\n",
    f"Manipulating {user}'s digital records.\n",
    f"Decrypting {user}'s private messages.\n",
    f"Breaching {user}'s virtual fortress.\n",
    f"Gathering sensitive data from {user}.\n",
    f"Penetrating {user}'s online defenses.\n",
    f"Hacking {user}'s digital presence.\n",
    f"Accessing {user}'s confidential files.\n",
    f"Intercepting {user}'s communication.\n",
    f"Initiating a takeover of {user}'s account.\n",
    f"Uncovering {user}'s online secrets.\n",
    f"Cracking {user}'s security codes.\n",
    f"Compromising {user}'s digital identity.\n",
    f"Extracting personal data from {user}.\n",
    f"Infiltrating {user}'s online world.\n",
    f"Initiating a cyber intrusion on {user}.\n"
], randint(5, 20))
    return randomlist
    
def random_messe():
    discours_floppaisme = [
    # Discours d'ouverture
    "Chers fidèles du Floppaisme, en ce Floppa Friday, nous nous rassemblons pour honorer notre divin félin, le dieu Floppa, dans l'unité et la prière.",
    
    # Discours sur la gratitude
    "En ce jour béni du Floppa Friday, nous exprimons notre gratitude envers le dieu Floppa pour les doux moments de repos qu'il nous accorde. Que son amour nous enveloppe à jamais.",
    
    # Discours sur la compassion
    "Le Floppaisme nous enseigne la compassion envers toutes les créatures, car le dieu Floppa veille sur chacun de ses enfants, quel que soit leur pelage. Pratiquons cette compassion aujourd'hui et toujours.",
    
    # Discours sur la tranquillité
    "Dans la quiétude de ce Floppa Friday, trouvons la paix intérieure en nous retirant dans la méditation, tout comme le dieu Floppa repose paisiblement sur son trône de coussins.",
    
    # Discours sur la communion
    "En partageant cette messe du Floppaisme en ce Floppa Friday, nous renforçons notre communion spirituelle et notre amour pour notre divin félin. Nous sommes une famille unie par la foi.",
    
    # Discours sur l'harmonie
    "Sachons préserver l'harmonie avec la nature et les êtres vivants en ce Floppa Friday, conformément à la volonté du dieu Floppa. Que son équilibre soit notre guide.",
    
    # Discours de conclusion
    "En ce Floppa Friday, que le dieu Floppa continue de guider nos pas et de nous remplir de son amour. Que notre foi dans le Floppaisme illumine notre chemin pour les jours à venir."
]
    return "".join(sample(discours_floppaisme, 1))


command_description = {
    "help":"help t'envoie en message privé la liste de toutes les commandes disponibles. c:",
    'serverinfo':"serverinfo te donne plus d'informations sur le serveur dans lequel tu as taper la commande.",
    "ping":"ping donne la latence du bot.",
    "invitelink":"invitelink t'envoie le lien qui me permet d'être invité dans un nouveau serveur.",
    "floppa":"Un Floppa sauvage apparaît !",
    "play":"play <musique>, ajoute la musique que tu propose a la queue ou la lance si celle-ci est vide. c:",
    "skip":"skip permet de passer une musique en cours. Si le vote est activé sur ton serveur, demande à un admin de l'enlever avec la commande setskip.",
    "remove":"remove <position|ALL> enlève une musique de la queue.",
    "search":"search <requête> recherche sur Youtube une requête fournie.",
    "scsearch":"scsearch <requête> recherche une requête fournie sur Soundcloud.",
    "shuffle":"shuffle mélange les chansons que vous avez ajoutées.",
    "nowplaying":"nowplaying affiche la chanson en cours de lecture. c:",
    "lyrics":"lyrics <nom musique> affiche les paroles d'une chanson.",
    "playlists":"playlists affiche les listes de lecture disponibles",
    "forceremove":"forceremove <utilisateur> supprime toutes les entrées d'un utilisateur de la file d'attente. (Seulement disponible pour les rôles DJ) c:",
    "forceskip":"forceskip skip le morceau en cours.(Seulement disponible pour les rôles DJ)",
    "movetrack":"movetrack <de> <a> déplace une piste de la file d'attente actuelle vers une autre position (Seulement disponible pour les rôles DJ).",
    "pause":"pause met en pause le morceau en cours",
    "playnext":"playnext <titre|URL> joue la musique proposée directement après (Seulement disponible pour les rôles DJ).",
    "loop":"loop [off|all|single]  Rajoute de la musique à la file d'attente lorsque qu'elle se termine (Seulement disponible pour les rôles DJ).",
    "skipto":"skipto <position> passe au morceau spécifié.",
    "stop":"stop Arrête la chanson en cours et efface la file d'attente. ;-; (Seulement disponible pour les rôles DJ)",
    "volume":"volume [0-150] définit ou affiche le volume (Seulement disponible pour les rôles DJ).",
    "setprefix":"setprefix <préfixe|AUCUN> définit un préfixe spécifique au serveur (Seulement disponible pour les rôles administrateurs).",
    "say":"say me fait dire la phrase que tu veux.",
    "setdj":"setdj <nomrôle|AUCUN> définit le rôle DJ pour certaines commandes musicales (Seulement disponible pour les rôles administrateurs).",
    "setskip":"setskip <0 - 100> Définit un pourcentage d'omission spécifique au serveur (Seulement disponible pour les rôles administrateurs).",
    "settc":"settc <salon|AUCUN> Définit le salon de texte pour les commandes de musique (Seulement disponible pour les rôles administrateurs).",
    "setvc":"setvc <salon|AUCUN> Définit le salon vocal pour la lecture de musique (Seulement disponible pour les rôles administrateurs).",
    "togglelvl":"togglelvl active ou désactive les messages de levelup sur le serveur (Seulement disponible pour les rôles administrateurs).",
    "setbotalert":"setbotalert <salon ou rien> défini le salon dans lequel je donnerai des infos, comme annonce de shutdown ou annonce de connexion (Seulement disponible pour les rôles administrateurs).",
    "disablebotalert":"disablebotalert désattribue le salon dans lequel je donne des infos, comme les annonces de shutdown ou de connexion. Dès maintenant, j'arrêterai de vous casser les pieds... ;-; (Seulement disponible pour les rôles administrateurs)",
    "msgcount":"Avec msgcount je te répond combien de messages j'ai lu de toi UwU.",
    "rank":"rank <mention | rien> te dit quel est ton niveau ou le niveau de la personne mentionnée. c:",
    "floppaffinite":"floppaffinite <rien|mention> te donne ton affinité avec Floppa.",
    "setbienvenue":"setbienvenue <rien|salon> désigne le salon dans lequel je shouaiterai la bienvenue aux nouveaux membres! c:",
    "disablebienvenue":"disablebienvenue désactive les messages de bienvenue que j'envoie.",
    "infofloppagames":"infofloppagames donne des explications sur les Floppa Games.",
    "shifumi":"shifumi te lance dans un pierre feuille ciseaux contre moi! (consulte infofloppagames pour en savoir plus.)",
    "toggleping":"toggleping bascule entre le mode où je te ping quand tu passe un niveau, et le mode ou ce n'est pas le cas. Tu monteras quand même en niveaux et recevras les floppaxks mais juste tu n'en sauras rien.",
    "inv":"inv <rien|mention> montre l'inventaire donc le nombre de Floppacks et ton floppa équipé. (consulte infofloppagames pour en savoir plus.)",
    "fp":"fp ouvre un floppack.(consulte infofloppagames pour en savoir plus.)",
    "storage":"storage <rien|utilisateur> affiche le stockage de floppa.",
    "equipfloppa":"une commande qui n'existe plus, remplacée par les boutons de la commande storage.", #--------------------
    "removefloppa":"removefloppa <rien|numerostorage(0, 1, 2)> supprime le floppa selectionné. Je te demande de confirmer avant que l'action de s'execute t'inquitète pas. (consulte infofloppagames pour en savoir plus.)",
    "daily":"daily te donne une recompense quotidienne (je conseille de le faire le venredi)! (consulte infofloppagames pour en savoir plus.)",
    "trade":"trade <mention> permet d'échanger ton floppa équipé contre le floppa équipé de la personne mentionné.",
    "hack":"hack <mention> pirate les données de l'utilisateur ciblé (pour de faux ;-;).",
    "roulette":"roullette <liste d'utilisateurs>, une roulette russe avec option de tirer sur un autre joueur. Attention, si la balle ne part pas, vous avez perdu et la partie s'arrète.",
    "bet":"bet <utilisateur>, permet de parier des floppacks ou un floppa dans un 1v1 dans des floppagames.",
    "mastermind":"mastermind <liste d'utilisateurs>, permet de jouer au mastermind."
}

