import sys, getopt, os, re, random, string
from datetime import datetime, timedelta, timezone

# to do list
#   1) get arguments OK
#   2) get params from file OK
#   3) generate targa OK
#   4) generate obu o pan OK
#   5) create folder viaggio OK
#   6) create switch case from tratta OK
#   7) operazione su idTemp OK
#   8) creazione xml eventi MANCA EVENTO SVINCOLO
#   9) param dict into func OK
#   10) CREARE EVENTO SCONTO PER CASHBACK


# FUNC ----------------------------------------------------------------------------------------------------

def getArgs(argv) -> dict:
    
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

def getParamsFromFile(file) -> dict: 

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

def genPlateNumber() -> string:

    alpha = string.ascii_uppercase
    f_chars = ''.join(random.choice(alpha) for i in range(2))
    
    num = str(random.randint(1,999))
    while len(num) != 3 :
        num = "0"+num
    
    l_chars = ''.join(random.choice(alpha) for i in range(2))
    
    plate_number = f_chars+num+l_chars
    return plate_number

def genApparato(dict) -> string:

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

def genIdTemporaliXevento(dict, evento, tratta) :
    
    sysdate = datetime.now()
    
    if evento == "E" :
        min_timeout=dict["old_entrata"]
        id_temp_entrata = sysdate + timedelta(minutes=-(int(timeout_apparato) - int(min_timeout)))
        id_temp_entrata = id_temp_entrata.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"
        return id_temp_entrata
    
    elif evento == "I" :
        min_timeout=params_list["old_itinere"]
        id_temp_itinere = sysdate + timedelta(minutes=-(int(timeout_apparato) - int(min_timeout)))
        id_temp_itinere = id_temp_itinere.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"
        return id_temp_itinere
    
    elif evento == "U" :
        min_timeout=params_list["old_uscita"]
        id_temp_uscita = sysdate + timedelta(minutes=-(int(timeout_apparato) - int(min_timeout)))
        id_temp_uscita = id_temp_uscita.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"
        return id_temp_uscita

    elif evento == "S" and tratta in ("EUS", "EIUS","US") :
        min_timeout=params_list["old_svincoloDopo"]
        dir_svincolo = "998"
        aperto_bool = False
        aperto_bool == True if tratta == "US" else False 
        id_temp_svincolo = sysdate + timedelta(minutes=-(int(timeout_apparato) - int(min_timeout)))
        id_temp_svincolo = id_temp_svincolo.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"
        return (id_temp_svincolo, dir_svincolo)
    
    elif evento == "S" and tratta in ("SEU", "UIES", "SU") :
        min_timeout=params_list["old_svincoloPrima"]
        dir_svincolo = "997"
        aperto_bool = False
        aperto_bool == True if tratta == "US" else False 
        id_temp_svincolo = sysdate + timedelta(minutes=-(int(timeout_apparato) - int(min_timeout)))
        id_temp_svincolo = id_temp_svincolo.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"
        return (id_temp_svincolo, dir_svincolo) 

def genEventoEntrataXml(rete, punto, id_temp, targa, dict_apparato) -> string:
    
    ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"

    ev1 = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns0:evento xmlns:ns0="http://transit.pr.auto.aitek.it/messages">
    <tipoEvento cod="E" />
    <idSpaziale periferica="62" progrMsg="1" corsia="0" dirMarcia="1" tipoPeriferica="P" rete="{rete}" punto="{punto}" />
    <idTemporale>{id_temp}</idTemporale>
    <infoVeicolo classe="10">
        <targaAnt nomeFile="targaAnt.jpg" affid="9" nazione="IT">{targa}</targaAnt>
        <targaPost nomeFile="targaPost.jpg" affid="9" nazione="IT">{targa}</targaPost>
        <targaRif nazione="IT">{targa}</targaRif>\n'''  

    if dict_apparato["cod_apparato"] == "SET" :
        ev2 = f'''		<SET CodiceIssuer="{dict_apparato["cod_prov"]}" PAN="{dict_apparato["apparato"]}" nazione="{dict_apparato["naz_prov"]}" EFCContextMark="604006001D09"/>\n'''
    else :
        ev2 = f'''        <OBU>{dict_apparato["apparato"]}</OBU>\n'''
            
    ev3 = f'''    </infoVeicolo>
    <reg dataOraMittente="{ts}" />
</ns0:evento>'''
            
    return ev1 + ev2 + ev3

def genEventoItinereXml(rete, punto, id_temp_i, dict_dati_entrata, dict_apparato) -> string:
    
    ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"

    ev1 = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns2:evento xmlns:ns2="http://transit.pr.auto.aitek.it/messages">
	<tipoEvento cod="I"/>
	<idSpaziale periferica="2" progrMsg="54171" corsia="2" dirMarcia="2" tipoPeriferica="B" rete="{rete}" punto="{punto}"/>
	<idTemporale>"{id_temp_i}"</idTemporale>
	<infoVeicolo classe="10">
		<targaAnt/>
		<targaPost/>
		<targaRif/>\n'''
    
    if dict_apparato["cod_apparato"] == "SET" :
        ev2 = f'''		<SET CodiceIssuer="{dict_apparato["cod_prov"]}" PAN="{dict_apparato["apparato"]}" nazione="{dict_apparato["naz_prov"]}" EFCContextMark="604006001D09"/>\n'''
    else :
        ev2 = f'''        <OBU>{dict_apparato["apparato"]}</OBU>\n'''

    ev3 = f'''    </infoVeicolo>
	<datiEntrata idTemporale="{dict_dati_entrata["id_temporale_entrata"]}" pista="2">
		<stazione punto="{dict_dati_entrata["punto_entrata"]}"/>
	</datiEntrata>
	<reg dataOraMittente="{ts}"/>
</ns2:evento>'''

    return ev1 + ev2 + ev3

def genEventoUscitaChiusoXml(rete, punto, id_temp_u, targa, dict_apparato, dict_dati_entrata) -> string:
    
    ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"

    ev1 = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns0:evento xmlns:ns0="http://transit.pr.auto.aitek.it/messages">
    <tipoEvento cod="U" />
    <idSpaziale periferica="62" progrMsg="4" corsia="0" dirMarcia="1" tipoPeriferica="P" rete="{rete}" punto="{punto}" />
    <idTemporale>{id_temp_u}</idTemporale>
    <infoVeicolo classe="10">
        <targaAnt nomeFile="targaAnt.jpg" affid="9" nazione="IT">{targa}</targaAnt>
        <targaPost nomeFile="targaPost.jpg" affid="9" nazione="IT">{targa}</targaPost>  
        <targaRif nazione="IT">{targa}</targaRif>\n'''

    if dict_apparato["cod_apparato"] == "SET" :
        ev2 = f'''		<SET CodiceIssuer="{dict_apparato["cod_prov"]}" PAN="{dict_apparato["apparato"]}" nazione="{dict_apparato["naz_prov"]}" EFCContextMark="604006001D09"/>\n'''
    else :
        ev2 = f'''        <OBU>{dict_apparato["apparato"]}</OBU>\n'''

    ev3 = '''	</infoVeicolo>
    <idViaggio mezzoPagamento="TL" />\n'''

    ev5 = f'''    <reg dataOraMittente="{ts}" />
</ns0:evento>'''

    if dict_dati_entrata["dati_entrata_bool"] :
        ev4 = f'''	<datiEntrata idTemporale="{dict_dati_entrata["id_temporale_entrata"]}" pista="12" classe="10">
        <stazione rete = "{dict_dati_entrata["rete_entrata"]}" punto = "{dict_dati_entrata["punto_entrata"]}"/>
    </datiEntrata>\n'''
        
        xml_eve = ev1 + ev2 + ev3 + ev4 + ev5
    else : 
        xml_eve = ev1 + ev2 + ev3 + ev5
    
    return xml_eve    

def genEventoUscitaApertoXml(rete, punto, id_temp, dict_apparato, dir_uscita) -> string:

    ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"

    ev1 = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns0:evento xmlns:ns0="http://transit.pr.auto.aitek.it/messages">
    <tipoEvento cod="U" />
    <idSpaziale periferica="62" progrMsg="4" corsia="0" dirMarcia="1" tipoPeriferica="P" rete="{rete}" punto="{punto}" />
    <idTemporale>{id_temp}</idTemporale>
    <infoVeicolo classe="10">\n'''
    
    if dict_apparato["cod_apparato"] == "SET" :
        ev2 = f'''		<SET CodiceIssuer="{dict_apparato["cod_prov"]}" PAN="{dict_apparato["apparato"]}" nazione="{dict_apparato["naz_prov"]}" EFCContextMark="604006001D09"/>\n'''
    else :
        ev2 = f'''        <OBU>{dict_apparato["apparato"]}</OBU>\n'''

    ev3 = f'''		</infoVeicolo>
	<datiEntrata>
		<stazione rete="{rete}" punto="{dir_uscita}"/>
	</datiEntrata>
	<reg dataOraMittente="{ts}"/>
</ns0:evento>'''
        
    return ev1 + ev2 + ev3  

def genEventoSvincoloXml(rete, punto, id_temp, dict_apparato, dir_svincolo) -> string:

    ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+01:00"

    ev1 = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ns2:evento xmlns:ns2="http://transit.pr.auto.aitek.it/messages">
    <tipoEvento cod="S"/>
    <idSpaziale corsia="1" dirMarcia="1" periferica="1" progrMsg="17621" punto="{punto}" rete="{rete}" tipoPeriferica="B"/>
    <idTemporale>{id_temp}</idTemporale>
    <infoVeicolo>\n'''
    
    if dict_apparato["cod_apparato"] == "SET" :
        ev2 = f'''		<SET CodiceIssuer="{dict_apparato["cod_prov"]}" PAN="{dict_apparato["apparato"]}" nazione="{dict_apparato["naz_prov"]}" EFCContextMark="604006001D09"/>\n'''
    else :
        ev2 = f'''        <OBU>{dict_apparato["apparato"]}</OBU>\n'''

    ev3 = f'''</infoVeicolo>
	<datiEntrata>
		<stazione rete="{rete}" punto="{dir_svincolo}"/>
	</datiEntrata>
    <reg dataOraMittente="{ts}"/>
</ns2:evento>'''
    
    return ev1 + ev2 +ev3

# MAIN -----------------------------------------------------------------------------------------


dumb_dict = {
        'arg_tratta' : 'EIUS',
        'arg_rete_e' : '1', 'arg_rete_u' : '1', 'arg_rete_i' : '41', 'arg_rete_s' : '37',
        'arg_punto_u' : '414', 'arg_punto_e' : '410', 'arg_punto_i' : '666', 'arg_punto_s' : '428',
        'arg_bool_dati_entrata' : 'y', 'arg_cod_apparato' : 's', 
        'arg_service_provider' : '151', 'arg_bool_cashback' : 'n' }


#args_dict = getArgs(sys.argv)
args_dict = dumb_dict
config_file = 'gen_events_conf.xml'

# check file conf
if os.path.isfile("./"+ config_file) :
    print(f"\n...recupero parametri di configurazione dal file '{config_file}'\n")
    params_list = getParamsFromFile(config_file)
else :
    print("\n...configuration file not found, I'll use default params\n")

#vars declaration
out_dir = "OUT_DIR_EVENTS"
pos_res=("Y", "y", "s", "S")
neg_res=("N", "n")
dati_entrata = True if args_dict["arg_bool_dati_entrata"] in (pos_res) else False
cod_apparato, timeout_name = ("OBU", "it.aitek.auto.pr.viaggi.close_cert_timeout_hours") if args_dict["arg_cod_apparato"] == "o" else ("SET", "it.aitek.auto.pr.viaggi.close_cert_timeout_hours")
timeout_apparato = params_list["timeout_SET"] if args_dict["arg_cod_apparato"] == "s" else params_list["timeout_OBU"]
tratta = args_dict["arg_tratta"]
tipo_viaggio = "Aperto" if tratta in ("US", "SU") else "Chiuso"
provider_list = str(params_list["providers_code"]).split(",")
naz_provider_list = str(params_list["naz_providers"]).split(",")
cod_service_provider = str(args_dict["arg_service_provider"])
naz_prov = naz_provider_list[provider_list.index(cod_service_provider)]

# check output directory
if os.path.exists(out_dir) :
    path_out_dir = os.path.abspath(out_dir)
    print(f"...cartella '{out_dir}' trovata al path: '{path_out_dir}' \n")
else :
   os.mkdir(out_dir)
   path_out_dir = os.path.abspath(out_dir)
   print(f"...cartella '{out_dir}' creata al path: '{path_out_dir}' \n")

# generate plate and apparato
plate_number = genPlateNumber()
apparato = genApparato(args_dict)

# create tratta dir
f_de = "-conDatiEntrata" if args_dict["arg_bool_dati_entrata"] in (pos_res) else ""
f_cc = "-CashbackCantieri" if args_dict["arg_bool_cashback"] in (pos_res) else ""

folder_name = "viaggio" + tipo_viaggio + "-" + cod_apparato + "-" + tratta + f_de + f_cc
folder_path = path_out_dir + "/" + folder_name

# verificare che elimini anche i file
if os.path.isdir(folder_path):
    os.remove(folder_path)
    print(f"...cartella esistente rimossa con successo\n")
    os.mkdir(folder_path)
    print(f"...cartella '{folder_name} creata con successo'\n")
else : 
    os.mkdir(folder_path)
    print(f"...cartella '{folder_name} creata con successo'\n")

# generate idTemp and events from tratta
i=0
sysdate = datetime.now()
print(f"...generazione idTemporali considerando '{timeout_name}' impostato a '{timeout_apparato}' minuti\n")

#default
dir_uscita="997"

#create dict for apparato
dict_apparato = {"cod_apparato" : cod_apparato,
                 "cod_prov" : cod_service_provider,
                 "naz_prov" : naz_prov,
                 "apparato" : apparato}

if tipo_viaggio == "Aperto" :
    if tratta == "SU" :
        dir_uscita = "998"
        
        
while i < len(tratta) : 
    evento = tratta[i]
    match evento :
        case "E":
            rete_entrata = args_dict["arg_rete_e"] 
            punto_entrata = args_dict["arg_punto_e"]
            filename = "entrata" + cod_apparato + "-" + punto_entrata + ".xml"
            
            id_temp_entrata = genIdTemporaliXevento(params_list, evento = "E", tratta = tratta)
            
            evento_entrata_xml = genEventoEntrataXml(rete_entrata, punto_entrata, id_temp_entrata, plate_number, dict_apparato)
            
            with open(folder_path + "/" + filename, 'w') as file :
                file.write(evento_entrata_xml)

            dict_dati_entrata = {"dati_entrata_bool" : dati_entrata,
                                 "rete_entrata" : rete_entrata,
                                 "punto_entrata" : punto_entrata,
                                 "id_temporale_entrata" : id_temp_entrata}
            i+=1

    match evento :
        case "I":
            rete_itinere = args_dict["arg_rete_i"]
            punto_itinere = args_dict["arg_punto_i"]
            filename = "itinere" + cod_apparato + "-" + punto_itinere + ".xml"

            id_temp_itinere = genIdTemporaliXevento(params_list, evento = "I", tratta = tratta)

            evento_itinere_xml = genEventoItinereXml(rete_itinere, punto_itinere, id_temp_itinere, dict_dati_entrata, dict_apparato)
            
            with open(folder_path + "/" + filename, 'w') as file :
                file.write(evento_itinere_xml)
            i+=1

    match evento :
        case "U":
            rete_uscita = args_dict["arg_rete_u"]
            punto_uscita = args_dict["arg_punto_u"]
            de = "-conDatiEntrata" if dati_entrata else ""
            filename = "uscita" + tipo_viaggio + cod_apparato + "-" + punto_uscita + de +".xml"
            id_temp_uscita = genIdTemporaliXevento(params_list, evento = "U", tratta = tratta)

            if tipo_viaggio == "Chiuso" :
                evento_uscita_xml = genEventoUscitaChiusoXml(rete_uscita, punto_uscita, id_temp_uscita, plate_number, dict_apparato, dict_dati_entrata)
            else : 
                evento_uscita_xml = genEventoUscitaApertoXml(rete_uscita, punto_uscita, id_temp_uscita, dict_apparato, dir_uscita)
                
            with open(folder_path + "/" + filename, 'w') as file :
                file.write(evento_uscita_xml)
            i+=1

    match evento :
        case "S":
            
            rete_svincolo = args_dict["arg_rete_s"]
            punto_svincolo = args_dict["arg_punto_s"]

            id_temp_svincolo, dir_svincolo = genIdTemporaliXevento(params_list, evento="S", tratta=tratta)
            tipo_svincolo = "svincoloPrima" if dir_svincolo == "997" else "svincoloDopo"
            
            filename = tipo_svincolo + cod_apparato + "-" + punto_svincolo +".xml"

            evento_svincolo = genEventoSvincoloXml(rete_svincolo, punto_svincolo, id_temp_svincolo, dict_apparato, dir_svincolo)

            with open(folder_path + "/" + filename, 'w') as file :
                file.write(evento_svincolo)
            i+=1













print(f"...generazione finale dati Viaggio\n")

print(f"............Tratta : {tratta}")
print(f"............Apparato : {apparato}")
print(f"............Targa : {plate_number}")

i=0
while i < len(tratta) : 
    evento = tratta[i]
    match evento :
        case "E":
            print(f"............Entrata '{punto_entrata}' il '{id_temp_entrata}'")
            i+=1
        case "I":
            print(f"............Itinere '{punto_itinere}' il '{id_temp_itinere}'")
            i+=1
        case "U":
            print(f"............Uscita '{punto_uscita}' il '{id_temp_uscita}'")
            i+=1
        case "S":
            print(f"............{tipo_svincolo} '{punto_svincolo}' il '{id_temp_svincolo}'\n\n")
            i+=1

print(f"...esecuzione terminata, tutti i file sono presenti al path: '{folder_path}'\n")
    

