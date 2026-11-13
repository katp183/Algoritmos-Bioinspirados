import random

# El virus que queremos neutralizar (Patrón objetivo)
ANTIGENO = [1, 0, 1, 1, 0, 0, 1, 0]

def calcular_afinidad(anticuerpo):
    # Suma 1 por cada bit que coincida con el antígeno
    return sum(1 for i in range(len(ANTIGENO)) if anticuerpo[i] == ANTIGENO[i])

def generar_anticuerpo():
    return [random.choice([0, 1]) for _ in range(len(ANTIGENO))]

def mutar(anticuerpo, afinidad):
    anticuerpo_mutado = list(anticuerpo)
    # Entre menor sea la afinidad, mayor es la probabilidad de mutar (Hipermutación)
    prob_mutacion = 1.0 - (afinidad / len(ANTIGENO)) 
    
    for i in range(len(anticuerpo_mutado)):
        if random.random() < prob_mutacion:
            anticuerpo_mutado[i] = 1 - anticuerpo_mutado[i] # Invierte el bit
    return anticuerpo_mutado

def sistema_inmune_artificial():
    tamano_poblacion = 10
    generaciones = 20
    
    # 1. Inicialización
    poblacion = [generar_anticuerpo() for _ in range(tamano_poblacion)]
    
    for gen in range(generaciones):
        # 2. Evaluar Afinidad
        afinidades = [(anticuerpo, calcular_afinidad(anticuerpo)) for anticuerpo in poblacion]
        afinidades.sort(key=lambda x: x[1], reverse=True) # Ordenar de mejor a peor
        
        mejor_anticuerpo = afinidades[0][0]
        mejor_afinidad = afinidades[0][1]
        
        if mejor_afinidad == len(ANTIGENO):
            print(f"¡Virus neutralizado en la generación {gen}!")
            print(f"Anticuerpo perfecto: {mejor_anticuerpo}")
            return

        nueva_poblacion = []
        
        # 3. Selección y Clonación (Seleccionamos los 5 mejores)
        mejores_anticuerpos = afinidades[:5]
        for anticuerpo, afinidad in mejores_anticuerpos:
            num_clones = afinidad  # Clona más a los mejores
            for _ in range(num_clones):
                # 4. Hipermutación Somática
                clon_mutado = mutar(anticuerpo, afinidad)
                nueva_poblacion.append(clon_mutado)
        
        # 5. Reemplazo y diversidad
        # Llenamos el resto de la población con anticuerpos nuevos al azar
        while len(nueva_poblacion) < tamano_poblacion:
            nueva_poblacion.append(generar_anticuerpo())
            
        poblacion = nueva_poblacion[:tamano_poblacion] # Mantener el tamaño de población

    print("No se encontró el anticuerpo perfecto.")

sistema_inmune_artificial()