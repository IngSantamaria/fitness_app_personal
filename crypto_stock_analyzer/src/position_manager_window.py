import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading

class PositionManagerWindow:
    """Ventana de gestión de posiciones con sistema de señales avanzado"""
    
    def __init__(self, parent, position_manager, data_collector, ai_analyzer):
        self.parent = parent
        self.position_manager = position_manager
        self.data_collector = data_collector
        self.ai_analyzer = ai_analyzer
        
        self.window = tk.Toplevel(parent)
        self.window.title("📊 Position Manager & Trading Signals")
        self.window.geometry("1200x800")
        self.window.resizable(True, True)
        
        # Centrar la ventana
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.refresh_positions()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Panel de control superior
        control_frame = ttk.LabelFrame(main_frame, text="⚙️ Position Controls", padding="10")
        control_frame.pack(fill='x', pady=(0, 10))
        
        # Botones de acción
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="➕ Add Position", 
                   command=self.add_position_dialog).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔄 Refresh Positions", 
                   command=self.refresh_positions).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📈 Update Signals", 
                   command=self.update_signals).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📊 Position Summary", 
                   command=self.show_summary).pack(side='left', padx=5)
        
        # Notebook para diferentes vistas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: Active Positions
        active_frame = ttk.Frame(notebook)
        notebook.add(active_frame, text="🟢 Active Positions")
        
        # Treeview para posiciones activas
        columns = ('Symbol', 'Type', 'Entry Price', 'Current Price', 'Signal', 'P&L', 'P&L%', 'ATR Stop Loss')
        self.active_tree = ttk.Treeview(active_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.active_tree.heading(col, text=col)
            if col == 'Symbol':
                self.active_tree.column(col, width=80)
            elif col == 'Type':
                self.active_tree.column(col, width=60)
            elif col in ['Entry Price', 'Current Price', 'ATR Stop Loss']:
                self.active_tree.column(col, width=100)
            elif col == 'Signal':
                self.active_tree.column(col, width=120)
            else:
                self.active_tree.column(col, width=80)
        
        active_scroll = ttk.Scrollbar(active_frame, orient=tk.VERTICAL, command=self.active_tree.yview)
        self.active_tree.configure(yscrollcommand=active_scroll.set)
        
        self.active_tree.pack(side='left', fill='both', expand=True)
        active_scroll.pack(side='right', fill='y')
        
        # Menu contextual para acciones en posiciones
        self.setup_context_menu()
        
        # Tab 2: Signal Interpretation Guide
        signals_frame = ttk.Frame(notebook)
        notebook.add(signals_frame, text="📚 Signal Guide")
        
        self.setup_signals_guide(signals_frame)
        
        # Tab 3: Closed Positions
        closed_frame = ttk.Frame(notebook)
        notebook.add(closed_frame, text="🔴 Closed Positions")
        
        # Treeview para posiciones cerradas
        closed_columns = ('Symbol', 'Type', 'Entry Price', 'Close Price', 'P&L', 'P&L%', 'Close Reason', 'Duration')
        self.closed_tree = ttk.Treeview(closed_frame, columns=closed_columns, show='headings', height=15)
        
        for col in closed_columns:
            self.closed_tree.heading(col, text=col)
            if col == 'Symbol':
                self.closed_tree.column(col, width=80)
            elif col == 'Type':
                self.closed_tree.column(col, width=60)
            elif col in ['Entry Price', 'Close Price']:
                self.closed_tree.column(col, width=100)
            elif col == 'Close Reason':
                self.closed_tree.column(col, width=120)
            elif col == 'Duration':
                self.closed_tree.column(col, width=80)
            else:
                self.closed_tree.column(col, width=80)
        
        closed_scroll = ttk.Scrollbar(closed_frame, orient=tk.VERTICAL, command=self.closed_tree.yview)
        self.closed_tree.configure(yscrollcommand=closed_scroll.set)
        
        self.closed_tree.pack(side='left', fill='both', expand=True)
        closed_scroll.pack(side='right', fill='y')
        
        # Panel de estado
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Position Manager Ready", foreground="green")
        self.status_label.pack(side='left')
        
    def setup_context_menu(self):
        """Configurar menú contextual para posiciones"""
        self.context_menu = tk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="📊 View Details", command=self.view_position_details)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✏️ Edit Position", command=self.edit_position)
        self.context_menu.add_command(label="❌ Close Position", command=self.close_position_dialog)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Delete Position", command=self.delete_position)
        
        self.active_tree.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        """Mostrar menú contextual"""
        item = self.active_tree.selection()
        if item:
            self.context_menu.post(event.x_root, event.y_root)
    
    def setup_signals_guide(self, parent):
        """Configurar guía de señales"""
        guide_frame = ttk.Frame(parent, padding="20")
        guide_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(guide_frame, text="📚 Trading Signals Guide", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Crear frame para las señales
        signals_container = ttk.Frame(guide_frame)
        signals_container.pack(fill='both', expand=True)
        
        # Scrollbar para la guía
        canvas = tk.Canvas(signals_container)
        scrollbar = ttk.Scrollbar(signals_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la guía
        signals_info = [
            {
                'signal': '🎯 ENTRY ZONE',
                'condition': 'Precio Actual ≈ Precio Compra (±2%)',
                'action': 'ENTRAR o AUMENTAR POSICIÓN',
                'description': 'El precio está cerca de tu punto de entrada ideal. Es una buena oportunidad para abrir nueva posición o aumentar la existente.',
                'color': 'green'
            },
            {
                'signal': '⏳ WAIT FOR DIP',
                'condition': 'Precio Actual > Precio Compra + 2%',
                'action': 'ESPERAR RETROCESO',
                'description': 'El precio ya subió más del 2% desde tu entrada. No compres ahora - espera un retroceso para mejor entrada.',
                'color': 'orange'
            },
            {
                'signal': '💰 TAKE PROFIT',
                'condition': 'Ganancias > 5%',
                'action': 'TOMAR GANANCIAS',
                'description': 'Tienes ganancias significativas (+5% o más). Considera tomar ganancias parciales o totales para asegurar beneficios.',
                'color': 'blue'
            },
            {
                'signal': '📊 HOLDING',
                'condition': 'Posición estable',
                'action': 'MANTENER',
                'description': 'La posición está estable sin señales claras. Continúa manteniendo y monitoreando.',
                'color': 'gray'
            },
            {
                'signal': '⚠️ STOP LOSS WARNING',
                'condition': 'Pérdidas > 2%',
                'action': 'REVISAR POSICIÓN',
                'description': 'Estás con pérdidas de más del 2%. Considera cerrar la posición o ajustar el stop loss para limitar pérdidas.',
                'color': 'red'
            },
            {
                'signal': '⏳ WAIT FOR RALLY',
                'condition': 'Posición corta con ganancias',
                'action': 'ESPERAR RALLY',
                'description': 'Tienes una posición corta con buenas ganancias. Espera un rally para cubrirla con mayor beneficio.',
                'color': 'orange'
            }
        ]
        
        row = 0
        for signal_info in signals_info:
            # Frame para cada señal
            signal_frame = ttk.LabelFrame(scrollable_frame, text="", padding="15")
            signal_frame.grid(row=row, column=0, sticky='ew', padx=10, pady=5)
            scrollable_frame.columnconfigure(0, weight=1)
            
            # Signal title
            signal_title = ttk.Label(signal_frame, text=signal_info['signal'], 
                                   font=('Arial', 12, 'bold'))
            signal_title.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
            
            # Condition
            ttk.Label(signal_frame, text="Condición:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w')
            ttk.Label(signal_frame, text=signal_info['condition']).grid(row=1, column=1, sticky='w', padx=(10, 0))
            
            # Action
            ttk.Label(signal_frame, text="Acción:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w')
            ttk.Label(signal_frame, text=signal_info['action']).grid(row=2, column=1, sticky='w', padx=(10, 0))
            
            # Description
            ttk.Label(signal_frame, text="Descripción:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='nw', pady=(5, 0))
            
            desc_text = tk.Text(signal_frame, height=3, width=60, wrap=tk.WORD)
            desc_text.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=(5, 0))
            desc_text.insert('1.0', signal_info['description'])
            desc_text.config(state='disabled')
            
            row += 1
        
        # ATR Information
        atr_frame = ttk.LabelFrame(scrollable_frame, text="🛡️ ATR Dynamic Stop Loss", padding="15")
        atr_frame.grid(row=row, column=0, sticky='ew', padx=10, pady=(20, 5))
        scrollable_frame.columnconfigure(0, weight=1)
        
        atr_info = """
        📊 FÓRMULA: Stop Loss = Precio Entrada - (2 * ATR)
        
        🔹 ATR (Average True Range): Mide la volatilidad actual del mercado
        🔹 Stop Loss Dinámico: Se ajusta automáticamente a la volatilidad
        🔹 Mayor volatilidad = Stop Loss más lejano
        🔹 Menor volatilidad = Stop Loss más cercano
        
        💡 Ventajas sobre stops fijos:
        • Se adapta a las condiciones del mercado
        • Evita salidas prematuras en alta volatilidad
        • Protege mejor en baja volatilidad
        • Basado en datos reales de movimiento del precio
        """
        
        atr_text = tk.Text(atr_frame, height=10, width=70, wrap=tk.WORD)
        atr_text.pack(fill='both', expand=True)
        atr_text.insert('1.0', atr_info)
        atr_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_position_dialog(self):
        """Diálogo para agregar nueva posición"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Add New Position")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        
        # Centrar el diálogo
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Campos
        ttk.Label(dialog, text="Symbol:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        symbol_entry = ttk.Entry(dialog, width=30)
        symbol_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Position Type:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        type_var = tk.StringVar(value="LONG")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, values=["LONG", "SHORT"], width=28)
        type_combo.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Entry Price:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_price_entry = ttk.Entry(dialog, width=30)
        entry_price_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Quantity:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        quantity_entry = ttk.Entry(dialog, width=30)
        quantity_entry.insert(0, "1")
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Take Profit Price:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        take_profit_entry = ttk.Entry(dialog, width=30)
        take_profit_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Notes:").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
        notes_text = tk.Text(dialog, width=30, height=4)
        notes_text.grid(row=5, column=1, padx=10, pady=5)
        
        def save_position():
            try:
                symbol = symbol_entry.get().strip().upper()
                position_type = type_var.get().upper()
                entry_price = float(entry_price.get())
                quantity = float(quantity_entry.get())
                take_profit = float(take_profit_entry.get()) if take_profit_entry.get().strip() else None
                notes = notes_text.get('1.0', 'end-1c').strip()
                
                if symbol and entry_price > 0 and quantity > 0:
                    position = self.position_manager.add_position(
                        symbol, entry_price, position_type, quantity, take_profit, notes
                    )
                    dialog.destroy()
                    self.refresh_positions()
                    messagebox.showinfo("Success", f"Added {position_type} position for {symbol}!")
                else:
                    messagebox.showerror("Error", "Please fill all required fields correctly")
            except ValueError:
                messagebox.showerror("Error", "Invalid price or quantity format")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add position: {str(e)}")
        
        # Botones
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_position).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def refresh_positions(self):
        """Refrescar display de posiciones"""
        def refresh_thread():
            try:
                self.update_status("Refreshing positions...", "blue")
                
                # Limpiar treeviews
                for item in self.active_tree.get_children():
                    self.active_tree.delete(item)
                for item in self.closed_tree.get_children():
                    self.closed_tree.delete(item)
                
                # Cargar posiciones activas
                active_positions = self.position_manager.get_active_positions()
                
                for symbol, positions in active_positions.items():
                    for position in positions:
                        signal = position.get('current_signal', 'UNKNOWN')
                        signal_interp = self.position_manager.get_signals_interpretation(signal)
                        
                        self.active_tree.insert('', 'end', values=(
                            symbol,
                            position.get('position_type', 'LONG'),
                            f"${position.get('entry_price', 0):.4f}",
                            f"${position.get('current_price', 0):.4f}",
                            f"{signal_interp['emoji']} {signal}",
                            f"${position.get('pnl', 0):.2f}",
                            f"{position.get('pnl_pct', 0):.2f}%",
                            f"${position.get('atr_stop_loss', 0):.4f}"
                        ), tags=(position.get('pnl', 0) >= 0 and 'profit' or 'loss',))
                
                # Configurar colores para P&L
                self.active_tree.tag_configure('profit', foreground='green')
                self.active_tree.tag_configure('loss', foreground='red')
                
                # Cargar posiciones cerradas
                all_positions = self.position_manager.positions
                for symbol, positions in all_positions.items():
                    for position in positions:
                        if position.get('status', '').startswith('CLOSED'):
                            # Calcular duración
                            try:
                                from datetime import datetime
                                entry_date = datetime.fromisoformat(position.get('entry_date', ''))
                                close_date = datetime.fromisoformat(position.get('close_date', ''))
                                duration = (close_date - entry_date).days
                            except:
                                duration = 0
                            
                            final_pnl = position.get('final_pnl', position.get('pnl', 0))
                            final_pnl_pct = position.get('final_pnl_pct', position.get('pnl_pct', 0))
                            
                            self.closed_tree.insert('', 'end', values=(
                                symbol,
                                position.get('position_type', 'LONG'),
                                f"${position.get('entry_price', 0):.4f}",
                                f"${position.get('close_price', 0):.4f}",
                                f"${final_pnl:.2f}",
                                f"{final_pnl_pct:.2f}%",
                                position.get('close_reason', 'Unknown'),
                                f"{duration} days"
                            ), tags=(final_pnl >= 0 and 'profit' or 'loss'))
                
                # Configurar colores para P&L cerradas
                self.closed_tree.tag_configure('profit', foreground='green')
                self.closed_tree.tag_configure('loss', foreground='red')
                
                self.update_status("Positions refreshed successfully", "green")
                
            except Exception as e:
                self.update_status(f"Error refreshing positions: {str(e)}", "red")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def update_signals(self):
        """Actualizar señales basadas en datos actuales del mercado"""
        def update_thread():
            try:
                self.update_status("Updating trading signals...", "blue")
                
                # Cargar datos actuales del mercado
                cryptos = ['BTC', 'ETH', 'ADA']  # Puedes hacer esto configurable
                stocks = ['AAPL', 'GOOGL', 'TSLA']
                
                # Obtener datos y análisis
                current_data = self.data_collector.update_all_data(cryptos, stocks)
                analysis_results = self.ai_analyzer.analyze_market()
                
                # Actualizar señales para cada posición activa
                active_positions = self.position_manager.get_active_positions()
                
                for symbol, positions in active_positions.items():
                    # Buscar datos del símbolo
                    symbol_data = None
                    symbol_analysis = None
                    
                    for key, data in current_data.items():
                        if symbol.lower() in key.lower():
                            symbol_data = data
                            break
                    
                    for key, analysis in analysis_results.items():
                        if symbol.lower() in key.lower():
                            symbol_analysis = analysis
                            break
                    
                    if symbol_data and symbol_analysis:
                        current_price = symbol_data.get('current_price', 0)
                        if current_price > 0:
                            self.position_manager.update_position_signals(
                                symbol, current_price, symbol_analysis
                            )
                
                # Refrescar display
                self.refresh_positions()
                self.update_status("Trading signals updated successfully!", "green")
                
            except Exception as e:
                self.update_status(f"Error updating signals: {str(e)}", "red")
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def show_summary(self):
        """Mostrar resumen de posiciones"""
        summary = self.position_manager.get_position_summary()
        
        summary_window = tk.Toplevel(self.window)
        summary_window.title("📊 Position Summary")
        summary_window.geometry("500x400")
        summary_window.resizable(False, False)
        
        # Centrar ventana
        summary_window.transient(self.window)
        summary_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(summary_window, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(main_frame, text="📊 Position Summary", 
                font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Estadísticas generales
        stats_frame = ttk.LabelFrame(main_frame, text="📈 General Statistics", padding="10")
        stats_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(stats_frame, text=f"Total Positions: {summary['total_positions']}").pack(anchor='w')
        ttk.Label(stats_frame, text=f"Active Positions: {summary['active_positions']}").pack(anchor='w')
        ttk.Label(stats_frame, text=f"Closed Positions: {summary['closed_positions']}").pack(anchor='w')
        ttk.Label(stats_frame, text=f"Win Rate: {summary['win_rate']:.1f}%").pack(anchor='w')
        
        # Finanzas
        pnl_frame = ttk.LabelFrame(main_frame, text="💰 Financial Summary", padding="10")
        pnl_frame.pack(fill='x', pady=(0, 10))
        
        total_color = 'green' if summary['total_pnl'] >= 0 else 'red'
        ttk.Label(pnl_frame, text=f"Total P&L: ${summary['total_pnl']:.2f}", 
                 foreground=total_color).pack(anchor='w')
        ttk.Label(pnl_frame, text=f"Active P&L: ${summary['active_pnl']:.2f}").pack(anchor='w')
        ttk.Label(pnl_frame, text=f"Closed P&L: ${summary['closed_pnl']:.2f}").pack(anchor='w')
        
        # Señales actuales
        signals_frame = ttk.LabelFrame(main_frame, text="📊 Current Signals", padding="10")
        signals_frame.pack(fill='x', pady=(0, 10))
        
        for signal, count in summary['signals_summary'].items():
            if count > 0:
                signal_interp = self.position_manager.get_signals_interpretation(signal)
                ttk.Label(signals_frame, 
                         text=f"{signal_interp['emoji']} {signal}: {count} positions").pack(anchor='w')
        
        # Botón cerrar
        ttk.Button(main_frame, text="Close", 
                  command=summary_window.destroy).pack(pady=20)
    
    def view_position_details(self):
        """Ver detalles de posición seleccionada"""
        selection = self.active_tree.selection()
        if not selection:
            return
        
        # Obtener datos de la posición seleccionada
        item = self.active_tree.item(selection[0])
        values = item['values']
        
        symbol = values[0]
        
        # Encontrar la posición completa
        active_positions = self.position_manager.get_active_positions()
        position = None
        if symbol in active_positions:
            for pos in active_positions[symbol]:
                if float(pos.get('entry_price', 0)) == float(values[2].replace('$', '')):
                    position = pos
                    break
        
        if position:
            self.show_position_details_dialog(position)
    
    def edit_position(self):
        """Editar posición seleccionada"""
        messagebox.showinfo("Info", "Edit position feature coming soon!")
    
    def close_position_dialog(self):
        """Diálogo para cerrar posición"""
        selection = self.active_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a position to close")
            return
        
        item = self.active_tree.item(selection[0])
        values = item['values']
        
        symbol = values[0]
        
        # Encontrar la posición completa
        active_positions = self.position_manager.get_active_positions()
        position = None
        if symbol in active_positions:
            for pos in active_positions[symbol]:
                if float(pos.get('entry_price', 0)) == float(values[2].replace('$', '')):
                    position = pos
                    break
        
        if position:
            # Confirmar cierre
            result = messagebox.askyesno(
                "Close Position", 
                f"Close {position.get('position_type')} position for {symbol}?\n\n"
                f"Entry: ${position.get('entry_price', 0):.4f}\n"
                f"Current: ${position.get('current_price', 0):.4f}\n"
                f"P&L: ${position.get('pnl', 0):.2f} ({position.get('pnl_pct', 0):.2f}%)\n\n"
                f"This action cannot be undone."
            )
            
            if result:
                success = self.position_manager.close_position(
                    symbol, position['id'], 
                    position.get('current_price'), 
                    'MANUAL'
                )
                
                if success:
                    self.refresh_positions()
                    messagebox.showinfo("Success", f"Position for {symbol} closed successfully!")
                else:
                    messagebox.showerror("Error", "Failed to close position")
    
    def delete_position(self):
        """Eliminar posición seleccionada"""
        selection = self.active_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a position to delete")
            return
        
        item = self.active_tree.item(selection[0])
        values = item['values']
        
        symbol = values[0]
        
        # Encontrar la posición completa
        active_positions = self.position_manager.get_active_positions()
        position = None
        if symbol in active_positions:
            for pos in active_positions[symbol]:
                if float(pos.get('entry_price', 0)) == float(values[2].replace('$', '')):
                    position = pos
                    break
        
        if position:
            result = messagebox.askyesno(
                "Delete Position", 
                f"Delete {position.get('position_type')} position for {symbol}?\n\n"
                f"Entry: ${position.get('entry_price', 0):.4f}\n"
                f"Current: ${position.get('current_price', 0):.4f}\n"
                f"P&L: ${position.get('pnl', 0):.2f}\n\n"
                f"⚠️ This will permanently delete the position record!"
            )
            
            if result:
                success = self.position_manager.delete_position(symbol, position['id'])
                
                if success:
                    self.refresh_positions()
                    messagebox.showinfo("Success", f"Position for {symbol} deleted successfully!")
                else:
                    messagebox.showerror("Error", "Failed to delete position")
    
    def show_position_details_dialog(self, position):
        """Mostrar diálogo con detalles completos de posición"""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Position Details - {position['symbol']}")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        
        # Centrar ventana
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(main_frame, text=f"📊 {position['symbol']} Position Details", 
                font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Información básica
        info_frame = ttk.LabelFrame(main_frame, text="📋 Position Information", padding="10")
        info_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Symbol: {position['symbol']}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Type: {position.get('position_type', 'LONG')}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Quantity: {position.get('quantity', 0)}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Status: {position.get('status', 'ACTIVE')}").pack(anchor='w')
        
        # Precios
        prices_frame = ttk.LabelFrame(main_frame, text="💰 Price Information", padding="10")
        prices_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(prices_frame, text=f"Entry Price: ${position.get('entry_price', 0):.4f}").pack(anchor='w')
        ttk.Label(prices_frame, text=f"Current Price: ${position.get('current_price', 0):.4f}").pack(anchor='w')
        
        if position.get('take_profit_price'):
            ttk.Label(prices_frame, text=f"Take Profit: ${position.get('take_profit_price', 0):.4f}").pack(anchor='w')
        
        if position.get('atr_stop_loss'):
            ttk.Label(prices_frame, text=f"ATR Stop Loss: ${position.get('atr_stop_loss', 0):.4f}").pack(anchor='w')
        
        # P&L
        pnl_frame = ttk.LabelFrame(main_frame, text="📈 Profit & Loss", padding="10")
        pnl_frame.pack(fill='x', pady=(0, 10))
        
        pnl_color = 'green' if position.get('pnl', 0) >= 0 else 'red'
        ttk.Label(pnl_frame, text=f"P&L: ${position.get('pnl', 0):.2f}", 
                 foreground=pnl_color).pack(anchor='w')
        ttk.Label(pnl_frame, text=f"P&L %: {position.get('pnl_pct', 0):.2f}%",
                 foreground=pnl_color).pack(anchor='w')
        
        # Señal actual
        signal = position.get('current_signal', 'UNKNOWN')
        signal_interp = self.position_manager.get_signals_interpretation(signal)
        
        signal_frame = ttk.LabelFrame(main_frame, text="🎯 Current Signal", padding="10")
        signal_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(signal_frame, text=f"{signal_interp['emoji']} {signal}", 
                 font=('Arial', 12, 'bold')).pack(anchor='w')
        ttk.Label(signal_frame, text=f"Action: {signal_interp['action']}", 
                 foreground=signal_interp['color']).pack(anchor='w')
        ttk.Label(signal_frame, text=signal_interp['description'], 
                 wraplength=400).pack(anchor='w', pady=(5, 0))
        
        # Notas
        if position.get('notes'):
            notes_frame = ttk.LabelFrame(main_frame, text="📝 Notes", padding="10")
            notes_frame.pack(fill='x', pady=(0, 10))
            
            ttk.Label(notes_frame, text=position.get('notes', ''), 
                     wraplength=400).pack(anchor='w')
        
        # Fechas
        dates_frame = ttk.LabelFrame(main_frame, text="📅 Dates", padding="10")
        dates_frame.pack(fill='x', pady=(0, 10))
        
        try:
            from datetime import datetime
            entry_date = datetime.fromisoformat(position.get('entry_date', ''))
            ttk.Label(dates_frame, text=f"Entry Date: {entry_date.strftime('%Y-%m-%d %H:%M')}").pack(anchor='w')
            ttk.Label(dates_frame, text=f"Last Updated: {position.get('last_updated', '')}").pack(anchor='w')
        except:
            pass
        
        # Botón cerrar
        ttk.Button(main_frame, text="Close", command=dialog.destroy).pack(pady=20)
    
    def update_status(self, message, color="black"):
        """Actualizar etiqueta de estado"""
        self.status_label.config(text=message, foreground=color)
        self.window.update_idletasks()