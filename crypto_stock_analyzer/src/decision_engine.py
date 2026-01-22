import numpy as np
from datetime import datetime, timedelta
import json

class DecisionEngine:
    def __init__(self):
        self.risk_tolerance = 0.5  # 0-1, donde 1 es alto riesgo
        self.min_confidence = 60  # Confianza mínima para tomar decisiones
        self.max_position_size = 0.1  # Máximo 10% del portfolio en un solo activo
        
        # Importar PositionManager
        try:
            from .position_manager import PositionManager
        except ImportError:
            from position_manager import PositionManager
        self.position_manager = PositionManager()
        
    def get_recommendations(self):
        """Generar recomendaciones de trading basadas en análisis de IA"""
        from .advanced_ai_analyzer import AdvancedAIAnalyzer
        
        analyzer = AdvancedAIAnalyzer()
        analysis_results = analyzer.analyze_market()
        
        recommendations = {}
        
        for asset, analysis in analysis_results.items():
            try:
                recommendation = self.generate_single_recommendation(asset, analysis)
                recommendations[asset] = recommendation
            except Exception as e:
                print(f"Error generating recommendation for {asset}: {e}")
                recommendations[asset] = {
                    'action': 'HOLD',
                    'reason': f'Error: {str(e)}',
                    'risk_level': 'HIGH',
                    'confidence': 0
                }
                
        return recommendations
        
    def generate_single_recommendation(self, asset, analysis):
        """Generar recomendación para un solo activo"""
        trend = analysis.get('trend', 'UNKNOWN')
        confidence = analysis.get('confidence', 0)
        volatility = analysis.get('volatility', 'MEDIUM')
        price_change_pct = analysis.get('price_change_pct', 0)
        current_price = analysis.get('current_price', 0)
        predicted_price = analysis.get('predicted_price', current_price)
        
        # NUEVOS INDICADORES
        volume_trend = analysis.get('volume_trend', 'NEUTRAL')
        distance_to_sma200 = analysis.get('distance_to_sma200_pct', 0)
        invalidation_level = analysis.get('invalidation_level', current_price * 0.95)
        
        # INDICADORES ADICIONALES PARA FILTRADO INSTITUCIONAL
        rsi_14 = 50  # Default
        risk_reward_ratio = analysis.get('risk_reward_ratio', 1.5)
        
        # Intentar obtener RSI de los indicadores anuales
        if 'annual_metrics' in analysis and 'rsi_14' in analysis['annual_metrics']:
            rsi_14_value = analysis['annual_metrics']['rsi_14']
            if isinstance(rsi_14_value, str):
                try:
                    rsi_14 = float(rsi_14_value)
                except:
                    rsi_14 = 50
            else:
                rsi_14 = rsi_14_value
        
        # Reglas de decisión base
        action = 'HOLD'
        reason = 'No clear signal'
        risk_level = 'MEDIUM'
        
        # Lógica de Filtrado de Señales (El "Cerebro Institucional")
        recommendation = ""
        signal_color = ""
        
        if risk_reward_ratio < 1.0:
            recommendation = "NO TRADE (Bad R:R)"
            signal_color = "GRAY"
            return {
                'action': 'HOLD',
                'reason': recommendation,
                'risk_level': 'HIGH',
                'confidence': confidence,
                'target_price': current_price,
                'stop_loss': current_price * 0.95,
                'signal_color': signal_color
            }

        elif rsi_14 > 80 and distance_to_sma200 > 30:
            recommendation = "DANGER: OVEREXTENDED (Wait for Pullback)"
            signal_color = "ORANGE"
            return {
                'action': 'HOLD',
                'reason': recommendation,
                'risk_level': 'HIGH',
                'confidence': confidence,
                'target_price': current_price,
                'stop_loss': current_price * 0.95,
                'signal_color': signal_color
            }

        elif rsi_14 < 25 and distance_to_sma200 < -20:
            recommendation = "STRONG BUY (Oversold Bounce)"
            signal_color = "GREEN"
            # Continuar con el análisis normal pero marcar como fuerte señal alcista
            # No retornar aquí, dejar que la lógica normal decida con esta preferencia
        
        # Ajustar por confianza
        if confidence < self.min_confidence:
            return {
                'action': 'HOLD',
                'reason': f'Low confidence ({confidence}%)',
                'risk_level': 'HIGH',
                'confidence': confidence,
                'target_price': current_price,
                'stop_loss': current_price * 0.95,
                'signal_color': 'GRAY'
            }
            
        # Lógica de decisión principal con NUEVOS INDICADORES
        if trend == 'BULLISH' and confidence > 70:
            # PENALIZACIÓN por distancia a SMA_200
            sma200_penalty = False
            if distance_to_sma200 > 15:  # Más de 15% arriba de SMA_200
                sma200_penalty = True
                confidence -= 15  # Reducir confianza significativamente
                reason = f'Bullish trend but {distance_to_sma200:.1f}% above SMA_200 - high risk entry'
                risk_level = 'HIGH'
            
            # VALIDACIÓN por Volume Trend
            volume_validation = True
            if volume_trend in ['BULLISH_WEAK']:
                confidence -= 10  # Penalizar subida sin volumen
                reason = f'Bullish trend without volume confirmation - potential trap'
                risk_level = 'HIGH'
                volume_validation = False
            elif volume_trend == 'BEARISH_CONFIRMED':
                confidence -= 20  # Penalizar fuertemente si volumen indica bajada
                reason = f'Bullish trend contradicted by bearish volume - avoid'
                risk_level = 'HIGH'
                volume_validation = False
            
            # Decisión final con validaciones
            if not sma200_penalty and volume_validation and volatility == 'LOW':
                action = 'BUY'
                reason = 'Strong bullish trend with low volatility and volume confirmation'
                risk_level = 'LOW'
            elif not sma200_penalty and volume_validation and volatility == 'MEDIUM' and confidence > 75:
                action = 'BUY'
                reason = 'Bullish trend with volume confirmation and acceptable volatility'
                risk_level = 'MEDIUM'
            else:
                action = 'HOLD'
                if not reason.startswith('Bullish trend'):
                    reason = 'Bullish trend but high volatility or weak signals - wait for better entry'
                risk_level = 'HIGH'
                
        elif trend == 'BEARISH' and confidence > 70:
            # VALIDACIÓN por Volume Trend para señales de venta
            volume_validation_sell = True
            if volume_trend == 'BEARISH_WEAK':
                confidence -= 10  # Penalizar bajada sin volumen
                reason = 'Bearish trend without volume confirmation - weak signal'
                risk_level = 'MEDIUM'
                volume_validation_sell = False
            elif volume_trend == 'BULLISH_CONFIRMED':
                confidence -= 25  # Penalizar fuertemente si volumen contradice bajada
                reason = 'Bearish trend contradicted by bullish volume - avoid selling'
                risk_level = 'HIGH'
                volume_validation_sell = False
                action = 'HOLD'
            
            if volume_validation_sell:
                if volatility == 'LOW':
                    action = 'SELL'
                    reason = 'Strong bearish trend with low volatility and volume confirmation'
                    risk_level = 'LOW'
                elif volatility == 'MEDIUM' and confidence > 75:
                    action = 'SELL'
                    reason = 'Bearish trend with volume confirmation - exit position'
                    risk_level = 'MEDIUM'
                else:
                    action = 'HOLD'
                    reason = 'Bearish trend but high volatility - wait for confirmation'
                    risk_level = 'HIGH'
                
        elif trend == 'NEUTRAL':
            action = 'HOLD'
            reason = 'Neutral trend - no action needed'
            risk_level = 'LOW'
            
        # Ajustar por cambio de precio predicho
        if price_change_pct > 5 and action == 'HOLD':
            action = 'BUY'
            reason = f'Predicted price increase of {price_change_pct}%'
        elif price_change_pct < -5 and action == 'HOLD':
            action = 'SELL'
            reason = f'Predicted price decrease of {price_change_pct}%'
            
        # Calcular precios objetivo y stop loss
        target_price, stop_loss = self.calculate_price_targets(
            current_price, predicted_price, action, volatility
        )
        
        # USAR ATR para stop loss dinámico (prioridad sobre otros métodos)
        atr = analysis.get('atr', current_price * 0.02)
        atr_stop_loss = current_price - (2 * atr)  # Fórmula: Precio - (2 * ATR)
        
        if action in ['BUY', 'SELL']:
            # Para BUY: usar ATR stop loss como principal
            if action == 'BUY':
                # Comparar ATR stop loss con otros métodos y usar el más conservador (más alto)
                stop_loss = max(atr_stop_loss, invalidation_level if invalidation_level else 0, stop_loss)
            # Para SELL: stop loss al alza
            else:
                stop_loss = min(atr_stop_loss, invalidation_level if invalidation_level else float('inf'), stop_loss)
        
        # Ajustar por tolerancia al riesgo
        if self.risk_tolerance < 0.3 and risk_level == 'HIGH':
            action = 'HOLD'
            reason = f'High risk position - below risk tolerance. Original: {reason}'
        
        # Determinar color de señal para acciones normales
        if not signal_color:  # Si no fue establecido por el filtrado institucional
            if action == 'BUY':
                signal_color = 'GREEN'
            elif action == 'SELL':
                signal_color = 'RED'
            else:
                signal_color = 'YELLOW'
            
        # Aplicar preferencia de señal institucional si aplica
        if recommendation and signal_color == 'GREEN':
            reason = f"{recommendation} - {reason}"
            if action != 'BUY':
                action = 'BUY'
                confidence = min(95, confidence + 10)
            
        return {
            'action': action,
            'reason': reason,
            'risk_level': risk_level,
            'confidence': confidence,
            'target_price': target_price,
            'stop_loss': stop_loss,
            'predicted_change': price_change_pct,
            'volatility': volatility,
            # NUEVOS INDICADORES en el resultado
            'volume_trend': volume_trend,
            'distance_to_sma200_pct': distance_to_sma200,
            'invalidation_level': invalidation_level,
            'atr': atr,
            'atr_pct': (atr / current_price) * 100,
            'dynamic_stop_loss': atr_stop_loss,
            'signal_color': signal_color
        }
        
    def calculate_price_targets(self, current_price, predicted_price, action, volatility):
        """Calcular precios objetivo y stop loss"""
        
        if action == 'BUY':
            # Target: precio predicho o 5% arriba del actual
            target_price = max(predicted_price, current_price * 1.05)
            
            # Stop loss: 2-5% abajo del actual, dependiendo de la volatilidad
            if volatility == 'LOW':
                stop_loss = current_price * 0.98
            elif volatility == 'MEDIUM':
                stop_loss = current_price * 0.95
            else:  # HIGH
                stop_loss = current_price * 0.92
                
        elif action == 'SELL':
            # Target: precio predicho o 5% abajo del actual
            target_price = min(predicted_price, current_price * 0.95)
            
            # Stop loss: 2-5% arriba del actual (para cubrir posición corta)
            if volatility == 'LOW':
                stop_loss = current_price * 1.02
            elif volatility == 'MEDIUM':
                stop_loss = current_price * 1.05
            else:  # HIGH
                stop_loss = current_price * 1.08
                
        else:  # HOLD
            target_price = current_price
            stop_loss = current_price
            
        return round(target_price, 4), round(stop_loss, 4)
        
    def calculate_position_size(self, asset, portfolio_value, risk_level):
        """Calcular tamaño de posición basado en riesgo"""
        
        # Tamaño base según nivel de riesgo
        if risk_level == 'LOW':
            base_size = 0.15  # 15% del portfolio
        elif risk_level == 'MEDIUM':
            base_size = 0.10  # 10% del portfolio
        else:  # HIGH
            base_size = 0.05  # 5% del portfolio
            
        # Ajustar por tolerancia al riesgo
        adjusted_size = base_size * self.risk_tolerance
        
        # Limitar al máximo permitido
        final_size = min(adjusted_size, self.max_position_size)
        
        return round(final_size, 3)
        
    def generate_portfolio_summary(self, recommendations):
        """Generar resumen del portfolio"""
        
        actions_count = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
        risk_distribution = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
        avg_confidence = 0
        
        for rec in recommendations.values():
            action = rec.get('action', 'HOLD')
            risk = rec.get('risk_level', 'MEDIUM')
            confidence = rec.get('confidence', 0)
            
            actions_count[action] += 1
            risk_distribution[risk] += 1
            avg_confidence += confidence
            
        total_assets = len(recommendations)
        if total_assets > 0:
            avg_confidence /= total_assets
            
        summary = {
            'total_assets': total_assets,
            'actions': actions_count,
            'risk_distribution': risk_distribution,
            'average_confidence': round(avg_confidence, 2),
            'market_sentiment': self.calculate_market_sentiment(actions_count),
            'overall_risk': self.calculate_overall_risk(risk_distribution)
        }
        
        return summary
        
    def calculate_market_sentiment(self, actions_count):
        """Calcular sentimiento del mercado"""
        
        total = sum(actions_count.values())
        if total == 0:
            return 'NEUTRAL'
            
        buy_ratio = actions_count['BUY'] / total
        sell_ratio = actions_count['SELL'] / total
        
        if buy_ratio > 0.6:
            return 'BULLISH'
        elif sell_ratio > 0.6:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
            
    def calculate_overall_risk(self, risk_distribution):
        """Calcular riesgo general del portfolio"""
        
        total = sum(risk_distribution.values())
        if total == 0:
            return 'MEDIUM'
            
        high_ratio = risk_distribution['HIGH'] / total
        
        if high_ratio > 0.5:
            return 'HIGH'
        elif high_ratio > 0.2:
            return 'MEDIUM'
        else:
            return 'LOW'
            
    def set_risk_tolerance(self, tolerance):
        """Ajustar tolerancia al riesgo (0-1)"""
        self.risk_tolerance = max(0, min(1, tolerance))
        
    def set_min_confidence(self, confidence):
        """Ajustar confianza mínima para decisiones (0-100)"""
        self.min_confidence = max(0, min(100, confidence))