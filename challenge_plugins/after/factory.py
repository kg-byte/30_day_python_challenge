"""Factory to create payment functions"""
from typing import Callable
from decimal import Decimal

PaymentHandlerFn = Callable[[Decimal], None]
payment_funcs: dict[str, Callable[..., PaymentHandlerFn]] = {}


def register(payment_name: str, creation_func: Callable[..., PaymentHandlerFn]):
    payment_funcs[payment_name] = creation_func

def unregister(payment_name: str) -> None:
    payment_funcs.pop(payment_name, None)

def create(name:str, inputs: list[str]) -> PaymentHandlerFn:
    try:
        creation_func = payment_funcs[name]
        return creation_func(inputs)
    except KeyError:
        print(f'Unknown payment method {name}')