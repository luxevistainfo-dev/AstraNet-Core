import time
import random
import json
import hashlib
from datetime import datetime

class GreenMiningOptimizer:
    """Green mining optimizer"""
    
    def __init__(self):
        self.total_energy_saved = 0
        self.carbon_offset = 0
        self.renewable_percentage = 0
        self.mining_nodes = {}
        self.energy_sources = {}
        self.start_time = time.time()
        
        self._init_energy_sources()
    
    def _init_energy_sources(self):
        """Initialize renewable energy sources"""
        self.energy_sources = {
            'solar': {
                'capacity': random.randint(100, 500),
                'current_output': 0,
                'efficiency': random.uniform(0.8, 0.95),
                'cost_per_kwh': 0.05
            },
            'wind': {
                'capacity': random.randint(200, 800),
                'current_output': 0,
                'efficiency': random.uniform(0.7, 0.9),
                'cost_per_kwh': 0.03
            },
            'hydro': {
                'capacity': random.randint(300, 1000),
                'current_output': 0,
                'efficiency': random.uniform(0.85, 0.98),
                'cost_per_kwh': 0.02
            },
            'fossil': {
                'capacity': 1000,
                'current_output': 0,
                'efficiency': random.uniform(0.3, 0.5),
                'cost_per_kwh': 0.12,
                'carbon_per_kwh': 0.5
            }
        }
    
    def optimize_mining(self, mining_power, urgency='medium'):
        """Optimize mining operation for minimal carbon footprint"""
        print(f"\n🌿 Optimizing mining for {mining_power}kW ({urgency} urgency)")
        
        renewable_available = self._calculate_renewable_availability()
        allocation = self._optimize_allocation(mining_power, renewable_available, urgency)
        
        carbon_saved = self._calculate_carbon_savings(allocation)
        self.carbon_offset += carbon_saved
        
        energy_saved = self._calculate_energy_savings(allocation)
        self.total_energy_saved += energy_saved
        
        self._update_renewable_percentage()
        
        return {
            'allocation': allocation,
            'carbon_saved_kg': round(carbon_saved, 2),
            'energy_saved_kwh': round(energy_saved, 2),
            'total_carbon_offset_kg': round(self.carbon_offset, 2),
            'renewable_percentage': round(self.renewable_percentage, 1),
            'cost_per_hour': round(self._calculate_cost(allocation), 2),
            'optimization_time': datetime.now().strftime("%H:%M:%S")
        }
    
    def _calculate_renewable_availability(self):
        """Calculate renewable energy availability"""
        availability = {}
        
        for source, data in self.energy_sources.items():
            if source != 'fossil':
                hour = datetime.now().hour
                
                if source == 'solar':
                    availability[source] = data['capacity'] * (0.3 + 0.7 * abs(12 - hour) / 12)
                elif source == 'wind':
                    availability[source] = data['capacity'] * random.uniform(0.4, 0.9)
                elif source == 'hydro':
                    availability[source] = data['capacity'] * random.uniform(0.8, 1.0)
                
                availability[source] *= data['efficiency']
                availability[source] = round(availability[source], 2)
        
        return availability
    
    def _optimize_allocation(self, needed_power, renewable_available, urgency):
        """Optimize energy allocation"""
        allocation = {}
        remaining_power = needed_power
        
        for source, available in renewable_available.items():
            if remaining_power <= 0:
                break
            
            allocated = min(available, remaining_power)
            allocation[source] = allocated
            remaining_power -= allocated
        
        if remaining_power > 0:
            fossil_available = self.energy_sources['fossil']['capacity'] * 0.8
            allocated = min(fossil_available, remaining_power)
            allocation['fossil'] = allocated
            remaining_power -= allocated
        
        if remaining_power > 0 and urgency == 'high':
            allocation['fossil'] = allocation.get('fossil', 0) + remaining_power
        
        return allocation
    
    def _calculate_carbon_savings(self, allocation):
        """Calculate carbon emission savings"""
        carbon_saved = 0
        
        for source, amount in allocation.items():
            if source != 'fossil':
                carbon_saved += amount * self.energy_sources['fossil']['carbon_per_kwh']
        
        return carbon_saved
    
    def _calculate_energy_savings(self, allocation):
        """Calculate total energy savings"""
        energy_saved = 0
        
        for source, amount in allocation.items():
            if source != 'fossil':
                fossil_efficiency = self.energy_sources['fossil']['efficiency']
                source_efficiency = self.energy_sources.get(source, {}).get('efficiency', 0.9)
                
                if source_efficiency > fossil_efficiency:
                    energy_saved += amount * (source_efficiency - fossil_efficiency)
        
        return energy_saved
    
    def _update_renewable_percentage(self):
        """Update renewable energy percentage"""
        total_energy = sum(self.energy_sources[s]['capacity'] for s in self.energy_sources)
        renewable_energy = sum(self.energy_sources[s]['capacity'] 
                              for s in self.energy_sources if s != 'fossil')
        
        if total_energy > 0:
            self.renewable_percentage = (renewable_energy / total_energy) * 100
    
    def _calculate_cost(self, allocation):
        """Calculate energy cost"""
        total_cost = 0
        
        for source, amount in allocation.items():
            cost_per_kwh = self.energy_sources.get(source, {}).get('cost_per_kwh', 0.1)
            total_cost += amount * cost_per_kwh
        
        return total_cost
    
    def add_mining_node(self, node_id, location, max_power):
        """Add new mining node"""
        self.mining_nodes[node_id] = {
            'location': location,
            'max_power': max_power,
            'current_power': 0,
            'renewable_usage': 0,
            'carbon_footprint': 0,
            'uptime': 0,
            'added_time': time.time()
        }
        
        print(f"✅ Mining node added: {node_id} at {location}")
        return self.mining_nodes[node_id]
    
    def get_environmental_stats(self):
        """Get environmental statistics"""
        total_uptime = time.time() - self.start_time
        
        return {
            'total_energy_saved_kwh': round(self.total_energy_saved, 2),
            'total_carbon_offset_kg': round(self.carbon_offset, 2),
            'renewable_percentage': round(self.renewable_percentage, 1),
            'equivalent_trees': round(self.carbon_offset / 21.77, 1),
            'mining_nodes': len(self.mining_nodes),
            'total_uptime_hours': round(total_uptime / 3600, 2),
            'energy_sources': list(self.energy_sources.keys()),
            'avg_cost_per_kwh': round(self._calculate_avg_cost(), 3)
        }
    
    def _calculate_avg_cost(self):
        """Calculate average cost per kWh"""
        total_cost = 0
        total_capacity = 0
        
        for source, data in self.energy_sources.items():
            total_cost += data['capacity'] * data['cost_per_kwh']
            total_capacity += data['capacity']
        
        if total_capacity > 0:
            return total_cost / total_capacity
        return 0.1

def simulate_mining_scenario():
    """Simulate mining scenario for demonstration"""
    optimizer = GreenMiningOptimizer()
    
    optimizer.add_mining_node('node_1', 'Solar Farm California', 300)
    optimizer.add_mining_node('node_2', 'Wind Park Texas', 450)
    optimizer.add_mining_node('node_3', 'Hydro Plant Norway', 600)
    
    return optimizer
