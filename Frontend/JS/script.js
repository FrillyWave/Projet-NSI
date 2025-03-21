document.addEventListener('DOMContentLoaded', () => {
    /**
     * Gestion du formulaire de création de joueur
     */
    const connexion_form = document.getElementById('connexion_form');
    const errorMessage = document.getElementById('errorMessage'); // Conteneur pour afficher les erreurs

    if (connexion_form) {
        connexion_form.addEventListener('submit', function (event) {
            event.preventDefault();
    
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
    
            if (!username || !password) {
                alert("Veuillez remplir tous les champs.");
                return;
            }
    
            fetch('http://localhost:3002/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(errorText => { throw new Error(errorText); });
                }
                return response.text();
            })
            .then(data => {
                console.log('Réponse du serveur :', data);
                localStorage.setItem('userProfile', JSON.stringify({ username }));
                window.location.href = '../html/main.html';
            })
            .catch(error => {
                console.error('Erreur lors de la connexion :', error);
                errorMessage.style.display = 'block';
                errorMessage.textContent = error.message;
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

                if (!name) {
                    alert("Nom requis pour supprimer le profil.");
                    return;
                }

                // Envoi de la requête de suppression au serveur
                fetch('http://localhost:3002/delete-user', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name }) // Envoi des identifiants du joueur
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


document.addEventListener('DOMContentLoaded', () => {
    const signUpForm = document.getElementById('sign_up-form');
    const errorMessage = document.getElementById('errorMessage'); // Conteneur pour afficher les erreurs

    if (signUpForm) {
        signUpForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Empêche le rechargement de la page
    
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            const validPassword = document.getElementById('valid-password').value.trim();
    
            if (!username || !password || !validPassword) {
                alert("Veuillez remplir tous les champs.");
                return;
            }

            if (password !== validPassword) {
                alert("Les mots de passe ne correspondent pas.");
                return;
            }

            console.log("Envoi des données au serveur...");

            try {
                const response = await fetch('http://localhost:3002/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                console.log("Réponse reçue du serveur :", response);

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText);
                }

                const data = await response.json();
                console.log("Inscription réussie :", data);

                // Stocker l'utilisateur en localStorage pour qu'il reste connecté
                localStorage.setItem('userProfile', JSON.stringify({ username }));

                // Redirection vers la page principale
                console.log("Redirection vers main.html...");
                window.location.href = '../html/main.html';

            } catch (error) {
                console.error('Erreur lors de l’inscription :', error);
                errorMessage.style.display = 'block';
                errorMessage.textContent = error.message;
            }
        });
    }
});




function quitter() {
    let openedWindow

    openedWindow = window.open("../html/main.html")
    openedWindow = window.close("../html/main.html")

}