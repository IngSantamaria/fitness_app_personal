import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.real_data_collector import RealDataCollector
from src.advanced_ai_analyzer import AdvancedAIAnalyzer
from src.position_manager import PositionManager
from src.position_manager_window import PositionManagerWindow
from src.decision_engine import DecisionEngine




class Database:
    def __init__(self):
        pass

class EducationalWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("📚 Trading Education Guide")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        # Centrar la ventana
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Notebook para pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Términos Básicos
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="📖 Términos Básicos")
        
        basic_text = tk.Text(basic_frame, wrap=tk.WORD, padx=10, pady=10)
        basic_scroll = ttk.Scrollbar(basic_frame, orient=tk.VERTICAL, command=basic_text.yview)
        basic_text.configure(yscrollcommand=basic_scroll.set)
        
        basic_text.pack(side='left', fill='both', expand=True)
        basic_scroll.pack(side='right', fill='y')
        
        basic_content = """
📚 GUÍA EDUCATIVA DE TRADING

🎯 TENDENCIAS DE MERCADO

🟢 BULLISH (Alcista)
• Significado: Mercado que sube de precio
• Características: Precios en aumento, optimismo, demanda alta
• Qué hacer: Considerar comprar, mantener posiciones largas
• Ejemplo: "BTC está en tendencia bullish - sube $5,000 en una semana"

🔴 BEARISH (Bajista)
• Significado: Mercado que baja de precio
• Características: Precios en descenso, pesimismo, oferta alta
• Qué hacer: Considerar vender, posiciones cortas, esperar
• Ejemplo: "ETH está en tendencia bearish - cae $3,000 en tres días"

🟡 NEUTRAL (Neutral)
• Significado: Mercado sin dirección clara
• Características: Precios laterales, indecisión, volumen bajo
• Qué hacer: Esperar, no tomar grandes posiciones
• Ejemplo: "ADA está neutral - se mueve entre $0.35 y $0.40"

📊 INDICADORES TÉCNICOS

📈 RSI (Relative Strength Index)
• Qué es: Indicador de momentum que mide velocidad y cambio de precios
• Rango: 0-100
• Interpretación:
  - Sobre 70: SOBRECOMPRA (precio muy alto, puede caer)
  - Debajo de 30: SOBREVENDA (precio muy bajo, puede subir)
  - 50: Línea media (equilibrio)
• Uso: Identificar puntos de entrada/salida

📉 MACD (Moving Average Convergence Divergence)
• Qué es: Indicador de tendencia que sigue el momentum
• Componentes: Línea MACD, Señal MACD, Histograma
• Interpretación:
  - MACD > Señal: Tendencia alcista
  - MACD < Señal: Tendencia bajista
  - Cruces: Señales de compra/venta
• Uso: Confirmar tendencias y detectar cambios

📊 SMA (Simple Moving Average)
• Qué es: Promedio de precios de un período específico
• Períodos comunes: 20, 50, 200 días
• Interpretación:
  - Precio > SMA: Tendencia alcista
  - Precio < SMA: Tendencia bajista
  - Cruces de SMA: Cambios de tendencia importantes
• Uso: Identificar dirección general del mercado

🎯 CONCEPTOS CLAVE

💰 SOPORTE (Support)
• Qué es: Nivel de precios donde la demanda es fuerte enough para detener caídas
• Características: "Piso" del precio, muchos compradores
• Estrategia: Comprar cerca del soporte
• Ejemplo: "BTC tiene soporte en $85,000"

📈 RESISTENCIA (Resistance)
• Qué es: Nivel de precios donde la oferta es strong enough para detener subidas
• Características: "Techo" del precio, muchos vendedores
• Estrategia: Vender cerca de la resistencia
• Ejemplo: "BTC tiene resistencia en $95,000"

🛡️ STOP LOSS
• Qué es: Orden automática para vender si el precio cae a cierto nivel
• Propósito: Limitar pérdidas, proteger capital
• Regla común: 5-10% por debajo del precio de compra
• Ejemplo: "Compré BTC a $90,000, puse stop loss en $81,000"

📊 VOLATILIDAD
• Qué es: Medida de cuánto varían los precios en un período
• Alta volatilidad: Grandes cambios de precio rápido (criptos)
• Baja volatilidad: Pequeños cambios de precio lento (acciones estables)
• Uso: Evaluar riesgo y determinar tamaño de posición

⚖️ RIESGO/RECOMPENSA (Risk/Reward)
• Qué es: Relación entre posible ganancia y posible pérdida
• Buen ratio: Ganancia potencial > 2x pérdida potencial
• Cálculo: (Precio objetivo - Precio entrada) / (Precio entrada - Stop loss)
• Ejemplo: "Ratio 3:1 - Por cada $1 de riesgo, $3 de ganancia potencial"

🔄 VOLUMEN (Volume)
• Qué es: Cantidad de activos negociados en un período
• Alto volumen: Mucha actividad, interés fuerte
• Bajo volumen: Poca actividad, interés débil
• Uso: Confirmar movimientos de precios

💡 CONSEJOS PRÁCTICOS

🎯 Regla del 1%
• Arriesga solo 1% de tu capital total en una sola operación
• Protege tu capital para operaciones futuras

📈 Comprar en la dips
• Compra cuando los precios caen (en soportes)
• Vende cuando los precios suben (en resistencias)

⏰ Paciencia
• Espera confirmaciones antes de entrar
• No te apresures por FOMO (Fear Of Missing Out)

📚 Educación continua
• Aprende sobre análisis técnico y fundamental
• Practica con cuentas demo antes de usar dinero real

⚠️ ADVERTENCIAS IMPORTANTES

🚨 NUNCA inviertas más de lo que puedes permitir perder
🚨 Siempre haz tu propia investigación (DYOR)
🚨 El trading pasado no garantiza resultados futuros
🚨 Las criptomonedas son extremadamente volátiles
🚯 Consulta a profesionales financieros si no estás seguro

¡Recuerda: El conocimiento es tu mejor herramienta! 🎓
        """
        
        basic_text.insert('1.0', basic_content)
        basic_text.config(state='disabled')
        
        # Pestaña 2: Patrones de Mercado
        patterns_frame = ttk.Frame(notebook)
        notebook.add(patterns_frame, text="🔍 Patrones de Mercado")
        
        patterns_text = tk.Text(patterns_frame, wrap=tk.WORD, padx=10, pady=10)
        patterns_scroll = ttk.Scrollbar(patterns_frame, orient=tk.VERTICAL, command=patterns_text.yview)
        patterns_text.configure(yscrollcommand=patterns_scroll.set)
        
        patterns_text.pack(side='left', fill='both', expand=True)
        patterns_scroll.pack(side='right', fill='y')
        
        patterns_content = """
🔍 PATRONES DE MERCADO COMUNES

📈 PATRONES ALCISTAS (Bullish Patterns)

🟢 HAMMER (Martillo)
• Apariencia: Vela pequeña con mecha larga inferior, sombra superior pequeña o nula
• Significado: Rechazo fuerte de vendedores, posible reversión alcista
• Contexto: Después de una tendencia bajista
• Acción: Considerar compra

🟢 ENGULFING (Patrón de envolvimiento alcista)
• Apariencia: Vela grande que "envuelve" completamente a la vela anterior
• Significado: Compradores fuertes toman control
• Contexto: Después de una tendencia bajista
• Acción: Señal de compra fuerte

🟢 MORNING STAR (Estrella de la mañana)
• Apariencia: Tres velas - pequeña, grande con gap abajo, pequeña
• Significado: Posible reversión alcista después de tendencia bajista
• Contexto: Al final de una caída
• Acción: Considerar compra

📉 PATRONES BAJISTAS (Bearish Patterns)

🔴 SHOOTING STAR (Estrella fugitiva)
• Apariencia: Vela pequeña con mecha larga superior, sombra inferior pequeña o nula
• Significado: Rechazo fuerte de compradores, posible reversión bajista
• Contexto: Después de una tendencia alcista
• Acción: Considerar venta

🔴 EVENING STAR (Estrella de la tarde)
• Apariencia: Tres velas - grande con gap arriba, pequeña, pequeña
• Significado: Posible reversión bajista después de tendencia alcista
• Contexto: Al final de una subida
• Acción: Considerar venta

🔴 DARK CLOUD COVER (Nube oscura)
• Apariencia: Vela grande que "envuelve" completamente a la vela anterior
• Significado: Vendedores fuertes toman control
• Contexto: Después de una tendencia alcista
• Acción: Señal de venta fuerte

🔄 PATRONES DE CONTINUACIÓN

📊 FLAGS (Banderas)
• Apariencia: Pequeño rectángulo inclinado después de movimiento fuerte
• Significado: Consolidación antes de continuar tendencia
• Acción: Esperar ruptura y operar en dirección de la ruptura

📊 TRIANGLES (Triángulos)
• Apariencia: Rango que se estrecha formando triángulo
• Significado: Indecisión antes de gran movimiento
• Acción: Operar en dirección de ruptura

📊 WEDGES (Cuñas)
• Apariencia: Triángulo con líneas convergiendo en una dirección
• Significado: Tendencia perdiendo momentum
• Acción: Operar en dirección opuesta a la convergencia

🎯 CÓMO USAR ESTOS PATRONES

✅ Confirmación múltiple
• Busca 2-3 señales que confirmen el patrón
• Usa volumen para validar el movimiento
• Espera ruptura clara antes de operar

✅ Contexto del mercado
• Los patrones funcionan mejor en tendencias claras
• Evita patrones en mercados laterales (ranging)
• Considera el timeframe (diario, semanal, mensual)

✅ Gestión de riesgos
• Siempre usa stop loss
• Determina tamaño de posición según el patrón
• Ten un plan claro antes de entrar

⚠️ LIMITACIONES DE LOS PATRONES

🚨 No son 100% confiables
• Los patrones pueden fallar
• Siempre hay falsas señales
• Necesita confirmación adicional

🚨 Subjetividad
• Diferentes traders ven patrones diferentes
• La experiencia mejora la identificación
• Practica con cuentas demo

🚨 Condiciones del mercado
• Los patrones funcionan diferente en varios mercados
• Las noticias pueden invalidar patrones
• El sentimiento del mercado afecta la fiabilidad

💡 CONSEJO FINAL

📚 Educa continuamente
• Aprende sobre análisis técnico
• Estudia gráficos históricos
• Practica identificación de patrones

🎯 Sé paciente
• Espera patrones claros y bien formados
• No te apresures por patrones imperfectos
• La calidad es más importante que la cantidad

📊 Usa múltiples herramientas
• Combina patrones con indicadores
• Considera análisis fundamental
• Mira el sentimiento del mercado

¡Recuerda: Los patrones son herramientas, no reglas absolutas! 🎯
        """
        
        patterns_text.insert('1.0', patterns_content)
        patterns_text.config(state='disabled')
        
        # Pestaña 3: Psicología del Trading
        psychology_frame = ttk.Frame(notebook)
        notebook.add(psychology_frame, text="🧠 Psicología del Trading")
        
        psychology_text = tk.Text(psychology_frame, wrap=tk.WORD, padx=10, pady=10)
        psychology_scroll = ttk.Scrollbar(psychology_frame, orient=tk.VERTICAL, command=psychology_text.yview)
        psychology_text.configure(yscrollcommand=psychology_scroll.set)
        
        psychology_text.pack(side='left', fill='both', expand=True)
        psychology_scroll.pack(side='right', fill='y')
        
        psychology_content = """
🧠 PSICOLOGÍA DEL TRADING

🎯 EMOCIONES COMUNES Y CÓMO MANEJARLAS

😰 MIEDO (Fear)
• Cuándo aparece: Antes de entrar, durante pérdidas, en mercados volátiles
• Efectos: Parálisis, venta prematura, no tomar oportunidades
• Solución:
  - Plan de trading claro antes de operar
  - Tamaños de posición pequeños
  - Stick a tu estrategia
  - Recuerda tu análisis original

🤑 CODICIA (Greed)
• Cuándo aparece: Después de ganancias, en mercados alcistas, FOMO
• Efectos: Sobreapalancar, no tomar ganancias, asumir riesgos excesivos
• Solución:
  - Objetivos de ganancia claros
  - Tomar ganancias parciales
  - No cambiar el plan mid-trade
  - Recordar que el mercado puede revertir

😤 ARREPENTIMIENTO (Regret)
• Cuándo aparece: Después de perder oportunidades, vender demasiado pronto/ tarde
• Efectos: Venganza trading, sobretrading, romper reglas
• Solución:
  - Aceptar que no puedes predecir perfectamente
  - Enfocarse en el próximo trade
  - Aprender de los errores sin castigarte
  - Mantener disciplina

🤔 ANSIEDAD (Anxiety)
• Cuándo aparece: En mercados rápidos, con mucho capital en juego
• Efectos: Sobreanálisis, entrada/salida prematura, estrés
• Solución:
  - Meditación y mindfulness
  - Reducir tamaño de posición
  - Tomar descansos cuando sea necesario
  - Enfocarse en proceso, no resultado

🎯 ESTADO MENTAL IDEAL

🧘 CALMA (Calm)
• Características: Decisiones racionales, seguimiento del plan
• Cómo lograrlo:
  - Buena preparación y análisis
  - Tamaños de posición manejables
  - Confianza en tu estrategia
  - Experiencia y práctica

🎯 ENFOCADO (Focused)
• Características: Atención a detalles, ejecución precisa
• Cómo lograrlo:
  - Entorno de trading sin distracciones
  - Checklist pre-trade
  - Monitoreo activo pero no obsesivo
  - Objetivos claros

📊 OBJETIVO (Objective)
• Características: Decisiones basadas en datos, no emociones
• Cómo lograrlo:
  - Sistema de trading claro
  - Reglas estrictas
  - Revisión regular de desempeño
  - Aprendizaje continuo

🚫 ERRORES PSICOLÓGICOS COMUNES

❌ OVERTRADING (Operar demasiado)
• Causa: Intentar recuperar pérdidas, FOMO, aburrimiento
• Solución: Límite de trades por día/semana, descansos obligatorios

❌ REVENGE TRADING (Trading de venganza)
• Causa: Intentar "recuperar" pérdidas rápidamente
• Solución: Aceptar pérdidas como parte del negocio, esperar próxima oportunidad

❌ CHASING (Perseguir precios)
• Causa: No querer perderse de movimientos rápidos
• Solución: Esperar pullbacks, usar órdenes límite

❌ ANALYSIS PARALYSIS (Parálisis por análisis)
• Causa: Demasiada información, indecisión
• Solución: Sistema simple, reglas claras, acción decisiva

📚 ESTRATEGIAS PSICOLÓGICAS

🎯 MINDFULNESS TRADING
• Práctica: Meditación antes de operar
• Beneficio: Claridad mental, reducción de estrés
• Cómo: 5-10 minutos de respiración profunda

📓 JOURNALING (Diario de trading)
• Qué registrar: Entradas, salidas, emociones, resultados
• Beneficio: Autoconocimiento, mejora continua
• Frecuencia: Después de cada trade

🎪 SIMULATION TRADING
• Práctica: Operar con cuenta demo
• Beneficio: Experiencia sin riesgo financiero
• Cuándo: Antes de usar dinero real, probar estrategias

👥 ACCOUNTABILITY (Responsabilidad)
• Método: Trading buddy, mentor, comunidad
• Beneficio: Disciplina, feedback externo
• Cómo: Compartir trades, discutir decisiones

🔄 RUTINAS SALUDABLES

🏃‍♂️ EJERCICIO FÍSICO
• Beneficios: Reducción de estrés, claridad mental
• Frecuencia: 30 minutos diarios
• Cuándo: Antes/después de sesión de trading

🧘 MEDITACIÓN
• Beneficios: Calma, enfoque, reducción de ansiedad
• Frecuencia: 10-15 minutos diarios
• Cuándo: Antes de tomar decisiones importantes

📚 APRENDIZAJE
• Beneficios: Confianza, mejora continua
• Frecuencia: 30 minutos diarios
• Qué: Libros, videos, análisis de mercado

🛌 DESCANSO
• Beneficios: Prevención de burnout, perspectiva fresca
• Frecuencia: 1-2 días libres por semana
• Importancia: El trading es maratón, no sprint

⚖️ EQUILIBRIO VIDA-TRADING

🏠 FAMILIA Y AMIGOS
• Mantener relaciones importantes
• No dejar que el trading consuma tu vida
• Tiempo de calidad sin pantallas

💼 TRABAJO/ESTUDIOS
• No dejar el trading por tu carrera
• Trading como side hustle al principio
• Transición gradual si es necesario

🎄 HOBBIES E INTERESES
• Mantener actividades fuera del trading
• Diversificar fuentes de felicidad
• Prevenir obsesión con mercados

💰 SALUD FINANCIERA
• Solo arriesgar capital que puedes perder
• Fondo de emergencia separado
• Metas financieras realistas

🚨 SEÑALES DE ADVERTENCIA

⚠️ CUANDO BUSCAR AYUDA
• Depresión persistente
• Ansiedad severa
• Adicción al trading
• Problemas de relaciones
• Problemas financieros serios

👥 PROFESIONALES A CONSULTAR
• Psicólogos especializados en trading
• Coaches financieros
• Grupos de apoyo
• Mentores experimentados

💡 CONSEJO FINAL

🎯 EL TRADING ES UN MARATÓN, NO UN SPRINT
• Enfócate en mejora a largo plazo
• Celebra pequeñas victorias
• Aprende de los errores

🧠 TU MENTE ES TU MÁXIMA HERRAMIENTA
• Entiende tu psicología
• Trabaja en tu mentalidad
• Desarrolla resiliencia

📈 EL ÉXITO EN TRADING = 70% PSICOLOGÍA + 30% TÉCNICA
• La mayoría pierde por errores psicológicos
• La técnica es importante pero no suficiente
• El autocontrol es la clave del éxito

¡Recuerda: Un trader exitoso tiene una mente exitosa! 🧠
        """
        
        psychology_text.insert('1.0', psychology_content)
        psychology_text.config(state='disabled')
        
        # Botón de cerrar
        close_frame = ttk.Frame(self.window)
        close_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(close_frame, text="Cerrar", command=self.window.destroy).pack(side='right')
        ttk.Label(close_frame, text="💡 Conocimiento es tu mejor herramienta de trading", foreground='blue').pack(side='left')

class CryptoStockAnalyzerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 TRADING ASSISTANT PRO - Datos Reales + Alertas + Educación")
        self.root.geometry("1400x900")
        
        # Inicializar componentes PRO
        self.data_collector = RealDataCollector()
        self.ai_analyzer = AdvancedAIAnalyzer()
        self.decision_engine = DecisionEngine()
        self.position_manager = PositionManager()
        self.database = Database()
        
        self.setup_ui()
        self.load_saved_watchlist()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🚀 TRADING ASSISTANT PRO - Datos Reales + Alertas + Educación", 
                                font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Panel izquierdo: Control y Watchlist
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Panel de control
        control_frame = ttk.LabelFrame(left_frame, text="⚙️ Control Panel", padding="10")
        control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Botones de acción principales
        ttk.Button(control_frame, text="🔄 Update Data", 
                   command=self.update_data).grid(row=0, column=0, pady=3, sticky="ew")
        ttk.Button(control_frame, text="🧠 Advanced Analysis", 
                   command=self.run_analysis).grid(row=1, column=0, pady=3, sticky="ew")
        ttk.Button(control_frame, text="💰 Price Recommendations", 
                   command=self.get_price_recommendations).grid(row=2, column=0, pady=3, sticky="ew")
        ttk.Button(control_frame, text="🔔 Check Alerts", 
                   command=self.check_alerts).grid(row=3, column=0, pady=3, sticky="ew")
        ttk.Button(control_frame, text="📊 Position Manager", 
                   command=self.open_position_manager).grid(row=4, column=0, pady=3, sticky="ew")
        ttk.Button(control_frame, text="📚 Trading Education", 
                   command=self.open_education, style='Accent.TButton').grid(row=5, column=0, pady=3, sticky="ew")
        
        # Panel de Watchlist
        watchlist_frame = ttk.LabelFrame(left_frame, text="📋 My Watchlist", padding="10")
        watchlist_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Botones de Watchlist
        ttk.Button(watchlist_frame, text="➕ Add to Watchlist", 
                   command=self.add_to_watchlist).grid(row=0, column=0, pady=3, sticky="ew")
        ttk.Button(watchlist_frame, text="🗑️ Clear Watchlist", 
                   command=self.clear_watchlist).grid(row=1, column=0, pady=3, sticky="ew")
        
        # Treeview para Watchlist
        columns = ('Symbol', 'Custom Name', 'Buy Alert', 'Sell Alert')
        self.watchlist_tree = ttk.Treeview(watchlist_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.watchlist_tree.heading(col, text=col)
            if col == 'Symbol':
                self.watchlist_tree.column(col, width=70)
            elif col == 'Custom Name':
                self.watchlist_tree.column(col, width=120)
            else:
                self.watchlist_tree.column(col, width=80)
        
        self.watchlist_tree.grid(row=2, column=0, pady=5, sticky="ew")
        
        # Configuración de activos (ahora más grande para nombres personalizados)
        config_frame = ttk.LabelFrame(left_frame, text="🔧 Asset Configuration", padding="10")
        config_frame.grid(row=2, column=0, sticky="ew")
        
        ttk.Label(config_frame, text="Cryptocurrencies:").grid(row=0, column=0, sticky="w")
        self.crypto_entry = ttk.Entry(config_frame, width=25)
        self.crypto_entry.grid(row=0, column=1, padx=5, pady=2)
        self.crypto_entry.insert(0, "BTC,ETH,ADA")
        
        ttk.Label(config_frame, text="Stocks:").grid(row=1, column=0, sticky="w")
        self.stock_entry = ttk.Entry(config_frame, width=25)
        self.stock_entry.grid(row=1, column=1, padx=5, pady=2)
        self.stock_entry.insert(0, "AAPL,GOOGL,TSLA")
        
        # Panel de resultados
        results_frame = ttk.LabelFrame(main_frame, text="📊 Analysis Results", padding="10")
        results_frame.grid(row=1, column=1, rowspan=2, sticky="nsew")
        
        # Text area para resultados
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=25, width=80)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Panel de estado
        status_frame = ttk.LabelFrame(main_frame, text="📡 Status", padding="10")
        status_frame.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready - PRO Mode", foreground="green")
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        # Configurar weights
        left_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def open_position_manager(self):
        """Abrir ventana de gestión de posiciones"""
        position_window = PositionManagerWindow(
            self.root, 
            self.position_manager, 
            self.data_collector, 
            self.ai_analyzer
        )
    
    def open_education(self):
        """Abrir ventana educativa"""
        education_window = EducationalWindow(self.root)
        
    def load_saved_watchlist(self):
        """Cargar watchlist guardada"""
        try:
            watchlist = self.data_collector.get_watchlist()
            
            # Limpiar treeview
            for item in self.watchlist_tree.get_children():
                self.watchlist_tree.delete(item)
            
            # Cargar elementos
            for key, asset in watchlist.items():
                buy_alert = f"${asset.get('buy_alert_price', 0):.4f}" if asset.get('buy_alert_price') else "None"
                sell_alert = f"${asset.get('sell_alert_price', 0):.4f}" if asset.get('sell_alert_price') else "None"
                
                self.watchlist_tree.insert('', 'end', values=(
                    asset['symbol'],
                    asset['custom_name'],
                    buy_alert,
                    sell_alert
                ))
            
            self.update_status(f"Loaded {len(watchlist)} assets from watchlist", "blue")
        except Exception as e:
            self.update_status(f"Error loading watchlist: {str(e)}", "red")
    
    def add_to_watchlist(self):
        """Diálogo para agregar activo a watchlist"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add to Watchlist")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Centrar el diálogo
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos
        ttk.Label(dialog, text="Symbol:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        symbol_entry = ttk.Entry(dialog, width=30)
        symbol_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Custom Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Buy Alert Price:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        buy_entry = ttk.Entry(dialog, width=30)
        buy_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Sell Alert Price:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        sell_entry = ttk.Entry(dialog, width=30)
        sell_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def save_asset():
            try:
                symbol = symbol_entry.get().strip().upper()
                custom_name = name_entry.get().strip()
                buy_price = float(buy_entry.get()) if buy_entry.get().strip() else None
                sell_price = float(sell_entry.get()) if sell_entry.get().strip() else None
                
                if symbol:
                    self.data_collector.add_to_watchlist(symbol, custom_name, buy_price, sell_price)
                    self.load_saved_watchlist()
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Added {symbol} to watchlist!")
                else:
                    messagebox.showerror("Error", "Please enter a symbol")
            except ValueError:
                messagebox.showerror("Error", "Invalid price format")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add asset: {str(e)}")
        
        # Botones
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_asset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def clear_watchlist(self):
        """Limpiar toda la watchlist"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the entire watchlist?"):
            try:
                self.data_collector.watchlist_config['watchlist'] = {}
                self.data_collector.save_watchlist_config()
                self.load_saved_watchlist()
                self.update_status("Watchlist cleared", "green")
            except Exception as e:
                self.update_status(f"Error clearing watchlist: {str(e)}", "red")
    
    def check_alerts(self):
        """Verificar alertas de precios"""
        def alerts_thread():
            try:
                self.start_progress()
                self.update_status("Checking price alerts...", "blue")
                
                # Cargar datos actuales
                cryptos = [c.strip() for c in self.crypto_entry.get().split(',')]
                stocks = [s.strip() for s in self.stock_entry.get().split(',')]
                
                current_data = self.data_collector.update_all_data(cryptos, stocks)
                
                # Verificar alertas
                alerts = self.data_collector.check_price_alerts(current_data)
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "🔔 PRICE ALERTS CHECK\n")
                self.results_text.insert(tk.END, "="*50 + "\n\n")
                
                if alerts:
                    for alert in alerts:
                        self.results_text.insert(tk.END, f"⚠️ {alert['message']}\n")
                        self.results_text.insert(tk.END, f"   Current Price: ${alert['current_price']:.4f}\n")
                        self.results_text.insert(tk.END, f"   Target Price: ${alert['target_price']:.4f}\n")
                        self.results_text.insert(tk.END, f"   Action: {alert['type']}\n")
                        self.results_text.insert(tk.END, f"   Data Source: {alert['data_source']}\n")
                        self.results_text.insert(tk.END, "-"*40 + "\n\n")
                    
                    self.update_status(f"Found {len(alerts)} active alerts!", "orange")
                else:
                    self.results_text.insert(tk.END, "✅ No price alerts triggered.\n\n")
                    self.results_text.insert(tk.END, "Current prices are within your specified ranges.\n")
                    self.results_text.insert(tk.END, "Add more assets to watchlist or adjust alert prices.\n")
                    self.update_status("No alerts triggered", "green")
                
            except Exception as e:
                self.update_status(f"Error checking alerts: {str(e)}", "red")
                messagebox.showerror("Error", f"Failed to check alerts: {str(e)}")
            finally:
                self.stop_progress()
        
        threading.Thread(target=alerts_thread, daemon=True).start()
    
    def get_price_recommendations(self):
        """Obtener recomendaciones de precios específicos"""
        def recommendations_thread():
            try:
                self.start_progress()
                self.update_status("Generating price recommendations...", "blue")
                
                # Cargar datos actuales
                cryptos = [c.strip() for c in self.crypto_entry.get().split(',')]
                stocks = [s.strip() for s in self.stock_entry.get().split(',')]
                
                current_data = self.data_collector.update_all_data(cryptos, stocks)
                
                # Ejecutar análisis avanzado
                analysis_results = self.ai_analyzer.analyze_market()
                
                # Generar recomendaciones usando el motor de decisión avanzado
                price_recommendations = self.decision_engine.get_recommendations()
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "💰 PRICE RECOMMENDATIONS\n")
                self.results_text.insert(tk.END, "="*60 + "\n\n")
                
                for key, rec in price_recommendations.items():
                    # Usar color de señal institucional si está disponible
                    signal_color = rec.get('signal_color', 'YELLOW')
                    if signal_color == 'GREEN':
                        action_emoji = "🟢"
                    elif signal_color == 'RED':
                        action_emoji = "🔴"
                    elif signal_color == 'ORANGE':
                        action_emoji = "🟠"
                    elif signal_color == 'GRAY':
                        action_emoji = "⚪"
                    else:
                        action_emoji = "🟡" if rec['action'] == 'HOLD' else "🟢" if rec['action'] == 'BUY' else "🔴"
                    
                    # Obtener precio actual del análisis
                    current_price = rec.get('current_price', 0)
                    if current_price == 0:
                        # Fallback: obtener de los datos recolectados
                        current_price = current_data.get(key, {}).get('current_price', 0)
                    
                    self.results_text.insert(tk.END, f"{action_emoji} {key.upper()}: {rec['action']}\n")
                    self.results_text.insert(tk.END, f"   Current Price: ${current_price:.4f}\n")
                    self.results_text.insert(tk.END, f"   💡 Target Price: ${rec.get('target_price', current_price):.4f}\n")
                    self.results_text.insert(tk.END, f"   🛡️ Stop Loss: ${rec.get('stop_loss', current_price * 0.95):.4f}\n")
                    self.results_text.insert(tk.END, f"   📊 Risk Level: {rec['risk_level']}\n")
                    self.results_text.insert(tk.END, f"   🎯 Confidence: {rec['confidence']}%\n")
                    self.results_text.insert(tk.END, f"   📝 Reason: {rec['reason']}\n")
                    
                    # Mostrar indicadores institucionales clave
                    if rec.get('distance_to_sma200_pct', 0) != 0:
                        self.results_text.insert(tk.END, f"   📏 Distance to SMA200: {rec.get('distance_to_sma200_pct', 0):.2f}%\n")
                    if rec.get('volume_trend'):
                        self.results_text.insert(tk.END, f"   📊 Volume Trend: {rec.get('volume_trend', 'NEUTRAL')}\n")
                    if rec.get('risk_reward_ratio', 0) > 0:
                        self.results_text.insert(tk.END, f"   ⚖️ Risk/Reward: {rec.get('risk_reward_ratio', 0):.2f}\n")
                    
                    # Señal institucional si aplica
                    if signal_color in ['ORANGE', 'GRAY']:
                        self.results_text.insert(tk.END, f"   🚨 INSTITUTIONAL SIGNAL: {rec['reason']}\n")
                    
                    self.results_text.insert(tk.END, "-"*60 + "\n\n")
                
                self.update_status("Price recommendations ready!", "green")
                
            except Exception as e:
                self.update_status(f"Error: {str(e)}", "red")
                messagebox.showerror("Error", f"Failed to generate recommendations: {str(e)}")
            finally:
                self.stop_progress()
        
        threading.Thread(target=recommendations_thread, daemon=True).start()
    
    def update_status(self, message, color="black"):
        self.status_label.config(text=message, foreground=color)
        self.root.update_idletasks()
        
    def start_progress(self):
        self.progress.start()
        
    def stop_progress(self):
        self.progress.stop()
        
    def update_data(self):
        def update_thread():
            try:
                self.start_progress()
                self.update_status("Fetching real market data...", "blue")
                
                cryptos = [c.strip().lower() for c in self.crypto_entry.get().split(',')]
                stocks = [s.strip().upper() for s in self.stock_entry.get().split(',')]
                
                data = self.data_collector.update_all_data(cryptos, stocks)
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "🔄 REAL DATA UPDATE\n")
                self.results_text.insert(tk.END, "="*50 + "\n\n")
                self.results_text.insert(tk.END, f"✅ Successfully updated data for:\n")
                self.results_text.insert(tk.END, f"   🪙 Cryptocurrencies: {', '.join([c.upper() for c in cryptos])}\n")
                self.results_text.insert(tk.END, f"   📈 Stocks: {', '.join(stocks)}\n")
                self.results_text.insert(tk.END, f"   📊 Total Assets: {len(data)}\n\n")
                
                self.results_text.insert(tk.END, "📋 Current Market Data:\n")
                self.results_text.insert(tk.END, "-"*40 + "\n")
                
                for key, item in data.items():
                    self.results_text.insert(tk.END, f"\n{key.replace('_', ' ').title()}:\n")
                    self.results_text.insert(tk.END, f"   Current Price: ${item['current_price']:.4f}\n")
                    self.results_text.insert(tk.END, f"   24h Change: {item.get('change_24h', 0):+.2f}%\n")
                    self.results_text.insert(tk.END, f"   Volume: ${item.get('volume_24h', 0):,.0f}\n")
                    self.results_text.insert(tk.END, f"   Data Source: {item.get('source', 'Unknown')}\n")
                
                self.results_text.insert(tk.END, f"\n{'-'*40}\n")
                self.results_text.insert(tk.END, "💡 Tip: Use 'Price Recommendations' for exact buy/sell prices!\n")
                self.results_text.insert(tk.END, "🔔 Use 'Check Alerts' to see if any watchlist items triggered.\n")
                self.results_text.insert(tk.END, "📚 Use 'Trading Education' to learn about market terms!\n")
                
                self.update_status("Real data updated successfully!", "green")
                
            except Exception as e:
                self.update_status(f"Error: {str(e)}", "red")
                messagebox.showerror("Error", f"Failed to update data: {str(e)}")
            finally:
                self.stop_progress()
        
        threading.Thread(target=update_thread, daemon=True).start()
        
    def run_analysis(self):
        def analysis_thread():
            try:
                self.start_progress()
                self.update_status("Running advanced analysis (1 year + 1 month data)...", "blue")
                
                # Cargar datos actuales
                cryptos = [c.strip() for c in self.crypto_entry.get().split(',')]
                stocks = [s.strip() for s in self.stock_entry.get().split(',')]
                
                current_data = self.data_collector.update_all_data(cryptos, stocks)
                
                if not current_data:
                    self.results_text.delete(1.0, tk.END)
                    self.results_text.insert(tk.END, "❌ No data found!\n")
                    self.results_text.insert(tk.END, "Please click 'Update Data' first.\n")
                    self.update_status("No data available", "orange")
                    self.stop_progress()
                    return
                
                # Ejecutar análisis avanzado
                results = self.ai_analyzer.analyze_market()
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "🧠 ADVANCED MARKET ANALYSIS (1 Year + 1 Month Data)\n")
                self.results_text.insert(tk.END, "="*60 + "\n\n")
                
                # Resumen general
                total_assets = len(results)
                bullish_count = sum(1 for r in results.values() if 'BULLISH' in r['trend'])
                bearish_count = sum(1 for r in results.values() if 'BEARISH' in r['trend'])
                neutral_count = total_assets - bullish_count - bearish_count
                avg_confidence = sum(r['confidence'] for r in results.values()) / total_assets if total_assets > 0 else 0
                
                self.results_text.insert(tk.END, "📊 ANALYSIS SUMMARY\n")
                self.results_text.insert(tk.END, f"Total Assets Analyzed: {total_assets}\n")
                self.results_text.insert(tk.END, f"🟢 Bullish: {bullish_count} | 🔴 Bearish: {bearish_count} | 🟡 Neutral: {neutral_count}\n")
                self.results_text.insert(tk.END, f"Average Confidence: {avg_confidence:.1f}%\n")
                self.results_text.insert(tk.END, f"Analysis Depth: 1 Year + 1 Month Historical Data\n")
                self.results_text.insert(tk.END, "-"*50 + "\n\n")
                
                # Análisis detallado
                for asset, analysis in results.items():
                    trend_emoji = "🟢" if 'BULLISH' in analysis['trend'] else "🔴" if 'BEARISH' in analysis['trend'] else "🟡"
                    
                    self.results_text.insert(tk.END, f"{trend_emoji} {asset.upper()}\n")
                    self.results_text.insert(tk.END, f"   Final Trend: {analysis['trend']}\n")
                    self.results_text.insert(tk.END, f"   Annual Trend: {analysis.get('annual_trend', 'N/A')}\n")
                    self.results_text.insert(tk.END, f"   Monthly Trend: {analysis.get('monthly_trend', 'N/A')}\n")
                    self.results_text.insert(tk.END, f"   Confidence: {analysis['confidence']}%\n")
                    self.results_text.insert(tk.END, f"   Volatility: {analysis['volatility']}\n")
                    self.results_text.insert(tk.END, f"   Current: ${analysis['current_price']:.4f}\n")
                    self.results_text.insert(tk.END, f"   Predicted: ${analysis['predicted_price']:.4f} ({analysis['price_change_pct']:+.2f}%)\n")
                    
                    # Métricas anuales si existen
                    if 'annual_metrics' in analysis and analysis['annual_metrics']:
                        self.results_text.insert(tk.END, f"   Annual Metrics:\n")
                        for metric, value in analysis['annual_metrics'].items():
                            self.results_text.insert(tk.END, f"     {metric}: {value}\n")
                    
                    # Métricas mensuales si existen
                    if 'monthly_metrics' in analysis and analysis['monthly_metrics']:
                        self.results_text.insert(tk.END, f"   Monthly Metrics:\n")
                        for metric, value in analysis['monthly_metrics'].items():
                            self.results_text.insert(tk.END, f"     {metric}: {value}\n")
                    
                    self.results_text.insert(tk.END, f"   Patterns: {analysis['indicators']}\n")
                    self.results_text.insert(tk.END, f"   Risk/Reward: {analysis.get('risk_reward_ratio', 'N/A')}\n")
                    
                    # NUEVOS INDICADORES AVANZADOS
                    self.results_text.insert(tk.END, f"   🚀 Advanced Indicators:\n")
                    self.results_text.insert(tk.END, f"     Volume Trend: {analysis.get('volume_trend', 'N/A')}\n")
                    self.results_text.insert(tk.END, f"     Distance to SMA200: {analysis.get('distance_to_sma200_pct', 0):.2f}%\n")
                    self.results_text.insert(tk.END, f"     Invalidation Level: ${analysis.get('invalidation_level', 0):.4f}\n")
                    self.results_text.insert(tk.END, f"     Invalidation Distance: {analysis.get('invalidation_distance_pct', 0):.2f}%\n")
                    
                    # Interpretación de los nuevos indicadores
                    volume_trend = analysis.get('volume_trend', 'NEUTRAL')
                    if volume_trend == 'BULLISH_CONFIRMED':
                        self.results_text.insert(tk.END, f"     ✅ Volume confirms price increase (REAL MOVE)\n")
                    elif volume_trend == 'BULLISH_WEAK':
                        self.results_text.insert(tk.END, f"     ⚠️ Price rising WITHOUT volume (TRAP WARNING)\n")
                    elif volume_trend == 'BEARISH_CONFIRMED':
                        self.results_text.insert(tk.END, f"     ✅ Volume confirms price decrease (REAL MOVE)\n")
                    elif volume_trend == 'BEARISH_WEAK':
                        self.results_text.insert(tk.END, f"     ⚠️ Price falling WITHOUT volume (WEAK SIGNAL)\n")
                    
                    distance_sma200 = analysis.get('distance_to_sma200_pct', 0)
                    if distance_sma200 > 15:
                        self.results_text.insert(tk.END, f"     🚨 HIGH RISK: {distance_sma200:.1f}% above SMA200 (OVEREXTENDED)\n")
                    elif distance_sma200 < -15:
                        self.results_text.insert(tk.END, f"     🟢 OPPORTUNITY: {abs(distance_sma200):.1f}% below SMA200 (OVERSOLD)\n")
                    
                    # NUEVO: ATR y Stop Loss dinámico
                    atr = analysis.get('atr', 0)
                    atr_pct = analysis.get('atr_pct', 0)
                    dynamic_stop = analysis.get('dynamic_stop_loss', 0)
                    
                    self.results_text.insert(tk.END, f"     📊 ATR: ${atr:.6f} ({atr_pct:.2f}%)\n")
                    self.results_text.insert(tk.END, f"     🛡️ Dynamic Stop Loss: ${dynamic_stop:.4f}\n")
                    self.results_text.insert(tk.END, f"     📏 Stop Distance: {((analysis['current_price'] - dynamic_stop) / analysis['current_price']) * 100:.2f}%\n")
                    
                    self.results_text.insert(tk.END, "-"*50 + "\n\n")
                
                self.update_status("Advanced analysis completed!", "green")
                
            except Exception as e:
                self.update_status(f"Error: {str(e)}", "red")
                messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            finally:
                self.stop_progress()
        
        threading.Thread(target=analysis_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = CryptoStockAnalyzerPro(root)
    root.mainloop()

if __name__ == "__main__":
    main()