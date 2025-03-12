import datetime
import csv

class UnitConverter:
    def convert_power_units(self, power, from_unit, to_unit):
        conversion_factors = {
            ('W', 'kW'): 0.001,
            ('kW', 'W'): 1000,
            ('HP', 'W'): 745.7,
            ('W', 'HP'): 1/745.7
        }
        return power * conversion_factors.get((from_unit, to_unit), 1)
    
    def convert_time_units(self, time, from_unit, to_unit):
        conversion_factors = {
            ('seconds', 'minutes'): 1/60,
            ('minutes', 'seconds'): 60,
            ('minutes', 'hours'): 1/60,
            ('hours', 'minutes'): 60
        }
        return time * conversion_factors.get((from_unit, to_unit), 1)

class EnergyCalculator:
    COMPANY_RATES = {
        "BATELEC": 11.8569,  # Updated rate per kWh in currency
        "MERALCO": 12.0262
    }
    
    def __init__(self, power, time, appliance, company):
        self.power = power
        self.time = time
        self.appliance = appliance
        self.company = company.upper()
    
    def calculate_energy(self):
        return self.power * self.time  # Energy (kWh) = Power (kW) * Time (h)
    
    def calculate_cost(self):
        energy = self.calculate_energy()
        rate = self.COMPANY_RATES.get(self.company, 0)
        return energy * rate

class ReportGenerator:
    def generate_report(self, appliance, energy, cost, company):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_data = [[timestamp, appliance, f"{energy:.2f} kWh", company, f"{cost:.2f}"]]
        
        with open("energy_report.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Appliance", "Energy Consumed", "Company", "Estimated Cost"])
            writer.writerows(report_data)
        
        print("\nReport saved as 'energy_report.csv'.")

class UserInterface:
    def run(self):
        print("Welcome to the Energy Calculator!")
        appliance = input("Enter the appliance name: ")
        power = float(input("Enter power value: "))
        power_unit = input("Enter power unit (W, kW, HP): ")
        time = float(input("Enter time value: "))
        time_unit = input("Enter time unit (seconds, minutes, hours): ")
        company = input("Choose company (BATELEC/MERALCO): ").upper()
        
        converter = UnitConverter()
        power_kW = converter.convert_power_units(power, power_unit, 'kW')
        time_hours = converter.convert_time_units(time, time_unit, 'hours')
        
        calculator = EnergyCalculator(power_kW, time_hours, appliance, company)
        energy = calculator.calculate_energy()
        cost = calculator.calculate_cost()
        
        print(f"Appliance: {appliance}")
        print(f"Energy consumed: {energy:.2f} kWh ({company} rates apply)")
        print(f"Estimated Cost: {cost:.2f} currency units")
        
        report_generator = ReportGenerator()
        report_generator.generate_report(appliance, energy, cost, company)

if __name__ == "__main__":
    UserInterface().run()