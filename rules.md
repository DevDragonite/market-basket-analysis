# Reglas del Proyecto - Market Basket Analysis + BI Dashboard

## Contexto
Proyecto de portafolio profesional. Cada decisión técnica debe explicarse 
en términos de negocio, no solo en términos técnicos.

## Estructura de código
- Todo el código Python va en /notebooks/
- Los archivos exportados para Power BI van en /exports/ como CSV
- Cada función debe tener un docstring con el "insight de negocio" que produce

## Estándares de calidad
- No uses datos hardcodeados. Todo debe leerse del archivo en /data/
- Maneja excepciones para columnas nulas o formatos incorrectos
- Al final de cada sección del notebook, agrega un bloque Markdown 
  con el insight ejecutivo en español

## Outputs obligatorios
El proyecto debe producir exactamente:
1. notebooks/01_eda_limpieza.py
2. notebooks/02_market_basket.py  
3. exports/reglas_asociacion.csv
4. exports/resumen_ejecutivo.csv
```

---

### 3. Despacha los 3 agentes en paralelo

El Manager View te permite hacer clic en "Start Conversation" para abrir múltiples agentes en diferentes workspaces que corren en paralelo. Puedes asignar un "Junior Agent" para tareas tediosas en el fondo mientras usas un "Senior Agent" para pair-programming. 

Abre **3 conversaciones nuevas** en el Manager View, una para cada agente:

---

**Agente 1 — EDA y Limpieza** (cópialo tal cual):
```
Eres un Senior Data Analyst construyendo un portafolio profesional.

TAREA: Crea el archivo notebooks/01_eda_limpieza.py para el dataset 
data/online_retail.xlsx

El script debe:
1. Cargar el dataset y mostrar shape, dtypes y primeras 5 filas
2. Identificar y reportar: valores nulos por columna, facturas de 
   devolución (InvoiceNo que empieza con 'C'), precios negativos o cero
3. Limpiar: eliminar nulos en CustomerID, eliminar devoluciones, 
   eliminar precios <= 0, eliminar duplicados
4. EDA visual: top 10 países por ventas, top 10 productos más vendidos, 
   distribución de ventas por mes
5. Al final de cada sección, un bloque Markdown con el insight de negocio

Exporta el dataframe limpio como exports/data_limpia.csv
```

---

**Agente 2 — Algoritmo Apriori** (nueva conversación):
```
Eres un Senior Data Analyst construyendo un portafolio profesional.

TAREA: Crea notebooks/02_market_basket.py

Asume que exports/data_limpia.csv ya existe (lo genera otro proceso).

El script debe:
1. Cargar data_limpia.csv
2. Filtrar solo transacciones de UK (el mercado principal)
3. Crear la basket matrix: filas=InvoiceNo, columnas=Description, 
   valores=1/0 (si el producto fue comprado en esa factura)
4. Aplicar algoritmo Apriori con mlxtend: min_support=0.01
5. Generar reglas de asociación: min_threshold=0.2 en métrica 'lift'
6. Filtrar reglas con lift > 1.5 (asociaciones reales, no aleatorias)
7. Ordenar por lift descendente y tomar top 20

Exportar como exports/reglas_asociacion.csv con columnas:
antecedents, consequents, support, confidence, lift

Al final, un bloque Markdown con los 3 insights de negocio más importantes
```

---

**Agente 3 — Resumen ejecutivo para Power BI** (nueva conversación):
```
Eres un Senior Data Analyst construyendo un portafolio profesional.

TAREA: Crea notebooks/03_resumen_ejecutivo.py

Asume que exports/reglas_asociacion.csv ya existe.

El script debe:
1. Cargar reglas_asociacion.csv
2. Calcular: AOV actual promedio (asume $45 como baseline)
3. Para las top 5 reglas por lift, calcular el AOV proyectado si se 
   implementan los bundles (usa confidence como proxy de adopción)
4. Crear un dataframe resumen con columnas:
   bundle_rank, producto_A, producto_B, lift, confidence, 
   aov_proyectado, incremento_pct
5. Exportar como exports/resumen_ejecutivo.csv

Este CSV alimentará las KPI Cards en Power BI, así que los números 
deben ser limpios y redondeados a 2 decimales.