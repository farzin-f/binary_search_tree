# encoding=utf-8

from threading import Timer
from time import time
from binary_search_tree import TreeMap
from red_black_tree import RedBlackTreeMap
from partially_balanced_tree import PartiallyBalancedTree

# Générateur des mots d'un fichier .txt
def wordGenerator(splitText):
    for fragment in splitText:
        word = ''
        idx = 0
        while idx < len(fragment):
            if fragment[idx].isalpha():
                word += fragment[idx].lower()
                idx += 1
            elif fragment[idx] == "-":
                if idx+1 < len(fragment) and fragment[idx+1] == "-":
                    #print (word)
                    yield word
                    word = ''
                    idx += 2
                else:
                    word += fragment[idx].lower()
                    idx +=1
            else:
                idx += 1
                
        yield word
        

# Itère sur les mots de splitText et les insère dans l'arbre tree
def buildTree(splitText, tree):
    
    global readMode 
        
    counter = 0
    readMode = True
    
    # Démarre le Timer (délai avant l'arrêt de la lecture)
    t = Timer(1, readModeOff)
    t.start()
    start = time()
    
    # Boucle arrête quand readMode passe à False
    for word in wordGenerator(splitText):
        if readMode:
          tree[word] = word
          counter += 1
        else:
          end = time()
          print(str(counter) + " mots lus et insérés en " + str(end-start) + " secondes ")
          return (counter, end-start) # Retourne tuple (nombre de mots, temps)
    
    print("Tous les " + str(counter) +" mots du fichier ont été lus.")
    return (counter, end-start) # Retourne tuple (nombre de mots, temps)
    
# Retire la clé associée à chaque 10e mot du texte
def removeFromTree(splitText, wordMax, tree):
        
        counter = 0
        deleted = 0
        
        
        start = time()
        
        for word in wordGenerator(splitText):
            if counter >= wordMax:
                break
            elif counter % 10 == 0:
                deleted += 1
                try: 
                    del tree[word]
                    #deleted += 1
                except KeyError:    # Ignore KeyError si on tente de supprimer le même mot plus d'une fois
                    pass
                    
            counter += 1
            
        end = time()
        print(str(deleted) + " mots lus et supprimés en " + str(end-start) + " secondes ")
        return (deleted, end-start) # Retourne tuple (nombre de mots, temps)

def readModeOff():
    global readMode
    readMode = False


pp = ""

def impression(arbre, p):
  global pp
    
  if arbre.left(p) is not None:
    pp += "("
    impression(arbre, arbre.left(p))
    pp += ")"
    
  pp += (str(p.value()))
  
  if arbre.right(p) is not None:
    pp += "("
    impression(arbre, arbre.right(p))
    pp += ")"

  return pp

        
# Initialisation des arbres
abr = TreeMap()
abr_modif_1 = PartiallyBalancedTree(1)
abr_modif_2 = PartiallyBalancedTree(2)
abr_modif_3 = PartiallyBalancedTree(3)
abr_modif_4 = PartiallyBalancedTree(4)
rougeNoir = RedBlackTreeMap()  

# Lecture et séparation du fichier .txt
text = open("big.txt")
splitText = text.read().split()

nbEssai = 3

# Test arbre binaire
testResultsInsertion = 0
testResultsSupp = 0

for i in range(nbEssai):
    abr = TreeMap() # Vider l'arbre
    print("Test arbre binaire - essai #" +str(i+1))
    wordsRead = buildTree(splitText, abr)
    wordsRemoved = removeFromTree(splitText, wordsRead[0], abr)
    testResultsInsertion += wordsRead[0]/wordsRead[1]   # Mots traités par seconde
    testResultsSupp += wordsRemoved[0]/wordsRemoved[1]
    
print("Moyenne insertion (mots/seconde) : " + str(testResultsInsertion/nbEssai))
print("Moyenne suppression (mots/seconde) : " + str(testResultsSupp/nbEssai) + "\n")

abr_print = "ABR (aucun balancement)\n" + impression(abr, abr.root())
file_abr = open("strat_1.out", "w")
file_abr.write(abr_print)
file_abr.close()


# Test arbre binaire modifié, pmax = 1
testResultsInsertion = 0
testResultsSupp = 0
for i in range(nbEssai):
    abr_modif_1 = PartiallyBalancedTree(1)  # Vider l'arbre
    print("Test arbre binaire modifié (pmax = 1) - essai #" +str(i+1))
    wordsRead = buildTree(splitText, abr_modif_1)
    wordsRemoved = removeFromTree(splitText, wordsRead[0], abr_modif_1)
    testResultsInsertion += wordsRead[0]/wordsRead[1]   # Mots traités par seconde
    testResultsSupp += wordsRemoved[0]/wordsRemoved[1]
    
print("Moyenne insertion (mots/seconde) : " + str(testResultsInsertion/nbEssai))
print("Moyenne suppression (mots/seconde) : " + str(testResultsSupp/nbEssai) + "\n")

abr_modif_1_print = "ABR (balancement partiel) - pmax = 1: \n" + impression(abr_modif_1, abr_modif_1.root())
file_abr_modif = open("strat_2pmax1.out", "w")
file_abr_modif.write(abr_modif_1_print)
file_abr_modif.close()


# Test arbre binaire modifié, pmax = 2
testResultsInsertion = 0
testResultsSupp = 0
for i in range(nbEssai):
    abr_modif_2 = PartiallyBalancedTree(2)  # Vider l'arbre
    print("Test arbre binaire modifié (pmax = 2) - essai #" +str(i+1))
    wordsRead = buildTree(splitText, abr_modif_2)
    wordsRemoved = removeFromTree(splitText, wordsRead[0], abr_modif_2)
    testResultsInsertion += wordsRead[0]/wordsRead[1]   # Mots traités par seconde
    testResultsSupp += wordsRemoved[0]/wordsRemoved[1]
    
print("Moyenne insertion (mots/seconde) : " + str(testResultsInsertion/nbEssai))
print("Moyenne suppression (mots/seconde) : " + str(testResultsSupp/nbEssai) + "\n")

abr_modif_2_print = "\n\nABR (balancement partiel) - pmax = 2: \n" + impression(abr_modif_2, abr_modif_2.root())
file_abr_modif = open("strat_2pmax2.out", "w")
file_abr_modif.write(abr_modif_2_print)
file_abr_modif.close()


# Test arbre binaire modifié, pmax = 3
testResultsInsertion = 0
testResultsSupp = 0
for i in range(nbEssai):
    abr_modif_3 = PartiallyBalancedTree(3) # Vider l'arbre
    print("Test arbre binaire modifié (pmax = 3) - essai #" +str(i+1))
    wordsRead = buildTree(splitText, abr_modif_3)
    wordsRemoved = removeFromTree(splitText, wordsRead[0], abr_modif_3)
    testResultsInsertion += wordsRead[0]/wordsRead[1]   # Mots traités par seconde
    testResultsSupp += wordsRemoved[0]/wordsRemoved[1]
    
print("Moyenne insertion (mots/seconde) : " + str(testResultsInsertion/nbEssai))
print("Moyenne suppression (mots/seconde) : " + str(testResultsSupp/nbEssai) + "\n")

abr_modif_3_print = "\n\nABR (balancement partiel) - pmax = 3: \n" + impression(abr_modif_3, abr_modif_3.root())
file_abr_modif = open("strat_2pmax3.out", "w")
file_abr_modif.write(abr_modif_3_print)
file_abr_modif.close()


# Test arbre binaire modifié, pmax = 4
testResultsInsertion = 0
testResultsSupp = 0
for i in range(nbEssai):
    abr_modif_4 = PartiallyBalancedTree(4)  # Vider l'arbre
    print("Test arbre binaire modifié (pmax = 4) - essai #" +str(i+1))
    wordsRead = buildTree(splitText, abr_modif_4)
    wordsRemoved = removeFromTree(splitText, wordsRead[0], abr_modif_4)
    testResultsInsertion += wordsRead[0]/wordsRead[1]   # Mots traités par seconde
    testResultsSupp += wordsRemoved[0]/wordsRemoved[1]
    
print("Moyenne insertion (mots/seconde) : " + str(testResultsInsertion/nbEssai))
print("Moyenne suppression (mots/seconde) : " + str(testResultsSupp/nbEssai) + "\n")

abr_modif_4_print = "\n\nABR (balancement partiel) - pmax = 4: \n" + impression(abr_modif_4, abr_modif_4.root())
file_abr_modif = open("strat_2pmax4.out", "w")
file_abr_modif.write(abr_modif_4_print)
file_abr_modif.close()


# Test arbre rouge-noir
testResultsInsertion = 0
testResultsSupp = 0
for i in range(nbEssai):
    rougeNoir = RedBlackTreeMap()  # Vider l'arbre
    print("Test arbre rouge-noir - essai #" +str(i+1))
    wordsRead = buildTree(splitText, rougeNoir)
    wordsRemoved = removeFromTree(splitText, wordsRead[0], rougeNoir)
    testResultsInsertion += wordsRead[0]/wordsRead[1]   # Mots traités par seconde
    testResultsSupp += wordsRemoved[0]/wordsRemoved[1]
    
print("Moyenne insertion (mots/seconde) : " + str(testResultsInsertion/nbEssai))
print("Moyenne suppression (mots/seconde) : " + str(testResultsSupp/nbEssai) + "\n")


rougeNoir_print = "Arbre Rouge-Noir (balancement total)\n" + impression(rougeNoir, rougeNoir.root())
file_rougeNoir = open("strat_3.out", "w")
file_rougeNoir.write(abr_print)
file_rougeNoir.close()

text.close()