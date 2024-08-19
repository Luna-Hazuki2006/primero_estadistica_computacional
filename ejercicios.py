import json
import matplotlib.pyplot as plt
import math
import numpy as np
from pprint import pprint

def primero(): 
    todo = []
    with open('primer.json', 'r+') as f: 
        try: 
            todo = json.load(f)
        except: 
            todo = f.readlines()
            todo = list(todo)
        if len(todo) == 0: 
            try: 
                r = str(input('Por favor, escribe la lista de los número separados por espacios: \n'))
                r = r.split(' ')
                r = [{'clase': list(map(lambda x: int(x), r))}]
            except: 
                print('¡Oh no! Ingresaste un dato que no era un número, ¡No te equivoques!')
                return
            json.dump(r, f, indent=4)
    todo = todo[0]['clase']
    print('++++++++++++++++++++++++++++++++++++++++++++')
    if len(todo) % 2 == 0: 
        primero = todo[len(todo) // 2 - 1]
        segundo = todo[len(todo) // 2]
        print(f'Mediana: {(primero + segundo) / 2}')
    else: 
        print(f'Mediana: {todo[len(todo) // 2]}')
    print(f'Media aritmética: {sum(todo) / len(todo)}')
    lista = {}
    for esto in todo: 
        try: lista[esto] += 1
        except: lista[esto] = 1
    lista = lista.items()
    lista = [(v, k) for k, v in lista]
    print(f'Moda: {max(lista)[1]}')
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print('**********************************************')
    print(f'Clases: {todo}')
    print('**********************************************')

def segundo(): 
    todo = []
    with open('segundo.json', 'r+') as f: 
        try: 
            todo = json.load(f)
        except: 
            todo = f.readlines()
            todo = list(todo)
        if len(todo) == 0: 
            try: 
                r = str(input('Por favor, escribe la lista de los intervalos separados por espacios: \n'))
                r = r.split(' ')
                lista = [{'clase': list(map(lambda x: {'minimo': int(x.split('-')[0]), 'maximo': int(x.split('-')[1])}, r))}]
            except: 
                print('¡Oh no! Ingresaste un dato que no era un número, ¡No te equivoques!')
                return
            r = str(input('Por favor, escribe la lista de los fi separados por espacios: \n'))
            r = r.split(' ')
            lista[0]['fi'] = list(map(lambda x: int(x), r))
            parte = []
            for esto in lista[0]['fi']: 
                if len(parte) >= 1: parte.append(esto + parte[-1])
                else: parte.append(esto)
            lista[0]['fa'] = parte
            lista[0]['xi'] = list(map(lambda x: (x['minimo'] + x['maximo']) / 2, lista[0]['clase']))
            lista[0]['fi.xi'] = [(xi * fi) for xi, fi in zip(lista[0]['fi'], lista[0]['xi'])]
            lista[0]['fsr'] = list(map(lambda x: x / lista[0]['fa'][-1], lista[0]['fi']))
            lista[0]['far'] = list(map(lambda x: x / lista[0]['fa'][-1], lista[0]['fa']))
            lista[0]['fsr%'] = list(map(lambda x: x * 100, lista[0]['fsr']))
            lista[0]['far%'] = list(map(lambda x: x * 100, lista[0]['far']))
            lista[0]['fi.xi^2'] = [(xi * fixi) for xi, fixi in zip(lista[0]['fi.xi'], lista[0]['xi'])]
            json.dump(lista, f, indent=4)
    mostrar_tabla(todo[0])
    total = todo[0]['fa'][-1]
    a = todo[0]['clase'][0]['maximo'] - todo[0]['clase'][0]['minimo'] + 1
    media = sum(todo[0]['fi.xi']) / total
    print(f'Media aritmética: {media}')
    calculo = total / 2
    fa = 0
    for esto in todo[0]['fa']: 
        if esto >= calculo: 
            fa = esto
            break
    indice = todo[0]['fa'].index(fa)
    li = todo[0]['clase'][indice]['minimo']
    fi_menos = todo[0]['fa'][indice - 1]
    fi = todo[0]['fi'][indice]
    mediana = li + ((calculo - fi_menos) / fi) * a
    print(f'Mediana: {mediana}')
    lugares_modales = buscar_modales(todo[0]['fi'])
    modales = []
    for esto in lugares_modales: 
        li = todo[0]['clase'][esto]['minimo']
        fi = todo[0]['fi'][esto]
        try: fi_menos = todo[0]['fi'][esto - 1]
        except: fi_menos = 0
        try: fi_mas = todo[0]['fi'][esto + 1]
        except: fi_mas = 0
        d1 = fi - fi_menos
        d2 = fi - fi_mas
        modal = li + (d1 / (d1 + d2)) * a
        modales.append(modal)
    print(f'Modales: {modales}')
    if total % 2 == 0: p33 = (33 / 100) * total
    else: p33 = (33 / 100) * (total + 1)
    print(f'Percentil 33: {p33}')
    if total % 2 == 0: p65 = (65 / 100) * total
    else: p65 = (65 / 100) * (total + 1)
    print(f'Percentil 65: {p65}')
    if total % 2 == 0: d2 = (20 / 100) * total
    else: d2 = (20 / 100) * (total + 1)
    print(f'Decil 2: {d2}')
    if total % 2 == 0: d9 = (90 / 100) * total
    else: d9 = (90 / 100) * (total + 1)
    print(f'Decil 9: {d9}')
    if total % 2 == 0: q3 = ((25 * 3) / 100) * total
    else: q3 = ((25 * 3) / 100) * (total + 1)
    print(f'Cuartil 3: {q3}')
    print('Para ver el siguiente gráfico cierre el actual')
    x = []
    for i in range(0, len(todo[0]['clase'])): 
        if i == 0: 
            x.append(todo[0]['clase'][i]['minimo'])
        else: 
            x.append(todo[0]['clase'][i]['maximo'])
    y = todo[0]['fi']
    plt.hist(x, weights=y, bins=len(x), color='brown', edgecolor='black')
    counts, bin_edges = np.histogram(x, bins=len(x), weights=y)
    bin_midpoints = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.plot(bin_midpoints, counts, marker='o')
    plt.xlabel('Datos de los intervalos')
    plt.ylabel('Veces encontradas')
    plt.title('Histograma con polígono de frecuencia de ejercicio 2')
    plt.show()
    labels = list(map(lambda x: f"{x['minimo']}-{x['maximo']}", todo[0]['clase']))
    plt.pie(y, labels=labels, autopct='%1.1f%%')
    plt.title('Pastel de ejercicio 2')
    plt.show()
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print('**********************************************')
    print('Clases: ')
    pprint(todo[0]["clase"])
    print('Frecuencias: ')
    pprint(todo[0]["fi"])
    print('**********************************************')

def buscar_modales(fi : list): 
    lista = []
    maximo = max(fi)
    for i in range(len(fi)): 
        if fi[i] == maximo: 
            lista.append(i)
    return lista

def tercero(): 
    todo = []
    with open('tercero.json', 'r+') as f: 
        try: 
            todo = json.load(f)
        except: 
            todo = f.readlines()
            todo = list(todo)
        if len(todo) == 0: 
            try: 
                r = str(input('Por favor, escribe la lista de los intervalos separados por espacios: \n'))
                r = r.split(' ')
                r = list(map(lambda x: int(x), r))
            except: 
                print('¡Oh no! Ingresaste un dato que no era un número, ¡No te equivoques!')
                return
            minimo = min(r)
            maximo = max(r)
            print(maximo)
            rango = maximo - minimo 
            print(rango)
            k = 1 + 3.3 * math.log(rango)
            print(k)
            amplitud = rango / k
            if amplitud > int(amplitud): 
                amplitud += 1
                amplitud = int(amplitud)
            print(amplitud)
            lista = {}
            for esto in r: 
                try: lista[esto] += 1
                except: lista[esto] = 1
            real = []
            para = 0
            while True: 
                if minimo > maximo: break
                para = minimo + amplitud - 1
                if para > maximo: para = maximo
                clase = {
                    'minimo': minimo, 
                    'maximo': para
                }
                minimo = para + 1
                real.append(clase)
            oficial = [{'clase': real}]
            oficial[0]['fi'] = []
            for esto in real: 
                numero = 0
                for i in range(esto['minimo'], esto['maximo'] + 1): 
                    try: numero += lista[i]
                    except: continue
                oficial[0]['fi'].append(numero)
            parte = []
            for esto in oficial[0]['fi']: 
                if len(parte) >= 1: parte.append(esto + parte[-1])
                else: parte.append(esto)
            oficial[0]['fa'] = parte
            oficial[0]['xi'] = list(map(lambda x: (x['minimo'] + x['maximo']) / 2, oficial[0]['clase']))
            oficial[0]['fi.xi'] = [(xi * fi) for xi, fi in zip(oficial[0]['fi'], oficial[0]['xi'])]
            oficial[0]['fsr'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fi']))
            oficial[0]['far'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fa']))
            oficial[0]['fsr%'] = list(map(lambda x: x * 100, oficial[0]['fsr']))
            oficial[0]['far%'] = list(map(lambda x: x * 100, oficial[0]['far']))
            oficial[0]['fi.xi^2'] = [(xi * fixi) for xi, fixi in zip(oficial[0]['fi.xi'], oficial[0]['xi'])]
            json.dump(oficial, f, indent=4)
    mostrar_tabla(todo[0])
    total = todo[0]['fa'][-1]
    a = todo[0]['clase'][0]['maximo'] - todo[0]['clase'][0]['minimo'] + 1
    media = sum(todo[0]['fi.xi']) / total
    print(f'Media aritmética: {media}')
    calculo = total / 2
    fa = 0
    for esto in todo[0]['fa']: 
        if esto >= calculo: 
            fa = esto
            break
    indice = todo[0]['fa'].index(fa)
    li = todo[0]['clase'][indice]['minimo']
    fi_menos = todo[0]['fa'][indice - 1]
    fi = todo[0]['fi'][indice]
    mediana = li + ((calculo - fi_menos) / fi) * a
    print(f'Mediana: {mediana}')
    lugares_modales = buscar_modales(todo[0]['fi'])
    modales = []
    for esto in lugares_modales: 
        li = todo[0]['clase'][esto]['minimo']
        fi = todo[0]['fi'][esto]
        try: fi_menos = todo[0]['fi'][esto - 1]
        except: fi_menos = 0
        try: fi_mas = todo[0]['fi'][esto + 1]
        except: fi_mas = 0
        d1 = fi - fi_menos
        d2 = fi - fi_mas
        modal = li + (d1 / (d1 + d2)) * a
        modales.append(modal)
    print(f'Modales: {modales}')
    varianza = (sum(todo[0]['fi.xi^2']) / total) - (media**2)
    print(f'Varianza: {varianza}')
    desviacion = math.sqrt(varianza)
    print(f'Desviación estándar: {desviacion}')
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print('**********************************************')
    print('Clases: ')
    pprint(todo[0]["clase"])
    print('Frecuencias: ')
    pprint(todo[0]["fi"])
    print('**********************************************')

def mostrar_tabla(todo : dict): 
    total = len(todo['clase'])
    llaves = todo.keys()
    texto = '|'
    for esto in llaves: texto += f' {esto} |'
    print(len(texto) * '-')
    print(texto)
    for i in range(total): 
        texto = '|'
        for esto in llaves: 
            if esto == 'clase': 
                minimo = todo[esto][i]['minimo']
                maximo = todo[esto][i]['maximo']
                texto += f' {minimo}-{maximo} |'
            else: texto += f' {todo[esto][i]} |'
        print(len(texto) * '-')
        print(texto)
    print(len(texto) * '-')

def main(): 
    try: 
        while True: 
            r = str(input('''¿Cuál ejercicios deseas hacer?
(Si deseas reingresar la información de un ejercicio específico 
entre al archivo .json correspondiente y haga lo siguiente: 
haga ctrl + a, presione borrar, haga ctrl + s y vuelva a la aplicación)
(a) El primer ejercicio 
(b) El segundo ejercicio 
(c) El tercer ejercicio
(d) Salir de la aplicación (Si esto no funciona usa ctrl + c)
'''))
            if r == 'a' or r == 'A' or r == '(a)' or r == '(A)': 
                primero()
            elif r == 'b' or r == 'B' or r == '(b)' or r == '(B)': 
                segundo()
            elif r == 'c' or r == 'C' or r == '(c)' or r == '(C)': 
                tercero()
            elif r == 'd' or r == 'D' or r == '(d)' or r == '(D)': 
                print('Chao (≧∇≦)ﾉ')
                break
    except Exception: 
        print('''¡Oh no! Parece que hubo un error ¡Pero no te preocupes! 
Probablemente es porque no tienes todas las librerías :D 
Lo único que tienes que hacer es escribir los siguientes comandos: 
python -m venv venv
pip install -r requirements.txt
(Al llamar esos comandos... Puede que tarde unos minutos en instalarse todo ヾ(•ω•`)o)
Si el problema persiste, borra la carpeta venv (CON TODOS SUS CONTENIDOS) y usa los DOS comandos
Si el problema AÚN persiste, borra la carpeta venv y SOLO usa el SEGUNDO comando''')
    except: 
        print('Chao (ﾉ*ФωФ)ﾉ')

if __name__ == '__main__': 
    main()