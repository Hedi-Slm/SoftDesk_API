# SoftDesk API

SoftDesk API est une API RESTful développée avec Django REST Framework qui permet aux entreprises de suivre et gérer les problèmes techniques pour leurs applications.

## Fonctionnalités

- **Authentification** sécurisée via JSON Web Token (JWT)
- **Gestion des utilisateurs** conforme au RGPD:
  - Consentement (peut être contacté, peut-on partager les données)
  - Vérification de l'âge (minimum 15 ans)
- **Gestion des projets**:
  - Création avec titre, description et type (back-end, front-end, iOS, Android)
  - Ajout/suppression de contributeurs
- **Gestion des problèmes (issues)**:
  - Création d'issues avec titre et description
  - Classification par priorité (LOW, MEDIUM, HIGH)
  - Classification par type (BUG, FEATURE, TASK)
  - Suivi de statut (TODO, IN_PROGRESS, FINISHED)
  - Attribution à des contributeurs
- **Système de commentaires**:
  - Ajout de commentaires sur les issues
  - Identification unique par UUID
- **Contrôle d'accès**:
  - Seuls les contributeurs d'un projet peuvent y accéder
  - Seul l'auteur d'une ressource peut la modifier ou la supprimer
- **Pagination** pour le listage des ressources

## Prérequis

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+
- Pip

## Installation

1. Clonez ce dépôt sur votre machine locale:
   ```
   git clone https://github.com/Hedi-Slm/SoftDesk_API
   ```

2. Créez un environnement virtuel:
   ```
   python -m venv env
   ```

3. Activez l'environnement virtuel:
   - Windows: `env\Scripts\activate`
   - macOS/Linux: `source env/bin/activate`

4. Installez les dépendances:
   ```
   pip install -r requirements.txt
   ```

5. Effectuez les migrations de la base de données:
   ```
   python manage.py migrate
   ```

6. Créez un superutilisateur (facultatif):
   ```
   python manage.py createsuperuser
   ```
   Permet d'accéder au panneau d'administration de Django. a l'adresse: http://127.0.0.1:8000/admin


7. Lancez le serveur de développement:
   ```
   python manage.py runserver
   ```

8. Accédez à l'API via votre navigateur ou Postman à l'adresse: http://127.0.0.1:8000/api/.


## Utilisation

### Endpoints de l'API

#### Authentification
- `POST /api/auth/register/` - Inscription d'un nouvel utilisateur
- `POST /api/auth/login/` - Obtention d'un token JWT (login)
- `POST /api/auth/refresh/` - Rafraîchissement du token JWT

#### Utilisateurs
- `GET /api/auth/me/` - Récupération des informations de l'utilisateur connecté

#### Projets
Voici un exemple d'utilisation pour chaque endpoints disponibles pour les projets:
- `GET /api/projects/` - Liste des projets auxquels l'utilisateur contribue
- `POST /api/projects/` - Création d'un nouveau projet
- `GET /api/projects/{id}/` - Détails d'un projet spécifique
- `POST /api/projects/{id}/add_contributor/` - Ajout d'un contributeur au projet (auteur uniquement)
- `DELETE /api/projects/{id}/remove_contributor/` - Suppression d'un contributeur du projet (auteur uniquement)

#### Issues
Voici un exemple d'utilisation pour chaque endpoints disponibles pour les issues:
- `GET /api/issues/` - Liste des issues
- `POST /api/issues/` - Création d'une nouvelle issue
- `GET /api/issues/{id}/` - Détails d'une issue spécifique

#### Commentaires
Voici un exemple d'utilisation pour chaque endpoints disponibles pour les commentaires:
- `GET /api/comments/` - Liste des commentaires
- `POST /api/comments/` - Création d'un nouveau commentaire
- `GET /api/comments/{id}/` - Détails d'un commentaire spécifique

### Filtres disponibles

#### Issues
- `project` - Filtrer par projet (ex: `/api/issues/?project={porject_id}`)
- `assignee` - Filtrer par assigné (ex: `/api/issues/?assignee={user_id}`)
- `author` - Filtrer par auteur (ex: `/api/issues/?author={user_id}`)
- Tri possible par (`?ordering=field`):
  - `priority` - Priorité des issues
  - `status` - Statut des issues
  - `tag` - Type d'issues

#### Commentaires
- `issue` - Filtrer par issue (ex: `/api/comments/?issue={issue_id}`)
- Tri possible par (`?ordering=field`):
  - `created_time` - Date de création
  - `issue` - Issue associée

### Exemples d'utilisation avec Postman

1. **Inscription d'un utilisateur**:
   - Méthode: POST
   - URL: `http://127.0.0.1:8000/api/auth/register/`
   - Corps (JSON):
     ```json
     {
       "username": "testuser",
       "password": "secure_password123",
       "password2": "secure_password123",
       "email": "user@example.com",
       "first_name": "Test",
       "last_name": "User",
       "age": 25,
       "can_be_contacted": true,
       "can_data_be_shared": false
     }
     ```

2. **Connexion**:
   - Méthode: POST
   - URL: `http://127.0.0.1:8000/api/auth/token/`
   - Corps (JSON):
     ```json
     {
       "username": "testuser",
       "password": "secure_password123"
     }
     ```
   - Réponse: Conservez les tokens d'accès et de rafraîchissement

3. **Création d'un projet**:
   - Méthode: POST
   - URL: `http://127.0.0.1:8000/api/projects/`
   - Headers: `Authorization: Bearer votre_token_jwt`
   - Corps (JSON):
     ```json
     {
       "title": "Mon Application Mobile",
       "description": "Une application pour suivre les activités quotidiennes",
       "type": "ANDROID"
     }
     ```

4. **Création d'une issue**:
   - Méthode: POST
   - URL: `http://127.0.0.1:8000/api/issues/`
   - Headers: `Authorization: Bearer votre_token_jwt`
   - Corps (JSON):
     ```json
     {
       "title": "Crash au démarrage",
       "description": "L'application se ferme lors du démarrage sur certains appareils",
       "project": "uuid-du-projet",
       "tag": "BUG",
       "priority": "HIGH",
       "status": "TODO",
       "assignee_id": "uuid-de-l-auteur"
     }
     ```

5. **Création d'un commentaire**:
   - Méthode: POST
   - URL: `http://127.0.0.1:8000/api/comments/`
   - Headers: `Authorization: Bearer votre_token_jwt`
   - Corps (JSON):
     ```json
     {
       "issue": "uuid-de-l-issue",
       "description": "Ceci est un commentaire"
     }
     ```

## Notes importantes

- Toutes les requêtes (sauf l'inscription et la connexion) nécessitent un token JWT valide dans l'en-tête d'autorisation.
- Les identifiants des projets, issues et commentaires sont des UUID.
- Seul l'auteur d'une ressource peut la modifier ou la supprimer.
- Seuls les contributeurs d'un projet peuvent accéder à ses issues et commentaires.
