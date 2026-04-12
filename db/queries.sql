

-- 1) 10 derniers événements
SELECT id, commande_texte, intention_detectee, resultat
FROM events
ORDER BY id DESC
LIMIT 10;
