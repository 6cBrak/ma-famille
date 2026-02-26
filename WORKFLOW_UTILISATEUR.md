# Workflow utilisateur — Arbre généalogique familial (MVP)

## Objectif
Permettre à une famille de construire son arbre à plusieurs :
1. un membre crée la famille,
2. ajoute sa famille nucléaire (père, mère, enfants),
3. invite les autres membres,
4. chaque invité complète sa propre branche.

---

## Parcours utilisateur

### 1) Création du compte
- L'utilisateur crée son compte (email + mot de passe).
- Il renseigne son profil minimal (prénom, nom, date de naissance optionnelle).

### 2) Création de la famille
- L'utilisateur clique sur **Créer une famille**.
- Le système génère :
  - un `family_id` unique,
  - un `invite_code` (ou lien d'invitation).
- Le créateur devient **admin de la famille**.

### 3) Ajout de la famille nucléaire
Le créateur ajoute :
- son père,
- sa mère,
- ses enfants,
- éventuellement son/sa conjoint(e).

Règles MVP :
- toute personne ajoutée appartient à un seul `family_id`,
- une personne ne peut pas être son propre parent,
- les liens autorisés : `PARENT_OF`, `SPOUSE_OF`.

### 4) Invitation des membres
Depuis l'espace famille, le créateur envoie des invitations :
- par email,
- ou en partageant le `family_id` + `invite_code`.

Statuts d'invitation :
- `pending` (envoyée),
- `accepted` (acceptée),
- `expired` (expirée),
- `revoked` (révoquée).

### 5) Entrée des membres invités
Un invité :
1. crée son compte (ou se connecte),
2. rejoint la famille via invitation,
3. confirme son identité dans l'arbre (match avec une personne existante) ou crée sa fiche,
4. complète sa branche (conjoint, enfants, parents si manquants).

### 6) Validation et contrôle
- Les membres modifient les fiches qu'ils ont créées.
- L'admin famille peut corriger/valider les liens conflictuels.
- Le système évite les doublons probables (même nom + date + parents proches).

### 7) Affichage de l'arbre
- Vue globale de la famille.
- Filtre par personne racine.
- Navigation par générations.

---

## Rôles et permissions (MVP)

### Admin famille
- inviter/supprimer des membres,
- valider ou corriger des liens,
- gérer les paramètres de la famille.

### Membre
- voir l'arbre de sa famille,
- proposer/éditer sa branche,
- accepter/refuser les suggestions de liaison le concernant.

---

## Données minimales à stocker

- `users` : compte utilisateur
- `families` : métadonnées de la famille
- `family_members` : appartenance user ↔ family + rôle
- `persons` : individus de l'arbre
- `relationships` : liens parent/enfant, conjoint
- `invitations` : token d'invitation + statut

---

## Critères d'acceptation MVP
- Un utilisateur peut créer une famille.
- Il peut ajouter père, mère, enfant(s).
- Il peut inviter un autre membre.
- L'invité peut rejoindre et compléter sa partie.
- Les données sont visibles dans un arbre unique par `family_id`.
