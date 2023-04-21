import sqlite3

con = sqlite3.connect('cartes.db')
cur = con.cursor()
print('Opened database successfully')

cur.execute("DROP TABLE survie")
cur.execute("""CREATE TABLE survie
            (c_id INT PRIMARY KEY NOT NULL,
             nom VARCHAR2(30) NOT NULL,
             phase INT NOT NULL,
             description VARCHAR(150) NOT NULL)
             """)
con.commit()
cur.execute("""
    INSERT INTO survie VALUES
        (1, 'Amplificateur', 4, "Retirez le pion Balise de la Plage pour avancer immédiatement le pion secours d'une case" ),
        (2, "Système D", 1, "Placer le pion Balise sur la plage"),
        (3, "Riposte", 1, "Tirer deux cartes Traque au hasard de la main de la créature et placez-les sous la pioche Traque"),
        (4, "Sixième sens", 1, "Reprenez en main deux cartes Lieu de votre défausse"),
        (5, "Adrénaline", 1, "Récupérer 1 de volonté"),
        (6, "Drone", 3, "A la place d'utiliser le pouvoir de votre carte Lieu, copier le pouvoir du Rover"),
        (7, "Détecteur", 3, "Evitez les effets du jeton Artemia"),
        (8, "Volte-face, 4, "Reprenez en main votre carte Lieu jouée"),
        (9, "Esquive", 3, "Evitez les effets du jeton Créature"),
        (10, "Hologramme", 3, "Déplacez le jeton Artemia sur un lieu adjacent"),
        (11, "Portail", 3, "A la place d'utiliser le pouvoir de votre carte Lieu, copier le pouvoir d'un lieu adjacent"),
        (12, "Brouillage", 1, "Tous les traqués cachent les cartes Lieu de leur défausse jusqu’à la fin du tour"),
        (13, "Fausse piste", 3, "Déplacez le jeton Créature sur un lieu adjacent"), 
        (14, "Vortex", 2, "Échangez votre carte Lieu jouée contre une carte Lieu de votre défausse"), 
        (15, "Sacrifice", 1, "Défaussez une carte Lieu. Aucune carte Traque ne peut être jouée ce tour-ci")
""")    
        
cur.execute("DROP TABLE traque")
cur.execute("""CREATE TABLE traque
            (c_id INT PRIMARY KEY NOT NULL,
             nom VARCHAR2(30) NOT NULL,
             phase INT,
             description VARCHAR(150) NOT NULL,
             Jeton_sup VARCHAR(10))
             """)

cur.execute("""
    INSERT INTO survie VALUES
(1, "Virus", 2,  "Ciblez 2 lieux adjacents. Les effets du jeton Artémia s’appliquent sur ces 2 lieux", "Artemia"),
(2, "Hurlements, 2, "Chaque traqué présent sur le lieu ciblé doit défausser 2 cartes Lieux, ou perdre 1 Volonté", "Cible"),
(3, "Cataclysme", 3, "Le pouvoir du lieu de votre choix est inutilisable", NULL),
(4, "Harcèlement", 2, "Chaque traqué ne peut récupérer que 1 seule carte lieu quand il utilise le pouvoir d’un lieu", NULL), 
(5, "Désespoir", 1, "Aucune carte Survie ne peut être jouée ou piochée pour le reste du tour", "Artémia"),
(6, "Clone", 2, "Considérez le jeton cible comme un second jeton créature", "Cible"),
(7, "Anticipation", 2, "Désignez un Traqué. Si vous l’attrapez avec le jeton Créature, le pion Assimilation avance d’une case supplémentaire", NULL),
(8, "Repérage", 4, "Au prochain tour, vous pouvez jouer jusqu’à 2 cartes Traque", NULL),
(9, "Acharnement", 2, "Le jeton Créature fait perdre 1 Volonté supplémentaire", NULL),
(10, "Zone interdite", 2, "Les Traqués défaussent simultanément 1 carte lieu", NULL), 
(11, "Champ de force", 1, "Avant que les Traqués ne jouent, ciblez 2 lieux adjacents. Ces lieux sont inaccessibles pour le tour", "Cible"),
(12, "Interférences", 2, "Les pouvoirs de la Plage et de l'Épave sont inutilisables", NULL),
(13, "Stase", 4, "Le pion secours n’avance pas lors de cette phase", NULL), 
(14, "Psychose", 2, "Le Traqué de votre choix vous révèle toutes les cartes Lieu de sa main sauf 2", "Artémia"),
(15, "Flashback", NULL, "Copier la dernière carte Traque défaussée", NULL), 
(16, "Toxine", 2, "Chaque Traquée présent sur le lieu ciblé défausse 1 carte Survie. Le pouvoir du lieu est inutilisable", "Cible"),
(17, "Mirage", 2, "Ciblez 2 lieux adjacents. Leurs pouvoirs sont inutilisables", "Cible"),
(18, "Détour", 3, "Avant de résoudre les lieux, déplacez 1 Traqué vers un lieu adjacent", NULL), 
(19, "Mutation", 2, "En plus de ses effets, le jeton Artémia fait perdre 1 Volonté", "Artémia"),
(20, "Emprise", 2, "Le Traqué de votre choix défausse toutes les Cartes Lieu de sa main sauf 2 ", NULL)
""") 

con.commit()
res = cur.execute("SELECT * FROM survie")
print(res.fetchall())
print("Table created successfully")
cur.close()
