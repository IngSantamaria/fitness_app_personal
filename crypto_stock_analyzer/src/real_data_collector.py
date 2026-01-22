import requests
import pandas as pd
import time
import json
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class RealDataCollector:
    """Colector de datos que usa APIs REST directamente sin dependencias problemáticas"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Headers para simular un navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Cargar configuración guardada
        self.config_file = os.path.join(self.data_dir, 'watchlist_config.json')
        self.load_watchlist_config()
    
    def load_watchlist_config(self):
        """Cargar configuración de watchlist guardada"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.watchlist_config = json.load(f)
            else:
                self.watchlist_config = {}
                self.watchlist_config['watchlist'] = {}
                self.watchlist_config['alerts'] = {}
                self.watchlist_config['created_at'] = datetime.now().isoformat()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.watchlist_config = {}
            self.watchlist_config['watchlist'] = {}
            self.watchlist_config['alerts'] = {}
    
    def get_watchlist(self):
        """Obtener watchlist configurada"""
        return self.watchlist_config.get('watchlist', {})
    
    def save_watchlist_config(self):
        """Guardar configuración de watchlist"""
        try:
            self.watchlist_config['updated_at'] = datetime.now().isoformat()
            with open(self.config_file, 'w') as f:
                json.dump(self.watchlist_config, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def add_to_watchlist(self, symbol, custom_name=None, buy_price=None, sell_price=None):
        """Agregar activo a watchlist con nombres personalizados y precios de alerta"""
        if 'watchlist' not in self.watchlist_config:
            self.watchlist_config['watchlist'] = {}
        
        asset_key = f"{symbol.lower()}"
        
        self.watchlist_config['watchlist'][asset_key] = {
            'symbol': symbol.upper(),
            'custom_name': custom_name or symbol.upper(),
            'buy_alert_price': buy_price,
            'sell_alert_price': sell_price,
            'added_date': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        self.save_watchlist_config()
        return True
    
    def check_price_alerts(self, current_data):
        """Verificar si se activan alertas de precios"""
        alerts_triggered = []
        watchlist = self.get_watchlist()
        
        for key, asset in watchlist.items():
            symbol = asset['symbol'].upper()
            buy_price = asset.get('buy_alert_price')
            sell_price = asset.get('sell_alert_price')
            
            # Buscar el símbolo en los datos actuales (puede ser BTC, BTC_crypto, etc.)
            current_price = None
            found_data_key = None
            
            for dk in current_data.keys():
                if symbol.lower() in dk.lower():
                    current_price = current_data[dk]['current_price']
                    found_data_key = dk
                    break
            
            # Si no encontramos el símbolo en datos actuales, continuar
            if current_price is None:
                continue
            
            # Verificar alerta de compra
            if buy_price and current_price <= buy_price:
                alerts_triggered.append({
                    'symbol': symbol,
                    'custom_name': asset['custom_name'],
                    'type': 'BUY',
                    'current_price': current_price,
                    'target_price': buy_price,
                    'message': f"¡ALERTA DE COMPRA! {asset['custom_name']} ha alcanzado ${buy_price:.4f}",
                    'data_source': found_data_key
                })
            
            # Verificar alerta de venta
            if sell_price and current_price >= sell_price:
                alerts_triggered.append({
                    'symbol': symbol,
                    'custom_name': asset['custom_name'],
                    'type': 'SELL',
                    'current_price': current_price,
                    'target_price': sell_price,
                    'message': f"¡ALERTA DE VENTA! {asset['custom_name']} ha alcanzado ${sell_price:.4f}",
                    'data_source': found_data_key
                })
        
        return alerts_triggered
    
    def update_all_data(self, cryptos, stocks):
        """Actualizar datos para todas las criptomonedas y acciones"""
        results = {}
        
        # Actualizar datos de criptomonedas
        for crypto in cryptos:
            try:
                data = self.get_crypto_data(crypto)
                if data:
                    results[f'{crypto.upper()}_crypto'] = data
                time.sleep(1)  # Evitar rate limiting
            except Exception as e:
                print(f"Error getting {crypto} data: {e}")
                
        # Actualizar datos de acciones
        for stock in stocks:
            try:
                data = self.get_stock_data(stock)
                if data:
                    results[f'{stock.upper()}_stock'] = data
                time.sleep(1)  # Evitar rate limiting
            except Exception as e:
                print(f"Error getting {stock} data: {e}")
                
        # Guardar datos
        self.save_data(results)
        return results
    
    def get_crypto_data(self, symbol):
        """Obtener datos de criptomonedas desde CoinGecko API"""
        try:
            # Mapeo de símbolos comunes a nombres completos de CoinGecko
            symbol_mapping = {
                'btc': 'bitcoin',
                'eth': 'ethereum', 
                'ada': 'cardano',
                'sol': 'solana',
                'dot': 'polkadot',
                'avax': 'avalanche-2',
                'matic': 'matic-network',
                'link': 'chainlink',
                'uni': 'uniswap',
                'atom': 'cosmos',
                'near': 'near-protocol',
                'ftm': 'fantom',
                'sand': 'the-sandbox',
                'mana': 'decentraland',
                'axs': 'axie-infinity',
                'enj': 'enjincoin',
                'chz': 'chiliz',
                'shib': 'shiba-inu',
                'doge': 'dogecoin',
                'ltc': 'litecoin',
                'bch': 'bitcoin-cash',
                'xrp': 'ripple',
                'xlm': 'stellar',
                'vet': 'vechain',
                'theta': 'theta-token',
                'bnb': 'binancecoin',
                'usdt': 'tether',
                'usdc': 'usd-coin'
            }
            
            # Usar el mapeo si existe, sino usar el símbolo original
            coin_id = symbol_mapping.get(symbol.lower(), symbol.lower())
            
            # CoinGecko API - gratuita y no requiere API key
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Obtener datos históricos de 1 año
                history_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=365"
                history_response = requests.get(history_url, headers=self.headers, timeout=10)
                
                historical_data = []
                monthly_data = []
                if history_response.status_code == 200:
                    history_data = history_response.json()
                    historical_data = [
                        {
                            'timestamp': datetime.fromtimestamp(item[0] / 1000).isoformat(),
                            'price': item[1],
                            'volume': 0  # CoinGecko no proporciona volumen en este endpoint
                        }
                        for item in history_data.get('prices', [])
                    ]
                
                # Obtener datos del último mes para análisis detallado
                monthly_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=30"
                monthly_response = requests.get(monthly_url, headers=self.headers, timeout=10)
                
                if monthly_response.status_code == 200:
                    monthly_history = monthly_response.json()
                    monthly_data = [
                        {
                            'timestamp': datetime.fromtimestamp(item[0] / 1000).isoformat(),
                            'price': item[1],
                            'volume': 0
                        }
                        for item in monthly_history.get('prices', [])
                    ]
                
                current_price = data['market_data']['current_price']['usd']
                change_24h = data['market_data']['price_change_percentage_24h']
                
                result = {
                    'symbol': symbol.upper(),
                    'type': 'crypto',
                    'current_price': current_price,
                    'volume_24h': data['market_data'].get('total_volume', {}).get('usd', 0),
                    'change_24h': change_24h,
                    'high_24h': data['market_data'].get('high_24h', {}).get('usd', current_price),
                    'low_24h': data['market_data'].get('low_24h', {}).get('usd', current_price),
                    'market_cap': data['market_data'].get('market_cap', {}).get('usd', 0),
                    'historical_data': historical_data,
                    'monthly_data': monthly_data,
                    'indicators': self.calculate_crypto_indicators(historical_data),
                    'monthly_indicators': self.calculate_monthly_indicators(monthly_data),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'CoinGecko API'
                }
                
                return result
                
        except Exception as e:
            print(f"Error fetching {symbol} from CoinGecko: {e}")
            
        # Fallback a Yahoo Finance
        return self.get_crypto_yahoo_fallback(symbol)
    
    def calculate_monthly_indicators(self, monthly_data):
        """Calcular indicadores técnicos con datos de 1 mes"""
        if len(monthly_data) < 20:
            return {}
        
        try:
            prices = [item['price'] for item in monthly_data]
            volumes = [item['volume'] for item in monthly_data]
            indicators = {}
            
            # Indicadores de corto plazo (1 mes)
            indicators['rsi_14'] = self.calculate_rsi(prices, 14)
            indicators['sma_20'] = sum(prices[-20:]) / 20 if len(prices) >= 20 else prices[-1]
            
            # Bandas de Bollinger mensuales
            if len(prices) >= 20:
                sma_20 = indicators['sma_20']
                variance = sum((p - sma_20) ** 2 for p in prices[-20:]) / 20
                std_dev = variance ** 0.5
                indicators['bb_upper'] = sma_20 + (2 * std_dev)
                indicators['bb_lower'] = sma_20 - (2 * std_dev)
                indicators['bb_width'] = (indicators['bb_upper'] - indicators['bb_lower']) / sma_20
            
            # Volatilidad mensual
            import statistics
            if len(prices) >= 10:
                returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, min(11, len(prices)))]
                indicators['volatility_10d'] = statistics.stdev(returns) if len(returns) > 1 else 0
            
            # Máximos y mínimos mensuales
            indicators['month_high'] = max(prices)
            indicators['month_low'] = min(prices)
            indicators['month_range'] = indicators['month_high'] - indicators['month_low']
            indicators['current_month_position'] = (prices[-1] - indicators['month_low']) / indicators['month_range']
            
            # Momentum semanal
            if len(prices) >= 7:
                momentum_1w = (prices[-1] - prices[-7]) / prices[-7] * 100
                indicators['momentum_1w'] = momentum_1w
            
            # NUEVO: Volume Trend mensual
            indicators['volume_trend'] = self.calculate_volume_trend(prices, volumes)
            
            # NUEVO: ATR mensual para stops dinámicos
            indicators['atr'] = self.calculate_atr(prices, volumes, 14)
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating monthly indicators: {e}")
            return {}
    
    def get_crypto_yahoo_fallback(self, symbol):
        """Fallback a Yahoo Finance para criptomonedas"""
        try:
            # Mapeo de nombres a símbolos para Yahoo Finance
            name_to_symbol = {
                'bitcoin': 'BTC',
                'ethereum': 'ETH', 
                'cardano': 'ADA',
                'solana': 'SOL',
                'polkadot': 'DOT',
                'avalanche': 'AVAX',
                'polygon': 'MATIC',
                'chainlink': 'LINK',
                'uniswap': 'UNI',
                'cosmos': 'ATOM'
            }
            
            symbol_for_yahoo = name_to_symbol.get(symbol.lower(), symbol[:4].upper())
            
            # Usar requests directamente con Yahoo Finance - datos de 1 año
            yahoo_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_for_yahoo}-USD"
            params = {
                'range': '1y',  # 1 año de datos
                'interval': '1d',
                'includePrePost': 'true'
            }
            
            response = requests.get(yahoo_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'chart' in data and data['chart']['result']:
                    chart = data['chart']['result'][0]
                    meta = chart.get('meta', {})
                    
                    # Verificar si tenemos datos válidos
                    if 'regularMarketPrice' in meta:
                        # Obtener precios históricos
                        timestamps = chart.get('timestamp', [])
                        indicators = chart.get('indicators', {})
                        quotes = indicators.get('quote', [{}])[0]
                        closes = quotes.get('close', [])
                        volumes = quotes.get('volume', [])
                        
                        historical_data = []
                        for i, ts in enumerate(timestamps):
                            if i < len(closes) and closes[i] is not None:
                                historical_data.append({
                                    'timestamp': datetime.fromtimestamp(ts).isoformat(),
                                    'price': closes[i],
                                    'volume': volumes[i] if i < len(volumes) and volumes[i] else 0
                                })
                        
                        # Obtener datos del último mes adicionalmente
                        monthly_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_for_yahoo}-USD"
                        monthly_params = {
                            'range': '1mo',  # 1 mes de datos
                            'interval': '1d',
                            'includePrePost': 'true'
                        }
                        
                        monthly_response = requests.get(yahoo_url, params=monthly_params, headers=self.headers, timeout=10)
                        monthly_data = []
                        
                        if monthly_response.status_code == 200:
                            monthly_data_response = monthly_response.json()
                            if 'chart' in monthly_data_response and monthly_data_response['chart']['result']:
                                monthly_chart = monthly_data_response['chart']['result'][0]
                                monthly_timestamps = monthly_chart.get('timestamp', [])
                                monthly_indicators = monthly_chart.get('indicators', {})
                                monthly_quotes = monthly_indicators.get('quote', [{}])[0]
                                monthly_closes = monthly_quotes.get('close', [])
                                monthly_volumes = monthly_quotes.get('volume', [])
                                
                                for i, ts in enumerate(monthly_timestamps):
                                    if i < len(monthly_closes) and monthly_closes[i] is not None:
                                        monthly_data.append({
                                            'timestamp': datetime.fromtimestamp(ts).isoformat(),
                                            'price': monthly_closes[i],
                                            'volume': monthly_volumes[i] if i < len(monthly_volumes) and monthly_volumes[i] else 0
                                        })

                        current_price = meta.get('regularMarketPrice', 0)
                        previous_close = meta.get('previousClose', current_price)
                        change_24h = ((current_price - previous_close) / previous_close) * 100 if previous_close and previous_close > 0 else 0
                        
                        result = {
                            'symbol': symbol.upper(),
                            'type': 'crypto',
                            'current_price': current_price,
                            'volume_24h': historical_data[-1]['volume'] if historical_data else 0,
                            'change_24h': change_24h,
                            'high_24h': meta.get('regularMarketDayHigh', current_price),
                            'low_24h': meta.get('regularMarketDayLow', current_price),
                            'historical_data': historical_data,
                            'monthly_data': monthly_data,
                            'indicators': self.calculate_crypto_indicators(historical_data),
                            'monthly_indicators': self.calculate_monthly_indicators(monthly_data),
                            'timestamp': datetime.now().isoformat(),
                            'source': 'Yahoo Finance API'
                        }
                        
                        return result
                
        except Exception as e:
            print(f"Error fetching {symbol} from Yahoo Finance: {e}")
            
        return None
    
    def get_stock_data(self, symbol):
        """Obtener datos de acciones desde Yahoo Finance"""
        try:
            # Usar requests directamente con Yahoo Finance - datos de 1 año
            yahoo_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'range': '1y',  # 1 año de datos
                'interval': '1d',
                'includePrePost': 'true'
            }
            
            response = requests.get(yahoo_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'chart' in data and data['chart']['result']:
                    chart = data['chart']['result'][0]
                    meta = chart.get('meta', {})
                    
                    # Verificar si tenemos datos válidos
                    if 'regularMarketPrice' in meta:
                        # Obtener precios históricos
                        timestamps = chart.get('timestamp', [])
                        indicators = chart.get('indicators', {})
                        quotes = indicators.get('quote', [{}])[0]
                        closes = quotes.get('close', [])
                        volumes = quotes.get('volume', [])
                        
                        historical_data = []
                        for i, ts in enumerate(timestamps):
                            if i < len(closes) and closes[i] is not None:
                                historical_data.append({
                                    'timestamp': datetime.fromtimestamp(ts).isoformat(),
                                    'price': closes[i],
                                    'volume': volumes[i] if i < len(volumes) and volumes[i] else 0
                                })
                        
                        # Obtener datos del último mes
                        monthly_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                        monthly_params = {
                            'range': '1mo',  # 1 mes de datos
                            'interval': '1d',
                            'includePrePost': 'true'
                        }
                        
                        monthly_response = requests.get(yahoo_url, params=monthly_params, headers=self.headers, timeout=10)
                        monthly_data = []
                        
                        if monthly_response.status_code == 200:
                            monthly_data_response = monthly_response.json()
                            if 'chart' in monthly_data_response and monthly_data_response['chart']['result']:
                                monthly_chart = monthly_data_response['chart']['result'][0]
                                monthly_timestamps = monthly_chart.get('timestamp', [])
                                monthly_indicators = monthly_chart.get('indicators', {})
                                monthly_quotes = monthly_indicators.get('quote', [{}])[0]
                                monthly_closes = monthly_quotes.get('close', [])
                                monthly_volumes = monthly_quotes.get('volume', [])
                                
                                for i, ts in enumerate(monthly_timestamps):
                                    if i < len(monthly_closes) and monthly_closes[i] is not None:
                                        monthly_data.append({
                                            'timestamp': datetime.fromtimestamp(ts).isoformat(),
                                            'price': monthly_closes[i],
                                            'volume': monthly_volumes[i] if i < len(monthly_volumes) and monthly_volumes[i] else 0
                                        })
                        
                        current_price = meta.get('regularMarketPrice', 0)
                        previous_close = meta.get('previousClose', current_price)
                        change_24h = ((current_price - previous_close) / previous_close) * 100 if previous_close and previous_close > 0 else 0
                        
                        result = {
                            'symbol': symbol.upper(),
                            'type': 'stock',
                            'current_price': current_price,
                            'volume_24h': historical_data[-1]['volume'] if historical_data else 0,
                            'change_24h': change_24h,
                            'high_24h': meta.get('regularMarketDayHigh', current_price),
                            'low_24h': meta.get('regularMarketDayLow', current_price),
                            'market_cap': meta.get('marketCap', 0),
                            'pe_ratio': meta.get('trailingPE', 0),
                            'dividend_yield': meta.get('dividendYield', 0) * 100 if meta.get('dividendYield') else 0,
                            'historical_data': historical_data,
                            'monthly_data': monthly_data,
                            'indicators': self.calculate_crypto_indicators(historical_data),
                            'monthly_indicators': self.calculate_monthly_indicators(monthly_data),
                            'timestamp': datetime.now().isoformat(),
                            'source': 'Yahoo Finance API'
                        }
                        
                        return result
                
        except Exception as e:
            print(f"Error fetching {symbol} from Yahoo Finance: {e}")
            
        return None
    
    def calculate_crypto_indicators(self, historical_data):
        """Calcular indicadores técnicos avanzados con datos de 1 año"""
        if len(historical_data) < 50:  # Necesitamos más datos para análisis anual
            return {}
        
        try:
            prices = [item['price'] for item in historical_data]
            volumes = [item['volume'] for item in historical_data]
            indicators = {}
            
            # --- INDICADORES AVANZADOS DE LARGO PLAZO ---
            
            # RSI con períodos múltiples
            indicators['rsi_14'] = self.calculate_rsi(prices, 14)
            indicators['rsi_30'] = self.calculate_rsi(prices, 30)
            
            # Medias móviles múltiples (para identificar tendencias de largo plazo)
            indicators['sma_20'] = sum(prices[-20:]) / 20
            indicators['sma_50'] = sum(prices[-50:]) / 50
            if len(prices) >= 100:
                indicators['sma_100'] = sum(prices[-100:]) / 100
            if len(prices) >= 200:
                indicators['sma_200'] = sum(prices[-200:]) / 200
            
            # NUEVO: % Distancia a SMA_200
            if 'sma_200' in indicators and indicators['sma_200'] > 0:
                indicators['distance_to_sma200_pct'] = ((prices[-1] - indicators['sma_200']) / indicators['sma_200']) * 100
            
            # Bandas de Bollinger anuales
            if len(prices) >= 20:
                sma_20 = sum(prices[-20:]) / 20
                variance = sum((p - sma_20) ** 2 for p in prices[-20:]) / 20
                std_dev = variance ** 0.5
                indicators['bb_upper'] = sma_20 + (2 * std_dev)
                indicators['bb_lower'] = sma_20 - (2 * std_dev)
                indicators['bb_width'] = (indicators['bb_upper'] - indicators['bb_lower']) / sma_20
            
            # MACD con señal de tendencia
            if len(prices) >= 26:
                ema_12 = self.calculate_ema(prices, 12)
                ema_26 = self.calculate_ema(prices, 26)
                indicators['macd'] = ema_12 - ema_26
                ema_diff = [ema_12 - ema_26]
                indicators['macd_signal'] = self.calculate_ema(ema_diff, 9)
                indicators['macd_histogram'] = indicators['macd'] - indicators['macd_signal']
            
            # Volatilidad anual (muy importante para riesgo)
            import statistics
            if len(prices) >= 30:
                returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, min(31, len(prices)))]
                indicators['volatility_30d'] = statistics.stdev(returns) if len(returns) > 1 else 0
            
            if len(prices) >= 252:  # Aprox 1 año de días de trading
                annual_returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, min(253, len(prices)))]
                indicators['volatility_annual'] = statistics.stdev(annual_returns) if len(annual_returns) > 1 else 0
            
            # --- INDICADORES DE SOPORTE Y RESISTENCIA ---
            indicators['year_high'] = max(prices)
            indicators['year_low'] = min(prices)
            indicators['year_range'] = indicators['year_high'] - indicators['year_low']
            indicators['current_position'] = (prices[-1] - indicators['year_low']) / indicators['year_range']
            
            # NUEVO: Invalidation Level (Stop Loss sugerido)
            indicators['invalidation_level'] = self.calculate_invalidation_level(prices, volumes)
            
            # NUEVO: ATR (Average True Range) para stops dinámicos
            indicators['atr'] = self.calculate_atr(prices, volumes, 14)  # ATR de 14 períodos
            
            # Momentum de 3 meses y 6 meses
            if len(prices) >= 90:
                momentum_3m = (prices[-1] - prices[-90]) / prices[-90] * 100
                indicators['momentum_3m'] = momentum_3m
            if len(prices) >= 180:
                momentum_6m = (prices[-1] - prices[-180]) / prices[-180] * 100
                indicators['momentum_6m'] = momentum_6m
            
            # NUEVO: Volume Trend
            indicators['volume_trend'] = self.calculate_volume_trend(prices, volumes)
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating advanced indicators: {e}")
            return {}
    
    def calculate_rsi(self, prices, period):
        """Calcular RSI con período específico"""
        if len(prices) < period + 1:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) >= period:
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            if avg_loss > 0:
                rs = avg_gain / avg_loss
                return 100 - (100 / (1 + rs))
            else:
                return 100.0
        
        return 50.0
    
    def calculate_volume_trend(self, prices, volumes):
        """Calcular tendencia de volumen para validar movimientos de precios"""
        if len(prices) < 10 or len(volumes) < 10:
            return 'INSUFFICIENT_DATA'
        
        try:
            # Calcular cambio de precio en los últimos 10 días
            price_change = (prices[-1] - prices[-10]) / prices[-10]
            
            # Calcular promedio de volumen
            recent_volume_avg = sum(volumes[-5:]) / 5  # Últimos 5 días
            historical_volume_avg = sum(volumes[-10:-5]) / 5  # 5 días anteriores
            
            # Determinar tendencia del volumen
            volume_ratio = recent_volume_avg / historical_volume_avg if historical_volume_avg > 0 else 1
            
            # Lógica de Volume Trend
            if price_change > 0.02:  # Precio sube > 2%
                if volume_ratio > 1.2:  # Volumen > 20% above average
                    return 'BULLISH_CONFIRMED'  # Subida con volumen real
                elif volume_ratio < 0.8:
                    return 'BULLISH_WEAK'  # Subida sin volumen (trampa)
                else:
                    return 'BULLISH_NEUTRAL'
            elif price_change < -0.02:  # Precio baja > 2%
                if volume_ratio > 1.2:
                    return 'BEARISH_CONFIRMED'  # Bajada con volumen real
                elif volume_ratio < 0.8:
                    return 'BEARISH_WEAK'  # Bajada sin volumen
                else:
                    return 'BEARISH_NEUTRAL'
            else:  # Precio estable
                if volume_ratio > 1.5:
                    return 'ACCUMULATION'  # Alto volumen sin movimiento
                else:
                    return 'NEUTRAL'
                    
        except Exception as e:
            print(f"Error calculating volume trend: {e}")
            return 'ERROR'
    
    def calculate_atr(self, prices, volumes, period=14):
        """Calcular Average True Range (ATR) para stops dinámicos"""
        if len(prices) < period + 1:
            return prices[-1] * 0.02  # Default 2% if insufficient data
        
        try:
            true_ranges = []
            
            # Calcular True Range para cada período
            for i in range(1, len(prices)):
                high = prices[i]  # Usamos close como high si no hay high/low
                low = prices[i]   # Usamos close como low si no hay high/low
                prev_close = prices[i-1]
                
                # True Range = max(high - low, abs(high - prev_close), abs(low - prev_close))
                tr1 = high - low
                tr2 = abs(high - prev_close)
                tr3 = abs(low - prev_close)
                
                true_range = max(tr1, tr2, tr3)
                true_ranges.append(true_range)
            
            # ATR es el promedio de los True Ranges del período
            if len(true_ranges) >= period:
                atr = sum(true_ranges[-period:]) / period
            else:
                atr = sum(true_ranges) / len(true_ranges)
            
            return round(atr, 6)
            
        except Exception as e:
            print(f"Error calculating ATR: {e}")
            return prices[-1] * 0.02  # Default 2% if error
    
    def calculate_invalidation_level(self, prices, volumes):
        """Calcular nivel de invalidación (stop loss sugerido) basado en estructura"""
        if len(prices) < 20:
            return prices[-1] * 0.95  # Default 5% below current
        
        try:
            current_price = prices[-1]
            
            # Encontrar soportes recientes
            recent_prices = prices[-20:]  # Últimos 20 días
            support_levels = []
            
            # Identificar mínimos locales como soportes
            for i in range(2, len(recent_prices) - 2):
                if (recent_prices[i] <= recent_prices[i-1] and 
                    recent_prices[i] <= recent_prices[i-2] and
                    recent_prices[i] <= recent_prices[i+1] and 
                    recent_prices[i] <= recent_prices[i+2]):
                    support_levels.append(recent_prices[i])
            
            # Si no hay soportes claros, usar método estadístico
            if not support_levels:
                import statistics
                # Usar 2 desviaciones estándar below the mean of recent lows
                recent_lows = sorted(recent_prices)[:len(recent_prices)//3]  # Bottom 33%
                if recent_lows:
                    mean_low = sum(recent_lows) / len(recent_lows)
                    std_dev = (sum((x - mean_low) ** 2 for x in recent_lows) / len(recent_lows)) ** 0.5
                    invalidation_level = max(mean_low - (2 * std_dev), current_price * 0.9)
                else:
                    invalidation_level = current_price * 0.92
            else:
                # Usar el soporte más cercano debajo del precio actual
                valid_supports = [s for s in support_levels if s < current_price]
                if valid_supports:
                    invalidation_level = max(valid_supports)  # Soporte más cercano
                else:
                    # Si todos los soportes están arriba, usar estadístico
                    import statistics
                    mean_support = sum(support_levels) / len(support_levels)
                    invalidation_level = min(mean_support, current_price * 0.95)
            
            # Ajuste por volatilidad
            if len(prices) >= 10:
                returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, min(11, len(prices)))]
                import statistics
                volatility = statistics.stdev(returns) if len(returns) > 1 else 0.02
                
                # Mayor volatilidad = mayor distancia al stop loss
                volatility_adjustment = min(0.05, volatility * 2)  # Máximo 5% extra
                invalidation_level -= (current_price * volatility_adjustment)
            
            # No dejar el stop loss demasiado lejos (máximo 15% below current)
            invalidation_level = max(invalidation_level, current_price * 0.85)
            
            return round(invalidation_level, 4)
            
        except Exception as e:
            print(f"Error calculating invalidation level: {e}")
            return prices[-1] * 0.95
    
    def calculate_ema(self, prices, period):
        """Calcular EMA (Exponential Moving Average)"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period  # Start with SMA
        
        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def save_data(self, data):
        """Guardar datos en archivos JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for key, value in data.items():
            filename = f"{key}_{timestamp}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(value, f, indent=2, default=str)
                
        # También guardar el último archivo como "latest"
        latest_file = os.path.join(self.data_dir, 'latest_data.json')
        with open(latest_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
    def load_latest_data(self):
        """Cargar los datos más recientes"""
        try:
            latest_file = os.path.join(self.data_dir, 'latest_data.json')
            if os.path.exists(latest_file):
                with open(latest_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading latest data: {e}")
        return {}