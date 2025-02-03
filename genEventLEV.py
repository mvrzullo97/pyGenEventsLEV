import sys
import getopt
import os
import re


def getArgs(argv) :
    
    args_dict = {}
    arg_help = "\n    -tr < tratta > (ex. 'EUS')\n    -re < rete Entrata >\n    -pe < punto Entrata >\n    -ri < rete Itinere >\n    -pi < punto Itinere >\n    -ru < rete Uscita >\n    -pu < punto Uscita >\n    -de < datiEntrata > (yY or nN)\n    -rs < rete Svincolo >\n    -ps < punto Svincolo >\n    -ap < tipo apparato ('o' for OBU or 's' for SET) >\n    -sp < codice Service Provider >\n    -pl < targa veicolo >\n    -cc < cashback cantieri (yY or nN) >\n"

    try:
        opts, args = getopt.getopt(argv[1:], 
                                   "h:tr:re:ru:ri:rs:pe:pu:pi:ps:de:ap:sp:tg:cc", 
                                   ["h=","tr=","re=","ru=","ri=","rs=","pe=","pu=","pi=","ps=","de=","ap=","sp=","tg=","cc="])
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
        elif opt == "--tg":
            args_dict["arg_targa"] = arg
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



args_list = getArgs(sys.argv)
config_file = "gen_events_conf.xml"

if os.path.isfile("./"+ config_file) :
    print("\n...recovered configuration params from file", config_file + "\n")
    params_list = getParamsFromFile(config_file)
else :
    print("\n...configuration file not found, I'll use default params\n")

    