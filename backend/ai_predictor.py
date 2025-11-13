import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import json

class StockPredictor:
    def __init__(self, db_name='pharmacy.db'):
        self.db_name = db_name
    
    def get_sales_history(self, medicine_id, days=30):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT sale_date, SUM(quantity) as total_qty
            FROM sales
            WHERE medicine_id = ? AND sale_date >= ?
            GROUP BY sale_date
            ORDER BY sale_date
        ''', (medicine_id, date_threshold))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def predict_stock_needs(self, medicine_id, days_ahead=7):
        sales_history = self.get_sales_history(medicine_id, days=30)
        
        if not sales_history:
            return {
                'predicted_demand': 0,
                'confidence': 'low',
                'recommendation': 'No sales history available'
            }
        
        # Simple moving average prediction
        total_quantity = sum(qty for _, qty in sales_history)
        avg_daily_sales = total_quantity / len(sales_history)
        predicted_demand = round(avg_daily_sales * days_ahead)
        
        # Get current stock
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT quantity, reorder_level FROM medicines WHERE id = ?', (medicine_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            current_stock, reorder_level = result
            stock_after_prediction = current_stock - predicted_demand
            
            if stock_after_prediction < reorder_level:
                recommendation = f'REORDER NEEDED: Stock will fall below reorder level'
                confidence = 'high' if len(sales_history) > 10 else 'medium'
            elif stock_after_prediction < 0:
                recommendation = f'URGENT: Stock will run out'
                confidence = 'high'
            else:
                recommendation = 'Stock levels adequate'
                confidence = 'medium'
        else:
            recommendation = 'Medicine not found'
            confidence = 'low'
        
        return {
            'predicted_demand': predicted_demand,
            'avg_daily_sales': round(avg_daily_sales, 2),
            'confidence': confidence,
            'recommendation': recommendation,
            'current_stock': result[0] if result else 0
        }
    
    def predict_30_day_demand(self, medicine_id):
        """Predict demand for next 30 days with weekly breakdown"""
        sales_history = self.get_sales_history(medicine_id, days=60)
        
        if not sales_history:
            return {
                'total_30_day_demand': 0,
                'weekly_breakdown': [0, 0, 0, 0],
                'confidence': 'low',
                'trend': 'insufficient_data'
            }
        
        # Calculate average daily sales
        total_quantity = sum(qty for _, qty in sales_history)
        avg_daily_sales = total_quantity / len(sales_history)
        
        # Calculate trend (comparing first half vs second half)
        mid_point = len(sales_history) // 2
        first_half_avg = sum(qty for _, qty in sales_history[:mid_point]) / max(mid_point, 1)
        second_half_avg = sum(qty for _, qty in sales_history[mid_point:]) / max(len(sales_history) - mid_point, 1)
        
        trend = 'stable'
        if second_half_avg > first_half_avg * 1.2:
            trend = 'increasing'
            avg_daily_sales = second_half_avg  # Use recent trend
        elif second_half_avg < first_half_avg * 0.8:
            trend = 'decreasing'
            avg_daily_sales = second_half_avg
        
        # 30-day prediction
        total_30_day = round(avg_daily_sales * 30)
        weekly_breakdown = [round(avg_daily_sales * 7) for _ in range(4)]
        
        confidence = 'high' if len(sales_history) > 20 else 'medium' if len(sales_history) > 10 else 'low'
        
        return {
            'total_30_day_demand': total_30_day,
            'weekly_breakdown': weekly_breakdown,
            'avg_daily_sales': round(avg_daily_sales, 2),
            'confidence': confidence,
            'trend': trend
        }
    
    def get_expiry_predictions(self):
        """Get medicines that will expire soon"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        today = datetime.now()
        thirty_days = (today + timedelta(days=30)).strftime('%Y-%m-%d')
        sixty_days = (today + timedelta(days=60)).strftime('%Y-%m-%d')
        ninety_days = (today + timedelta(days=90)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT id, name, quantity, expiry_date, price
            FROM medicines
            WHERE expiry_date <= ?
            ORDER BY expiry_date
        ''', (ninety_days,))
        
        medicines = cursor.fetchall()
        conn.close()
        
        expiry_list = []
        for med_id, name, quantity, expiry_date, price in medicines:
            expiry_dt = datetime.strptime(expiry_date, '%Y-%m-%d')
            days_until_expiry = (expiry_dt - today).days
            
            # Get sales velocity
            sales_history = self.get_sales_history(med_id, days=30)
            if sales_history:
                total_qty = sum(qty for _, qty in sales_history)
                avg_daily_sales = total_qty / len(sales_history)
                days_to_sell = quantity / avg_daily_sales if avg_daily_sales > 0 else 999
            else:
                avg_daily_sales = 0
                days_to_sell = 999
            
            # Determine risk level
            if days_until_expiry < 0:
                risk = 'expired'
                action = 'REMOVE IMMEDIATELY'
            elif days_until_expiry <= 30:
                if days_to_sell > days_until_expiry:
                    risk = 'critical'
                    action = 'Discount or dispose'
                else:
                    risk = 'warning'
                    action = 'Monitor closely'
            elif days_until_expiry <= 60:
                risk = 'caution'
                action = 'Increase promotion'
            else:
                risk = 'low'
                action = 'Normal sales'
            
            potential_loss = quantity * price if days_to_sell > days_until_expiry else 0
            
            expiry_list.append({
                'medicine_id': med_id,
                'medicine_name': name,
                'quantity': quantity,
                'expiry_date': expiry_date,
                'days_until_expiry': days_until_expiry,
                'avg_daily_sales': round(avg_daily_sales, 2),
                'days_to_sell': round(days_to_sell, 1),
                'risk_level': risk,
                'action': action,
                'potential_loss': round(potential_loss, 2)
            })
        
        return expiry_list
    
    def get_top_selling_drugs(self, limit=10, days=30):
        """Get top-selling medicines"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT m.id, m.name, m.category, 
                   SUM(s.quantity) as total_sold,
                   SUM(s.total_price) as total_revenue,
                   COUNT(s.id) as transaction_count
            FROM medicines m
            JOIN sales s ON m.id = s.medicine_id
            WHERE s.sale_date >= ?
            GROUP BY m.id
            ORDER BY total_sold DESC
            LIMIT ?
        ''', (date_threshold, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        top_sellers = []
        for med_id, name, category, total_sold, revenue, transactions in results:
            avg_per_transaction = total_sold / transactions if transactions > 0 else 0
            
            top_sellers.append({
                'medicine_id': med_id,
                'medicine_name': name,
                'category': category,
                'total_sold': total_sold,
                'total_revenue': round(revenue, 2),
                'transaction_count': transactions,
                'avg_per_transaction': round(avg_per_transaction, 2)
            })
        
        return top_sellers
    
    def get_slow_moving_drugs(self, limit=10, days=30):
        """Get slow-moving medicines"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Get all medicines with their sales
        cursor.execute('''
            SELECT m.id, m.name, m.category, m.quantity, m.price,
                   COALESCE(SUM(s.quantity), 0) as total_sold
            FROM medicines m
            LEFT JOIN sales s ON m.id = s.medicine_id AND s.sale_date >= ?
            GROUP BY m.id
            HAVING m.quantity > 0
            ORDER BY total_sold ASC, m.quantity DESC
            LIMIT ?
        ''', (date_threshold, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        slow_movers = []
        for med_id, name, category, quantity, price, total_sold in results:
            inventory_value = quantity * price
            turnover_rate = (total_sold / quantity * 100) if quantity > 0 else 0
            
            # Determine status
            if total_sold == 0:
                status = 'no_sales'
                recommendation = 'Consider promotion or discontinue'
            elif turnover_rate < 10:
                status = 'very_slow'
                recommendation = 'Reduce stock, increase marketing'
            elif turnover_rate < 30:
                status = 'slow'
                recommendation = 'Monitor and promote'
            else:
                status = 'moderate'
                recommendation = 'Maintain current strategy'
            
            slow_movers.append({
                'medicine_id': med_id,
                'medicine_name': name,
                'category': category,
                'current_stock': quantity,
                'total_sold': total_sold,
                'inventory_value': round(inventory_value, 2),
                'turnover_rate': round(turnover_rate, 2),
                'status': status,
                'recommendation': recommendation
            })
        
        return slow_movers
    
    def get_all_predictions(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM medicines')
        medicines = cursor.fetchall()
        conn.close()
        
        predictions = []
        for med_id, med_name in medicines:
            pred = self.predict_stock_needs(med_id)
            pred['medicine_id'] = med_id
            pred['medicine_name'] = med_name
            predictions.append(pred)
        
        return predictions
