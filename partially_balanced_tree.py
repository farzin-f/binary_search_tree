# encoding=utf-8

from linked_binary_tree import LinkedBinaryTree
from map_base import MapBase
from linked_queue import LinkedQueue
from binary_search_tree import TreeMap
import math

class PartiallyBalancedTree(TreeMap):
    
  """Override du constructeur de TreeMap"""
  def __init__(self, pmax):
    super(PartiallyBalancedTree, self).__init__()
    self._compteur = 0      # Compteur d'opérations pour rebalancement
    self._pmax = pmax      # profondeur maximum pour rebalancement
    
  #---------------------------- override _Node class ----------------------------
  class _Node(LinkedBinaryTree._Node):
    """Override de la classe Node et ajouter les attributs pour compter 
    le nombredes nodes de sous-arbre gauche et droit d'un position"""
    def __init__(self, element, parent=None, left=None, right=None, leftSubtreeSize=0, rightSubtreeSize=0):
    
      self._element = element
      self._parent = parent
      self._left = left
      self._right = right

      """ **NOUVEAUX ATTRIBUTS**"""
      self._leftSubtreeSize = leftSubtreeSize
      self._rightSubtreeSize = rightSubtreeSize
      
  #---------------------------- override Position class ----------------------------
  class Position(LinkedBinaryTree.Position):
    def key(self):
      """Return key of map's key-value pair."""
      return self.element()._key

    def value(self):
      """Return value of map's key-value pair."""
      return self.element()._value
      
    def leftSubtreeSize(self):
      """ **NOUVELLE MÉTHODE**
          Retourne le nombre d'enfants dans le sous-arbre gauche """
      return self._node._leftSubtreeSize
      
    def rightSubtreeSize(self):
      """ **NOUVELLE MÉTHODE**
          Retourne le nombre d'enfants dans le sous-arbre droit """
      return self._node._rightSubtreeSize
      
    def setSubtreeSize(self, left, newSize):
      """ **NOUVELLE MÉTHODE**
          Entre newSize comme taille du sous-arbre gauche si left = True, droit sinon """
      if left:
        self._node._leftSubtreeSize = newSize
      else:
        self._node._rightSubtreeSize = newSize
      
      return newSize  


  def updateSubtreeSize(self, p, grandparent):
    """ **NOUVELLE MÉTHODE**
        Met à jour l'attribut SubtreeSize gauche ou droit de chaque ancêtre de p jusqu'à la position grandparent
    
        Mise à jour du noeud p (calcul des deux enfants) """
    if self.left(p) is not None:
        p.setSubtreeSize(True, self.left(p).leftSubtreeSize()+self.left(p).rightSubtreeSize()+1)
    else:
        p.setSubtreeSize(True, 0)
    if self.right(p) is not None:
        p.setSubtreeSize(False, self.right(p).leftSubtreeSize()+self.right(p).rightSubtreeSize()+1)
    else:
        p.setSubtreeSize(False, 0)
        
    """ Propage nouveaux SubtreeSize de p jusqu'à la racine """
    while self.parent(p) is not None and self.parent(p) is not grandparent:
        self.parent(p).setSubtreeSize(self.is_leftChild(p), p.leftSubtreeSize()+p.rightSubtreeSize()+1)
        p = self.parent(p)
        
  def is_leftChild(self, p):
    """ **NOUVELLE MÉTHODE**
        Retourne True si p est l'enfant gauche de son parent, False s'il est l'enfant droit"""
    if not self.is_root(p):
        return self.left(self.parent(p)) == p


      
  #--------------------- hooks used by subclasses to balance a tree ---------------------
  def _rebalance_insert(self, p):
    """Call to indicate that position p is newly added."""
    self.updateSubtreeSize(p, self.root())
    self._compteur += 1
    if self._compteur == 100:
        self.rebalancement(self.root())   # commence à la racine
        self._compteur = 0      # remettre le compteur à 0

  def _rebalance_delete(self, p):
    """Call to indicate that a child of p has been removed."""
    self.updateSubtreeSize(p, self.root())
    self._compteur += 1
    if self._compteur == 100:
        self.rebalancement(self.root())   # commence à la racine
        self._compteur = 0      # remettre le compteur à 0

  def _rebalance_access(self, p):
    """Call to indicate that position p was recently accessed."""
    pass
    

  #--------------------- nonpublic methods to support tree balancing ---------------------
  def _rotate(self, p):
    """Rotate Position p above its parent.

    Switches between these configurations, depending on whether p==a or p==b.

          b                  a
         / \                /  \
        a  t2             t0   b
       / \                     / \
      t0  t1                  t1  t2

    Caller should ensure that p is not the root.
    """
    """Rotate Position p above its parent."""
    x = p._node
    px = p
    y = x._parent                                 # we assume this exists
    py = self.parent(p)
    z = y._parent                                 # grandparent (possibly None)
    pz = self.parent(py)
    
    if z is None:            
      self._root = x                              # x becomes root
      x._parent = None        
    else:
      self._relink(z, x, y == z._left)            # x becomes a direct child of z
      self.updateSubtreeSize(px, pz)              # mise a jour le nombre de noeuds a gauche et a droite de position px
      
    # now rotate x and y, including transfer of middle subtree
    if x == y._left:
      self._relink(y, x._right, True)             # x._right becomes left child of y
            
      self._relink(x, y, False)                   # y becomes right child of x
      self.updateSubtreeSize(py, pz)              # mise a jour du nombre de noeuds a gauche et a droite de position py
    else:
      self._relink(y, x._left, False)             # x._left becomes right child of y
      self._relink(x, y, True)                    # y becomes left child of x
      self.updateSubtreeSize(py, pz)              # mise a jour du nombre de noeuds a gauche et a droite de position py


  #------------Nouvelles methodes pour balancement patiel------------
          
  def rebalancement(self, p):
    """Trouver les noeuds dans chaque niveau pour balancer l'arbre
        jusqu'a la profondeur pmax"""
    if p is None or self.depth(p) > self._pmax:   # version récursive
        return
    newRoot = p
    if abs(p.leftSubtreeSize()-p.rightSubtreeSize()) > 1:
        newRoot = self.deplacer(p)
    self.rebalancement(self.left(newRoot))
    self.rebalancement(self.right(newRoot))
  
  def deplacer(self, p):
    """ balancement des element de noeud p verifier si la difference
    entre le nombre d'enfants gauches et droits est plus grande que 1"""
    n = p.rightSubtreeSize()+p.leftSubtreeSize()+1          # nombre total de noeud dans le sous-arbre dont la racine est p
    gauche = math.ceil(n/2) - 1                             # nombre de noeuds à gauche lorsque balancé
    noeudsAGauche = p.leftSubtreeSize()
    walk = p
    
    while noeudsAGauche != gauche:                      # trouver nouvelle racine
      if noeudsAGauche < gauche:                        # pas assez de noeuds à gauche - continuer vers la droite
        walk = self.right(walk)
        noeudsAGauche += (1 + walk.leftSubtreeSize())
      else:                                             # trop de noeuds à gauche - continuer vers la gauche
        walk = self.left(walk)
        noeudsAGauche -= (1 + walk.rightSubtreeSize())
    
    self._partial_balance(p, walk)
    return walk
        

  def _partial_balance(self, p, pMid):
    """ Cette methode fait le balancement partiel d'un sous-arbre
    p: la racine de ce sous-arbre
    pMid: le noeud de milieu de ce sous-arbre"""
        
    pParent = self.parent(p)
    pMidParent = self.parent(pMid)

    while pParent != pMidParent:
      self._rotate(pMid)
      pMidParent = self.parent(pMid)