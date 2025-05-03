class FuelCalculator:
    def __init__(self):
        self.default_mpg = {
            'car': 25,
            'suv': 20,
            'truck': 18,
            'motorcycle': 45,
            'electric': 0  # No fuel cost
        }
        self.fuel_price_per_gallon = 3.50  # USD
        self.usd_to_krw = 1300  # Approximate conversion rate
    
    def calculate_cost(self, distance_miles, vehicle_type='car', mpg=None):
        if mpg is None:
            mpg = self.default_mpg.get(vehicle_type, 25)
        
        if mpg == 0:  # Electric vehicle
            return "$0 (Electric Vehicle)"
        
        gallons_needed = distance_miles / mpg
        cost_usd = gallons_needed * self.fuel_price_per_gallon
        cost_krw = cost_usd * self.usd_to_krw
        
        return f"${cost_usd:.2f} (₩{cost_krw:,.0f})"
    
    def set_fuel_price(self, price):
        self.fuel_price_per_gallon = price