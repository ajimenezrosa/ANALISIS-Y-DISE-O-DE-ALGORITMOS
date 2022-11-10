import random
import matplotlib.pyplot as plt

mensaje_inicio = """
SIMULACION DE MONTECARLO - VENDEDOR DE PERIODICOS

Un distribuidor local de periodicos compra mañana una cantidad
fija de periodicos Q a 700$/unidad, para su posterior venta a 
1400$/unidad.
Los periodicos que no son vendidos el mismo dia, se venden para
su reciclaje a un valor de salvamento de 50$/unidad.

De acuerdo con las anotaciones historicas del vendedor de
periodicos, la demanda diaria de periodicos esta dada
por la siguiente tabla de probabilidades:

    Demanda     P(x)
    10          0.08
    25          0.1
    40          0.15
    55          0.24
    70          0.21
    85          0.15 
    100         0.07
"""

COMPRA_UNIDAD = 700
VENTA_UNIDAD = 1400
SALVAMENTO_UNIDAD = 50

"Distribucion de la demanda"
distribucion_demanda = {
        10: 0.08,
        25: 0.1,
        40: 0.15,
        55: 0.24,
        70: 0.21,
        85: 0.15,
        100: 0.07
}
demanda_unidad = list(distribucion_demanda.keys())
probabilidad_demanda = list(distribucion_demanda.values())

"Distribucion de la probabilidad"
distribucion_probabilidad = dict()
limite_inferior, limite_superior = float(), float()

for i in range(len(demanda_unidad)):
    distribucion_probabilidad[demanda_unidad[i]] = {"LI": 0, "LS": 0}    
    limite_superior, limite_inferior = 0.0, 0.0

    if i > 0:
        limite_inferior = distribucion_probabilidad[demanda_unidad[i-1]]["LS"]
        limite_inferior = round(limite_inferior, 3)

    limite_superior = limite_inferior + distribucion_demanda[demanda_unidad[i]]
    limite_superior = round(limite_superior, 3)

    distribucion_probabilidad[demanda_unidad[i]]["LI"] = limite_inferior
    distribucion_probabilidad[demanda_unidad[i]]["LS"] = limite_superior

"Calcular Utilidad promedio en un año"
def utilidad_promedio(cantidad_compra: int) -> float:
    utilidades = list()

    for _ in range(364):
        random_number = random.random()
        px_index = 0

        for i in range(len(demanda_unidad)):
            limite_inferior = distribucion_probabilidad[demanda_unidad[i]]["LI"]
            limite_superior = distribucion_probabilidad[demanda_unidad[i]]["LS"]

            if limite_inferior <= random_number <= limite_superior:
                px_index = i

        demanda = demanda_unidad[px_index]

        periodicos_vendidos = min(demanda, cantidad_compra)
        periodicos_no_vendidos = cantidad_compra - periodicos_vendidos

        costo_total = cantidad_compra * COMPRA_UNIDAD
        ingreso_ventas_regulares = periodicos_vendidos * VENTA_UNIDAD
        ingreso_salvamento = periodicos_no_vendidos * SALVAMENTO_UNIDAD

        utilidad = ingreso_salvamento + ingreso_ventas_regulares - costo_total
        utilidades.append(utilidad)

    promedio = round(sum(utilidades)/len(utilidades), 3)
    return promedio

if __name__ == "__main__":
    print(mensaje_inicio)
    qs = [15,25,35,45,55,105]
    promedios = list()

    for i in qs:
        r1 = utilidad_promedio(i)
        r2 = utilidad_promedio(i)
        r3 = utilidad_promedio(i)
        r4 = utilidad_promedio(i)

        promedio = round((r1+r2+r3+r4)/4, 3)

        print("Q Cantidad =", str(i))
        print(f"R1 -> {r1}\nR2 -> {r2}\nR3 -> {r3}\nR4 -> {r4}\nPromedio -> {promedio}\n")

        promedios.append(promedio)

    plt.plot(qs, promedios)
    plt.title("Utilidad promedio")
    plt.xlabel("Cantidad de compra")
    plt.ylabel("Promedio")
    plt.show()
