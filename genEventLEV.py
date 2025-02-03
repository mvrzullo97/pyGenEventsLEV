import sys
import getopt

def getArgs(argv):
    
    param_list = {}
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
            param_list["arg_tratta"] = arg
        elif opt == "--re":
            param_list["arg_rete_e"] = arg
        elif opt == "--ru":
            param_list["arg_rete_u"] = arg
        elif opt == "--ri":
            param_list["arg_rete_i"] = arg
        elif opt == "--rs":
            param_list["arg_rete_s"] = arg 
        elif opt == "--pe":
            param_list["arg_punto_e"] = arg
        elif opt == "--pu":
            param_list["arg_punto_u"] = arg
        elif opt == "--pi":
            param_list["arg_punto_i"] = arg
        elif opt == "--ps":
            param_list["arg_punto_s"] = arg
        elif opt == "--de":
            param_list["arg_bool_dati_entrata"] = arg
        elif opt == "--ap":
            param_list["arg_cod_apparato"] = arg
        elif opt == "--sp":
            param_list["arg_service_provider"] = arg
        elif opt == "--tg":
            param_list["arg_targa"] = arg
        elif opt == "--cc":
            param_list["arg_bool_cashback"] = arg

    return param_list



param_list = getArgs(sys.argv)

