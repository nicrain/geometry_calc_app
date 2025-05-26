# Calculatrice de Géométrie

Une application de calculatrice de géométrie moderne construite avec PyQt6. Cette application permet aux utilisateurs de calculer l'aire et le périmètre de diverses formes géométriques avec une interface utilisateur intuitive et responsive, spécialement conçue pour les enfants en âge scolaire.

## Fonctionnalités

- **Formes Multiples** : Supporte le calcul pour les rectangles, cercles, triangles et trapèzes
- **Interface Intuitive** : Interface utilisateur moderne et conviviale avec un design responsive
- **Calculs en Temps Réel** : Résultats instantanés lors de la saisie des valeurs
- **Validation des Entrées** : Validation robuste des entrées utilisateur avec gestion d'erreurs
- **Design Responsive** : Fonctionne parfaitement sur desktop et mobile
- **Thème Sombre** : Interface moderne avec un thème sombre élégant
- **Support Multi-Modal** : Interface traditionnelle avec préparation pour le contrôle oculaire

## Formes Supportées

### Rectangle
- **Aire** : longueur × largeur
- **Périmètre** : 2 × (longueur + largeur)

### Cercle
- **Aire** : π × rayon²
- **Périmètre** : 2 × π × rayon

### Triangle
- **Aire** : (base × hauteur) ÷ 2
- **Périmètre** : côté1 + côté2 + côté3

### Trapèze
- **Aire** : ((base1 + base2) × hauteur) ÷ 2
- **Périmètre** : base1 + base2 + côté1 + côté2

## 🛠️ Technologies et Dépendances

### Dépendances Actuellement Utilisées

#### Dépendance Principale
- **PyQt6 (≥6.5.0)** - Framework GUI multiplateforme moderne, dépendance principale du projet
- **Modules Python intégrés** - math, pathlib, etc. pour les calculs mathématiques de base et les opérations de fichiers

#### Outils de Développement
- **pytest (≥7.3.1)** - Framework de tests unitaires
- **pytest-qt (≥4.2.0)** - Support de test pour les applications PyQt6
- **black (≥23.3.0)** - Outil de formatage de code
- **flake8 (≥6.0.0)** - Outil de vérification de la qualité du code
- **isort (≥5.12.0)** - Outil de tri des déclarations d'importation
- **pyinstaller (≥5.9.0)** - Création de fichiers exécutables autonomes

### Dépendances Réservées (Non Utilisées Actuellement)

Les dépendances suivantes sont commentées dans requirements.txt et réservées pour les extensions futures :

#### Calculs Mathématiques Avancés
- **NumPy (≥1.24.0)** - Pour les calculs mathématiques complexes et les opérations matricielles
  - *État actuel* : Utilise le module math intégré de Python
  - *Usage prévu* : Transformations géométriques, analyses statistiques, fonctions mathématiques avancées

#### Technologies de Suivi Oculaire
- **MediaPipe (≥0.10.0)** - Bibliothèque de vision par apprentissage automatique de Google
  - *État actuel* : Interface réservée, non implémentée
  - *Usage prévu* : Suivi oculaire en temps réel, interaction par contrôle oculaire
- **OpenCV (≥4.7.0)** - Bibliothèque de vision par ordinateur
  - *État actuel* : Non utilisée
  - *Usage prévu* : Traitement d'images, préprocessing des données de suivi oculaire

#### Fonctionnalités de Traitement d'Images
- **Pillow (≥9.5.0)** - Bibliothèque de traitement d'images Python
  - *État actuel* : Non utilisée
  - *Usage prévu* : Édition d'images, conversion de formats, export graphique

#### Système de Retour Vocal
- **pyttsx3 (≥2.90)** - Moteur de synthèse vocale
  - *État actuel* : Fonctionnalité réservée
  - *Usage prévu* : Invites vocales, retour d'opérations, assistance d'apprentissage

#### Visualisation de Données
- **Matplotlib (≥3.7.1)** - Bibliothèque de visualisation pour le calcul scientifique
  - *État actuel* : Non utilisée
  - *Usage prévu* : Graphiques statistiques, visualisation des progrès d'apprentissage, analyse de données

#### Support d'Internationalisation
- **python-i18n (≥0.3.9)** - Bibliothèque de support multilingue
  - *État actuel* : Interface française codée en dur
  - *Usage prévu* : Commutation dynamique de langues, interface multilingue
- **pygettext (≥2.7)** - Outils d'internationalisation
  - *État actuel* : Non utilisé
  - *Usage prévu* : Gestion des fichiers de traduction, outils de localisation

## Comment Utiliser

1. **Sélectionner une Forme** : Choisissez la forme géométrique que vous souhaitez calculer dans la liste déroulante
2. **Saisir les Dimensions** : Entrez les dimensions requises dans les champs de saisie
3. **Voir les Résultats** : L'aire et le périmètre sont calculés automatiquement et affichés en temps réel
4. **Changer de Forme** : Sélectionnez une autre forme pour effectuer différents calculs

## Structure du Projet

```
geometry_calc_app/
├── main.py                              # Point d'entrée de l'application PyQt6
├── requirements.txt                     # Liste des dépendances du projet
├── README.md                           # Documentation principale du projet
├── README_CN.md                        # Documentation détaillée en chinois
└── modules/                            # Package des modules fonctionnels
    ├── __init__.py                     # Fichier marqueur de package Python
    ├── ui_components_pyqt.py           # Composants UI Metro (boutons, composants de base)
    ├── geometry_module_refactored.py   # Module de dessin géométrique (version refactorisée)
    ├── calculator_module_pyqt.py       # Module calculatrice
    ├── eye_tracker_module.py           # Module de suivi oculaire (interface réservée)
    ├── canvas.py                       # Composant canvas de dessin
    ├── shapes.py                       # Définitions des formes et énumérations
    ├── factories.py                    # Classes Factory (gestionnaires et panneaux)
    ├── shape_handlers/                 # Répertoire des gestionnaires de formes
    │   ├── __init__.py                 # Classe de base ShapeHandler
    │   ├── point_handler.py            # Gestionnaire de forme point
    │   ├── line_handler.py             # Gestionnaire de forme ligne
    │   ├── rectangle_handler.py        # Gestionnaire de rectangle
    │   ├── circle_handler.py           # Gestionnaire de cercle
    │   └── triangle_handler.py         # Gestionnaire de triangle
    ├── property_panels/                # Répertoire des panneaux de propriétés
    │   ├── __init__.py                 # Classe de base PropertyPanel
    │   ├── point_properties_panel.py   # Panneau de propriétés de point
    │   ├── line_properties_panel.py    # Panneau de propriétés de ligne
    │   ├── rectangle_properties_panel.py # Panneau de propriétés de rectangle
    │   ├── circle_properties_panel.py  # Panneau de propriétés de cercle
    │   └── triangle_properties_panel.py # Panneau de propriétés de triangle
    └── shapes/                         # Répertoire des définitions de formes
        ├── __init__.py                 # Types de formes et énumérations
        └── point.py                    # Définition spécialisée de la classe Point
```

## Installation et Configuration

### Prérequis Système
- Python 3.8+ (recommandé 3.9+)
- Système d'exploitation : Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- Mémoire : 4GB+ RAM recommandé
- Carte graphique : Support OpenGL 2.0+ (pour le rendu graphique)

### Étapes d'Installation

1. **Cloner le Répertoire**
   ```bash
   git clone [url-du-repo]
   cd geometry_calc_app
   ```

2. **Créer et Activer un Environnement Virtuel** (fortement recommandé)
   ```bash
   # Créer un environnement virtuel
   python -m venv .venv
   
   # Activer l'environnement virtuel
   # macOS/Linux:
   source .venv/bin/activate
   # Windows:
   .venv\Scripts\activate
   ```

3. **Installer les Dépendances**
   ```bash
   # Installation de base (uniquement les dépendances actuellement utilisées)
   pip install -r requirements.txt
   
   # Vérifier l'installation
   python -c "import PyQt6; print('PyQt6 installé avec succès')"
   ```

4. **Optionnel : Activer les Fonctionnalités Réservées**

   Pour activer des fonctionnalités spécifiques réservées, éditez le fichier requirements.txt et décommentez les lignes de dépendances correspondantes :

   ```bash
   # Activer les fonctionnalités de suivi oculaire
   pip install mediapipe>=0.10.0 opencv-python>=4.7.0
   
   # Activer le retour vocal
   pip install pyttsx3>=2.90
   
   # Activer les calculs mathématiques avancés
   pip install numpy>=1.24.0
   
   # Activer la visualisation de données
   pip install matplotlib>=3.7.1
   
   # Activer le support multilingue
   pip install python-i18n>=0.3.9
   ```

5. **Exécuter le Programme**
   ```bash
   python main.py
   ```

### Résolution des Problèmes Courants

**Q: Erreur "Impossible d'importer les modules PyQt6"**
```bash
# Solution : Réinstaller PyQt6
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6>=6.5.0
```

**Q: Échec d'importation de module**
```bash
# S'assurer d'être dans le bon répertoire
ls modules/  # Devrait afficher les fichiers .py
python -c "import sys; print(sys.path)"
```

**Q: Souhait d'activer les fonctionnalités de suivi oculaire**
```bash
# Décommenter les lignes pertinentes dans requirements.txt, puis installer
pip install mediapipe>=0.10.0 opencv-python>=4.7.0
# Note : Cette fonctionnalité est actuellement une interface réservée nécessitant un développement supplémentaire
```

### Options d'Exécution

Le programme supporte les arguments de ligne de commande suivants :

```bash
# Exécution de base
python main.py

# Mode débogage
python main.py --debug

# Spécifier la taille de fenêtre
python main.py --width 1280 --height 800

# Désactiver les effets d'animation (pour les appareils à faibles performances)
python main.py --no-animations

# Spécifier la langue (si supporté)
python main.py --lang fr

# Voir les informations d'aide
python main.py --help
```

## Caractéristiques du Code

### Structure PyQt6
- Structure sémantique avec des composants appropriés
- Design responsive utilisant les layouts PyQt6
- Gestion d'événements moderne et réactive

### CSS et Styling
- Variables de couleur personnalisées pour une maintenance facile
- Animations fluides et transitions
- Thème moderne avec un excellent contraste

### Logique Python
- Code modulaire avec séparation des préoccupations
- Validation robuste des entrées utilisateur
- Gestion d'erreurs avec messages utilisateur informatifs
- Calculs en temps réel avec performance optimisée

## Validation des Entrées

L'application inclut une validation complète des entrées :
- **Vérification des Nombres** : S'assure que toutes les entrées sont des nombres valides
- **Valeurs Positives** : Valide que toutes les dimensions sont positives
- **Messages d'Erreur** : Fournit des messages d'erreur clairs et utiles
- **Mise en Évidence Visuelle** : Met en évidence les champs avec des erreurs

## Compatibilité

Cette application est compatible avec :
- **Systèmes d'exploitation** : Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python** : 3.8+ (recommandé 3.9+)
- **PyQt6** : 6.5.0+

## 🔮 Améliorations Futures

### Objectifs à Court Terme (3 mois)
- [ ] Compléter les fonctionnalités d'édition graphique du module géométrie
- [ ] Ajouter des fonctionnalités de calcul avancées à la calculatrice
- [ ] Implémenter le système de retour vocal de base (activer pyttsx3)
- [ ] Améliorer la couverture des tests unitaires (objectif 80%+)

### Objectifs à Moyen Terme (6 mois)
- [ ] Intégrer les fonctionnalités de suivi oculaire MediaPipe
- [ ] Ajouter le support multilingue (activer python-i18n, supporter chinois, anglais, français)
- [ ] Implémenter la persistance des données (sauvegarder les progrès utilisateur)
- [ ] Ajouter plus de formes géométriques : trapèzes, polygones, etc.
- [ ] Intégrer NumPy pour les calculs mathématiques avancés

### Objectifs à Long Terme (1 an)
- [ ] Développer un mode d'enseignement et un apprentissage guidé
- [ ] Ajouter des éléments de gamification et des mécanismes de récompense
- [ ] Supporter les fonctionnalités de collaboration en réseau
- [ ] Développer une version mobile (PyQt for Mobile)
- [ ] Intégrer des fonctionnalités d'apprentissage assisté par IA
- [ ] Ajouter des fonctionnalités de visualisation de données (activer Matplotlib)

## 📊 Explication de la Gestion des Dépendances

### Dépendances Principales (Obligatoires)
La version actuelle ne nécessite que l'installation de PyQt6, toutes les autres fonctionnalités sont implémentées en utilisant les modules Python intégrés.

### Dépendances Optionnelles (Activation selon les Besoins)
Selon les fonctionnalités requises, vous pouvez installer sélectivement les dépendances réservées :

- **Suivi oculaire** : `mediapipe`, `opencv-python`
- **Retour vocal** : `pyttsx3`
- **Mathématiques avancées** : `numpy`
- **Visualisation de données** : `matplotlib`
- **Support multilingue** : `python-i18n`, `pygettext`
- **Traitement d'images** : `pillow`

### Dépendances de Développement
Les outils pour l'assurance qualité du code et les tests sont inclus dans requirements.txt.

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pusher vers la branche
5. Ouvrir une Pull Request

## 🐛 Problèmes Connus

- Sur certaines distributions Linux, des plugins de plateforme Qt supplémentaires peuvent être nécessaires
- Les fonctionnalités de suivi oculaire sont actuellement des interfaces réservées nécessitant un développement supplémentaire
- Des problèmes de mise à l'échelle d'interface peuvent exister sur les écrans haute DPI
- Les dépendances réservées NumPy, MediaPipe, etc. ne sont pas encore intégrées dans le code

## Licence

Ce projet est open source et disponible sous la [Licence MIT](LICENSE).

## Support

Si vous rencontrez des problèmes ou avez des questions, n'hésitez pas à ouvrir une issue dans le répertoire du projet.

---

<p align="center">
    <i>🌟 Un voyage d'apprentissage mathématique conçu pour les enfants 🌟</i><br>
    <sub>Rendre l'apprentissage amusant et productif</sub>
</p>
