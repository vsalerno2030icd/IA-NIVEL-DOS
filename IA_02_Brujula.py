from random import random


valor_piezas={
    "p":1,
    "c":3,
    "a":3,
    "t":5,
    "d":9,
    "r":100,
}
def casilla_atacada_porblancas_(tablero, f_obj,c_obj):
    for f in range(8):
        for c in range(8):
            pieza=tablero[f][c]
            if es_pieza_blanca(pieza):
                movs=obtener_movimientos_pieza(tablero,f,c,turno_ia=False)
                if any(f_des== f_obj and c_des==c_obj for_,_,f_des,c_des in movs):
                    return True
    return False
def ia_nivel_2(tablero):
    for fila in range(8):
        for columna in range(8):
            casilla=tablero[fila][columna]
            if es_pieza_negra(casilla):
                movs=obtener_movimientos_pieza(tablero,fila,columna,turno_ia=True)
                jugadas_disponibles.extend(movs)
    if not jugadas_disponibles:
        return None
    mejor_jugada=None
    mejor_puntaje=float("-int")
    for jugada in jugadas_disponibles:
        f_ori,cori,f_des,c_des=jugada
        objetivo=tablero[f_des][c_des]
        puntajes=0.0
        if objetivo != "."and es_pieza_blanca(ojetivo):
            puntaje+=valor_piezas.get(objetivo.lower(),1)*10
        simulado=copiar_tablero(tablero)
        ejecutar_movimiento(simulado, jugada)
        pieza_final=simulado[f_des][c_des]
        if casilla_atacada_por_blancas(simulado, f_des,c_des):
            puntaje -=valor_piezas.get(pieza_final.lower(),1)*6
        puntaje+= random.uniform(0.0,0.3)
        if puntaje >mejor_puntaje:
            mejor_puntaje=puntaje
            mejor_jugada=jugada
    return mejor_jugada                