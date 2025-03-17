const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

// Middleware pour parser les données envoyées en POST
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Lire le fichier JSON contenant les utilisateurs
function readUsersFromFile() {
    return new Promise((resolve, reject) => {
        const usersPath = path.join(__dirname, 'Data', 'users.json');

        fs.readFile(usersPath, 'utf8', (err, data) => {
            if (err) {
                reject("Erreur lors de la lecture du fichier JSON :" + err);
                return;
            }

            try {
                const users = JSON.parse(data);
                resolve(users); // Résoudre la promesse avec les utilisateurs
            } catch (e) {
                reject('Erreur de parsing : ' + e);
            }
        });
    });
}

// Récupérer la liste des utilisateurs
app.get('/users', async (req, res) => {
    try {
        const users = await readUsersFromFile();
        res.status(200).json(users); // Retourne les utilisateurs
    } catch (error) {
        res.status(500).json({ error: error });
    }
});

// Connexion
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        const users = await readUsersFromFile();

        // Chercher l'utilisateur dans le fichier JSON
        const user = users.find(u => u.username === username);

        if (!user) {
            console.log('user not found')
            return res.status(404).json({ error: 'Utilisateur non trouvé' });
        }

        // Vérifier le mot de passe
        if (user.password === password) {
            return res.status(200).json({ message: 'Connexion réussie' });
        } else {
            return res.status(400).json({ error: 'Mot de passe incorrect' });
        }
    } catch (error) {
        return res.status(500).json({ error: 'Erreur lors de la lecture des utilisateurs' });
    }
});

// Démarrer le serveur
app.listen(3001, () => {
    console.log('Server running on http://localhost:3001');
});
