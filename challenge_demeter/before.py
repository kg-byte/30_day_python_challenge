from dataclasses import dataclass, field
from decimal import Decimal

class ItemNotFoundException(Exception):
    pass

@dataclass
class Item:
    name: str
    price: Decimal
    quantity: int
    
    def update_price(self, new_price: Decimal) -> None:
        self.price = new_price
    
    def update_quantity(self, updated_quantity: int) -> None:
        self.quantity = updated_quantity
    
    @property
    def subtotal(self)-> Decimal:
        return self.price * self.quantity
    

@dataclass
class ShoppingCart:
    items: list[Item] = field(default_factory=list)
    discount_code: str | None = None

    @property
    def total(self) -> Decimal:
        return Decimal(sum(item.subtotal for item in self.items))
    
    def find_item(self, item_name:str):
        for item in self.items:
            if item.name == item_name:
                return item
        raise ItemNotFoundException(f"Item '{item_name}' not found.")
    
    def add_item(self, item: Item)-> None:
        self.items.append(item)
    
    def remove_item(self, item_name: str) -> None:
        found_item = self.find_item(item_name)
        self.items.remove(found_item)
    
    def update_item_quantity(self, item_name: str, updated_quantity: int)->None:
        item = self.find_item(item_name)
        item.update_quantity(updated_quantity)
    
    def update_item_price(self, item_name: str, new_price: Decimal) -> None:
        item = self.find_item(item_name)
        item.update_price(new_price)

    def display(self):
        print("Shopping Cart:")
        print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
        for item in self.items:
            print(
                f"{item.name:<12}${item.price:>7.2f}{item.quantity:>7}     ${item.subtotal:>7.2f}"
            )
        print("=" * 40)
        print(f"Total: ${self.total:>7.2f}")

def main() -> None:
    # Create a shopping cart and add some items to it
    cart = ShoppingCart(
        items=[
            Item("Apple", Decimal("1.5"), 10),
            Item("Banana", Decimal("2"), 2),
            Item("Pizza", Decimal("11.90"), 5),
        ],
    )

    # Update some items' quantity and price
    cart.update_item_quantity('Apple', 10)
    cart.update_item_price('Pizza', Decimal("3.50"))
    
    # cart.items[0].quantity = 10
    # cart.items[2].price = Decimal("3.50")

    # Remove an item
    # cart.items.remove(cart.items[1])
    cart.remove_item('Banana')
    # total = sum(item.price * item.quantity for item in cart.items)
    cart.display()

    # # Print the cart
    # print("Shopping Cart:")
    # print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
    # for item in cart.items:
    #     total_price = item.price * item.quantity
    #     print(
    #         f"{item.name:<12}${item.price:>7.2f}{item.quantity:>7}     ${total_price:>7.2f}"
    #     )
    # print("=" * 40)
    # print(f"Total: ${total:>7.2f}")


if __name__ == "__main__":
    main()
