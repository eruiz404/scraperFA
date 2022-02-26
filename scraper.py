import sys
import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, titulo):
        self.url = "https://www.filmaffinity.com/es/search.php"
        self.titulo = titulo

    def search(self):
        keys, values = [], []
        # buscamos en FilmAffinity
        form_data = { 'stext': self.titulo }
        response = requests.post(self.url, data=form_data)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # NOTA DE LA PELÍCULA
        ratingValue = soup.find('div', attrs={"itemprop":"ratingValue"})
        self.fa_rating = ratingValue['content']

        # DATOS GENERALES DE LA PELÍCULA
        # buscamos e iteramos en los elementos DL con la clase css "movie-info"
        for dlitem in soup.findAll('dl', attrs={"class":"movie-info"}):
            if len(dlitem["class"]) == 1:
                infomovie = dlitem

        # iteramos en los resultados de los elementos DD dentro de DT
        for dt in infomovie.findAll('dt'):
            keys.append(dt.text.strip())
        for dd in infomovie.findAll('dd'):
            values.append(dd.text.strip())

        return dict(zip(keys, values))

    def mostrar(self):
        contador = 1
        # llamamos a la función "search" de la propia clase
        resultados = self.search()

        # recorremos los resultados y los pintamos en pantalla
        for key in resultados:
            # Si ya vamos por la segunda línea, se muestra la nota (después del título, que será la primera)
            if contador == 2:
              print("Nota FA -> ", self.fa_rating)

            # mostramos por pantalla los datos
            print(key, '-> ', resultados[key])

            # incrementamos el contador
            contador += 1

def main(fa_titulo):
    # instanciamos el objeto scraper del tipo Crawler
    scraper = Crawler(fa_titulo)
    scraper.mostrar()
            
        
if __name__ == "__main__":
    fa_titulo = sys.argv[1]
    main(fa_titulo)

        