# wamdaScraping

wamdaScraping est un programme qui permet d'extraire les données des produits et les images associées provenant du site https://www.wamda.com/media

# Configuration :

1. Placez-vous dans le répertoire qui contiendra le projet 
  
2. Récupérer le code venant de GitHub (faire un clone) :  
```
git clone https://github.com/glgstyle/wamdaScraping.git
cd wamdaScraping
```
3. Créer un environnement virtuel : 

```python -m venv env```

4. Activer l'environnement :  

```source env/bin/activate ```

ou 

```env\scripts\activate```

5. Installer les packages :

```pip install -r requirements.txt```  
```pip freeze``` (pour vérifier que les packages se sont bien installés)

# Extraire les infos d'un article

1. Scrapper un article avec scrap_article.py :
- Dans le terminal écrire la ligne de commande python scrap_article.py suivi de l'url de l'article, exemple :  
```python scrap_article.py https://www.wamda.com/2024/02/tawaref-series-golden-rules-entering-saudi-market```
2. Appuyez sur entrée
3. Un fichier article_data.csv s'est crée dans le dossier data comportant les informations du produit (à ouvrir avec excel)

# Extraire les liens de toutes les pages du blog

1. Scrapper les pages avec python scrap_all_articles_links.py :
- Dans le terminal écrire la ligne de commande :  
``` python scrap_all_articles_links.py```
2. Appuyez sur entrée
3. Un fichier all_articles_links.csv s'est crée dans le dossier data comportant les liens de tous les articles de toutes les pages (à ouvrir avec excel)