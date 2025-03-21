const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors'); // Middleware CORS

const app = express();
const PORT = 3002;

app.use(cors());
app.use(bodyParser.json());

// Endpoint pour ajouter un joueur
app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    const filePath = path.join(__dirname, 'Data', 'users.json'); // Assure-toi que le chemin est correct

    if (!username || !password) {
        return res.status(400).json({ error: 'Tous les champs sont requis' });
    }

    console.log("Nouvel utilisateur :", username);

    // Lire le fichier JSON
    fs.readFile(filePath, 'utf8', (err, data) => {
        let users = [];

        if (!err && data) {
            try {
                users = JSON.parse(data);
            } catch (parseErr) {
                console.error('Erreur parsing JSON :', parseErr);
                return res.status(500).json({ error: 'Erreur de lecture des utilisateurs' });
            }
        }

        // Vérifier si l'utilisateur existe déjà
        if (users.some(user => user.username === username)) {
            return res.status(400).json({ error: 'Nom d’utilisateur déjà pris' });
        }

        // Ajouter le nouvel utilisateur
        users.push({ username, password });

        // Écrire dans users.json
        fs.writeFile(filePath, JSON.stringify(users, null, 2), (writeErr) => {
            if (writeErr) {
                console.error('Erreur d’écriture dans le fichier :', writeErr);
                return res.status(500).json({ error: 'Impossible d’enregistrer l’utilisateur' });
            }
            console.log(`Utilisateur ${username} enregistré avec succès !`);
            res.status(201).json({ message: 'Utilisateur créé avec succès' });
        });
    });
});



// Endpoint pour supprimer un joueur
app.post('/delete-user', (req, res) => {
    const { username } = req.body;  // On récupère uniquement le nom d'utilisateur

    if (!username) {
        return res.status(400).send({ success: false, message: 'Nom requis.' });
    }

    const filePath = path.join(__dirname, 'data', 'users.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Erreur de lecture du fichier :', err);
            return res.status(500).send({ success: false, message: 'Erreur interne du serveur.' });
        }

        let users = JSON.parse(data || '[]');

        // Vérifie si l'utilisateur existe
        const userIndex = users.findIndex(user => user.username === username);
        if (userIndex === -1) {
            return res.status(404).send({ success: false, message: 'Profil introuvable.' });
        }

        // Supprime l'utilisateur du tableau
        users.splice(userIndex, 1);

        // Sauvegarde le fichier mis à jour
        fs.writeFile(filePath, JSON.stringify(users, null, 2), (err) => {
            if (err) {
                console.error('Erreur d\'écriture du fichier :', err);
                return res.status(500).send({ success: false, message: 'Erreur interne du serveur.' });
            }

            console.log(`Profil ${username} supprimé.`);
            res.send({ success: true, message: 'Profil supprimé avec succès.' });
        });
    });
});


app.post('/update-progress', (req, res) => {
    const { name, currentPage } = req.body;

    if (!name || !currentPage) {
        return res.status(400).send('Nom et page actuelle requis');
    }

    const filePath = path.join(__dirname, 'user.json');

    // Charger le fichier JSON
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) return res.status(500).send('Erreur lecture fichier JSON');

        const users = JSON.parse(data);

        // Trouver et mettre à jour le joueur
        const user = users.find(p => p.name === name);
        if (!user) return res.status(404).send('Joueur non trouvé');

        user.currentPage = currentPage;

        // Sauvegarder le fichier mis à jour
        fs.writeFile(filePath, JSON.stringify(users, null, 2), (err) => {
            if (err) return res.status(500).send('Erreur écriture fichier JSON');
            res.send('Progression mise à jour');
        });
    });
});


app.post('/login', (req, res) => {
    const { username, password } = req.body

    const filePath = path.join(__dirname, 'Data', 'users.json')

    fs.readFile(filePath, 'utf8', (err, data) => {
        if(err) {
            console.error("Erreur de lecture du fichier :", err)
            return res.status(500).send('Erreur interne du serveur')
        }

        const users = JSON.parse(data || '[]')
        const user = users.find(u => u.name === username && u.password === password)

        if(user) {
            res.send('Connexion réussie')
        } else {
            res.status(400).send(`Erreur : nom d'utilisateur ou mot de passe incorrect`)
        }
    })
})


app.listen(PORT, () => {
    console.log(`Serveur en cours d'exécution sur http://localhost:${PORT}`);
});
