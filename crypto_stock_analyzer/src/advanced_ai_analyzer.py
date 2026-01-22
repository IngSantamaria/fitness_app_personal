import numpy as np
import pandas as pd
import random
from datetime import datetime

class AdvancedAIAnalyzer:
    """Analizador IA con datos de 1 año + 1 mes y análisis dual"""
    
    def __init__(self):
        self.models_dir = 'models'
        
    def analyze_market(self):
        """Analizar el mercado usando 1 año + 1 mes de datos históricos"""
        # Cargar datos reales más recientes
        try:
            from .real_data_collector import RealDataCollector
            collector = RealDataCollector()
            latest_data = collector.load_latest_data()
        except:
            latest_data = {}
        
        results = {}
        
        for key, data in latest_data.items():
            try:
                # Obtener indicadores de 1 año y 1 mes
                annual_indicators = data.get('indicators', {})
                monthly_indicators = data.get('monthly_indicators', {})
                change_24h = data.get('change_24h', 0)
                current_price = data.get('current_price', 0)
                volume = data.get('volume_24h', 0)
                
                # Análisis dual: combinación de datos anuales y mensuales
                annual_trend = self.advanced_trend_analysis(annual_indicators, change_24h)
                monthly_trend = self.monthly_trend_analysis(monthly_indicators, change_24h)
                
                # Combinar tendencias para análisis final
                final_trend = self.combine_trends(annual_trend, monthly_trend)
                
                confidence = self.calculate_dual_confidence(annual_indicators, monthly_indicators, change_24h, volume)
                volatility = self.determine_dual_volatility(annual_indicators, monthly_indicators)
                
                # Predicción dual con ambos períodos
                predicted_price = self.dual_price_prediction(current_price, annual_indicators, monthly_indicators, final_trend)
                
                # Identificar patrones combinados
                patterns = self.identify_dual_patterns(annual_indicators, monthly_indicators, final_trend)
                
                # Análisis de riesgo-recompensa dual
                risk_reward = self.calculate_dual_risk_reward(annual_indicators, monthly_indicators, current_price)
                
                # NUEVOS INDICADORES
                volume_trend = annual_indicators.get('volume_trend', 'NEUTRAL')
                distance_to_sma200 = annual_indicators.get('distance_to_sma200_pct', 0)
                invalidation_level = annual_indicators.get('invalidation_level', current_price * 0.95)
                atr = annual_indicators.get('atr', current_price * 0.02)
                
                results[key] = {
                    'trend': final_trend,
                    'annual_trend': annual_trend,
                    'monthly_trend': monthly_trend,
                    'confidence': round(confidence, 2),
                    'volatility': volatility,
                    'indicators': ', '.join(patterns),
                    'predicted_price': round(predicted_price, 4),
                    'current_price': current_price,
                    'price_change_pct': round(((predicted_price - current_price) / current_price) * 100, 2),
                    'analysis_depth': 'DUAL_1YR_1MO',
                    'annual_metrics': self.extract_key_metrics(annual_indicators),
                    'monthly_metrics': self.extract_key_metrics(monthly_indicators),
                    'risk_reward_ratio': risk_reward,
                    # NUEVOS INDICADORES
                    'volume_trend': volume_trend,
                    'distance_to_sma200_pct': round(distance_to_sma200, 2),
                    'invalidation_level': round(invalidation_level, 4),
                    'invalidation_distance_pct': round(((current_price - invalidation_level) / current_price) * 100, 2),
                    'atr': round(atr, 6),
                    'atr_pct': round((atr / current_price) * 100, 2),
                    'dynamic_stop_loss': round(current_price - (2 * atr), 4)  # Fórmula: Precio - (2 * ATR)
                }
                
            except Exception as e:
                print(f"Error analyzing {key}: {e}")
                # Fallback con valores por defecto
                results[key] = {
                    'trend': 'NEUTRAL',
                    'annual_trend': 'NEUTRAL',
                    'monthly_trend': 'NEUTRAL',
                    'confidence': 50.0,
                    'volatility': 'MEDIUM',
                    'indicators': 'RSI, MACD, Volume, SMA',
                    'predicted_price': data.get('current_price', 100),
                    'current_price': data.get('current_price', 100),
                    'price_change_pct': 0.0,
                    'analysis_depth': 'LIMITED'
                }
                
        return results
    
    def monthly_trend_analysis(self, monthly_indicators, change_24h):
        """Análisis de tendencia con datos de 1 mes"""
        if not monthly_indicators:
            return 'NEUTRAL'
        
        trend_score = 0
        
        # RSI mensual
        rsi_14 = monthly_indicators.get('rsi_14', 50)
        if rsi_14 > 60:
            trend_score += 2
        elif rsi_14 < 40:
            trend_score -= 2
        
        # SMA mensual
        sma_20 = monthly_indicators.get('sma_20', 0)
        current_price = 0  # Placeholder
        
        # Momentum semanal
        momentum_1w = monthly_indicators.get('momentum_1w', 0)
        if momentum_1w > 5:
            trend_score += 2
        elif momentum_1w < -5:
            trend_score -= 2
        
        # Posición en rango mensual
        current_month_position = monthly_indicators.get('current_month_position', 0.5)
        if current_month_position > 0.8:
            trend_score += 1
        elif current_month_position < 0.2:
            trend_score -= 1
        
        # Determinar tendencia mensual
        if trend_score >= 3:
            return 'STRONG_BULLISH'
        elif trend_score >= 1:
            return 'BULLISH'
        elif trend_score <= -3:
            return 'STRONG_BEARISH'
        elif trend_score <= -1:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def combine_trends(self, annual_trend, monthly_trend):
        """Combinar tendencias anuales y mensuales"""
        trend_weights = {
            'STRONG_BULLISH': 3,
            'BULLISH': 2,
            'NEUTRAL': 0,
            'BEARISH': -2,
            'STRONG_BEARISH': -3
        }
        
        annual_score = trend_weights.get(annual_trend, 0)
        monthly_score = trend_weights.get(monthly_trend, 0)
        
        # Dar más peso a la tendencia anual (60%) que a la mensual (40%)
        combined_score = (annual_score * 0.6) + (monthly_score * 0.4)
        
        if combined_score >= 2:
            return 'STRONG_BULLISH'
        elif combined_score >= 0.5:
            return 'BULLISH'
        elif combined_score <= -2:
            return 'STRONG_BEARISH'
        elif combined_score <= -0.5:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def calculate_dual_confidence(self, annual_indicators, monthly_indicators, change_24h, volume):
        """Calcular confianza combinando datos anuales y mensuales"""
        confidence = 50  # Base
        
        # Confianza de datos anuales (60% peso)
        if annual_indicators:
            rsi_14 = annual_indicators.get('rsi_14', 50)
            rsi_30 = annual_indicators.get('rsi_30', 50)
            
            if abs(rsi_14 - rsi_30) < 10:  # RSI consistente
                confidence += 9  # 60% de 15
            
            volatility_annual = annual_indicators.get('volatility_annual', 0.5)
            if 0.2 < volatility_annual < 0.8:
                confidence += 6  # 60% de 10
        
        # Confianza de datos mensuales (40% peso)
        if monthly_indicators:
            rsi_monthly = monthly_indicators.get('rsi_14', 50)
            if 40 <= rsi_monthly <= 60:  # RSI en zona neutral
                confidence += 6  # 40% de 15
            
            volatility_10d = monthly_indicators.get('volatility_10d', 0.5)
            if 0.1 < volatility_10d < 0.4:
                confidence += 4  # 40% de 10
        
        # Volumen significativo
        if volume > 10000000:
            confidence += 10
        elif volume > 5000000:
            confidence += 5
        
        return min(95, max(25, confidence))
    
    def determine_dual_volatility(self, annual_indicators, monthly_indicators):
        """Determinar volatilidad combinando datos anuales y mensuales"""
        if not annual_indicators and not monthly_indicators:
            return 'MEDIUM'
        
        volatility_scores = []
        
        if annual_indicators:
            volatility_annual = annual_indicators.get('volatility_annual', 0.5)
            volatility_scores.append(volatility_annual)
        
        if monthly_indicators:
            volatility_10d = monthly_indicators.get('volatility_10d', 0.5)
            volatility_scores.append(volatility_10d)
        
        if volatility_scores:
            avg_volatility = sum(volatility_scores) / len(volatility_scores)
            
            if avg_volatility > 0.8:
                return 'VERY_HIGH'
            elif avg_volatility > 0.5:
                return 'HIGH'
            elif avg_volatility > 0.3:
                return 'MEDIUM'
            elif avg_volatility > 0.15:
                return 'LOW'
            else:
                return 'VERY_LOW'
        
        return 'MEDIUM'
    
    def dual_price_prediction(self, current_price, annual_indicators, monthly_indicators, trend):
        """Predicción dual usando datos anuales y mensuales"""
        # Base prediction según tendencia
        trend_multipliers = {
            'STRONG_BULLISH': 1.05,
            'BULLISH': 1.03,
            'NEUTRAL': 1.01,
            'BEARISH': 0.98,
            'STRONG_BEARISH': 0.95
        }
        
        base_multiplier = trend_multipliers.get(trend, 1.01)
        
        # Ajuste por posición en rango anual
        if annual_indicators:
            current_position = annual_indicators.get('current_position', 0.5)
            if current_position > 0.85:
                base_multiplier *= 0.98
            elif current_position < 0.15:
                base_multiplier *= 1.02
        
        # Ajuste por posición en rango mensual
        if monthly_indicators:
            current_month_position = monthly_indicators.get('current_month_position', 0.5)
            if current_month_position > 0.9:
                base_multiplier *= 0.99
            elif current_month_position < 0.1:
                base_multiplier *= 1.01
        
        # Ajuste por momentum combinado
        momentum_adjustment = 1.0
        if annual_indicators:
            momentum_3m = annual_indicators.get('momentum_3m', 0)
            momentum_adjustment += (momentum_3m / 100) * 0.2
        
        if monthly_indicators:
            momentum_1w = monthly_indicators.get('momentum_1w', 0)
            momentum_adjustment += (momentum_1w / 100) * 0.1
        
        base_multiplier *= momentum_adjustment
        
        predicted_price = current_price * base_multiplier
        return predicted_price
    
    def identify_dual_patterns(self, annual_indicators, monthly_indicators, trend):
        """Identificar patrones combinados anuales y mensuales"""
        patterns = []
        
        # Patrones anuales
        if annual_indicators:
            rsi_14 = annual_indicators.get('rsi_14', 50)
            if rsi_14 > 70:
                patterns.append('OVERBOUGHT_ANNUAL')
            elif rsi_14 < 30:
                patterns.append('OVERSOLD_ANNUAL')
            
            current_position = annual_indicators.get('current_position', 0.5)
            if current_position > 0.9:
                patterns.append('YEAR_HIGH_PROXIMITY')
            elif current_position < 0.1:
                patterns.append('YEAR_LOW_PROXIMITY')
        
        # Patrones mensuales
        if monthly_indicators:
            rsi_monthly = monthly_indicators.get('rsi_14', 50)
            if rsi_monthly > 70:
                patterns.append('OVERBOUGHT_MONTHLY')
            elif rsi_monthly < 30:
                patterns.append('OVERSOLD_MONTHLY')
            
            current_month_position = monthly_indicators.get('current_month_position', 0.5)
            if current_month_position > 0.85:
                patterns.append('MONTH_HIGH_PROXIMITY')
            elif current_month_position < 0.15:
                patterns.append('MONTH_LOW_PROXIMITY')
        
        # Patrones de tendencia combinada
        if trend == 'STRONG_BULLISH':
            patterns.append('DUAL_BULLISH_CONFIRMATION')
        elif trend == 'STRONG_BEARISH':
            patterns.append('DUAL_BEARISH_CONFIRMATION')
        
        return patterns if patterns else ['NEUTRAL_PATTERN']
    
    def calculate_dual_risk_reward(self, annual_indicators, monthly_indicators, current_price):
        """Calcular ratio riesgo-recompensa dual"""
        upside_potential = 0
        downside_risk = 0
        
        # Potencial basado en datos anuales
        if annual_indicators:
            year_high = annual_indicators.get('year_high', current_price * 1.5)
            year_low = annual_indicators.get('year_low', current_price * 0.5)
            
            annual_upside = (year_high - current_price) / current_price
            annual_downside = (current_price - year_low) / current_price
            
            upside_potential += annual_upside * 0.7  # 70% peso
            downside_risk += annual_downside * 0.7
        
        # Potencial basado en datos mensuales
        if monthly_indicators:
            month_high = monthly_indicators.get('month_high', current_price * 1.2)
            month_low = monthly_indicators.get('month_low', current_price * 0.8)
            
            monthly_upside = (month_high - current_price) / current_price
            monthly_downside = (current_price - month_low) / current_price
            
            upside_potential += monthly_upside * 0.3  # 30% peso
            downside_risk += monthly_downside * 0.3
        
        if downside_risk > 0:
            risk_reward = upside_potential / downside_risk
        else:
            risk_reward = 2.0
        
        return round(risk_reward, 2)
    
    def advanced_trend_analysis(self, indicators, change_24h):
        """Análisis de tendencia con múltiples plazos"""
        
        # Análisis de medias móviles (tendencia de largo plazo)
        sma_20 = indicators.get('sma_20', 0)
        sma_50 = indicators.get('sma_50', 0)
        sma_100 = indicators.get('sma_100', 0)
        sma_200 = indicators.get('sma_200', 0)
        
        trend_score = 0
        trend_factors = []
        
        # 1. Tendencia de medias móviles (60% peso)
        current_price = 0  # Placeholder - debería venir de data
        
        if sma_20 > sma_50:
            trend_score += 2
            trend_factors.append("SMA_20>50_BULLISH")
        elif sma_20 < sma_50:
            trend_score -= 2
            trend_factors.append("SMA_20<50_BEARISH")
            
        if sma_50 > sma_200:
            trend_score += 3
            trend_factors.append("SMA_50>200_BULLISH")
        elif sma_50 < sma_200:
            trend_score -= 3
            trend_factors.append("SMA_50<200_BEARISH")
        
        # 2. Momentum (20% peso)
        momentum_3m = indicators.get('momentum_3m', 0)
        momentum_6m = indicators.get('momentum_6m', 0)
        
        if momentum_3m > 10:
            trend_score += 1
            trend_factors.append("3M_MOMENTUM_BULLISH")
        elif momentum_3m < -10:
            trend_score -= 1
            trend_factors.append("3M_MOMENTUM_BEARISH")
            
        if momentum_6m > 15:
            trend_score += 2
            trend_factors.append("6M_MOMENTUM_BULLISH")
        elif momentum_6m < -15:
            trend_score -= 2
            trend_factors.append("6M_MOMENTUM_BEARISH")
        
        # 3. Posición en rango anual (10% peso)
        current_position = indicators.get('current_position', 0.5)
        if current_position > 0.8:
            trend_score += 1
            trend_factors.append("YEAR_HIGH_ZONE")
        elif current_position < 0.2:
            trend_score -= 1
            trend_factors.append("YEAR_LOW_ZONE")
        
        # 4. RSI múltiples (10% peso)
        rsi_14 = indicators.get('rsi_14', 50)
        rsi_30 = indicators.get('rsi_30', 50)
        
        if rsi_14 > 60 and rsi_30 > 55:
            trend_score += 1
            trend_factors.append("RSI_BULLISH")
        elif rsi_14 < 40 and rsi_30 < 45:
            trend_score -= 1
            trend_factors.append("RSI_BEARISH")
        
        # Determinar tendencia final
        if trend_score >= 4:
            return 'STRONG_BULLISH'
        elif trend_score >= 1:
            return 'BULLISH'
        elif trend_score <= -4:
            return 'STRONG_BEARISH'
        elif trend_score <= -1:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def calculate_advanced_confidence(self, indicators, change_24h, volume):
        """Calcular confianza basada en múltiples factores anuales"""
        confidence = 50  # Base
        
        # 1. Consistencia de indicadores
        rsi_14 = indicators.get('rsi_14', 50)
        rsi_30 = indicators.get('rsi_30', 50)
        
        if abs(rsi_14 - rsi_30) < 10:  # RSI consistente
            confidence += 15
        
        # 2. Volumen significativo
        if volume > 10000000:  # Alto volumen
            confidence += 10
        elif volume > 5000000:
            confidence += 5
        
        # 3. Datos históricos robustos
        volatility_annual = indicators.get('volatility_annual', 0.5)
        if 0.2 < volatility_annual < 0.8:  # Volatilidad moderada (buena señal)
            confidence += 10
        elif volatility_annual <= 0.2:  # Muy baja volatilidad (confiable)
            confidence += 15
        
        # 4. Posición en rango anual
        current_position = indicators.get('current_position', 0.5)
        if 0.3 <= current_position <= 0.7:  # Zona neutral de riesgo
            confidence += 10
        
        # 5. Momentum consistente
        momentum_3m = indicators.get('momentum_3m', 0)
        momentum_6m = indicators.get('momentum_6m', 0)
        
        if (momentum_3m > 0 and momentum_6m > 0) or (momentum_3m < 0 and momentum_6m < 0):
            confidence += 15  # Momentum consistente
        
        # 6. Magnitud del cambio actual
        if abs(change_24h) > 5:
            confidence += 10
        elif abs(change_24h) > 2:
            confidence += 5
        
        return min(95, max(25, confidence))
    
    def determine_advanced_volatility(self, indicators):
        """Determinar volatilidad con datos anuales"""
        volatility_annual = indicators.get('volatility_annual', 0.5)
        bb_width = indicators.get('bb_width', 0.1)
        
        # Combinar volatilidad histórica con ancho de bandas
        combined_volatility = (volatility_annual + bb_width) / 2
        
        if combined_volatility > 0.8:
            return 'VERY_HIGH'
        elif combined_volatility > 0.5:
            return 'HIGH'
        elif combined_volatility > 0.3:
            return 'MEDIUM'
        elif combined_volatility > 0.15:
            return 'LOW'
        else:
            return 'VERY_LOW'
    
    def advanced_price_prediction(self, current_price, indicators, trend):
        """Predicción avanzada usando datos anuales"""
        
        # Base prediction según tendencia
        trend_multipliers = {
            'STRONG_BULLISH': 1.05,
            'BULLISH': 1.03,
            'NEUTRAL': 1.01,
            'BEARISH': 0.98,
            'STRONG_BEARISH': 0.95
        }
        
        base_multiplier = trend_multipliers.get(trend, 1.01)
        
        # Ajuste por posición en rango anual
        current_position = indicators.get('current_position', 0.5)
        if current_position > 0.85:  # Cerca del máximo anual
            base_multiplier *= 0.98  # Corrección a la baja
        elif current_position < 0.15:  # Cerca del mínimo anual
            base_multiplier *= 1.02  # Potencial de rebote
        
        # Ajuste por momentum
        momentum_3m = indicators.get('momentum_3m', 0)
        momentum_adjustment = 1 + (momentum_3m / 100) * 0.3  # 30% del momentum
        base_multiplier *= momentum_adjustment
        
        # Ajuste por volatilidad
        volatility_annual = indicators.get('volatility_annual', 0.5)
        if volatility_annual > 0.7:
            base_multiplier *= 1.01  # Mayor potencial de cambio
        elif volatility_annual < 0.2:
            base_multiplier *= 0.99  # Movimientos más limitados
        
        predicted_price = current_price * base_multiplier
        return predicted_price
    
    def identify_annual_patterns(self, indicators, trend):
        """Identificar patrones anuales significativos"""
        patterns = []
        
        # RSI patterns
        rsi_14 = indicators.get('rsi_14', 50)
        if rsi_14 > 70:
            patterns.append('OVERBOUGHT_ANNUAL')
        elif rsi_14 < 30:
            patterns.append('OVERSOLD_ANNUAL')
        
        # SMA crossovers
        sma_20 = indicators.get('sma_20', 0)
        sma_50 = indicators.get('sma_50', 0)
        sma_200 = indicators.get('sma_200', 0)
        
        if sma_20 > sma_50 and sma_50 > sma_200:
            patterns.append('GOLDEN_CROSS_ANNUAL')
        elif sma_20 < sma_50 and sma_50 < sma_200:
            patterns.append('DEATH_CROSS_ANNUAL')
        
        # Position patterns
        current_position = indicators.get('current_position', 0.5)
        if current_position > 0.9:
            patterns.append('YEAR_HIGH_PROXIMITY')
        elif current_position < 0.1:
            patterns.append('YEAR_LOW_PROXIMITY')
        
        # Momentum patterns
        momentum_6m = indicators.get('momentum_6m', 0)
        if momentum_6m > 30:
            patterns.append('STRONG_ANNUAL_UPTREND')
        elif momentum_6m < -30:
            patterns.append('STRONG_ANNUAL_DOWNTREND')
        
        # MACD patterns
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        if macd > macd_signal:
            patterns.append('MACD_BULLISH_CROSS')
        else:
            patterns.append('MACD_BEARISH_CROSS')
        
        return patterns if patterns else ['NEUTRAL_PATTERN']
    
    def calculate_risk_reward_ratio(self, indicators, current_price):
        """Calcular ratio riesgo-recompensa basado en datos anuales"""
        year_high = indicators.get('year_high', current_price * 1.5)
        year_low = indicators.get('year_low', current_price * 0.5)
        
        # Potencial de subida vs bajada
        upside_potential = (year_high - current_price) / current_price
        downside_risk = (current_price - year_low) / current_price
        
        if downside_risk > 0:
            risk_reward = upside_potential / downside_risk
        else:
            risk_reward = 2.0  # Default favorable
        
        return round(risk_reward, 2)
    
    def extract_key_metrics(self, indicators):
        """Extraer métricas clave para mostrar"""
        metrics = {}
        
        if not indicators:
            return metrics
        
        # Indicadores anuales
        annual_indicators = ['rsi_14', 'sma_20', 'sma_50', 'sma_200', 'momentum_3m', 'momentum_6m', 
                           'volatility_annual', 'current_position', 'year_high', 'year_low']
        
        # Indicadores mensuales
        monthly_indicators = ['rsi_14', 'sma_20', 'volatility_10d', 'current_month_position', 
                            'month_high', 'month_low', 'momentum_1w']
        
        # Seleccionar los indicadores apropiados según el tipo
        key_indicators = annual_indicators if 'volatility_annual' in indicators else monthly_indicators
        
        for indicator in key_indicators:
            value = indicators.get(indicator)
            if value is not None:
                if indicator in ['current_position', 'current_month_position']:
                    metrics[indicator] = f"{value:.1%}"
                elif indicator in ['momentum_3m', 'momentum_6m', 'momentum_1w']:
                    metrics[indicator] = f"{value:.1f}%"
                elif indicator in ['rsi_14']:
                    metrics[indicator] = f"{value:.1f}"
                else:
                    metrics[indicator] = f"{value:.4f}"
        
        return metrics

# Usar el nombre original para compatibilidad
AIAnalyzer = AdvancedAIAnalyzer