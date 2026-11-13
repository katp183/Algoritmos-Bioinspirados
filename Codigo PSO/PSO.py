import random

# Función objetivo: f(x, y) = x^2 + y^2 (Queremos llegar a 0)
def evaluar_terreno(posicion):
    return posicion[0]**2 + posicion[1]**2

class Particula:
    def __init__(self):
        # Posición y velocidad aleatorias iniciales
        self.posicion = [random.uniform(-10, 10), random.uniform(-10, 10)]
        self.velocidad = [random.uniform(-1, 1), random.uniform(-1, 1)]
        
        # Memoria individual (pbest)
        self.mejor_posicion_personal = list(self.posicion)
        self.mejor_valor_personal = evaluar_terreno(self.posicion)

def optimizacion_enjambre():
    num_particulas = 20
    iteraciones = 50
    enjambre = [Particula() for _ in range(num_particulas)]
    
    # Memoria global (gbest)
    mejor_posicion_global = []
    mejor_valor_global = float('inf')
    
    # Encontrar el mejor valor inicial
    for particula in enjambre:
        if particula.mejor_valor_personal < mejor_valor_global:
            mejor_valor_global = particula.mejor_valor_personal
            mejor_posicion_global = list(particula.mejor_posicion_personal)

    # Parámetros del PSO
    w = 0.5  # Inercia (qué tanto mantiene su dirección original)
    c1 = 1.5 # Coeficiente cognitivo (sigue su propia memoria)
    c2 = 1.5 # Coeficiente social (sigue a la memoria del grupo)

    for i in range(iteraciones):
        for particula in enjambre:
            for dim in range(2): # Para x e y
                r1, r2 = random.random(), random.random()
                
                # 1. Actualizar velocidad
                atraccion_personal = c1 * r1 * (particula.mejor_posicion_personal[dim] - particula.posicion[dim])
                atraccion_grupal = c2 * r2 * (mejor_posicion_global[dim] - particula.posicion[dim])
                
                particula.velocidad[dim] = (w * particula.velocidad[dim]) + atraccion_personal + atraccion_grupal
                
                # 2. Actualizar posición
                particula.posicion[dim] += particula.velocidad[dim]
            
            # 3. Evaluar nueva posición
            valor_actual = evaluar_terreno(particula.posicion)
            
            # 4. Actualizar memorias
            if valor_actual < particula.mejor_valor_personal:
                particula.mejor_valor_personal = valor_actual
                particula.mejor_posicion_personal = list(particula.posicion)
                
            if valor_actual < mejor_valor_global:
                mejor_valor_global = valor_actual
                mejor_posicion_global = list(particula.posicion)

    print(f"Mejor posición encontrada: x={mejor_posicion_global[0]:.4f}, y={mejor_posicion_global[1]:.4f}")
    print(f"Valor mínimo encontrado: {mejor_valor_global:.6f}")

optimizacion_enjambre()