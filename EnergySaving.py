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

class UserPreferences:
    def __init__(self, preferred_power_unit='kW', preferred_time_unit='hours'):
        self.preferred_power_unit = preferred_power_unit
        self.preferred_time_unit = preferred_time_unit
    
    def save_preferences(self):
        with open('preferences.txt', 'w') as file:
            file.write(f"{self.preferred_power_unit}\n{self.preferred_time_unit}")
    
    def load_preferences(self):
        try:
            with open('preferences.txt', 'r') as file:
                lines = file.readlines()
                self.preferred_power_unit = lines[0].strip()
                self.preferred_time_unit = lines[1].strip()
        except FileNotFoundError:
            pass

class EnergyCalculator:
    COMPANY_RATES = {
        "BATELEC": 11.8569,
        "MERALCO": 12.0262
    }
    
    APPLIANCE_DATABASE = {
        "Air Conditioner": 1.5,
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
    
    def generate_text_report(self, appliance, energy, cost, company):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_content = f"Timestamp: {timestamp}\nAppliance: {appliance}\nEnergy Consumed: {energy:.2f} kWh\nCompany: {company}\nEstimated Cost: ₱{cost:.2f}\n"
        
        with open("energy_report.txt", "w") as file:
            file.write(report_content)
        
        print("\nReport saved as 'energy_report.txt'.")

class UserInterface:
    def get_input(self, prompt):
        user_input = input(prompt).strip()
        if user_input.lower() == "cancel" or user_input == "0":
            print("Returning to main menu...")
            return None
        return user_input
    
    def run(self):
        while True:
            print("\n=================================")
            print("Welcome to the Energy Calculator!")
            print("=================================")
            print("1. Enter power manually")
            print("2. Choose an appliance")
            print("3. Exit")
            print("---------------------------------")
            choice = self.get_input("Select an option: ")
            
            if choice is None or choice == "3":
                print("Exiting program. Goodbye!")
                break
            
            if choice == "2":
                print("\n=================================")
                print("Available appliances:")
                print("=================================")
                for i, appliance in enumerate(EnergyCalculator.APPLIANCE_DATABASE.keys(), 1):
                    print(f"{i}. {appliance}")
                print("---------------------------------")
                
                appliance_choice = self.get_input("Choose an appliance by number (Press 0 to cancel): ")
                if appliance_choice is None:
                    continue
                
                appliance_list = list(EnergyCalculator.APPLIANCE_DATABASE.keys())
                
                if not appliance_choice.isdigit() or int(appliance_choice) not in range(1, len(appliance_list) + 1):
                    print("Invalid selection. Try again.")
                    continue
                
                appliance = appliance_list[int(appliance_choice) - 1]
                power = EnergyCalculator.APPLIANCE_DATABASE[appliance]
                power_unit = "kW"
            elif choice == "1":
                print("\n=================================")
                print("Press 0 to cancel at any time.")
                appliance = self.get_input("Enter the appliance name (Press 0 to cancel): ")
                if appliance is None:
                    continue
                try:
                    power = float(self.get_input("Enter power value (Press 0 to cancel): "))
                    if power is None:
                        continue
                    power_unit = self.get_input("Enter power unit (W, kW, HP) (Press 0 to cancel): ")
                    if power_unit is None:
                        continue
                except ValueError:
                    print("Invalid input. Try again.")
                    continue
            else:
                print("Invalid selection. Try again.")
                continue
            
            print("\n=================================")
            
            time = self.get_input("Enter time in hours (Press 0 to cancel): ")
            if time is None:
                continue
            try:
                time = float(time)
            except ValueError:
                print("Invalid time input. Try again.")
                continue
            
            company = self.get_input("Enter your electricity provider (BATELEC/MERALCO) (Press 0 to cancel): ")
            if company is None:
                continue
            
            calculator = EnergyCalculator(power, time, appliance, company)
            energy_used = calculator.calculate_energy()
            cost = calculator.calculate_cost()
            
            print("\n=================================")
            print(f"Appliance: {appliance}")
            print(f"Energy Consumed: {energy_used:.2f} kWh")
            print(f"Estimated Cost: ₱{cost:.2f}")
            print("=================================")
            
            report_generator = ReportGenerator()
            report_generator.generate_report(appliance, energy_used, cost, company)
            report_generator.generate_text_report(appliance, energy_used, cost, company)

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
