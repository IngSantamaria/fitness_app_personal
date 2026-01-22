import sqlite3
import json
import os
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.db_dir, exist_ok=True)
        
        self.db_path = os.path.join(self.db_dir, 'trading_data.db')
        
        # Inicializar base de datos
        self.init_database()
        
    def init_database(self):
        """Inicializar tablas de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de datos de mercado
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    current_price REAL,
                    volume_24h REAL,
                    change_24h REAL,
                    high_24h REAL,
                    low_24h REAL,
                    indicators TEXT,
                    raw_data TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de análisis de IA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    trend TEXT,
                    confidence REAL,
                    volatility TEXT,
                    indicators TEXT,
                    predicted_price REAL,
                    current_price REAL,
                    price_change_pct REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de recomendaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    action TEXT,
                    reason TEXT,
                    risk_level TEXT,
                    confidence REAL,
                    target_price REAL,
                    stop_loss REAL,
                    predicted_change REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de trades ejecutados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    action TEXT NOT NULL,
                    quantity REAL,
                    price REAL,
                    timestamp DATETIME NOT NULL,
                    profit_loss REAL,
                    status TEXT DEFAULT 'OPEN',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de portfolio
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    quantity REAL,
                    average_price REAL,
                    current_price REAL,
                    total_value REAL,
                    profit_loss REAL,
                    profit_loss_pct REAL,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol)
                )
            ''')
            
            # Crear índices
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_market_data_symbol ON market_data(symbol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_market_data_timestamp ON market_data(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ai_analysis_symbol ON ai_analysis(symbol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_recommendations_symbol ON recommendations(symbol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol)')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            
    def save_market_data(self, symbol, asset_type, data):
        """Guardar datos de mercado"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO market_data 
                (symbol, asset_type, timestamp, current_price, volume_24h, change_24h, 
                 high_24h, low_24h, indicators, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                asset_type,
                datetime.now(),
                data.get('current_price'),
                data.get('volume_24h'),
                data.get('change_24h'),
                data.get('high_24h'),
                data.get('low_24h'),
                json.dumps(data.get('indicators', {})),
                json.dumps(data)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving market data: {e}")
            
    def save_ai_analysis(self, symbol, analysis):
        """Guardar análisis de IA"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ai_analysis 
                (symbol, timestamp, trend, confidence, volatility, indicators,
                 predicted_price, current_price, price_change_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                datetime.now(),
                analysis.get('trend'),
                analysis.get('confidence'),
                analysis.get('volatility'),
                analysis.get('indicators'),
                analysis.get('predicted_price'),
                analysis.get('current_price'),
                analysis.get('price_change_pct')
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving AI analysis: {e}")
            
    def save_recommendation(self, symbol, recommendation):
        """Guardar recomendación"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO recommendations 
                (symbol, timestamp, action, reason, risk_level, confidence,
                 target_price, stop_loss, predicted_change)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                datetime.now(),
                recommendation.get('action'),
                recommendation.get('reason'),
                recommendation.get('risk_level'),
                recommendation.get('confidence'),
                recommendation.get('target_price'),
                recommendation.get('stop_loss'),
                recommendation.get('predicted_change')
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving recommendation: {e}")
            
    def get_latest_market_data(self, symbol=None, limit=100):
        """Obtener datos de mercado más recientes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if symbol:
                cursor.execute('''
                    SELECT * FROM market_data 
                    WHERE symbol = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (symbol, limit))
            else:
                cursor.execute('''
                    SELECT * FROM market_data 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convertir a diccionarios
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in rows:
                data_dict = dict(zip(columns, row))
                # Parsear JSON
                if data_dict.get('indicators'):
                    data_dict['indicators'] = json.loads(data_dict['indicators'])
                if data_dict.get('raw_data'):
                    data_dict['raw_data'] = json.loads(data_dict['raw_data'])
                results.append(data_dict)
                
            return results
            
        except Exception as e:
            print(f"Error getting market data: {e}")
            return []
            
    def get_portfolio_summary(self):
        """Obtener resumen del portfolio"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT symbol, quantity, average_price, current_price, 
                       total_value, profit_loss, profit_loss_pct
                FROM portfolio
                ORDER BY total_value DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            columns = [desc[0] for desc in cursor.description]
            portfolio = [dict(zip(columns, row)) for row in rows]
            
            # Calcular totales
            total_value = sum(item['total_value'] for item in portfolio if item['total_value'])
            total_pnl = sum(item['profit_loss'] for item in portfolio if item['profit_loss'])
            
            return {
                'positions': portfolio,
                'total_value': total_value,
                'total_profit_loss': total_pnl,
                'position_count': len(portfolio)
            }
            
        except Exception as e:
            print(f"Error getting portfolio summary: {e}")
            return {'positions': [], 'total_value': 0, 'total_profit_loss': 0, 'position_count': 0}
            
    def update_portfolio(self, symbol, quantity, price, action):
        """Actualizar portfolio después de un trade"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if action == 'BUY':
                # Verificar si ya existe posición
                cursor.execute('SELECT quantity, average_price FROM portfolio WHERE symbol = ?', (symbol,))
                existing = cursor.fetchone()
                
                if existing:
                    # Actualizar posición existente
                    old_quantity, old_avg_price = existing
                    new_quantity = old_quantity + quantity
                    new_avg_price = ((old_quantity * old_avg_price) + (quantity * price)) / new_quantity
                    
                    cursor.execute('''
                        UPDATE portfolio 
                        SET quantity = ?, average_price = ?, current_price = ?,
                            total_value = quantity * current_price,
                            last_updated = ?
                        WHERE symbol = ?
                    ''', (new_quantity, new_avg_price, price, datetime.now(), symbol))
                else:
                    # Nueva posición
                    cursor.execute('''
                        INSERT INTO portfolio 
                        (symbol, quantity, average_price, current_price, total_value)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (symbol, quantity, price, price, quantity * price))
                    
            elif action == 'SELL':
                # Reducir o eliminar posición
                cursor.execute('SELECT quantity FROM portfolio WHERE symbol = ?', (symbol,))
                existing = cursor.fetchone()
                
                if existing:
                    old_quantity = existing[0]
                    new_quantity = old_quantity - quantity
                    
                    if new_quantity <= 0:
                        # Eliminar posición
                        cursor.execute('DELETE FROM portfolio WHERE symbol = ?', (symbol,))
                    else:
                        # Actualizar cantidad
                        cursor.execute('''
                            UPDATE portfolio 
                            SET quantity = ?, last_updated = ?
                            WHERE symbol = ?
                        ''', (new_quantity, datetime.now(), symbol))
                        
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating portfolio: {e}")
            
    def get_performance_metrics(self, days=30):
        """Obtener métricas de rendimiento"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener trades del período
            since_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT COUNT(*) as total_trades,
                       SUM(CASE WHEN action = 'BUY' THEN 1 ELSE 0 END) as buys,
                       SUM(CASE WHEN action = 'SELL' THEN 1 ELSE 0 END) as sells,
                       SUM(profit_loss) as total_pnl
                FROM trades 
                WHERE timestamp >= ?
            ''', (since_date,))
            
            trade_metrics = cursor.fetchone()
            
            # Obtener recomendaciones del período
            cursor.execute('''
                SELECT COUNT(*) as total_recommendations,
                       SUM(CASE WHEN action = 'BUY' THEN 1 ELSE 0 END) as buy_recs,
                       SUM(CASE WHEN action = 'SELL' THEN 1 ELSE 0 END) as sell_recs,
                       AVG(confidence) as avg_confidence
                FROM recommendations 
                WHERE timestamp >= ?
            ''', (since_date,))
            
            rec_metrics = cursor.fetchone()
            
            conn.close()
            
            return {
                'period_days': days,
                'trades': {
                    'total': trade_metrics[0] or 0,
                    'buys': trade_metrics[1] or 0,
                    'sells': trade_metrics[2] or 0,
                    'total_pnl': trade_metrics[3] or 0
                },
                'recommendations': {
                    'total': rec_metrics[0] or 0,
                    'buy_signals': rec_metrics[1] or 0,
                    'sell_signals': rec_metrics[2] or 0,
                    'avg_confidence': rec_metrics[3] or 0
                }
            }
            
        except Exception as e:
            print(f"Error getting performance metrics: {e}")
            return {'period_days': days, 'trades': {}, 'recommendations': {}}