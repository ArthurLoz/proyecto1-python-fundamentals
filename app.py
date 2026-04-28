import streamlit as st
import pandas as pd
import numpy as np
from libreria_funciones_proyecto1 import calcular_valor_futuro
from libreria_clases_proyecto1 import ProyectoInversion

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Proyecto 1 - Jimmy Lopez",
    page_icon="💰",
    layout="wide"
)

if "movimientos" not in st.session_state:
    st.session_state.movimientos = []

if "np_nombres" not in st.session_state:
    st.session_state.np_nombres = np.array([])
    st.session_state.np_categorias = np.array([])
    st.session_state.np_precios = np.array([])
    st.session_state.np_cantidades = np.array([])

if "historico_vf" not in st.session_state:
    st.session_state.historico_vf = []

if "proyectos" not in st.session_state:
    st.session_state.proyectos = {}

pagina = st.sidebar.selectbox(
    "📂 Navegación",
    ["🏠 Home", "📋 Ejercicio 1", "📊 Ejercicio 2", "🧮 Ejercicio 3", "🏗️ Ejercicio 4"]
)

if pagina == "🏠 Home":
    st.title("💰 Aplicación Financiera Interactiva")
    st.subheader("Proyecto 1 – Python Fundamentals")
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 👤 Datos del Estudiante")
        st.markdown("""
        | Campo | Detalle |
        |---|---|
        | **Nombre** | Jimmy Arthur Lopez Ore |
        | **Módulo** | Python Fundamentals – Módulo 1 |
        | **Curso** | Especialización Python for Analytics |
        | **Año** | 2025 |
        """)
    with col2:
        st.markdown("### 📌 Descripción del Proyecto")
        st.write(
            "Esta aplicación interactiva fue desarrollada como parte del Proyecto 1 del "
            "Módulo de Python Fundamentals. Integra conceptos fundamentales de programación "
            "aplicados al área de sistemas financieros, incluyendo el registro de flujos de caja, "
            "control de inventario de inversiones, cálculo de valor futuro con interés compuesto "
            "y gestión CRUD de proyectos de inversión."
        )
        st.markdown("### 🛠️ Tecnologías Utilizadas")
        st.markdown("""
        - 🐍 **Python 3**
        - 📊 **Streamlit** – Interfaz interactiva
        - 🔢 **NumPy** – Manejo de arrays
        - 🗂️ **Pandas** – DataFrames y tablas
        - 📐 **Math** – Cálculos financieros
        """)
    st.markdown("---")
    st.markdown("### 📚 Contenido de la Aplicación")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("**Ejercicio 1**\n\nFlujo de caja con listas")
    with c2:
        st.info("**Ejercicio 2**\n\nRegistro de inversiones con NumPy")
    with c3:
        st.info("**Ejercicio 3**\n\nCalculadora de Valor Futuro")
    with c4:
        st.info("**Ejercicio 4**\n\nCRUD de Proyectos de Inversión")

elif pagina == "📋 Ejercicio 1":
    st.title("📋 Ejercicio 1 – Flujo de Caja")
    st.markdown("""
    ### 📖 Descripción
    Registra tus movimientos financieros indicando el concepto, tipo (Ingreso o Gasto) y valor.
    La aplicación calcula el saldo final e indica si el flujo está **a favor** o **en contra**.
    """)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        concepto = st.text_input("📝 Concepto", placeholder="Ej: Salario, Alquiler...")
    with col2:
        tipo = st.selectbox("💱 Tipo de Movimiento", ["Ingreso", "Gasto"])
    valor = st.number_input("💵 Valor (S/.)", min_value=0.01, step=0.01, format="%.2f")

    if st.button("➕ Agregar Movimiento"):
        if concepto.strip() == "":
            st.warning("⚠️ Por favor ingresa un concepto.")
        else:
            st.session_state.movimientos.append({"Concepto": concepto, "Tipo": tipo, "Valor (S/.)": valor})
            st.success(f"✅ '{concepto}' agregado.")

    if st.button("🗑️ Limpiar movimientos"):
        st.session_state.movimientos = []
        st.info("Lista limpiada.")

    st.markdown("---")
    if st.session_state.movimientos:
        st.markdown("### 📊 Movimientos Registrados")
        st.dataframe(pd.DataFrame(st.session_state.movimientos), use_container_width=True)
        total_ingresos = sum(m["Valor (S/.)"] for m in st.session_state.movimientos if m["Tipo"] == "Ingreso")
        total_gastos = sum(m["Valor (S/.)"] for m in st.session_state.movimientos if m["Tipo"] == "Gasto")
        saldo = total_ingresos - total_gastos
        st.markdown("### 📈 Resumen")
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Total Ingresos", f"S/. {total_ingresos:,.2f}")
        col2.metric("❌ Total Gastos", f"S/. {total_gastos:,.2f}")
        col3.metric("💰 Saldo Final", f"S/. {saldo:,.2f}")
        if saldo >= 0:
            st.success(f"🟢 Flujo A FAVOR: S/. {saldo:,.2f}")
        else:
            st.error(f"🔴 Flujo EN CONTRA: S/. {abs(saldo):,.2f}")
    else:
        st.info("📭 Aún no hay movimientos registrados.")

elif pagina == "📊 Ejercicio 2":
    st.title("📊 Ejercicio 2 – Registro de Inversiones con NumPy")
    st.markdown("""
    ### 📖 Descripción
    Registra instrumentos de inversión almacenados en **arrays NumPy** y visualizados en un **DataFrame**.
    """)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        nombre_prod = st.text_input("📦 Instrumento", placeholder="Ej: Bono del Tesoro, Acción BCP...")
        categoria = st.selectbox("🏷️ Categoría", ["Renta Fija", "Renta Variable", "Fondo Mutuo", "Criptomoneda", "Otro"])
    with col2:
        precio = st.number_input("💲 Precio Unitario (S/.)", min_value=0.01, step=0.01, format="%.2f")
        cantidad = st.number_input("🔢 Cantidad", min_value=1, step=1)

    if st.button("➕ Agregar Registro"):
        if nombre_prod.strip() == "":
            st.warning("⚠️ Ingresa el nombre del instrumento.")
        else:
            st.session_state.np_nombres = np.append(st.session_state.np_nombres, nombre_prod)
            st.session_state.np_categorias = np.append(st.session_state.np_categorias, categoria)
            st.session_state.np_precios = np.append(st.session_state.np_precios, precio)
            st.session_state.np_cantidades = np.append(st.session_state.np_cantidades, cantidad)
            st.success(f"✅ '{nombre_prod}' agregado.")

    if st.button("🗑️ Limpiar Registros"):
        st.session_state.np_nombres = np.array([])
        st.session_state.np_categorias = np.array([])
        st.session_state.np_precios = np.array([])
        st.session_state.np_cantidades = np.array([])
        st.info("Registros limpiados.")

    st.markdown("---")
    if len(st.session_state.np_nombres) > 0:
        totales = st.session_state.np_precios * st.session_state.np_cantidades
        df_inv = pd.DataFrame({
            "Instrumento": st.session_state.np_nombres,
            "Categoría": st.session_state.np_categorias,
            "Precio (S/.)": np.round(st.session_state.np_precios, 2),
            "Cantidad": st.session_state.np_cantidades.astype(int),
            "Total (S/.)": np.round(totales, 2)
        })
        st.markdown("### 📋 Portafolio")
        st.dataframe(df_inv, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("💼 Total Portafolio", f"S/. {np.sum(totales):,.2f}")
        col2.metric("📊 Precio Promedio", f"S/. {np.mean(st.session_state.np_precios):,.2f}")
        col3.metric("🔢 N° Instrumentos", len(st.session_state.np_nombres))
    else:
        st.info("📭 Aún no hay instrumentos registrados.")

elif pagina == "🧮 Ejercicio 3":
    st.title("🧮 Ejercicio 3 – Calculadora de Valor Futuro")
    st.markdown("""
    ### 📖 Descripción
    Usa la función `calcular_valor_futuro` para proyectar el crecimiento de una inversión con **interés compuesto**.
    **Fórmula:** `VF = P × (1 + r/n)^(n×t)`
    """)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        monto_inicial = st.number_input("💵 Monto Inicial (S/.)", min_value=1.0, value=1000.0, step=100.0)
        tasa_anual = st.number_input("📈 Tasa Anual (%)", min_value=0.1, max_value=100.0, value=8.0, step=0.5)
    with col2:
        anios = st.number_input("📅 Años", min_value=1, max_value=50, value=5, step=1)
        capitalizaciones = st.selectbox(
            "🔄 Capitalizaciones por Año",
            options=[1, 2, 4, 12, 365],
            index=2,
            format_func=lambda x: {1: "Anual", 2: "Semestral", 4: "Trimestral", 12: "Mensual", 365: "Diaria"}[x]
        )

    if st.button("📐 Calcular Valor Futuro"):
        try:
            resultado = calcular_valor_futuro(
                monto_inicial=monto_inicial,
                tasa_anual_pct=tasa_anual,
                anios=anios,
                capitalizaciones_por_anio=capitalizaciones
            )
            st.markdown("### 📊 Resultado")
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Monto Inicial", f"S/. {monto_inicial:,.2f}")
            col2.metric("📈 Valor Futuro", f"S/. {resultado['valor_futuro']:,.2f}")
            col3.metric("🎯 Interés Ganado", f"S/. {resultado['interes_ganado']:,.2f}")
            cap_nombre = {1: "Anual", 2: "Semestral", 4: "Trimestral", 12: "Mensual", 365: "Diaria"}[capitalizaciones]
            st.session_state.historico_vf.append({
                "Monto Inicial (S/.)": monto_inicial,
                "Tasa (%)": tasa_anual,
                "Años": anios,
                "Capitalización": cap_nombre,
                "Valor Futuro (S/.)": resultado["valor_futuro"],
                "Interés Ganado (S/.)": resultado["interes_ganado"]
            })
            st.success("✅ Guardado en histórico.")
        except ValueError as e:
            st.error(f"❌ Error: {e}")

    if st.button("🗑️ Limpiar Histórico"):
        st.session_state.historico_vf = []
        st.info("Histórico limpiado.")

    st.markdown("---")
    if st.session_state.historico_vf:
        st.markdown("### 📋 Histórico de Cálculos")
        st.dataframe(pd.DataFrame(st.session_state.historico_vf), use_container_width=True)
    else:
        st.info("📭 Aún no hay cálculos en el histórico.")

elif pagina == "🏗️ Ejercicio 4":
    st.title("🏗️ Ejercicio 4 – Gestión de Proyectos de Inversión (CRUD)")
    st.markdown("""
    ### 📖 Descripción
    Gestiona proyectos de inversión con la clase `ProyectoInversion`.
    Operaciones: **Crear**, **Ver**, **Actualizar** y **Eliminar**.
    """)
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Crear", "📋 Ver", "✏️ Actualizar", "🗑️ Eliminar"])

    with tab1:
        st.subheader("➕ Nuevo Proyecto")
        nombre_proy = st.text_input("📌 Nombre", placeholder="Ej: Expansión Planta Norte")
        inversion_ini = st.number_input("💵 Inversión Inicial (S/.)", min_value=1.0, value=50000.0, step=1000.0)
        tasa_desc = st.number_input("📉 Tasa de Descuento (%)", min_value=0.1, max_value=99.9, value=12.0, step=0.5)
        flujos_texto = st.text_input("📅 Flujos por período separados por comas", placeholder="Ej: 15000, 20000, 25000")
        if st.button("💾 Guardar Proyecto"):
            if nombre_proy.strip() == "":
                st.warning("⚠️ Ingresa el nombre.")
            elif nombre_proy in st.session_state.proyectos:
                st.warning("⚠️ Ya existe ese proyecto.")
            else:
                try:
                    flujos = [float(f.strip()) for f in flujos_texto.split(",") if f.strip() != ""]
                    if len(flujos) == 0:
                        st.warning("⚠️ Ingresa al menos un flujo.")
                    else:
                        proyecto = ProyectoInversion(nombre_proy, inversion_ini, flujos, tasa_desc)
                        resumen = proyecto.resumen()
                        st.session_state.proyectos[nombre_proy] = {
                            "inversion_inicial": inversion_ini, "tasa_descuento": tasa_desc,
                            "flujos": flujos, "vpn": resumen["vpn"], "roi_pct": resumen["roi_pct"],
                            "payback_anios": resumen["payback_anios"], "decision": resumen["decision"]
                        }
                        st.success(f"✅ Proyecto '{nombre_proy}' guardado.")
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("VPN (S/.)", f"{resumen['vpn']:,.2f}")
                        col2.metric("ROI (%)", f"{resumen['roi_pct']}%")
                        col3.metric("Payback (años)", f"{resumen['payback_anios']}")
                        col4.metric("Decisión", resumen["decision"])
                except ValueError as e:
                    st.error(f"❌ Error: {e}")

    with tab2:
        st.subheader("📋 Proyectos Registrados")
        if st.session_state.proyectos:
            filas = [{"Proyecto": n, "Inversión (S/.)": d["inversion_inicial"], "Tasa (%)": d["tasa_descuento"],
                      "VPN (S/.)": d["vpn"], "ROI (%)": d["roi_pct"], "Payback (años)": d["payback_anios"],
                      "Decisión": d["decision"]} for n, d in st.session_state.proyectos.items()]
            st.dataframe(pd.DataFrame(filas), use_container_width=True)
            viables = sum(1 for d in st.session_state.proyectos.values() if d["decision"] == "Viable")
            col1, col2 = st.columns(2)
            col1.metric("📁 Total Proyectos", len(st.session_state.proyectos))
            col2.metric("✅ Proyectos Viables", viables)
        else:
            st.info("📭 No hay proyectos aún.")

    with tab3:
        st.subheader("✏️ Actualizar Proyecto")
        if st.session_state.proyectos:
            proy_sel = st.selectbox("Selecciona", list(st.session_state.proyectos.keys()))
            datos_act = st.session_state.proyectos[proy_sel]
            nueva_inversion = st.number_input("💵 Nueva Inversión (S/.)", value=float(datos_act["inversion_inicial"]), min_value=1.0, step=1000.0)
            nueva_tasa = st.number_input("📉 Nueva Tasa (%)", value=float(datos_act["tasa_descuento"]), min_value=0.1, max_value=99.9, step=0.5)
            nuevos_flujos_texto = st.text_input("📅 Nuevos Flujos", value=", ".join([str(f) for f in datos_act["flujos"]]))
            if st.button("🔄 Actualizar"):
                try:
                    nuevos_flujos = [float(f.strip()) for f in nuevos_flujos_texto.split(",") if f.strip() != ""]
                    proyecto_act = ProyectoInversion(proy_sel, nueva_inversion, nuevos_flujos, nueva_tasa)
                    resumen_act = proyecto_act.resumen()
                    st.session_state.proyectos[proy_sel] = {
                        "inversion_inicial": nueva_inversion, "tasa_descuento": nueva_tasa,
                        "flujos": nuevos_flujos, "vpn": resumen_act["vpn"], "roi_pct": resumen_act["roi_pct"],
                        "payback_anios": resumen_act["payback_anios"], "decision": resumen_act["decision"]
                    }
                    st.success(f"✅ '{proy_sel}' actualizado.")
                except ValueError as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.info("📭 No hay proyectos para actualizar.")

    with tab4:
        st.subheader("🗑️ Eliminar Proyecto")
        if st.session_state.proyectos:
            proy_eliminar = st.selectbox("Selecciona a eliminar", list(st.session_state.proyectos.keys()))
            if st.button("❌ Eliminar"):
                del st.session_state.proyectos[proy_eliminar]
                st.success(f"✅ '{proy_eliminar}' eliminado.")
        else:
            st.info("📭 No hay proyectos para eliminar.")
