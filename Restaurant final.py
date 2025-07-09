from queue import Queue
from collections import namedtuple
import json
class MenuItem:
    def __init__(self, name: str, price: float, is_vegan: bool = False):
        self.name = name
        self.price = price
        self.is_vegan = is_vegan

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_price(self):
        return self.price

    def set_price(self, price: float):
        self.price = price

    def get_is_vegan(self):
        return self.is_vegan

    def set_is_vegan(self, is_vegan: bool):
        self.is_vegan = is_vegan

    def is_vegan_item(self):
        return self.is_vegan

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "is_vegan": self.is_vegan,
            "type": self.__class__.__name__
        }


class Appetizer(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)

    def __str__(self):
        return f"Appetizer: {self.name}, Price: {self.price}"


class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, protein: str, grains: str, vegetables: str):
        super().__init__(name, price)
        self.protein = protein
        self.grains = grains
        self.vegetables = vegetables

    def get_protein(self):
        return self.protein

    def set_protein(self, protein: str):
        self.protein = protein

    def get_grains(self):
        return self.grains

    def set_grains(self, grains: str):
        self.grains = grains

    def get_vegetables(self):
        return self.vegetables

    def set_vegetables(self, vegetables: str):
        self.vegetables = vegetables

    def __str__(self):
        return (f"Main Course: {self.name}, Price: {self.price}, "
                f"Protein: {self.protein}, Grains: {self.grains}, Vegetables: {self.vegetables}")

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "protein": self.protein,
            "grains": self.grains,
            "vegetables": self.vegetables
        })
        return base


class Beverage(MenuItem):
    def __init__(self, name: str, price: float, size: str, beverage_type: str):
        super().__init__(name, price)
        self.size = size
        self.beverage_type = beverage_type

    def get_size(self):
        return self.size

    def set_size(self, size: str):
        self.size = size

    def get_beverage_type(self):
        return self.beverage_type

    def set_beverage_type(self, beverage_type: str):
        self.beverage_type = beverage_type

    def __str__(self):
        return (f"Beverage: {self.name}, Price: {self.price}, "
                f"Size: {self.size}, Type: {self.beverage_type}")

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "size": self.size,
            "beverage_type": self.beverage_type
        })
        return base


class Dessert(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)

    def __str__(self):
        return f"Dessert: {self.name}, Price: {self.price}"


class Order:
    def __init__(self, items: list[MenuItem]):
        self.items = items

    def add_item(self, item: MenuItem):
        self.items.append(item)
    #discount1: 10% for 15 items, 0.5% for each additional item, max 30%
    def discount1(self) -> float:
        n = len(self.items)
        if n > 15:
            extra_items = n - 15
            discount_percent = 10 + (extra_items * 0.5)
            if discount_percent > 30:
                discount_percent = 30
            return discount_percent
        return 0.0
    #discount2: 50% on beverages (applied later) for more than 3 main courses 
    def discount2(self) -> float:
        main_courses = [item for item in self.items if isinstance(item, MainCourse)]
        if len(main_courses) > 3:
            return 50.0
        return 0.0

    def get_bill(self) -> float:
        total = 0.0
        beverage_discount = self.discount2()
        for item in self.items:
            if isinstance(item, Beverage) and beverage_discount > 0:
                total += item.price * 0.5  # 50% off
            else:
                total += item.price
        discount_percent = self.discount1()
        if discount_percent > 0:
            total -= total * (discount_percent / 100)
        return total

    def __str__(self):
        order_str = "Order\n-------------------\n"
        for item in self.items:
            order_str += str(item) + "\n"
        order_str += f"-------------------\nBeverages: {len([item for item in self.items if isinstance(item, Beverage)])}\n"
        order_str += f"-------------------\nBeverages Price: {sum(item.price for item in self.items if isinstance(item, Beverage))}\n"
        order_str += f"-------------------\nAppetizers: {len([item for item in self.items if isinstance(item, Appetizer)])}\n"
        order_str += f"-------------------\nAppetizers Price: {sum(item.price for item in self.items if isinstance(item, Appetizer))}\n"
        order_str += f"-------------------\nMain Courses: {len([item for item in self.items if isinstance(item, MainCourse)])}\n"
        order_str += f"-------------------\nMain Courses Price: {sum(item.price for item in self.items if isinstance(item, MainCourse))}\n"
        order_str += f"-------------------\nDesserts: {len([item for item in self.items if isinstance(item, Dessert)])}\n"
        order_str += f"-------------------\nDesserts Price: {sum(item.price for item in self.items if isinstance(item, Dessert))}\n"
        order_str += f"-------------------\nTotal Items: {len(self.items)}\n"
        order_str += f"-------------------\nTotal Price: {sum(item.price for item in self.items)}\n"
        order_str += f"-------------------\nOverall Discount: {self.discount1()}%\n"
        order_str += f"-------------------\nNet Total: {self.get_bill():.2f}\n-------------------"
        return order_str
    
class Payment:
    def __init__(self):
        pass

    def pay(self, amount: float):
        raise NotImplementedError("pay() should be implemented in subclasses.")
    
class CardPayment(Payment):
    def __init__(self, card_number: str, cvv: str):
        super().__init__()
        self.__card_number = card_number
        self.__cvv = cvv

    def set_card_number(self, card_number: str):
        self.__card_number = card_number

    def get_card_number(self) -> str:
        return self.__card_number

    def set_cvv(self, cvv: str):
        self.__cvv = cvv

    def get_cvv(self) -> str:
        return self.__cvv

    def pay(self, amount: float):
        print(f"Paid {amount:.2f} using card ************{self.__card_number[-4:]}")

class CashPayment(Payment):
    def __init__(self, amount_given: float):
        super().__init__()
        self.amount_given = amount_given

    def pay(self, amount: float):
        if self.amount_given >= amount:
            print(f"Paid {amount:.2f} in cash. Change: {(self.amount_given - amount):.2f}")
        else:
            print(f"Not enough cash provided. Amount due: {(amount - self.amount_given):.2f}")

#RETO7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Menu = namedtuple("Menu", ["name", "items"])

def default_menu():
    menu = {}
    menu["Empanadas"] = Appetizer("Empanadas", 3.50)
    menu["Cheese Sticks"] = Appetizer("Cheese Sticks", 4.00)
    menu["Mini Burgers"] = Appetizer("Mini Burgers", 5.00)
    menu["Mini Waffles"] = Appetizer("Mini Waffles", 2.50)
    menu["Salchipapa"] = Appetizer("Salchipapa", 5.00)
    menu["Baby Beef"] = MainCourse("Baby Beef", 10.00, "Beef", "Rice", "Salad")
    menu["Cordon Blue"] = MainCourse("Cordon Blue", 12.00, "Chicken", "Potatoes", "Salad")
    menu["Salmon"] = MainCourse("Salmon", 15.00, "Fish", "Quinoa", "Lettuce")
    menu["Burger"] = MainCourse("Burger", 8.00, "Beef", "Bread", "Onion")
    menu["Coca Cola"] = Beverage("Coca Cola", 2.00, "Medium", "Soda")
    menu["Orange Juice"] = Beverage("Orange Juice", 3.00, "Large", "Juice")
    menu["Quatro"] = Beverage("Quatro", 2.50, "Small", "Soda")
    menu["Chocolate Milkshake"] = Beverage("Chocolate Milkshake", 4.00, "Large", "Milkshake")
    menu["Chocolate Cake"] = Dessert("Chocolate Cake", 5.00)
    menu["Nutella Waffles"] = Dessert("Nutella Waffles", 6.00)
    menu["Flan"] = Dessert("Flan", 4.00)
    menu["Lemon Cheesecake"] = Dessert("Lemon Cheesecake", 5.00)
    return menu

default = Menu(name="Default Menu", items=default_menu())
 
def menucreator():
    menu = {}
    while True:
        item = input("Insert the item's name:\n")
        price = float(input("Insert the item's price:\n"))
        selec = input(
            "Write the correspondent number for this item's type:\n"
            "1) Appetizer\n"
            "2) MainCourse\n"
            "3) Beverage\n"
            "4) Dessert\n"
        )
        match selec:
            case "1":
                menu[item] = Appetizer(item, price)
            case "2":
                protein = input("Enter the protein for this main course:\n")
                grains = input("Enter the grains for this main course:\n")
                vegetables = input("Enter the vegetables for this main course:\n")
                menu[item] = MainCourse(item, price, protein, grains, vegetables)
            case "3":
                size = input("Enter the size of the beverage:\n")
                beverage_type = input("Enter the type of beverage:\n")
                menu[item] = Beverage(item, price, size, beverage_type)
            case "4":
                menu[item] = Dessert(item, price)
            case _:
                print("What? try again.")
        conf = input("Add another item? (y/n):\n")
        if conf.lower() != "y":
            break
    return menu

def create_and_store_menu():
    menuname = input("Write the name of the menu:\n")
    items = menucreator()
    menu = Menu(name=menuname, items=items)
    return menu

def modify_menu(menus):
        for menu in menus:
            print(f"Menu name: {menu.name}")
            print("Items:")
            for item_name, item_obj in menu.items.items():
                print(f"  {item_name}: {item_obj}")
        modify = input("Do you want to modify a menu? (y/n):\n")
        if modify.lower() == "y":
            while True:
                menu_name = input("Enter the name of the menu to modify (or type 'exit' to go back):\n")
                if menu_name.lower() == "exit":
                    return
                for menu in menus:
                    if menu.name == menu_name:
                        print("Current items:")
                        for item_name, item_obj in menu.items.items():
                            print(f"  {item_name}: {item_obj}")
                        while True:
                            print("What do you want to do with this menu?")
                            select = input("1) Add item"
                                           "\n2) Remove item"
                                           "\n3) Modify item"
                                           "\n4) Exit menu modification\n")
                            match select:
                                case "1":
                                    item_name = input("Enter the name of the new item:\n")
                                    price = float(input("Enter the price of the new item:\n"))
                                    item_type = input("Enter the type of the new item (Appetizer/MainCourse/Beverage/Dessert):\n")
                                    if item_type == "Appetizer":
                                        menu.items[item_name] = Appetizer(item_name, price)
                                    elif item_type == "MainCourse":
                                        protein = input("Enter the protein for this main course:\n")
                                        grains = input("Enter the grains for this main course:\n")
                                        vegetables = input("Enter the vegetables for this main course:\n")
                                        menu.items[item_name] = MainCourse(item_name, price, protein, grains, vegetables)
                                    elif item_type == "Beverage":
                                        size = input("Enter the size of the beverage:\n")
                                        beverage_type = input("Enter the type of beverage:\n")
                                        menu.items[item_name] = Beverage(item_name, price, size, beverage_type)
                                    elif item_type == "Dessert":
                                        menu.items[item_name] = Dessert(item_name, price)
                                    else:
                                        print("Invalid item type.")
                                case "2":
                                    remove_item = input("Enter the name of the item to remove:\n")
                                    if remove_item in menu.items:
                                        del menu.items[remove_item]
                                        print(f"Item '{remove_item}' removed.")
                                    else:
                                        print(f"Item '{remove_item}' not found in menu '{menu.name}'.")
                                case "3":
                                    modify_item = input("Enter the name of the item to modify:\n")
                                    if modify_item in menu.items:
                                        new_name = input(f"Enter new name for {modify_item} (leave blank to keep current name):\n")
                                        new_price = float(input(f"Enter new price for {modify_item}:\n"))
                                        menu.items[modify_item].set_price(new_price)
                                        if new_name and new_name != modify_item:
                                            menu.items[modify_item].set_name(new_name)
                                            menu.items[new_name] = menu.items.pop(modify_item)
                                            print(f"Item '{modify_item}' updated to '{new_name}' with new price {new_price}.")
                                        else:
                                            print(f"Item '{modify_item}' updated with new price {new_price}.")
                                    else:
                                        print(f"Item '{modify_item}' not found in menu '{menu.name}'.")
                                case "4":
                                    print("Exiting menu modification.")
                                    break
                                case _:
                                    print("Invalid selection. Please choose again.")
                        break  # Exit the for-loop after modifying the menu
                else:
                    print(f"Menu '{menu_name}' not found. Please try again.")

def make_order(menus, order_queue):
    while True:
        print("\nOrder Menu:")
        print("1) Place a new order")
        print("2) Serve next order in queue")
        print("3) Check if order queue is full")
        print("4) Back to main menu")
        choice = input("Choose an option: ")

        match choice:
            case "1":
                if order_queue.full():
                    print("Order queue is full! Cannot place a new order right now.")
                    continue
                if len(menus) == 0:
                    print("No menus available to order from.")
                    continue
                print("Available menus:")
                for i, menu in enumerate(menus, 1):
                    print(f"{i}) {menu.name}")
                menu_choice = input("Enter the number of the menu you'd like to order from:\n")
                try:
                    menu_i = int(menu_choice) - 1
                    selected_menu = menus[menu_i]
                except (ValueError, IndexError):
                    print("Invalid menu selection.")
                    continue

                print(f"\nItems in '{selected_menu.name}':")
                item_list = list(selected_menu.items.items())
                for idx, (item_name, item_obj) in enumerate(item_list, 1):
                    print(f"{idx}) {item_name} - {item_obj}")

                order_items = []
                while True:
                    item_choice = input("Enter the number of the item to add to your order (or 'done' to finish):\n")
                    if item_choice.lower() == "done":
                        break
                    try:
                        item_j = int(item_choice) - 1
                        item_obj = item_list[item_j][1]
                        order_items.append(item_obj)
                        print(f"Added {item_obj.name} to your order.")
                    except (ValueError, IndexError):
                        print("Invalid item selection.")

                if not order_items:
                    print("No items selected for the order.")
                    continue

                order = Order(order_items)
                order_queue.put(order)
                print("\nYour order has been placed and added to the queue!")
                print(order)

            case "2":
                if order_queue.empty():
                    print("No orders to serve.")
                else:
                    next_order = order_queue.get()
                    print("\nServing order:")
                    print(next_order)
                    payment_method = input("Payment method? (card/cash): ")
                    if payment_method == "card":
                        card = CardPayment(input("Card number: "), input("CVV: "))
                        card.pay(next_order.get_bill())
                    elif payment_method == "cash":
                        amount = float(input("Amount given: "))
                        cash = CashPayment(amount)
                        cash.pay(next_order.get_bill())
                    else:
                        print("Unknown payment method.")

            case "3":
                if order_queue.full():
                    print("The order queue is FULL (Serve them!!!).")
                else:
                    print("The order queue is NOT FULL (Order some more!!!).")

            case "4":
                print("Returning to main menu.")
                break

            case _:
                print("Invalid selection. Please choose again.")

def export_menus(menus, filename=r"C:\Users\danie\Downloads\menus.json"):
    json_menus = []
    for menu in menus:
        json_menu = {
            "name": menu.name,
            "items": {name: item.to_dict() for name, item in menu.items.items()}
        }
        json_menus.append(json_menu)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_menus, f, indent=4)
    print(f"Menus exported to {filename}")

def mainrestaurant():
    menus = [default]
    while True:
            selec = input("Welcome to my restaurant!, please, write the number of the thing you'd like to do:\n"
                          "1) Create a new menu.\n"
                          "2) Look at menus and modify them.\n"
                          "3) Make an order\n"
                          "4) Export menus\n"
                          "5) Exit the restaurant\n")
            match selec:
                case "1":
                    print("Create a new menu?, but it's my restaurant...\n")
                    menu = create_and_store_menu()
                    menus.append(menu)
                    print(f"Menu '{menu.name}' created with {len(menu.items)} items.")
                case "2":
                    print("Look at menus and modify them? Sure, a costumer modifying menus...\n")
                    modify_menu(menus)
                case "3":
                    make_order(menus, order_queue=Queue(maxsize=3))
                case "4":
                    print("Exporting menus to JSON files? That's espionage!\n")
                    export_menus(menus, filename="menus.json")
                case "5":
                    print("Exiting the restaurant...\n"
                    "weird costumer huh?")
                    break
                case _:
                    print("Invalid selection. Please choose again.")

if __name__ == "__main__":
    mainrestaurant()