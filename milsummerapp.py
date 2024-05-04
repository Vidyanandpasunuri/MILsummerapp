from enum import Enum
from datetime import datetime

class SolderType(Enum):
    LEAD = 1
    LEAD_FREE = 2
    ROSIN_CORE = 3
    ACID_CORE = 4

class DisplayType(Enum):
    HDMI = 1
    VGA = 2
    DISPLAYPORT = 3
    MICRO_HDMI = 4

class EthernetAlphaType(Enum):
    MALE = 1
    FEMALE = 2

class EthernetBetaType(Enum):
    MALE = 1
    FEMALE = 2

class EthernetSpeed(Enum):
    MBPS_10 = 1
    MBPS_100 = 2
    GBPS_1 = 3
    GBPS_10 = 4

class PartCharacteristics:
    def __init__(self, sku, last_updated):
        self.sku = sku
        self.last_updated = last_updated

class Resistor(PartCharacteristics):
    def __init__(self, sku, last_updated, resistance, tolerance):
        super().__init__(sku, last_updated)
        self.resistance = resistance
        self.tolerance = tolerance

class Solder(PartCharacteristics):
    def __init__(self, sku, last_updated, solder_type, length):
        super().__init__(sku, last_updated)
        self.solder_type = solder_type
        self.length = length

class Wire(PartCharacteristics):
    def __init__(self, sku, last_updated, gauge, length):
        super().__init__(sku, last_updated)
        self.gauge = gauge
        self.length = length

class DisplayCable(PartCharacteristics):
    def __init__(self, sku, last_updated, cable_type, length, color):
        super().__init__(sku, last_updated)
        self.cable_type = cable_type
        self.length = length
        self.color = color

class EthernetCable(PartCharacteristics):
    def __init__(self, sku, last_updated, alpha_type, beta_type, speed, length):
        super().__init__(sku, last_updated)
        self.alpha_type = alpha_type
        self.beta_type = beta_type
        self.speed = speed
        self.length = length

class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def add_part(self, part):
        self.inventory[part.sku] = part

    def add_inventory(self, sku, quantity):
        if sku in self.inventory:
            self.inventory[sku].quantity += quantity
        else:
            raise ValueError("Part not found.")

    def get_inventory(self):
        return self.inventory

    def search(self, part_type, **criteria):
        results = []
        for part in self.inventory.values():
            if isinstance(part, part_type):
                match = all(getattr(part, key) == value for key, value in criteria.items())
                if match:
                    results.append(part)
        return results

    def delete_part(self, sku):
        if sku in self.inventory:
            del self.inventory[sku]
        else:
            raise ValueError("Part not found.")

def display_menu():
    """
    Displays the menu options for the inventory management system.
    """
    print("\nInventory Management System")
    print("1. Add Part")
    print("2. Add Inventory")
    print("3. View Inventory")
    print("4. Search Parts")
    print("5. Delete Part")
    print("6. Exit")

def add_part(manager):
    """
    Adds a new part to the inventory.

    Args:
        manager (InventoryManager): An instance of the InventoryManager class.
    """
    sku = int(input("Enter SKU: "))
    part_type = input("Enter Part Type (Resistor/Solder/Wire/Display Cable/Ethernet Cable): ").lower()

    if part_type == "resistor":
        resistance = int(input("Enter Resistance (Ohms): "))
        tolerance = int(input("Enter Tolerance (%): "))
        part = Resistor(sku=sku, last_updated=datetime.now(), resistance=resistance, tolerance=tolerance)
    elif part_type == "solder":
        solder_type = input("Enter Solder Type (Lead/Lead-Free/Rosin-Core/Acid-Core): ")
        length = float(input("Enter Length (inches): "))
        part = Solder(sku=sku, last_updated=datetime.now(), solder_type=SolderType[solder_type.upper()], length=length)
    elif part_type == "wire":
        gauge = float(input("Enter Gauge: "))
        length = float(input("Enter Length (inches): "))
        part = Wire(sku=sku, last_updated=datetime.now(), gauge=gauge, length=length)
    elif part_type == "display cable":
        cable_type = input("Enter Cable Type (HDMI/VGA/DISPLAYPORT/MICRO HDMI): ")
        length = float(input("Enter Length (inches): "))
        color = input("Enter Color (Hexadecimal format, e.g., #RRGGBB): ")
        part = DisplayCable(sku=sku, last_updated=datetime.now(), cable_type=DisplayType[cable_type.upper()], length=length, color=color)
    elif part_type == "ethernet cable":
        alpha_type = input("Enter Alpha Type (MALE/FEMALE): ")
        beta_type = input("Enter Beta Type (MALE/FEMALE): ")
        speed = input("Enter Speed (10MBPS/100MBPS/1GBPS/10GBPS): ")
        length = float(input("Enter Length (inches): "))
        part = EthernetCable(sku=sku, last_updated=datetime.now(), alpha_type=EthernetAlphaType[alpha_type.upper()], beta_type=EthernetBetaType[beta_type.upper()], speed=EthernetSpeed[speed.upper()], length=length)
    else:
        print("Invalid part type.")
        return

    manager.add_part(part)
    print("Part added successfully.")

def add_inventory(manager):
    """
    Adds inventory for an existing part.

    Args:
        manager (InventoryManager): An instance of the InventoryManager class.
    """
    sku = int(input("Enter SKU of the part: "))
    quantity = int(input("Enter quantity to add: "))
    try:
        manager.add_inventory(sku, quantity)
        print("Inventory updated successfully.")
    except ValueError as e:
        print(e)

def view_inventory(manager):
    """
    Displays the current inventory.

    Args:
        manager (InventoryManager): An instance of the InventoryManager class.
    """
    inventory = manager.get_inventory()
    if not inventory:
        print("Inventory is empty.")
    else:
        print("\nCurrent Inventory:")
        for sku, part in inventory.items():
            print(f"SKU: {sku}, Part: {part.__class__.__name__}, Quantity: {part.quantity}")

def search_parts(manager):
    """
    Searches for parts based on user-specified criteria.

    Args:
        manager (InventoryManager): An instance of the InventoryManager class.
    """
    part_type = input("Enter Part Type (Resistor/Solder/Wire/Display Cable/Ethernet Cable): ")
    criteria = input("Enter Search Criteria (e.g., resistance=100 for resistors): ")
    try:
        part_class = globals()[part_type]
        criteria_dict = dict([criteria.split("=")])
        results = manager.search(part_class, **criteria_dict)
        if results:
            print("\nSearch Results:")
            for result in results:
                print(result)
        else:
            print("No matching parts found.")
    except KeyError:
        print("Invalid part type.")

def delete_part(manager):
    """
    Deletes a part from the inventory.

    Args:
        manager (InventoryManager): An instance of the InventoryManager class.
    """
    sku = int(input("Enter SKU of the part to delete: "))
    try:
        manager.delete_part(sku)
        print("Part deleted successfully.")
    except ValueError as e:
        print(e)

def main():
    """
    Main function to run the inventory management system.
    """
    manager = InventoryManager()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_part(manager)
        elif choice == "2":
            add_inventory(manager)
        elif choice == "3":
            view_inventory(manager)
        elif choice == "4":
            search_parts(manager)
        elif choice == "5":
            delete_part(manager)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
