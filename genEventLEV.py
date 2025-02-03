import sys, getopt, os, re, random, string
from datetime import datetime

# to do list
#   1) get arguments OK
#   2) get params from file OK
#   3) generate targa OK
#   4) generate obu o pan OK
#   5) create folder viaggio OK
#   6) create switch case from tratta OK
#   7) operazione su idTemp


def getArgs(argv) :
    
    args_dict = {
        'arg_tratta' : '',
        'arg_rete_e' : '', 'arg_rete_u' : '', 'arg_rete_i' : '', 'arg_rete_s' : '',
        'arg_punto_u' : '', 'arg_punto_e' : '', 'arg_punto_i' : '', 'arg_punto_s' : '',
        'arg_bool_dati_entrata' : '', 'arg_cod_apparato' : '', 
        'arg_service_provider' : '', 'arg_bool_cashback' : '' }
    
    arg_help = "\n    -tr < tratta > (ex. 'EUS')\n    -re < rete Entrata >\n    -pe < punto Entrata >\n    -ri < rete Itinere >\n    -pi < punto Itinere >\n    -ru < rete Uscita >\n    -pu < punto Uscita >\n    -de < datiEntrata > (yY or nN)\n    -rs < rete Svincolo >\n    -ps < punto Svincolo >\n    -ap < tipo apparato ('o' for OBU or 's' for SET) >\n    -sp < codice Service Provider >\n    -cc < cashback cantieri (yY or nN) >\n"

    try:
        opts, args = getopt.getopt(argv[1:], 
                                   "h:tr:re:ru:ri:rs:pe:pu:pi:ps:de:ap:sp:cc", 
                                   ["h=","tr=","re=","ru=","ri=","rs=","pe=","pu=","pi=","ps=","de=","ap=","sp=","cc="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(arg_help)
            sys.exit(2)
        elif opt == "--tr":
            args_dict["arg_tratta"] = arg
        elif opt == "--re":
            args_dict["arg_rete_e"] = arg
        elif opt == "--ru":
            args_dict["arg_rete_u"] = arg
        elif opt == "--ri":
            args_dict["arg_rete_i"] = arg
        elif opt == "--rs":
            args_dict["arg_rete_s"] = arg 
        elif opt == "--pe":
            args_dict["arg_punto_e"] = arg
        elif opt == "--pu":
            args_dict["arg_punto_u"] = arg
        elif opt == "--pi":
            args_dict["arg_punto_i"] = arg
        elif opt == "--ps":
            args_dict["arg_punto_s"] = arg
        elif opt == "--de":
            args_dict["arg_bool_dati_entrata"] = arg
        elif opt == "--ap":
            args_dict["arg_cod_apparato"] = arg
        elif opt == "--sp":
            args_dict["arg_service_provider"] = arg
        elif opt == "--cc":
            args_dict["arg_bool_cashback"] = arg
    
    return args_dict

def getParamsFromFile(file) : 

    params_dict = {}
    f = open(file, "r")
    
    for line in f:
        if re.search("timeout_SET", line) :
           params_dict["timeout_SET"] = line.partition("=")[2].strip()
        if re.search("timeout_OBU", line) :
           params_dict["timeout_OBU"] = line.partition("=")[2].strip()
        if re.search("old_entrata", line) :
           params_dict["old_entrata"] = line.partition("=")[2].strip()
        if re.search("old_itinere", line) :
           params_dict["old_itinere"] = line.partition("=")[2].strip()
        if re.search("old_uscita", line) :
           params_dict["old_uscita"] = line.partition("=")[2].strip()
        if re.search("old_svincoloPrima", line) :
           params_dict["old_svincoloPrima"] = line.partition("=")[2].strip()
        if re.search("old_svincoloDopo", line) :
           params_dict["old_svincoloDopo"] = line.partition("=")[2].strip()
        if re.search("providers_code", line) :
           params_dict["providers_code"] = line.partition("=")[2].strip()
        if re.search("naz_providers", line) :
           params_dict["naz_providers"] = line.partition("=")[2].strip()   
    f.close()
    return params_dict

def genPlateNumber() :

    alpha = string.ascii_uppercase
    f_chars = ''.join(random.choice(alpha) for i in range(2))
    
    num = str(random.randint(1,999))
    while len(num) != 3 :
        num = "0"+num
    
    l_chars = ''.join(random.choice(alpha) for i in range(2))
    
    plate_number = f_chars+num+l_chars
    return plate_number

def genApparato(dict) :

    sysdate = datetime.now()

    if dict["arg_cod_apparato"] == "s" :
        f_part = sysdate.strftime('%Y%m%d%H%M')
        num = str(random.randint(1,9999999))
        while len(num) != 7 :
            num = num + str(random.randint(1,9))
        apparato = f_part + num + "F"
    
    elif dict["arg_cod_apparato"] == "o" :
        apparato = str(random.randint(1,999999999))

    return apparato



args_dict = getArgs(sys.argv)
config_file = "gen_events_conf.xml"

# check file conf
if os.path.isfile("./"+ config_file) :
    print("\n...recovered configuration params from file", config_file + "\n")
    params_list = getParamsFromFile(config_file)
else :
    print("\n...configuration file not found, I'll use default params\n")

#vars declaration
out_dir = "OUT_DIR_EVENTS"
pos_res=("Y", "y")
neg_res=("N", "n")
dati_entrata = True if args_dict["arg_bool_dati_entrata"] in (pos_res) else False
cod_apparato = "OBU" if args_dict["arg_cod_apparato"] == "o" else "SET"
timeout_apparato = params_list["timeout_SET"] if args_dict["arg_cod_apparato"] == "s" else params_list["timeout_OBU"]
tratta = args_dict["arg_tratta"]

# check output directory
if os.path.exists(out_dir) :
    path_out_dir = os.path.abspath(out_dir)
    print("...", out_dir, "found at path:", path_out_dir, "\n")
else :
   os.mkdir(out_dir)
   path_out_dir = os.path.abspath(out_dir)
   print("...created", out_dir, "at path: ", path_out_dir, "\n")

# generate plate and apparato
plate_number = genPlateNumber()
apparato = genApparato(args_dict)

# create tratta dir
f_de = "-conDatiEntrata" if args_dict["arg_bool_dati_entrata"] in (pos_res) else ""
f_cc = "-CashbackCantieri" if args_dict["arg_bool_cashback"] in (pos_res) else ""

folder_name = "Viaggio-" + cod_apparato + "-" + tratta + f_de + f_cc

if os.path.isdir(path_out_dir + "/" + folder_name):
    os.rmdir(path_out_dir + "/" + folder_name)
    os.mkdir(path_out_dir + "/" + folder_name)
    print("rimuovo")
else : 
    os.mkdir(path_out_dir + "/" + folder_name)
    print("creo")

# get idTemporali

id_temp_entrata = datetime.now()
past_time_and_date = id_temp_entrata + datetime.timedelta(days=-0, hours=-0, minutes=-timeout_apparato)
print(id_temp_entrata)
print(past_time_and_date)
print(timeout_apparato)



# generate events from tratta
i=0

while i < len(tratta) : 
    evento = tratta[i]
    
    match evento :
        case "E":
            i+=1
    match evento :
        case "I":
            i+=1
    match evento :
        case "U":
            i+=1
    match evento :
        case "S":
            i+=1



    

