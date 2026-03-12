from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# --- PARTIE 1 & 2 : Base et Boissons ---
class Boisson(ABC):
    @abstractmethod
    def cout(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    # PARTIE 4 & 6 : Surcharge de l'opérateur +
    def __add__(self, other):
        if isinstance(other, Boisson):
            return BoissonCombinee(self, other)
        return NotImplemented

class BoissonCombinee(Boisson):
    def __init__(self, b1: Boisson, b2: Boisson):
        self.b1 = b1
        self.b2 = b2
    def cout(self): return self.b1.cout() + self.b2.cout()
    def description(self): return f"{self.b1.description()} + {self.b2.description()}"

class Cafe(Boisson):
    def cout(self): return 2.0
    def description(self): return "Café simple"

class The(Boisson):
    def cout(self): return 1.5
    def description(self): return "Thé"

# --- PARTIE 3 & 6 : Décorateurs (Ingrédients) ---
class DecorateurBoisson(Boisson):
    def __init__(self, boisson: Boisson):
        self._boisson = boisson

class Lait(DecorateurBoisson):
    def cout(self): return self._boisson.cout() + 0.5
    def description(self): return self._boisson.description() + ", Lait"

class Sucre(DecorateurBoisson):
    def cout(self): return self._boisson.cout() + 0.2
    def description(self): return self._boisson.description() + ", Sucre"

class Caramel(DecorateurBoisson):
    def cout(self): return self._boisson.cout() + 0.7
    def description(self): return self._boisson.description() + ", Caramel"

# --- PARTIE 5 : Client ---
@dataclass
class Client:
    nom: str
    numero: int
    points_fidelite: int = 0

# --- PARTIE 7 : Gestion des Commandes ---
class Fidelite:
    def ajouter_points(self, client: Client, montant: float):
        points = int(montant)
        client.points_fidelite += points
        print(f"-> {points} points ajoutés au compte de {client.nom}")

class Commande:
    def __init__(self, client: Client):
        self.client = client
        self.boissons: List[Boisson] = []

    def ajouter_boisson(self, boisson: Boisson):
        self.boissons.append(boisson)

    def calculer_total(self) -> float:
        return sum(b.cout() for b in self.boissons)

    def afficher_commande(self):
        print(f"Client : {self.client.nom} (ID: {self.client.numero})")
        for b in self.boissons:
            print(f"- {b.description()} : {round(b.cout(), 2)}€")
        print(f"Total à payer : {round(self.calculer_total(), 2)}€")

# Travail demandé : Types de commandes
class CommandeSurPlace(Commande):
    def afficher_commande(self):
        print("\n--- COMMANDE SUR PLACE ---")
        super().afficher_commande()

class CommandeEmporter(Commande):
    def afficher_commande(self):
        print("\n--- COMMANDE À EMPORTER ---")
        super().afficher_commande()

# Travail demandé : Héritage multiple
class CommandeFidele(Commande, Fidelite):
    def valider_commande(self):
        total = self.calculer_total()
        self.ajouter_points(self.client, total)
        print(f"Validation terminée. Nouveau solde : {self.client.points_fidelite} points.")

# --- PARTIE 7.5 : Test du système ---
if __name__ == "__main__":
    # 1. Création client
    mon_client = Client("Ahmed", 456)

    # 2. Création boissons
    boisson1 = Sucre(Lait(Cafe()))  # Café avec Lait et Sucre
    boisson2 = Caramel(The())        # Thé avec Caramel
    
    # 3. Commande fidèle
    ma_commande = CommandeFidele(mon_client)
    ma_commande.ajouter_boisson(boisson1)
    ma_commande.ajouter_boisson(boisson2)

    # 4. Affichage et validation
    ma_commande.afficher_commande()
    ma_commande.valider_commande()