import json
import tkinter as  tk

class mJ:
    jason_dict = {}

    def check_for_name(fn):
        if type(mJ.jason_dict.get('name', None)) == type(None):
            mJ.jason_dict.update({'name': fn})

    def get_jason_name(fn):
        # den zum Bild passenden json-filename ermitteln
        JsonFile = str()
        JsonFile = fn
        JsonFile = './json/' + JsonFile + '.json'
        # JsonFile = JsonFile.replace(".png",".json")
        return JsonFile

    def write_json(fn):
        # prettyprint to file
        json_file = open(fn, 'w')
        json_file.write(json.dumps(mJ.jason_dict, indent = 4, sort_keys=True))
        json_file.close()

    def load_json(fn):
        with open(fn) as f:
            return json.load(f)

    def delete_gruppe(gn, t=None, st=None):
        if t is None:         # Fall nur 1. Ebene
            dict_gn = mJ.jason_dict.get(gn, None)
            if dict_gn is not None:
                del mJ.jason_dict[gn]
            else:
                pass
        elif st is None:      # Fall 2. Ebene
            dict_gn = mJ.jason_dict.get(gn, None)
            if dict_gn is not None:
                dict_gn_t = mJ.jason_dict[gn].get(t,None)
                if dict_gn_t is not None:
                    del mJ.jason_dict[gn][t]
                else:
                    pass  #nichts da zu löschen
            else:
                pass    # wenn das Kopf nicht existiert, dann kann die 2. Ebene nicht existieren
        else:
            dict_gn = mJ.jason_dict.get(gn, None)
            if dict_gn is not None:
                dict_gn_t = mJ.jason_dict[gn].get(t,None)
                if dict_gn_t is not None:
                    dict_gn_t_st = mJ.jason_dict[gn][t].get(st,None)
                    if dict_gn_t_st is not None:
                        del mJ.jason_dict[gn][t][st]

    def update_gruppe(gn, Value, t=None, st=None):
        # Die Gruppe muss es geben 
        if mJ.jason_dict.get(gn, None) is None:
            mJ.jason_dict.update({gn: {}})
        
        #Wenn es nicht weiter verschachtelt ist, dann schreiben
        if t is None:         # Fall nur 1. Ebene
            mJ.jason_dict.update({gn: Value})

        # Wenn es nur einfach verschachtel ist, dann die erste Ebene schreiben
        if t is not None and st is None:      # Fall 2. Ebene
            mJ.jason_dict[gn].update({t: Value})

        if t is not None and st is not None:      # Fall 2. Ebene
            dict_gn_t = mJ.jason_dict[gn].get(t, None)
            if dict_gn_t is None:
                mJ.jason_dict[gn].update({t:{}})
            mJ.jason_dict[gn][t].update({st: Value})

    def get_gruppen_value(gn, t=None, st=None):
        Val = None
        if t is None:         # Fall nur 1. Ebene
            dict_gn = mJ.jason_dict.get(gn, None)
            if dict_gn is not None:
                Val = mJ.jason_dict[gn]
        
        elif st is None:      # Fall 2. Ebene
            dict_gn = mJ.jason_dict.get(gn, None)
            if dict_gn is not None:
                dict_gn_t = mJ.jason_dict[gn].get(t,None)
                if dict_gn_t is not None:
                    Val = mJ.jason_dict[gn][t]
            else:
                pass    # wenn das Kopf nicht existiert, dann kann die 2. Ebene nicht existieren
        else:
            dict_gn = mJ.jason_dict.get(gn, None)
            if dict_gn is not None:
                dict_gn_t = mJ.jason_dict[gn].get(t,None)
                if dict_gn_t is not None:
                    dict_gn_t_st = mJ.jason_dict[gn][t].get(st,None)
                    if dict_gn_t_st is not None:
                        Val = mJ.jason_dict[gn][t][st]
        return Val

    def saveRahmen(f_name, g_name, Points):
        fkt_name = 'saveRahmen in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        mJ.check_for_name(f_name)
        mJ.update_gruppe(g_name, str(Points), 'Rahmen')
        mJ.write_json(mJ.get_jason_name(f_name))

    def getRahmen(f_name, g_name):
        fkt_name = 'getRahmen in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        Val = mJ.get_gruppen_value(g_name, 'Rahmen')
        return eval(Val)

    def savePunkteVorherNahher(f_name, g_name, PointsV, PointsN):
        fkt_name = 'savePunkteVorherNahher in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        mJ.check_for_name(f_name)
        mJ.update_gruppe(g_name, str(PointsV), 'Points', 'vorher' )
        mJ.update_gruppe(g_name, str(PointsN), 'Points', 'nachher' )
        mJ.write_json(mJ.get_jason_name(f_name))

    def getPunkteVorherNahher(f_name, g_name):
        fkt_name = 'getPunkteVorherNahher in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        Val1 = mJ.get_gruppen_value(g_name, 'Points', 'vorher')
        Val2 = mJ.get_gruppen_value(g_name, 'Points', 'nachher')
        return eval(Val1), eval(Val2)

    def saveFixPunkte(f_name, g_name, Point):
        fkt_name = 'saveFixPunkte in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        mJ.check_for_name(f_name)
        mJ.update_gruppe(g_name, str(Point), 'FixPunkt' )
        mJ.write_json(mJ.get_jason_name(f_name))

    def getFixPunkte(f_name, g_name):
        fkt_name = 'getFixPunkte in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        Val = mJ.get_gruppen_value(g_name, 'FixPunkt')
        return eval(Val)

    def saveFunktion(f_name, g_name, Points, Grad):
        fkt_name = 'saveFixPunkte in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        mJ.check_for_name(f_name)
        mJ.update_gruppe(g_name, str(Points), 'Funktion','Punkte' )
        mJ.update_gruppe(g_name, str(Grad), 'Funktion','Grad' )
        mJ.write_json(mJ.get_jason_name(f_name))

    def getFunktion(f_name, g_name):
        fkt_name = 'getFunktion in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        Val1 = mJ.get_gruppen_value(g_name, 'Funktion', 'Punkte')
        Val2 = mJ.get_gruppen_value(g_name, 'Funktion', 'Grad')
        return eval(Val1), eval(Val2)

    def GruppeKomplettLoeschen(f_name, g_name):
        fkt_name = 'GruppeKomplettLoeschen in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        mJ.delete_gruppe(g_name)
        mJ.write_json(mJ.get_jason_name(f_name))

    def GruppeLoeschen(f_name, g_name, t):
        fkt_name = 'GruppeLoeschen in morphjson: '
        try:
            mJ.jason_dict = mJ.load_json(mJ.get_jason_name(f_name))
        except Exception as e:
            print(fkt_name, ' Error: ', str(e))
        mJ.delete_gruppe(g_name,t=t)
        mJ.write_json(mJ.get_jason_name(f_name))


 


