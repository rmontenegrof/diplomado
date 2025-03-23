# Primero clonamos el repositorio git en la consola git
# $ git clone https://github.com/AllenDowney/ThinkStats2.git

import numpy as np  # Asegúrate de importar numpy

from os.path import basename, exists

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        
        local, _ = urlretrieve(url, filename)
        print("Downloaded " + local)

download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/thinkstats2.py")
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/thinkplot.py")
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/nsfg.py")

download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dct")
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dat.gz")

# PARA EL EJERCICIO DE LA CLASE 1
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dct")
download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dat.gz")

import nsfg
import numpy as np
import pandas as pd
import thinkplot
import thinkstats2
from numpy import random
df = pd.read_csv("winequality-red.csv")
df.head()


# Parte 1 (2 pts):
df.isnull().sum() # Valida si hay datos faltantes o null en el dataframe
df.dtypes # Corroborar tipos de datos

# Parte 2 (2 pts):
df['good'] = df['quality'].apply(lambda x: 1 if x >= 7 else 0) # creación de columna good
df.head() # valido creación de columna

# Parte 3 (3 pts):
calificacion_hist = thinkstats2.Hist(df["quality"])
calificacion_hist[10] # Cuantos vinos tienen una calificación de 10
calificacion_hist[3] # Cuantos vinos tienen una calificación de 3

good_hist = thinkstats2.Hist(df["good"])
good_hist[1] # Cuantos vinos son considerados de buena calidad ( >= 7 )

# Parte 4 (7 pts):
thinkplot.Hist(calificacion_hist) # histograma de la variable “quality”

# Evaluando outliers
Q1 = np.percentile(calificacion_hist, 25)
Q3 = np.percentile(calificacion_hist, 75)
RIQ = Q3 - Q1

# Límites para outliers
limite_inferior = Q1 - 1.5 * RIQ
limite_superior = Q3 + 1.5 * RIQ
limite_inferior # Da 0,5
limite_superior # Da 10,5

# El valor mas frecuente en el histograma (la moda) es la calificación 5 con 681 ocurrencias
# La mayor parte de los valores se distribuyen entre las calificaciones 5 y 6
# las calificaciones 3 y 8 en este caso podrían muy bajos, pero no outliers
# ya que no sonmenores 183 0,5 ni mayores que 10,5
# El gráfico presenta una asimetría hacia la derecha

thinkplot.Hist(good_hist) # histograma de la variable “good"
# El valor cero representa la moda con 1382 ocurrencias
# Es practicamente una distribución de una variable binaria, 
# ya que solo toma valores 0 y 1

# Parte 5 (10 pts):
excluye_good = df.drop(columns=['good']) #excluimos la columna 

promedio_valores = excluye_good.mean()
de_valores = excluye_good.std()
promedio_valores
de_valores

#Las variables total sulfur dioxide y free sulfur dioxide presentan una mayor desviación estándar
# porque sus valores se concentran en un rango de valores mas alto que 
# las demás variables que se coincentran en un rango de valores bastante mas pequeños


# Parte 6 (10 pts):
residual_sugar_hist = thinkstats2.Hist(df["residual sugar"])
thinkplot.Hist(residual_sugar_hist) # histograma de la variable residual_sugar

# Contar las frecuencias de cada valor en 'residual sugar'
valor_frecuencia = df['residual sugar'].value_counts()
# Mostrar los 5 valores más grandes con sus frecuencias
top_5 = valor_frecuencia.sort_index(ascending=False).head(15)
print(top_5)

# Mostrar los 5 valores más pequeños con sus frecuencias
bottom_5 = valor_frecuencia.sort_index(ascending=True).head(5)
print(bottom_5)

Q1 = np.percentile(residual_sugar_hist, 25)
Q3 = np.percentile(residual_sugar_hist, 75)
RIQ = Q3 - Q1

# Límites para outliers
limite_inferior = Q1 - 1.5 * RIQ
limite_superior = Q3 + 1.5 * RIQ
limite_inferior # Da -3,1499999999999995
limite_superior # Da 12,25

# Los 5 números más altos son considerados outliers, ya que superan el límite superior de 12,25
# Estos son: 15,5 - 15,4 - 13,9 - 13,8 - 13,4. Incluso el sexto número 12,9 también está oputliers
# Con respescto a los 5 numeros mas bajos, estos no son considerados outliers, ya que están sobre
# el límite inferior de -3,1499999999999995

# Parte 7 (10 pts):
df_buenos = df[df["good"] == 1] # Se separan los datos en vinos buenos
df_buenos 

df_malos = df[df["good"] == 0] # Se separan los datos en vinos malos
df_malos

alcohol_hist_buenos = thinkstats2.Hist(df_buenos["alcohol"])
alcohol_hist_malos = thinkstats2.Hist(df_malos["alcohol"])
width = 0.45
thinkplot.PrePlot(2) #dos histogramas
thinkplot.Hist(alcohol_hist_buenos, align='right', width=width) 
thinkplot.Hist(alcohol_hist_malos, align='left', width=width, color='red') 
thinkplot.Show(xlabel='% alcohol', ylabel='frequency')


alcohol_hist_buenos = thinkstats2.Pmf(df_buenos["alcohol"])
alcohol_hist_malos = thinkstats2.Pmf(df_malos["alcohol"])
width = 0.45
thinkplot.PrePlot(2) #dos histogramas
thinkplot.Hist(alcohol_hist_buenos, align='right', width=width) 
thinkplot.Hist(alcohol_hist_malos, align='left', width=width, color='red') 
thinkplot.Show(xlabel='% alcohol', ylabel='probability')

# En el primer gráfico de histograma hay una escala mas rande porque se muestra los valores absolutos
# mientras el PMF muetsra las proporciones oprobabilidad. Entonces si bien varía la información del eje y
# y en coinseceuncia la interpretación, el comportamiento se mantiene.

# para comparar las distribuciones, claramente conviene utilizar el histograma que nos permita visualizar
# el valor total de ocurrencias y compararlas directamente

# Parte 8 (6 pts):
def CohenEffectSize(group1, group2): # Se define fórmula
    diff = group1.mean() - group2.mean()
    var1 = group1.var()
    var2 = group2.var()
    n1, n2 = len(group1), len(group2)
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / np.sqrt(pooled_var)
    return d

num1 = CohenEffectSize(df_buenos["alcohol"], df_malos["alcohol"]) # Se manda a llamar la función
num1
# El valor obtenido (1.3013961896335728) evidencia que el grado de alcohol en los vinos buenos es mayor
# que en los vinos malos

# El valor hace sentido, ya que en la comparación directa se puede observar claramente que el grado de 
# de alcohol en los vinos buenos es muy superior a los malos

# Parte 9 (10 pts):
good_hist = thinkstats2.Hist(df["good"])
p = good_hist[1] / (good_hist[1] + good_hist[0])
n = 10000 

muestra = random.binomial(n=n, p=p, size=100000)
n*p
hist_good = thinkstats2.Hist(muestra)
thinkplot.Hist(hist_good)

muestra.mean() # promedio de la muestra obtenida
n*p # Pormedio teorico de la distribución binomial

# Finalmente, hace sentido la media de la muestra ya que se asemeja bastante al promedio teorico