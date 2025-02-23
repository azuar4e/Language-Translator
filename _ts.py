#____________________________________________
#imports

#____________________________________________
#variables

TSLexico = {}
pos = 0
contador = 1
archivo = None

#____________________________________________
#clases

class TablaSimbolos:
    def __init__(self):
        self.tabla_global = {}
        self.tablas_locales = {}

    def buscartsglobal(self, lexema):
        if lexema in self.tabla_global:
            return self.tabla_global[lexema]
        return None
    
    def insertarlexema(self, lexema, tabla):
        if tabla is None:
            self.tabla_global[lexema] = {}
        else:
            self.tablas_locales[tabla][lexema] = {}
    
    def insertartipots(self, lexema, tipo, tabla):
        if tabla is None:
            self.tabla_global[lexema]["tipo"] = tipo
        else:
            self.tablas_locales[tabla][lexema]["tipo"] = tipo

    def insertardesplts(self, lexema, despl, tabla):
        if tabla is None:
            self.tabla_global[lexema]["despl"] = despl
        else:
            self.tablas_locales[tabla][lexema]["despl"] = despl
            
    def contiene(self, lexema):
        if lexema in self.tabla_global:
            return True, "global", self.tabla_global[lexema]["despl"]
        elif self.tablas_locales is not None and lexema in self.tablas_locales:
            return True, "local", self.tablas_locales[lexema]["despl"]
        else:
            return False
            
    def buscatipots(self, lexema):        
        if self.tablas_locales is None:
            return self.tabla_global[lexema]["tipo"]
        else:
            if lexema in self.tablas_locales:
                return self.tablas_locales[lexema]["tipo"]
            else:
                return self.tabla_global[lexema]["tipo"]

    def buscatipotsfunc(self, lexema):
        if lexema not in self.tabla_global:
            return None

        if 'tipoparam' not in self.tabla_global[lexema]:
            return None
        return self.tabla_global[lexema]['tipoparam']     

    # def sindeclarar(self, lexema, despl):
    #     self.tabla_global[lexema] = {'tipo': 'ent', 'despl': despl}
        
    # def insertarts(self, lexema, tipo, desplazamiento):
    #     if self.tablas_locales is None:
    #         if lexema not in self.tabla_global:
    #             self.tabla_global[lexema] = {}
    #         self.tabla_global[lexema] = {"tipo": tipo, "despl": desplazamiento}
    #     else:
    #         if lexema not in self.tablas_locales:
    #             self.tablas_locales[lexema] = {}
    #         self.tablas_locales[lexema] = {"tipo": tipo, "despl": desplazamiento}

    def tiporet(self, lexema):
        if lexema in self.tabla_global:
            return self.tabla_global[lexema]['tiporet']
        else:
            return None
            
    # def insertar_funcion(self, lexema, numparam, tiporet):
    #     if lexema not in self.tabla_global:
    #         self.tabla_global[lexema] = {}
        
    #     self.tabla_global[lexema]['tipo'] = 'function'
    #     self.tabla_global[lexema][numparam] = numparam
    #     self.tabla_global[lexema]['tiporet'] = tiporet
        
    #------- funciones para el crear las ts's -------
        
    def insertarnumparam(self, lexema, numparam):
        self.tabla_global[lexema]["numParam"] = numparam
        
    def insertartipoparam(self, lexema, tipoparam, pos):
        self.tabla_global[lexema][f"tipoParam{pos}"] = tipoparam
        
    def insertarmodoparam(self, lexema, modoparam, pos):
        self.tabla_global[lexema][f"modoParam{pos}"] = modoparam
        
    def insertartiporet(self, lexema, tiporet):
        self.tabla_global[lexema]["tiporet"] = tiporet
        
    def insertaretiqfuncion(self, lexema, etiqfuncion):
        self.tabla_global[lexema]["EtiqFuncion"] = etiqfuncion

    # solo para la local porque principal siempre va a haber
    def crearts(self, numero):
        self.tablas_locales[numero] = {}