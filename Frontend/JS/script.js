document.addEventListener('DOMContentLoaded', () => {
    /**
     * Gestion du formulaire de connexion
     */
    const connexion_form = document.getElementById('connexion_form');
    const errorMessage = document.getElementById('errorMessage'); // Conteneur pour afficher les erreurs

    // Vérifie si le formulaire de connexion existe sur la page
    if (connexion_form) {
        // Écoute l'événement de soumission du formulaire
        connexion_form.addEventListener('submit', function (event) {
            event.preventDefault(); // Empêche le rechargement de la page lors de la soumission
    
            // Récupère les valeurs des champs de formulaire (nom d'utilisateur et mot de passe)
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
    
            // Vérifie si les champs sont vides
            if (!username || !password) {
                alert("Veuillez remplir tous les champs.");
                return;
            }
    
            // Envoie les données au serveur via une requête POST
            fetch('http://localhost:3002/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
            .then(response => {
                // Si la réponse n'est pas correcte (non OK), on gère l'erreur
                if (!response.ok) {
                    return response.text().then(errorText => { throw new Error(errorText); });
                }
                return response.text();
            })
            .then(data => {
                // Réponse du serveur après la connexion réussie
                console.log('Réponse du serveur :', data);
                // Enregistre le profil de l'utilisateur dans le localStorage
                localStorage.setItem('userProfile', JSON.stringify({ username }));
                // Redirige l'utilisateur vers la page principale
                window.location.href = '../html/main.html';
            })
            .catch(error => {
                // Si une erreur survient lors de la requête, on l'affiche
                console.error('Erreur lors de la connexion :', error);
                errorMessage.style.display = 'block';
                errorMessage.textContent = error.message;
            });
        });
    }

    

    /**
     * Gestion du bouton "Supprimer le profil"
     */
    const deleteProfileButton = document.getElementById('deleteProfileButton');

    if (deleteProfileButton) {
        // Écoute l'événement de clic sur le bouton
        deleteProfileButton.addEventListener('click', function (event) {
            event.preventDefault(); // Empêche tout comportement par défaut du bouton

            // Demande confirmation avant suppression du profil
            const confirmDelete = confirm("Êtes-vous sûr de vouloir supprimer votre profil ?");
            if (confirmDelete) {
                const name = prompt("Entrez votre nom :");

                if (!name) {
                    alert("Nom requis pour supprimer le profil.");
                    return;
                }

                // Envoie la requête pour supprimer le profil au serveur
                fetch('http://localhost:3002/delete-user', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: name }) // Envoi des informations de l'utilisateur
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Votre profil a été supprimé avec succès !");
                            localStorage.removeItem('userProfile'); // Supprime le profil du localStorage
                            window.location.href = '../html/connexion.html'; // Redirige vers la page de connexion
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

    // Vérifie si le formulaire d'inscription existe sur la page
    if (signUpForm) {
        signUpForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Empêche le rechargement de la page lors de la soumission
    
            // Récupère les valeurs des champs du formulaire (nom d'utilisateur, mot de passe et validation du mot de passe)
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            const validPassword = document.getElementById('valid-password').value.trim();
    
            // Vérifie si les champs sont vides
            if (!username || !password || !validPassword) {
                alert("Veuillez remplir tous les champs.");
                return;
            }

            // Vérifie si les mots de passe correspondent
            if (password !== validPassword) {
                alert("Les mots de passe ne correspondent pas.");
                return;
            }

            console.log("Envoi des données au serveur...");

            try {
                // Envoie les données d'inscription au serveur
                const response = await fetch('http://localhost:3002/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                console.log("Réponse reçue du serveur :", response);

                // Si la réponse n'est pas OK, on gère l'erreur
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText);
                }

                const data = await response.json();
                console.log("Inscription réussie :", data);

                // Enregistre l'utilisateur en localStorage pour qu'il reste connecté
                localStorage.setItem('userProfile', JSON.stringify({ username }));

                // Redirection vers la page principale
                console.log("Redirection vers main.html...");
                window.location.href = '../html/main.html';

            } catch (error) {
                // Si une erreur survient lors de l'inscription, on l'affiche
                console.error('Erreur lors de l’inscription :', error);
                errorMessage.style.display = 'block';
                errorMessage.textContent = error.message;
            }
        });
    }
});

/**
 * Fonction pour quitter une fenêtre ou rediriger vers une autre page
 */
function quitter() {
    let openedWindow

    openedWindow = window.open("../html/main.html");
    openedWindow = window.close("../html/main.html");
}
