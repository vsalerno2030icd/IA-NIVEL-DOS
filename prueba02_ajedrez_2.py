import random



def crear_tablero():
    return [
        ["t", "c", "a", "d", "r", "a", "c", "t"],  # Fila 0: Negras (IA)
        ["p", "p", "p", "p", "p", "p", "p", "p"],  # Fila 1: Peones IA
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],  # Fila 6: Peones Blancas
        ["T", "C", "A", "D", "R", "A", "C", "T"]   # Fila 7: Blancas (Humano)
    ]

def imprimir_tablero(tablero):
    print("  0 1 2 3 4 5 6 7")
    for idx, fila in enumerate(tablero):
        print(f"{idx} " + " ".join(fila))
    print()

def es_aliada(pieza, turno_ia):
    if pieza == ".":
        return False
    return pieza.islower() if turno_ia else pieza.isupper() 

def es_enemiga(pieza, turno_ia):
    if pieza == ".":
        return False
    return pieza.isupper() if turno_ia else pieza.islower()

def obtener_movimientos_pieza(tablero, f, c, turno_ia=True):
    pieza = tablero[f][c].lower()
    movs = []
    
    # 1. PEÓN
    if pieza == "p":
        dir_f = 1 if turno_ia else -1
        fila_inicio = 1 if turno_ia else 6
        # Avance simple
        if 0 <= f + dir_f < 8 and tablero[f + dir_f][c] == ".":
            movs.append((f, c, f + dir_f, c))
            # Regla especial: Avance doble desde el inicio
            if f == fila_inicio and tablero[f + 2 * dir_f][c] == ".":
                movs.append((f, c, f + 2 * dir_f, c))
        # Capturas diagonales
        for dc in [-1, 1]:
            if 0 <= f + dir_f < 8 and 0 <= c + dc < 8:
                if es_enemiga(tablero[f + dir_f][c + dc], turno_ia):
                    movs.append((f, c, f + dir_f, c + dc))

    # 2. CABALLO
    elif pieza == "c":
        saltos = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
        for df, dc in saltos:
            nf, nc = f + df, c + dc
            if 0 <= nf < 8 and 0 <= nc < 8 and not es_aliada(tablero[nf][nc], turno_ia):
                movs.append((f, c, nf, nc))

    # 3. REY
    elif pieza == "r":
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0: continue
                nf, nc = f + df, c + dc
                if 0 <= nf < 8 and 0 <= nc < 8 and not es_aliada(tablero[nf][nc], turno_ia):
                    movs.append((f, c, nf, nc))

    # 4. TORRE, ALFIL Y DAMA (Deslizamiento)
    elif pieza in ["t", "a", "d"]:
        direcciones = []
        if pieza in ["t", "d"]: direcciones.extend([(-1,0), (1,0), (0,-1), (0,1)])
        if pieza in ["a", "d"]: direcciones.extend([(-1,-1), (-1,1), (1,-1), (1,1)])
        
        for df, dc in direcciones:
            nf, nc = f + df, c + dc
            while 0 <= nf < 8 and 0 <= nc < 8:
                if tablero[nf][nc] == ".":
                    movs.append((f, c, nf, nc))
                elif es_enemiga(tablero[nf][nc], turno_ia):
                    movs.append((f, c, nf, nc))
                    break
                else:
                    break
                nf += df
                nc += dc
    return movs

def ejecutar_movimiento(tablero, jugada):
    f_ori, c_ori, f_des, c_des = jugada
    pieza = tablero[f_ori][c_ori]
    # Regla especial: Coronación automática a Dama
    if pieza == "p" and f_des == 7: pieza = "d"
    if pieza == "P" and f_des == 0: pieza = "D"
    tablero[f_des][c_des] = pieza
    tablero[f_ori][c_ori] = "."

def ia_nivel_1(tablero):
    #Se guardaran todas las jigadas posibles en formato (f_ori,c_ori, f_des,c_des)
    jugadas_disponibles=[]
    #Escanear el tablero buscando las piezas
    for fila in range(8):
        for columna in range(8):
            casilla=tablero[fila][columna]
        #verificar si la casilla  tiene una pieza del bot(minuscula)
            if casilla.islower():
                #Pedir las reglas al codigo
                movimientos_de_esta_pieza=obtener_movimientos_pieza(tablero,fila,columna,turno_ia=True)
                jugadas_disponibles.extend(movimientos_de_esta_pieza)
    if len(jugadas_disponibles)>0:
        jugada_elegida= random.choice(jugadas_disponibles)
        return jugada_elegida
    else:
        return None


# =====================================================================
# PARTE 2: BOTS, MENÚ, SÍMBOLOS, JAQUE, JAQUE MATE Y ENTRADA SIMPLE
# =====================================================================

VALOR_PIEZAS = {
    "p": 1,
    "c": 3,
    "a": 3,
    "t": 5,
    "d": 9,
    "r": 100,
}

SIGNOS_PIEZAS = {
    "P": "♙", "T": "♖", "C": "♘", "A": "♗", "D": "♕", "R": "♔",
    "p": "♟", "t": "♜", "c": "♞", "a": "♝", "d": "♛", "r": "♚",
    ".": "·",
}

NOMBRES_CANONICOS = {
    "p": "peon",
    "t": "torre",
    "c": "caballo",
    "a": "alfil",
    "d": "dama",
    "r": "rey",
}

NOMBRES_PIEZAS = {
    "p": "peon", "peon": "p", "peón": "p",
    "t": "torre", "torre": "t",
    "c": "caballo", "caballo": "c",
    "a": "alfil", "alfil": "a",
    "d": "dama", "dama": "d", "reina": "d",
    "r": "rey", "rey": "r",
}

CONECTORES_ENTRADA = {"al", "en", "hacia"}
COLUMNAS_LETRAS = "abcdefgh"


def es_pieza_blanca(pieza):
    return pieza in {"P", "T", "C", "A", "D", "R"}


def es_pieza_negra(pieza):
    return pieza in {"p", "t", "c", "a", "d", "r"}


def nombre_pieza_por_codigo(codigo):
    return NOMBRES_CANONICOS.get(codigo, codigo)


def copiar_tablero(tablero):
    return [fila[:] for fila in tablero]


def coord_a_notacion(fila, col):
    """Convierte (fila 0..7, col 0..7) a notación de ajedrez (ej. 'e2')."""
    return f"{COLUMNAS_LETRAS[col]}{8 - fila}"


def notacion_a_coord(casilla_str):
    """Convierte 'f4' en (fila 0..7, col 0..7) o devuelve None si no es válida."""
    casilla_str = casilla_str.strip().lower()
    if len(casilla_str) != 2:
        return None
    col_char, fila_char = casilla_str[0], casilla_str[1]
    if col_char not in COLUMNAS_LETRAS or fila_char not in "12345678":
        return None
    col = COLUMNAS_LETRAS.index(col_char)
    fila = 8 - int(fila_char)
    return (fila, col)


def signo_de_pieza(simbolo):
    return SIGNOS_PIEZAS.get(simbolo, simbolo)


def nombre_legible_pieza(simbolo):
    if not simbolo or simbolo == ".":
        return "pieza"
    return nombre_pieza_por_codigo(simbolo.lower())


def imprimir_tablero_ajedrez(tablero):
    print("    a b c d e f g h")
    print("  +-----------------+")
    for idx, fila in enumerate(tablero):
        fila_num = 8 - idx
        simbolos = " ".join(signo_de_pieza(casilla) for casilla in fila)
        print(f"{fila_num} | {simbolos} | {fila_num}")
    print("  +-----------------+")
    print("    a b c d e f g h")
    print("  Blancas: ♔ ♕ ♖ ♗ ♘ ♙  |  Negras: ♚ ♛ ♜ ♝ ♞ ♟\n")


def buscar_rey(tablero, bando_objetivo):
    """Devuelve (fila, col) del rey de 'blancas' o 'negras', o None si no está."""
    objetivo = "R" if bando_objetivo == "blancas" else "r"
    for f in range(8):
        for c in range(8):
            if tablero[f][c] == objetivo:
                return (f, c)
    return None


def piezas_amenazando_rey(tablero, bando_rey):
    """Devuelve una lista de tuplas (pieza, fila, col) que atacan al rey indicado."""
    pos_rey = buscar_rey(tablero, bando_rey)
    if pos_rey is None:
        return []

    f_rey, c_rey = pos_rey
    atacantes_son_negras = bando_rey == "blancas"
    amenazas = []

    for f in range(8):
        for c in range(8):
            pieza = tablero[f][c]
            if atacantes_son_negras and es_pieza_negra(pieza):
                movs = obtener_movimientos_pieza(tablero, f, c, turno_ia=True)
            elif not atacantes_son_negras and es_pieza_blanca(pieza):
                movs = obtener_movimientos_pieza(tablero, f, c, turno_ia=False)
            else:
                continue

            if any(f_des == f_rey and c_des == c_rey for _, _, f_des, c_des in movs):
                amenazas.append((pieza, f, c))

    return amenazas


def casilla_atacada_por_blancas(tablero, f_obj, c_obj):
    """Devuelve True si alguna pieza blanca amenaza la casilla (f_obj, c_obj)."""
    for f in range(8):
        for c in range(8):
            pieza = tablero[f][c]
            if es_pieza_blanca(pieza):
                movs = obtener_movimientos_pieza(tablero, f, c, turno_ia=False)
                if any(f_des == f_obj and c_des == c_obj for _, _, f_des, c_des in movs):
                    return True
    return False


def ia_nivel_2(tablero):
    """Bot Brújula (Nivel 2): prioriza capturas valiosas, jaques y evitar piezas colgadas."""
    jugadas_disponibles = []
    for fila in range(8):
        for columna in range(8):
            casilla = tablero[fila][columna]
            if es_pieza_negra(casilla):
                movs = obtener_movimientos_pieza(tablero, fila, columna, turno_ia=True)
                jugadas_disponibles.extend(movs)

    if not jugadas_disponibles:
        return None

    mejor_jugada = None
    mejor_puntaje = float("-inf")

    for jugada in jugadas_disponibles:
        f_ori, c_ori, f_des, c_des = jugada
        objetivo = tablero[f_des][c_des]
        puntaje = 0.0

        if objetivo != "." and es_pieza_blanca(objetivo):
            puntaje += VALOR_PIEZAS.get(objetivo.lower(), 1) * 10

        simulado = copiar_tablero(tablero)
        ejecutar_movimiento(simulado, jugada)
        pieza_final = simulado[f_des][c_des]

        if piezas_amenazando_rey(simulado, "blancas"):
            puntaje += 3.5

        if casilla_atacada_por_blancas(simulado, f_des, c_des):
            puntaje -= VALOR_PIEZAS.get(pieza_final.lower(), 1) * 6

        puntaje += random.uniform(0.0, 0.3)

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_jugada = jugada

    return mejor_jugada


BOTS_DISPONIBLES = {
    "1": {
        "nombre": "Chispas",
        "nivel": "Nivel 1 (Básico / Aleatorio)",
        "descripcion": "Elige al azar entre los movimientos legales disponibles.",
        "funcion": ia_nivel_1,
    },
    "2": {
        "nombre": "Brújula",
        "nivel": "Nivel 2 (Táctico / Posicional)",
        "descripcion": "Busca capturas valiosas, da jaque y cuida sus piezas.",
        "funcion": ia_nivel_2,
    },
}


def tiene_movimiento_para_salir_de_jaque(tablero, bando_rey):
    """Devuelve True si el bando indicado tiene al menos una jugada que deje a su rey a salvo."""
    es_negra = bando_rey == "negras"
    for f in range(8):
        for c in range(8):
            pieza = tablero[f][c]
            if es_negra and es_pieza_negra(pieza):
                movs = obtener_movimientos_pieza(tablero, f, c, turno_ia=True)
            elif not es_negra and es_pieza_blanca(pieza):
                movs = obtener_movimientos_pieza(tablero, f, c, turno_ia=False)
            else:
                continue

            for jugada in movs:
                simulado = copiar_tablero(tablero)
                ejecutar_movimiento(simulado, jugada)
                if not piezas_amenazando_rey(simulado, bando_rey):
                    return True
    return False


def evaluar_estado_turno(tablero, turno_ia_siguiente, modo, bot):
    """
    Revisa si el bando que va a mover está en jaque, jaque mate o ahogado.
    Devuelve True si la partida debe terminar.
    """
    bando_afectado = "negras" if turno_ia_siguiente else "blancas"
    pos_rey = buscar_rey(tablero, bando_afectado)
    if pos_rey is None:
        return True

    amenazas = piezas_amenazando_rey(tablero, bando_afectado)
    en_jaque = len(amenazas) > 0
    tiene_escape = tiene_movimiento_para_salir_de_jaque(tablero, bando_afectado)

    nombre_afectado = (
        bot["nombre"] if (turno_ia_siguiente and modo == "bot")
        else ("Negras" if turno_ia_siguiente else "Blancas")
    )
    nombre_ganador = (
        "Tú" if (turno_ia_siguiente and modo == "bot")
        else ("Blancas" if turno_ia_siguiente else "Negras")
    )

    if en_jaque:
        casilla_rey = coord_a_notacion(*pos_rey)
        etiqueta_rey = "Rey Blanco (♔)" if bando_afectado == "blancas" else "Rey Negro (♚)"
        detalles = ", ".join(
            f"{signo_de_pieza(p)} {nombre_legible_pieza(p)} en {coord_a_notacion(f, c)}"
            for p, f, c in amenazas
        )
        print(f"¡JAQUE! {etiqueta_rey} en {casilla_rey} está amenazado por: {detalles}.\n")

        if not tiene_escape:
            print(f"¡JAQUE MATE! El rey de {nombre_afectado} no tiene escape. ¡Gana {nombre_ganador}!\n")
            return True
        return False

    if not tiene_escape:
        print(f"¡AHOGADO / TABLAS! {nombre_afectado} no tiene movimientos legales y su rey no está en jaque.\n")
        return True

    return False


def aplicar_y_reportar_jugada(tablero, jugada, autor):
    """Ejecuta una jugada, informa capturas y devuelve True si se capturó un rey."""
    f_ori, c_ori, f_des, c_des = jugada
    pieza_movida = tablero[f_ori][c_ori]
    pieza_capturada = tablero[f_des][c_des]
    rey_capturado = pieza_capturada.lower() == "r"

    ejecutar_movimiento(tablero, jugada)

    origen_txt = coord_a_notacion(f_ori, c_ori)
    destino_txt = coord_a_notacion(f_des, c_des)
    nombre_movida = nombre_legible_pieza(pieza_movida)
    signo_movida = signo_de_pieza(pieza_movida)

    if pieza_capturada != ".":
        nombre_capturada = nombre_legible_pieza(pieza_capturada)
        signo_capturada = signo_de_pieza(pieza_capturada)
        print(
            f"{autor} movió {signo_movida} ({nombre_movida}) de {origen_txt} a {destino_txt} "
            f"y ¡capturó {signo_capturada} ({nombre_capturada})!\n"
        )
    else:
        print(f"{autor} movió {signo_movida} ({nombre_movida}) de {origen_txt} a {destino_txt}.\n")

    return rey_capturado


def resolver_jugada_ajedrez(tablero, turno_ia, texto):
    limpio = texto.strip().lower().replace("->", " ").replace("=>", " ")
    partes = [p for p in limpio.split() if p not in CONECTORES_ENTRADA]
    if not partes:
        return None, "Escribe una jugada, por ejemplo: 'peon f4', 'p f4' o 'caballo c3'."

    codigo_pieza = None
    if partes[0] in NOMBRES_PIEZAS:
        codigo_pieza = NOMBRES_PIEZAS[partes[0]]
        casillas_str = partes[1:]
    else:
        casillas_str = partes

    if len(casillas_str) not in (1, 2):
        return None, "Usa formato 'pieza casilla' (ej. 'peon f4') o 'origen destino' (ej. 'e2 e4')."

    coords = [notacion_a_coord(c) for c in casillas_str]
    if any(coord is None for coord in coords):
        return None, "Casilla inválida. Usa letras de 'a' a 'h' y números de '1' a '8' (ej. f4, e2)."

    # Caso 1: origen y destino -> ej. 'peon e2 e4' o 'e2 e4'
    if len(coords) == 2:
        (f_ori, c_ori), (f_des, c_des) = coords
        pieza_casilla = tablero[f_ori][c_ori]
        if not es_aliada(pieza_casilla, turno_ia):
            return None, f"No tienes una pieza tuya en {coord_a_notacion(f_ori, c_ori)}."
        if codigo_pieza and pieza_casilla.lower() != codigo_pieza:
            nombre_esperado = nombre_pieza_por_codigo(codigo_pieza)
            return None, f"En {coord_a_notacion(f_ori, c_ori)} no hay un {nombre_esperado}."
        jugada = (f_ori, c_ori, f_des, c_des)
        if jugada not in obtener_movimientos_pieza(tablero, f_ori, c_ori, turno_ia=turno_ia):
            return None, f"Ese movimiento a {coord_a_notacion(f_des, c_des)} no es legal."
        return jugada, None

    # Caso 2: solo destino (y opcionalmente tipo de pieza) -> ej. 'peon f4', 'p f4' o 'f4'
    f_des, c_des = coords[0]
    candidatas = []
    for f in range(8):
        for c in range(8):
            casilla = tablero[f][c]
            if not es_aliada(casilla, turno_ia):
                continue
            if codigo_pieza is not None and casilla.lower() != codigo_pieza:
                continue
            if (f, c, f_des, c_des) in obtener_movimientos_pieza(tablero, f, c, turno_ia=turno_ia):
                candidatas.append((f, c, f_des, c_des))

    destino_txt = coord_a_notacion(f_des, c_des)
    if len(candidatas) == 1:
        return candidatas[0], None

    if len(candidatas) == 0:
        if codigo_pieza:
            nombre_pieza = nombre_pieza_por_codigo(codigo_pieza)
            return None, f"Ningún {nombre_pieza} tuyo puede moverse legalmente a {destino_txt}."
        return None, f"Ninguna pieza tuya puede moverse legalmente a {destino_txt}."

    ejemplos = ", ".join(
        f"{nombre_pieza_por_codigo(tablero[f][c].lower())} {coord_a_notacion(f, c)} {destino_txt}"
        for f, c, _, _ in candidatas
    )
    return None, (
        f"Varias piezas pueden ir a {destino_txt}. Especifica cuál mover, por ejemplo: {ejemplos}."
    )


def pedir_jugada_humano(tablero, turno_ia):
    bando = "Negras (♚)" if turno_ia else "Blancas (♔)"
    while True:
        print(f"Turno de {bando}")
        print("Escribe 'pieza casilla' (ej. 'peon f4', 'p f4', 'caballo c3') o 'salir'")
        entrada = input("Tu jugada: ").strip()

        if entrada.lower() == "salir":
            return "salir"

        jugada, error = resolver_jugada_ajedrez(tablero, turno_ia, entrada)
        if error:
            print(f"{error}\n")
            continue
        return jugada


def seleccionar_bot():
    while True:
        print("\n========================================")
        print("           BOTS DISPONIBLES            ")
        print("========================================")
        for clave, bot in BOTS_DISPONIBLES.items():
            print(f"{clave}. {bot['nombre']} — {bot['nivel']}")
            print(f"   {bot['descripcion']}")
        print("0. Volver al menú principal")
        print("========================================")

        eleccion = input("Elige un bot: ").strip()
        if eleccion == "0":
            return None
        if eleccion in BOTS_DISPONIBLES:
            return BOTS_DISPONIBLES[eleccion]
        print("Opción no válida. Intenta de nuevo.\n")


def jugar_partida(modo, bot=None):
    tablero = crear_tablero()
    turno_ia = False  # False = Blancas (♔), True = Negras (♚)

    if modo == "pvp":
        print("\n--- Modo: Jugador contra Jugador ---")
        print("Jugador 1: Blancas (♔) | Jugador 2: Negras (♚)\n")
    else:
        etiqueta_bot = f"{bot['nombre']} ({bot['nivel']})"
        print(f"\n--- Modo: Jugador contra {etiqueta_bot} ---")
        print(f"Tú juegas con Blancas (♔). {bot['nombre']} juega con Negras (♚).\n")

    while True:
        imprimir_tablero_ajedrez(tablero)

        if turno_ia and modo == "bot":
            print(f"Turno de {bot['nombre']}...")
            jugada = bot["funcion"](tablero)
            if jugada is None:
                print(f"{bot['nombre']} no tiene movimientos disponibles. ¡Ganaste!\n")
                break
            rey_capturado = aplicar_y_reportar_jugada(tablero, jugada, bot["nombre"])
            if rey_capturado:
                imprimir_tablero_ajedrez(tablero)
                print(f"¡Fin de la partida! {bot['nombre']} capturó tu rey.\n")
                break
        else:
            jugada = pedir_jugada_humano(tablero, turno_ia)
            if jugada == "salir":
                print("\nVolviendo al menú principal...\n")
                break
            autor = "Negras" if turno_ia else "Blancas"
            if modo == "bot":
                autor = "Tú"
            rey_capturado = aplicar_y_reportar_jugada(tablero, jugada, autor)
            if rey_capturado:
                imprimir_tablero_ajedrez(tablero)
                print(f"¡Fin de la partida! {autor} capturó el rey rival.\n")
                break

        turno_ia = not turno_ia
        if evaluar_estado_turno(tablero, turno_ia, modo, bot):
            imprimir_tablero_ajedrez(tablero)
            break


def mostrar_menu():
    while True:
        print("========================================")
        print("           AJEDREZ EN PYTHON            ")
        print("========================================")
        print("1. Jugador contra Jugador")
        print("2. Jugador contra Bot")
        print("3. Salir")
        print("========================================")

        opcion = input("Elige una opción (1-3): ").strip()

        if opcion == "1":
            jugar_partida("pvp")
        elif opcion == "2":
            bot_elegido = seleccionar_bot()
            if bot_elegido is not None:
                jugar_partida("bot", bot=bot_elegido)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")


if __name__ == "__main__":
    mostrar_menu()