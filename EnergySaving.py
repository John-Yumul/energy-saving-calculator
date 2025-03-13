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
        "BATELEC": 11.8569,
        "MERALCO": 12.0262
    }
    
    APPLIANCE_DATABASE = {
        "Air Conditioner": 1.5,  # kW
        "Refrigerator": 0.2,
        "Washing Machine": 0.5,
        "Microwave": 1.2,
        "Electric Fan": 0.075,
        "Iron": 1.0,
        "Television": 0.1,
        "Laptop": 0.05,
        "Desktop Computer": 0.2,
        "Water Heater": 3.0,
        "Toaster": 0.8,
        "Blender": 0.3,
        "Rice Cooker": 0.6,
        "Electric Kettle": 1.5
    }
    
    def __init__(self, power, time, appliance, company):
        self.power = power
        self.time = time
        self.appliance = appliance
        self.company = company.upper()
    
    def calculate_energy(self):
        return self.power * self.time
    
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
        while True:
            print("\n=================================")
            print("Welcome to the Energy Calculator!")
            print("=================================")
            print("1. Enter power manually")
            print("2. Choose an appliance")
            print("3. Exit")
            print("---------------------------------")
            choice = input("Select an option: ").strip()
            
            if choice == "3":
                print("Exiting program. Goodbye!")
                break
            
            if choice == "2":
                print("\n=================================")
                print("Available appliances:")
                print("=================================")
                for i, appliance in enumerate(EnergyCalculator.APPLIANCE_DATABASE.keys(), 1):
                    print(f"{i}. {appliance}")
                print("---------------------------------")
                appliance_choice = input("Choose an appliance by number: ")
                appliance_list = list(EnergyCalculator.APPLIANCE_DATABASE.keys())
                
                if not appliance_choice.isdigit() or int(appliance_choice) not in range(1, len(appliance_list) + 1):
                    print("Invalid selection. Try again.")
                    continue
                
                appliance = appliance_list[int(appliance_choice) - 1]
                power = EnergyCalculator.APPLIANCE_DATABASE[appliance]
                power_unit = "kW"
            elif choice == "1":
                print("\n=================================")
                appliance = input("Enter the appliance name: ")
                power = float(input("Enter power value: "))
                power_unit = input("Enter power unit (W, kW, HP): ")
            else:
                print("Invalid selection. Try again.")
                continue
            
            print("\n=================================")
            time = float(input("Enter time value: "))
            time_unit = input("Enter time unit (seconds, minutes, hours): ")
            company = input("Choose company (BATELEC/MERALCO): ").upper()
            
            converter = UnitConverter()
            power_kW = converter.convert_power_units(power, power_unit, 'kW')
            time_hours = converter.convert_time_units(time, time_unit, 'hours')
            
            calculator = EnergyCalculator(power_kW, time_hours, appliance, company)
            energy = calculator.calculate_energy()
            cost = calculator.calculate_cost()
            
            print("\n=================================")
            print(f"Appliance: {appliance}")
            print(f"Energy consumed: {energy:.2f} kWh ({company} rates applied)")
            print(f"Estimated Cost: ₱{cost:.2f}")
            print("=================================")
            
            report_generator = ReportGenerator()
            report_generator.generate_report(appliance, energy, cost, company)
            
            input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    UserInterface().run()
