import sys
import getopt

def getArgs(argv):
    arg_tratta = ""
    arg_rete_e = ""
    arg_rete_u = ""
    arg_rete_i = ""
    arg_rete_s = ""
    arg_punto_e = ""
    arg_punto_u = ""
    arg_punto_i = ""
    arg_punto_s = ""
    arg_bool_dati_entrata = ""
    arg_cod_apparato = ""
    arg_service_provider = ""
    arg_targa = ""
    arg_bool_cashback = ""
    arg_help = "\n    -tr < tratta > (ex. 'EUS')\n    -re < rete Entrata >\n    -pe < punto Entrata >\n    -ri < rete Itinere >\n    -pi < punto Itinere >\n    -ru < rete Uscita >\n    -pu < punto Uscita >\n    -de < datiEntrata > (yY or nN)\n    -rs < rete Svincolo >\n    -ps < punto Svincolo >\n    -ap < tipo apparato ('o' for OBU or 's' for SET) >\n    -sp < codice Service Provider >\n    -pl < targa veicolo >\n    -cc < cashback cantieri (yY or nN) >\n"

    try:
        opts, args = getopt.getopt(argv[1:], 
                                   "h:tr:re:ru:ri:rs:pe:pu:pi:ps:de:ap:sp:tg:cc", 
                                   ["h=","tr=","re=","ru=","ri=","rs=","pe=","pu=","pi=","ps=","de=","ap=","sp=","tg=","cc="])
    except:
        print("tiro su un'eccezione")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(arg_help)
            sys.exit(2)
        elif opt == "--tr":
            arg_tratta = arg
        elif opt == "--re":
            arg_rete_e = arg
        elif opt == "--ru":
            arg_rete_u = arg
        elif opt == "--ri":
            arg_rete_i = arg
        elif opt == "--rs":
            arg_rete_s = arg 
        elif opt == "--pe":
            arg_punto_e = arg
        elif opt == "--pu":
            arg_punto_u = arg
        elif opt == "--pi":
            arg_punto_i = arg
        elif opt == "--ps":
            arg_punto_s = arg
        elif opt == "--de":
            arg_bool_dati_entrata = arg
        elif opt == "--ap":
            arg_cod_apparato = arg
        elif opt == "--sp":
            arg_service_provider = arg
        elif opt == "--tg":
            arg_targa = arg
        elif opt == "--cc":
            arg_bool_cashback = arg

    print("tratta" , arg_tratta)

getArgs(sys.argv)
