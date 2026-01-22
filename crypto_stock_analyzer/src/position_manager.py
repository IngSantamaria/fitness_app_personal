import json
import os
from datetime import datetime

class PositionManager:
    """Gestor de posiciones con sistema de señales avanzado"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.positions_file = os.path.join(self.data_dir, 'positions.json')
        self.load_positions()
    
    def load_positions(self):
        """Cargar posiciones guardadas"""
        try:
            if os.path.exists(self.positions_file):
                with open(self.positions_file, 'r') as f:
                    self.positions = json.load(f)
            else:
                self.positions = {}
        except Exception as e:
            print(f"Error loading positions: {e}")
            self.positions = {}
    
    def save_positions(self):
        """Guardar posiciones en archivo"""
        try:
            with open(self.positions_file, 'w') as f:
                json.dump(self.positions, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving positions: {e}")
    
    def add_position(self, symbol, entry_price, position_type='LONG', quantity=0, 
                    take_profit_price=None, notes=""):
        """Agregar nueva posición"""
        if symbol not in self.positions:
            self.positions[symbol] = []
        
        position = {
            'id': len(self.positions[symbol]) + 1,
            'symbol': symbol.upper(),
            'entry_price': entry_price,
            'position_type': position_type.upper(),  # LONG or SHORT
            'quantity': quantity,
            'take_profit_price': take_profit_price,
            'current_price': entry_price,
            'entry_date': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'status': 'ACTIVE',
            'notes': notes,
            'pnl': 0.0,
            'pnl_pct': 0.0,
            'current_signal': 'ENTRY_ZONE',
            'atr_stop_loss': 0.0,
            'original_stop_loss': 0.0
        }
        
        self.positions[symbol].append(position)
        self.save_positions()
        return position
    
    def update_position_signals(self, symbol, current_price, analysis_data):
        """Actualizar señales de trading para posiciones existentes"""
        if symbol not in self.positions:
            return
        
        symbol_positions = self.positions[symbol]
        
        for position in symbol_positions:
            if position['status'] != 'ACTIVE':
                continue
            
            entry_price = position['entry_price']
            
            # Calcular señales basadas en precio actual vs precio de entrada
            current_signal = self.calculate_trading_signal(current_price, entry_price, position['position_type'])
            
            # Calcular ATR stop loss si tenemos datos
            atr = analysis_data.get('atr', current_price * 0.02)
            atr_stop_loss = entry_price - (2 * atr) if position['position_type'] == 'LONG' else entry_price + (2 * atr)
            
            # Calcular P&L
            if position['position_type'] == 'LONG':
                pnl = (current_price - entry_price) * position['quantity']
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
            else:  # SHORT
                pnl = (entry_price - current_price) * position['quantity']
                pnl_pct = ((entry_price - current_price) / entry_price) * 100
            
            # Actualizar posición
            position.update({
                'current_price': current_price,
                'current_signal': current_signal,
                'atr_stop_loss': atr_stop_loss,
                'pnl': pnl,
                'pnl_pct': pnl_pct,
                'last_updated': datetime.now().isoformat()
            })
            
            # Verificar si se debe cerrar la posición
            if position['take_profit_price'] and position['position_type'] == 'LONG':
                if current_price >= position['take_profit_price']:
                    position['status'] = 'CLOSED_TP'
                    position['close_reason'] = 'TAKE_PROFIT_HIT'
                elif current_price <= atr_stop_loss:
                    position['status'] = 'CLOSED_SL'
                    position['close_reason'] = 'ATR_STOP_LOSS_HIT'
            elif position['take_profit_price'] and position['position_type'] == 'SHORT':
                if current_price <= position['take_profit_price']:
                    position['status'] = 'CLOSED_TP'
                    position['close_reason'] = 'TAKE_PROFIT_HIT'
                elif current_price >= atr_stop_loss:
                    position['status'] = 'CLOSED_SL'
                    position['close_reason'] = 'ATR_STOP_LOSS_HIT'
        
        self.save_positions()
    
    def calculate_trading_signal(self, current_price, entry_price, position_type='LONG'):
        """Calcular señal de trading basada en precio actual vs entrada"""
        
        if position_type == 'LONG':
            # Para posiciones largas
            price_change_pct = ((current_price - entry_price) / entry_price) * 100
            
            if current_price > entry_price * 1.02:  # Más de 2% arriba del precio de compra
                return 'WAIT_FOR_DIP'  # Esperar retroceso
            elif abs(current_price - entry_price) / entry_price <= 0.02:  # Dentro del 2% del precio de entrada
                return 'ENTRY_ZONE'  # Zona de entrada
            elif price_change_pct >= 5:  # Ganancia de 5% o más
                return 'TAKE_PROFIT'  # Tomar ganancias
            elif price_change_pct <= -2:  # Pérdida de 2% o más
                return 'STOP_LOSS_WARNING'  # Advertencia de stop loss
            else:
                return 'HOLDING'  # Mantener posición
                
        elif position_type == 'SHORT':
            # Para posiciones cortas (venta en corto)
            price_change_pct = ((entry_price - current_price) / entry_price) * 100
            
            if current_price < entry_price * 0.98:  # Más de 2% abajo del precio de venta
                return 'WAIT_FOR_RALLY'  # Esperar rally
            elif abs(current_price - entry_price) / entry_price <= 0.02:  # Dentro del 2% del precio de entrada
                return 'ENTRY_ZONE'  # Zona de entrada
            elif price_change_pct >= 5:  # Ganancia de 5% o más
                return 'TAKE_PROFIT'  # Tomar ganancias
            elif price_change_pct <= -2:  # Pérdida de 2% o más
                return 'STOP_LOSS_WARNING'  # Advertencia de stop loss
            else:
                return 'HOLDING'  # Mantener posición
        
        return 'UNKNOWN'
    
    def get_active_positions(self):
        """Obtener todas las posiciones activas"""
        active_positions = {}
        
        for symbol, positions in self.positions.items():
            active_positions[symbol] = [p for p in positions if p['status'] == 'ACTIVE']
        
        return active_positions
    
    def get_position_summary(self):
        """Obtener resumen de todas las posiciones"""
        summary = {
            'total_positions': 0,
            'active_positions': 0,
            'closed_positions': 0,
            'total_pnl': 0.0,
            'active_pnl': 0.0,
            'closed_pnl': 0.0,
            'win_rate': 0.0,
            'positions_by_symbol': {},
            'signals_summary': {
                'WAIT_FOR_DIP': 0,
                'ENTRY_ZONE': 0,
                'TAKE_PROFIT': 0,
                'HOLDING': 0,
                'STOP_LOSS_WARNING': 0
            }
        }
        
        total_closed = 0
        winning_trades = 0
        
        for symbol, positions in self.positions.items():
            symbol_summary = {
                'total': len(positions),
                'active': len([p for p in positions if p['status'] == 'ACTIVE']),
                'closed': len([p for p in positions if p['status'].startswith('CLOSED')]),
                'pnl': sum(p['pnl'] for p in positions)
            }
            
            summary['positions_by_symbol'][symbol] = symbol_summary
            summary['total_positions'] += len(positions)
            summary['active_positions'] += symbol_summary['active']
            summary['closed_positions'] += symbol_summary['closed']
            summary['total_pnl'] += symbol_summary['pnl']
            
            # Contar señales actuales
            for position in positions:
                if position['status'] == 'ACTIVE':
                    signal = position.get('current_signal', 'UNKNOWN')
                    if signal in summary['signals_summary']:
                        summary['signals_summary'][signal] += 1
                    summary['active_pnl'] += position['pnl']
                elif position['status'].startswith('CLOSED'):
                    total_closed += 1
                    summary['closed_pnl'] += position['pnl']
                    if position['pnl'] > 0:
                        winning_trades += 1
        
        # Calcular win rate
        if total_closed > 0:
            summary['win_rate'] = (winning_trades / total_closed) * 100
        
        return summary
    
    def close_position(self, symbol, position_id, close_price=None, reason='MANUAL'):
        """Cerrar una posición específica"""
        if symbol not in self.positions:
            return False
        
        for position in self.positions[symbol]:
            if position['id'] == position_id and position['status'] == 'ACTIVE':
                position['status'] = f'CLOSED_{reason.upper()}'
                position['close_price'] = close_price or position['current_price']
                position['close_date'] = datetime.now().isoformat()
                position['close_reason'] = reason
                
                # Recalcular P&L final
                if position['position_type'] == 'LONG':
                    pnl = (position['close_price'] - position['entry_price']) * position['quantity']
                    pnl_pct = ((position['close_price'] - position['entry_price']) / position['entry_price']) * 100
                else:  # SHORT
                    pnl = (position['entry_price'] - position['close_price']) * position['quantity']
                    pnl_pct = ((position['entry_price'] - position['close_price']) / position['entry_price']) * 100
                
                position['final_pnl'] = pnl
                position['final_pnl_pct'] = pnl_pct
                
                self.save_positions()
                return True
        
        return False
    
    def delete_position(self, symbol, position_id):
        """Eliminar una posición"""
        if symbol not in self.positions:
            return False
        
        self.positions[symbol] = [p for p in self.positions[symbol] if p['id'] != position_id]
        
        # Si no quedan posiciones para el símbolo, eliminar la entrada
        if not self.positions[symbol]:
            del self.positions[symbol]
        
        self.save_positions()
        return True
    
    def get_signals_interpretation(self, signal):
        """Obtener interpretación de la señal"""
        interpretations = {
            'WAIT_FOR_DIP': {
                'emoji': '⏳',
                'description': 'El precio está >2% arriba de tu entrada. Espera un retroceso para comprar más.',
                'action': 'ESPERAR - No comprar ahora',
                'color': 'orange'
            },
            'ENTRY_ZONE': {
                'emoji': '🎯',
                'description': 'El precio está cerca de tu entrada de compra. Buena zona para entrar.',
                'action': 'ENTRAR o AUMENTAR POSICIÓN',
                'color': 'green'
            },
            'TAKE_PROFIT': {
                'emoji': '💰',
                'description': 'Tienes ganancias de >5%. Considera tomar ganancias parciales o totales.',
                'action': 'TOMAR GANANCIAS',
                'color': 'blue'
            },
            'HOLDING': {
                'emoji': '📊',
                'description': 'Posición estable. Mantener y monitorear.',
                'action': 'MANTENER',
                'color': 'gray'
            },
            'STOP_LOSS_WARNING': {
                'emoji': '⚠️',
                'description': 'Pérdidas de >2%. Considera cerrar o ajustar stop loss.',
                'action': 'REVISAR POSICIÓN',
                'color': 'red'
            },
            'WAIT_FOR_RALLY': {
                'emoji': '⏳',
                'description': 'Posición corta con buenas ganancias. Espera rally para cubrir.',
                'action': 'ESPERAR - No cubrir ahora',
                'color': 'orange'
            }
        }
        
        return interpretations.get(signal, {
            'emoji': '❓',
            'description': 'Señal desconocida',
            'action': 'REVISAR',
            'color': 'black'
        })