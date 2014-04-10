from tkinter import *
import helper
import random 

class Vue():
    def __init__(self,parent,largeur,hauteur):
        self.parent=parent
        self.modele=self.parent.modele
        self.root=Tk()
        self.tuile=32
        self.canevas=Canvas(self.root,width=largeur*self.tuile,
                            height=hauteur*self.tuile,bg="white")
        self.canevas.grid(column=0,row=1,columnspan=2)
        self.canevas.bind("<Button>",self.clic)
        self.canevas.bind("<Double-Button>",self.doubleclic)
        self.selection=[0,0]
        self.info={}
        self.cadreInfo()
        self.cadreCommandes()
        
    def cadreCommandes(self):
        bexpedier=Button(self.root,text="Expedier",command=self.expedierFlotte)
        bexpedier.grid(column=0,row=2,pady=16)
        
        self.echelle=Scale(self.root,state=DISABLED,to=0.0,orient=HORIZONTAL,label="")
        self.echelle.grid(column=1,row=2,sticky=W+E+S)
        
        fguerre=Frame(self.root)
        
        bguerre=Button(fguerre,text="LA GUERRE")#, command=self.prochainTour)
        bguerre.bind("<Button>",self.prochainTour)
        self.root.bind("<Return>",self.prochainTour)
        
        self.lguerre=Label(fguerre,text="---")
        bguerre.grid(column=0,row=0,sticky=W+E)
        self.lguerre.grid(column=0,row=1,sticky=W+E)
        
        fguerre.grid(column=2,row=2,sticky=W+E)
        
    def avertirTour(self,msg):
        self.lguerre.config(text=msg)
        
    def prochainTour(self,evt):
        self.parent.prochainTour()
        
    def expedierFlotte(self):
        if self.echelle.get()>0:
            self.parent.expedieFlotte(self.echelle.get(),self.selection[0],self.selection[1],self.info["duree"].cget("text"))
            
            self.miseajourOrigine()
            self.miseajourDestination()
            self.miseajourEchelle(self.selection[0])
            self.miseajourVaisseaux()
    def doubleclic(self,evt):
        t=self.canevas.gettags(CURRENT)
        if "etoile" in t:
            e=self.parent.getEtoile(int(t[1]))
            print("INFO",e.x,e.y,e.manufactures,e.vaisseaux)
                
    def clic(self,evt):
        t=self.canevas.gettags(CURRENT)
        if "etoile" in t:
            e=self.parent.getEtoile(int(t[1]))
            if self.selection[0]:
                if self.selection[0]!=e:
                    self.selection[1]=e
            else:
                self.selection[0]=e
                self.miseajourEchelle(e)
                    
        
        else:
            self.selection=[0,0]
            self.miseajourEchelle("")
            
        self.afficheSelection()
        #self.miseajourInfo()
        self.miseajourOrigine()
        self.miseajourDestination()
        #self.miseajourVaisseaux()
        
    def miseajourEchelle(self,e):
        if self.parent.joueurHumain(e):
            self.echelle.config(to=e.vaisseaux)
            self.echelle.config(label=e.vaisseaux)
            self.echelle.config(showvalue=1)
            self.echelle.config(state=NORMAL)
            self.echelle.set(0)
        else:
            self.echelle.config(to=0)
            self.echelle.config(label="")
            self.echelle.config(showvalue=0)
            self.echelle.config(state=DISABLED)
    def miseajourAnnee(self):
        self.info["annee"].config(text=self.modele.annee)
        
    def miseajourInfo(self):
        self.info["humain"].config(text=len(self.modele.civs["humain"].dependances))
        self.info["gubru"].config(text=len(self.modele.civs["gubru"].dependances))
        self.info["czin"].config(text=len(self.modele.civs["czin"].dependances))
        self.miseajourAnnee()
        
    def miseajourVaisseaux(self):
        self.info["port"].config(text=self.parent.getVaisseauxPort())
        self.info["transit"].config(text=self.parent.getVaisseauxTransit())
    
    def miseajourOrigine(self):
        if self.selection[0]:
            self.info["origine"].config(text=str(self.selection[0].x)+","+str(self.selection[0].y))
        else:
            self.info["origine"].config(text="")
    def miseajourDestination(self):
        if self.selection[1]:
            self.info["destination"].config(text=str(self.selection[1].x)+","+str(self.selection[1].y))
            dist= helper.Helper.calcDistance(self.selection[0].x,self.selection[0].y,
                                           self.selection[1].x,self.selection[1].y)
           
            
            self.info["distance"].config(text=round(dist,1))
            if dist<2:
                duree=dist/2
            else:
                duree=1+((dist-2)/3)
            self.info["duree"].config(text=round(duree,1))
        
        
        else:
            self.info["destination"].config(text="")
            self.info["distance"].config(text="")
            self.info["duree"].config(text="")
            
            
    def afficheSelection(self):
        self.canevas.delete("selection")
        taille=20
        if self.selection[0]:
            i=self.selection[0]
            x=i.x*self.tuile+(self.tuile/2)
            y=i.y*self.tuile+(self.tuile/2)
            self.canevas.create_rectangle(x-taille,y-taille,x+taille,y+taille,
                                          outline="darkgreen",dash=( 1, 1 ),
                                          tags=("selection",i.id,i.prop))
        
        if self.selection[1]:
            j=self.selection[1]
            demi=self.tuile/2
            x=j.x*self.tuile+(self.tuile/2)
            y=j.y*self.tuile+(self.tuile/2)
            self.canevas.create_oval(x-taille,y-taille,x+taille,y+taille,
                                          outline="darkgreen",dash=( 1, 1 ),
                                          tags=("selection",j.id,j.prop))
            
            self.canevas.create_line(i.x*self.tuile+demi,i.y*self.tuile+demi,j.x*self.tuile+demi,j.y*self.tuile+demi,
                                          tags=("selection",))
        #self.miseajourVaisseaux()
        
    def cadreInfo(self):
        
        b1=Button(self.root, text="Demarre partie",
                  command=self.parent.demarrePartie)
        b1.grid(column=0,row=0)
        fstats=Frame(self.root)
        lh=Label(fstats,text="Humain").grid(sticky=W,column=0,row=0)
        lg=Label(fstats,text="Gubru").grid(sticky=W,column=0,row=1)
        lc=Label(fstats,text="Czin").grid(sticky=W,column=0,row=2)
        la=Label(fstats,text="Attaque").grid(column=0,row=3,columnspan=2)
        lp=Label(fstats,text="A partir:").grid(sticky=W,column=0,row=4)
        lv=Label(fstats,text="Vers:").grid(sticky=W,column=0,row=5)
        ld=Label(fstats,text="Dist:").grid(sticky=W,column=0,row=6)
        ldu=Label(fstats,text="Duree:").grid(sticky=W,column=0,row=7)
        lf=Label(fstats,text="Flotte").grid(column=0,row=8,columnspan=2)
        lp=Label(fstats,text="Port").grid(sticky=W,column=0,row=9)
        lt=Label(fstats,text="Transit").grid(sticky=W,column=0,row=10)
        lper=Label(fstats,text="Periode").grid(column=0,row=11,columnspan=2)
        lan=Label(fstats,text="Annee:").grid(sticky=W,column=0,row=12)
        
        lh=Label(fstats,text="1000000")
        lh.grid(sticky=E,column=1,row=0)
        self.info["humain"]=lh
        
        lg=Label(fstats,text="0")
        lg.grid(sticky=E,column=1,row=1)
        self.info["gubru"]=lg
        
        lc=Label(fstats,text="0")
        lc.grid(sticky=E,column=1,row=2)
        self.info["czin"]=lc

        lo=Label(fstats,text="0")
        lo.grid(sticky=E,column=1,row=4)
        self.info["origine"]=lo
        
        ldest=Label(fstats,text="0")
        ldest.grid(sticky=E,column=1,row=5)
        self.info["destination"]=ldest
        
        ldist=Label(fstats,text="0")
        ldist.grid(sticky=E,column=1,row=6)
        self.info["distance"]=ldist
        
        ldu=Label(fstats,text="0")
        ldu.grid(sticky=E,column=1,row=7)
        self.info["duree"]=ldu

        lp=Label(fstats,text="0")
        lp.grid(sticky=E,column=1,row=9)
        self.info["port"]=lp
        
        lt=Label(fstats,text="0")
        lt.grid(sticky=E,column=1,row=10)
        self.info["transit"]=lt

        lan=Label(fstats,text="Annee:")
        lan.grid(sticky=E,column=1,row=12)
        self.info["annee"]=lan
        
        fstats.grid(column=2,row=1,sticky=N)
        
    def affichePartie(self,modele):
        self.canevas.delete("etoile")
        taille=6
        for i in modele.etoiles:
            if i.prop:
                couleur=i.prop.couleur
            else:
                couleur="black"
            x=i.x*self.tuile+(self.tuile/2)
            y=i.y*self.tuile+(self.tuile/2)
            self.canevas.create_rectangle(x-taille,y-taille,
                                     x+taille,y+taille,fill=couleur,
                                     tags=("etoile",i.id,i.prop))
        
        self.miseajourInfo()
        self.miseajourOrigine()
        self.miseajourDestination()
        self.miseajourVaisseaux()


class Espace():
    def __init__(self,parent):
        self.parent=parent
        self.nextId=0
        self.largeur=28
        self.hauteur=22
        self.annee=0
        self.etoiles=[]
        self.civs={}
        
    def prochainTour(self):
        self.parent.avertirTour("Strategie Gubru")
        self.civs["gubru"].prochainTour()
        self.parent.avertirTour("Strategie Czin")
        self.civs["czin"].prochainTour()
        n=0.1
        courant=self.annee
        for i in range(10):
            courant=round(courant+n,1)
            self.parent.avertirTour("Evalue"+str(courant))
            for j in self.civs:
                
                self.civs[j].evalueFlotte(courant)
        self.annee=self.annee+1
        for i in self.civs:
            self.civs[i].deletedeaddependances()
        self.mettreEtoileAJour()
        
    def mettreEtoileAJour(self):
        for i in self.etoiles:
            i.vaisseaux=i.vaisseaux+i.manufactures
        
        
    def demarrePartie(self):
        self.etoiles=[]
        h,g,c=self.makeEtoiles(50)
        self.civs={"humain":Humain(self,h,"olivedrab2",10,100),
                   "gubru":Gubru(self,g,"red",10,100),
                   "czin":Czin(self,c,"deepskyblue2",10,100)}
        

    def mettreAJour(self):
        pass
    def getEtoile(self,n):
        for i in self.etoiles:
            if i.id==n :
                return i 
        return None
        
        self.makeEtoiles(50)
    def getVaisseauxPort(self,civ):
        n=0
        for i in self.civs[civ].dependances:
            n=n+i.vaisseaux
        return n
    def getVaisseauxTransit(self,civ):
        n=0
        for i in self.civs[civ].flottes:
            for j in self.civs[civ].flottes[i]:
                n=n+j.vaisseaux
        return n
        
    def makeEtoiles(self,n=50):
        co=[]
        while n:
            x=random.randrange(self.largeur)
            y=random.randrange(self.hauteur)
            if [x,y] not in co:
                co.append([x,y])
                n=n-1
        for i in co:
            self.etoiles.append(Etoile(self,self.nextId,i))
            self.nextId=self.nextId+1
            
        etoiles=self.etoiles[:]
        h=random.choice(etoiles)
        etoiles.remove(h)
        g=random.choice(etoiles)
        etoiles.remove(g)
        c=random.choice(etoiles)
        return h,g,c
            
class Etoile():
    def __init__(self,parent,id,pos,prop=""):
        self.parent=parent
        self.id=id
        self.valeurGrappe=0
        self.x=pos[0]
        self.y=pos[1]
        self.prop=prop
        self.manufactures=random.randrange(7)
        self.vaisseaux=self.manufactures
        
    def mettreAjour(self):
        pass
    
class Flotte():
    def __init__(self,destination,vaisseaux):
        self.destination=destination
        self.vaisseaux=vaisseaux

class Civ():
    def __init__(self,parent,etoilemere):
        self.parent=parent
        self.etoiles=[]
        self.etoilemere=etoilemere
        etoilemere.prop=self
        self.dependances=[etoilemere]
        self.deaddependances=[]
        self.flottes={}
        self.couleur="black"
    def deletedeaddependances(self):
        for i in self.deaddependances:
            self.dependances.remove(i)
        self.deaddependances=[]
        
    def creeFlotte(self,nv,origine,dest,duree):
        origine.vaisseaux=origine.vaisseaux-nv
        d=duree+self.parent.annee
        f=Flotte(dest,nv)
        if d in self.flottes:
            self.flottes[d].append(f)
        else:
            self.flottes[d]=[f]
        return f
    
    def evalueFlotte(self,courant):
        if courant in self.flottes:
            print("Une flotte arrive",len(self.flottes[courant]))
            for i in self.flottes[courant]:
                if i.destination in self.dependances:
                    i.destination.vaisseaux=i.destination.vaisseaux+i.vaisseaux
                else:
                    if i.destination.vaisseaux:
                        decision=self.evalueCombat(i)
                    else:
                        decision=1
                    if decision:
                        if i.destination.prop:
                            i.destination.prop.deaddependances.append(i.destination)
                        i.destination.vaisseaux=i.vaisseaux
                        i.destination.prop=self
                        if i.destination not in self.dependances:
                            self.dependances.append(i.destination)
            del self.flottes[courant]
                
    def evalueCombat(self,f):
        vd=f.destination.vaisseaux
        v=f.vaisseaux
        t=1
        tourdefense=1
        while t:
            combat=random.randrange(10)
            if combat<7:
                if tourdefense:
                    v=v-1
                else:
                    vd=vd-1
            else:
                if tourdefense:
                    vd=vd-1
                else:
                    v=v-1
            if v==0 or vd ==0:
                t=0
            else:
                if tourdefense:
                    tourdefense=0
                else:
                    tourdefense=1
        f.destination.vaisseaux=vd
        f.vaisseaux=v
        if v:
            return 1
        else:
            return 0
            
        
class Gubru(Civ):
    def __init__(self,parent,etoilemere,couleur,manufactures,vaisseaux):
        Civ.__init__(self,parent,etoilemere)
        self.couleur=couleur
        etoilemere.manufactures=manufactures
        etoilemere.vaisseaux=vaisseaux
        self.cibles=[]
        self.ciblestemp=[]
        self.vaisseauxparattaque=5
        self.forceminattaque=10
        self.garnisonminimale=15
        self.garnisonlimite=25
        
    def prochainTour(self):
        self.etoilemere=self.dependances[0]
        forcedattaque=max(self.parent.annee*(self.vaisseauxparattaque+self.forceminattaque),
                           2*self.forceminattaque)
        print("Condition",self.etoilemere.vaisseaux,">",forcedattaque,self.forceminattaque)
        if self.etoilemere.vaisseaux>forcedattaque+self.forceminattaque:
            nbrattaque=int(self.etoilemere.vaisseaux/forcedattaque)
            print("NbraTTAQUE",nbrattaque)
            for i in range(nbrattaque):
                e=self.trouveplaneteproche()
            for i in self.cibles:
                self.creeFlotte(forcedattaque, self.etoilemere, i[0], i[1])
                print("GUBRU ATTAQUE",i[0].x,i[0].y,forcedattaque)
            self.cibles=[]
            self.ciblestemp=[]
        for i in self.dependances:
            if i !=self.etoilemere:
                if i.vaisseaux>self.garnisonlimite:
                    dist=helper.Helper.calcDistance(i.x,i.y,self.etoilemere.x,self.etoilemere.y)
                    if dist<2:
                        duree=dist/2
                    else:
                        duree=1+((dist-2)/3)
                    self.creeFlotte(i.vaisseaux-self.garnisonminimale, i, self.etoilemere, round(duree,1))
                    #self.creeFlotte(i.vaisseaux, i, self.etoilemere, d)
    def trouveplaneteproche(self):
        e=""
        de=1000000
        x=self.etoilemere.x
        y=self.etoilemere.y
        for i in self.parent.etoiles:
            d=round(helper.Helper.calcDistance(x,y,i.x,i.y),1)
            if d<de and i not in self.dependances and i not in self.ciblestemp:
                e=i
                de=d
        self.ciblestemp.append(e)
        if de<2:
            duree=de/2
        else:
            duree=1+((de-2)/3)
        self.cibles.append([e,round(duree,1)])
            
class Czin(Civ):
    def __init__(self,parent,etoilemere,couleur,manufactures,vaisseaux):
        Civ.__init__(self,parent,etoilemere)
        self.couleur=couleur
        etoilemere.manufactures=manufactures
        etoilemere.vaisseaux=vaisseaux
        self.etoileBase=self.etoilemere
        self.armada=""
        self.dist_grappe=4
        self.vaisseauxparattaque=4
        self.forceattaquebasique=20
        self.garnisonminimale=15
        self.garnisonlimite=25
        self.grappes={} #liste d'etoiles autour d'une base
        self.calcValeurGrappe()
        self.modeActif="armada"#base,invasion,renforcement 
        self.actionAFaire={"armada":self.construisArmada,
                           "base":self.construisBase,
                           "invasion":self.construisInvasion,
                           "renforcement":self.renforcement}
    def prochainTour(self):
        self.actionAFaire[self.modeActif]()
        
    def testGarnisonArmada(self):
        pass
        
        
    def construisArmada(self):# ICI
        print("Czin construit ARMADA")
        garnisonpretpourarmada=self.testGarnisonArmada()
        if not self.armada:
            base=self.choisirGrappe()
            duree=12
            i=self.etoileBase
            dist=helper.Helper.calcDistance(i.x,i.y,base.x,base.y)
            if dist<2:
                duree=dist/2
            else:
                duree=1+((dist-2)/3)
            self.creeFlotte(i.vaisseaux-self.garnisonminimale, i, self.etoilemere, round(duree,1))
            
        
    def renforcement(self):
        print("Czin construit RENFORCEMENT") 
        
        force=self.parent.annee*self.vaisseauxparattaque*self.forceattaquebasique
        if self.etoileBase.vaisseaux>force:
            self.modeActif="armada"
    
    def construisBase(self):
        print("Czin construit BASE")
    def construisInvasion(self):
        print("Czin construit INVASION")  
        
    def calcValeurGrappe(self):
        for i in self.parent.etoiles:
            i.valeurGrappe=0
        for i in self.parent.etoiles:
            for j in self.parent.etoiles:
                dist=helper.Helper.calcDistance(i.x,i.y,j.x,j.y)
                if dist<= self.dist_grappe:
                    s=self.dist_grappe-dist+1
                    i.valeurGrappe=i.valeurGrappe+(s*s)
        for i in self.parent.etoiles:
            print("VAL",i.id,i.x,i.y,i.prop,i.valeurGrappe)
    
        
    def choisirGrappe(self):
        base=self.etoileBase
        for i in self.parent.etoiles:
            if i.valeurGrappe> base.valeurGrappe and i not in self.dependances:
                base=i
        return base               
        
    def tourGubru(self):
        self.etoilemere=self.dependances[0]
        forcedattaque=max(self.parent.annee*(self.vaisseauxparattaque+self.forceminattaque),
                           2*self.forceminattaque)
        print("Condition",self.etoilemere.vaisseaux,">",forcedattaque,self.forceminattaque)
        if self.etoilemere.vaisseaux>forcedattaque+self.forceminattaque:
            nbrattaque=int(self.etoilemere.vaisseaux/forcedattaque)
            print("NbraTTAQUE",nbrattaque)
            for i in range(nbrattaque):
                e=self.trouveplaneteproche()
            for i in self.cibles:
                self.creeFlotte(forcedattaque, self.etoilemere, i[0], i[1])
                print("GUBRU ATTAQUE",i[0].x,i[0].y,forcedattaque)
            self.cibles=[]
            self.ciblestemp=[]
        for i in self.dependances:
            if i !=self.etoilemere:
                if i.vaisseaux>self.garnisonlimite:
                    d=round(helper.Helper.calcDistance(i.x,i.y,self.etoilemere.x,self.etoilemere.y),1)
                    self.creeFlotte(i.vaisseaux-self.garnisonminimale, i, self.etoilemere, d)
                    #self.creeFlotte(i.vaisseaux, i, self.etoilemere, d)

class Humain(Civ):
    def __init__(self,parent,etoilemere,couleur,manufactures,vaisseaux):
        Civ.__init__(self,parent,etoilemere)
        self.couleur=couleur
        etoilemere.manufactures=manufactures
        etoilemere.vaisseaux=vaisseaux
    
class Controleur():
    def __init__(self):
        self.modele=Espace(self)
        self.vue=Vue(self,self.modele.largeur,
                     self.modele.hauteur)
        #self.vue.afficheMenu()
        self.vue.root.mainloop()
        
    def demarrePartie(self):
        self.modele.demarrePartie()
        self.vue.affichePartie(self.modele)
        
    def getEtoile(self,n):
        return self.modele.getEtoile(n)
    
    def getVaisseauxPort(self):
        return self.modele.getVaisseauxPort("humain")
    def getVaisseauxTransit(self):
        return self.modele.getVaisseauxTransit("humain")
    def joueurHumain(self,e):
        if e in self.modele.civs["humain"].dependances:
            return 1
        else:
            return 0
        
    def expedieFlotte(self,nv,origine,dest,duree):
        self.modele.civs["humain"].creeFlotte(nv,origine,dest,duree)
        
    def prochainTour(self):
        self.modele.prochainTour()
        self.vue.affichePartie(self.modele)
        
    def avertirTour(self,msg):
        self.vue.avertirTour(msg)
        


if __name__ == '__main__':
    c=Controleur()