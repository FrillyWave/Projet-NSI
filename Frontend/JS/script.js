document.addEventListener('DOMContentLoaded', () => {
    /**
     * Gestion du formulaire de création de joueur
     */
    const connexion_form = document.getElementById('connexion_form');
    const errorMessage = document.getElementById('errorMessage'); // Conteneur pour afficher les erreurs

    if (connexion_form) {
        connexion_form.addEventListener('submit', function (event) {
            event.preventDefault(); // Empêche le rechargement de la page lors de la soumission du formulaire

            // Récupération des données du formulaire (nom et mot de passe)
            const userName = document.getElementById('userName').value.trim();
            const password = document.getElementById('password').value.trim();

            // Vérification si les champs sont remplis
            if (!userName || !password) {
                alert("Veuillez remplir tous les champs");
                return;
            }

            // Création de l'objet contenant les données du joueur
            const userData = {
                name: userName,
                password: password,
            };

            console.log('Données du joueur avant envoi :', userData);

            // Réinitialisation des messages d'erreur
            errorMessage.style.display = 'none';
            errorMessage.textContent = '';

            // Envoi des données du joueur au serveur pour l'enregistrer
            fetch('http://localhost:3000/add-user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData) // Envoie des données en format JSON
            })
                .then(response => {
                    if (!response.ok) {
                        // Si la réponse n'est pas OK, récupérer le message d'erreur
                        return response.text().then(errorText => { throw new Error(errorText); });
                    }
                    return response.text(); // Récupérer la réponse du serveur
                })
                .then(data => {
                    console.log('Réponse du serveur :', data);
                    localStorage.setItem('userProfile', JSON.stringify(userData)); // Sauvegarde locale des infos du joueur
                    window.location.href = '../html/main.html'; // Redirection vers la page d'introduction du jeu
                })
                .catch(error => {
                    console.error('Erreur lors de l\'envoi des données :', error);
                    errorMessage.style.display = 'block';
                    errorMessage.textContent = error.message;

                    // Si le nom est déjà pris, vider les champs pour forcer le joueur à en choisir un autre
                    if (error.message.includes("existe déjà")) {
                        document.getElementById('userName').value = '';
                        document.getElementById('password').value = '';
                    }
                });
        });
    }

    /**
     * Sauvegarde de la progression du joueur
     */
    const currentPage = window.location.pathname.split('/').pop(); // Récupère la page actuelle (ex. "debut.html")
    const userProfile = JSON.parse(localStorage.getItem('userProfile'));

    if (userProfile) {
        userProfile.currentPage = currentPage; // Met à jour la progression dans le stockage local
        localStorage.setItem('userProfile', JSON.stringify(userProfile));

        // Envoi de la progression mise à jour au serveur
        fetch('http://localhost:3000/update-progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: userProfile.name,
                currentPage: currentPage
            })
        }).catch(error => console.error('Erreur mise à jour progression :', error));
    }

    /**
     * Gestion du bouton "Reprendre la partie"
     */
    const resumeButton = document.getElementById('resumeButton');

    if (resumeButton) {
        resumeButton.addEventListener('click', () => {
            const userProfile = JSON.parse(localStorage.getItem('userProfile'));

            if (userProfile && userProfile.currentPage) {
                // Redirige le joueur vers la dernière page visitée
                window.location.href = `../html/${userProfile.currentPage}`;
            } else {
                alert('Aucune sauvegarde trouvée. Commencez une nouvelle partie.');
            }
        });
    }

    /**
     * Gestion du bouton "Supprimer le profil"
     */
    const deleteProfileButton = document.getElementById('deleteProfileButton');

    if (deleteProfileButton) {
        deleteProfileButton.addEventListener('click', function (event) {
            event.preventDefault(); // Empêche tout comportement par défaut du bouton

            // Demande confirmation avant suppression
            const confirmDelete = confirm("Êtes-vous sûr de vouloir supprimer votre profil ?");
            if (confirmDelete) {
                const name = prompt("Entrez votre nom :");
                const password = prompt("Entrez votre mot de passe :");

                if (!name || !password) {
                    alert("Nom et mot de passe requis pour supprimer le profil.");
                    return;
                }

                // Envoi de la requête de suppression au serveur
                fetch('http://localhost:3000/delete-user', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, password }) // Envoi des identifiants du joueur
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Votre profil a été supprimé avec succès !");
                            localStorage.removeItem('userProfile'); // Supprime le profil en local
                            window.location.href = '../html/index.html'; // Redirige vers l'accueil
                        } else {
                            alert(data.message || "Erreur lors de la suppression du profil.");
                        }
                    })
                    .catch(error => {
                        console.error("Erreur lors de la suppression :", error);
                    });
            }
        });
    } else {
        console.warn("Bouton 'Supprimer le profil' introuvable sur cette page.");
    }
});



function quitter() {
    let openedWindow

    openedWindow = window.open("../html/main.html")
    openedWindow = window.close("../html/main.html")

}