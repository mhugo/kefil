import math
from escpos import printer
import escpos.exceptions
import os

max_items_per_ticket = 4

g_printer = None


def usb_printer():
    global g_printer
    if g_printer is None:
        g_printer = printer.File(os.environ.get("KEFIL_PRINTER", "/dev/usb/lp0"))
    return g_printer


def print_order_(order, my_printer=None):
    order_id = order["id_in_day"]
    if my_printer is None:
        my_printer = usb_printer()
    my_printer.set(custom_size=True, height=2, width=2, bold=True)
    my_printer.text(f"Commande n°{order_id}")
    items = [[item["quantity"], item["name"]] for item in order["items"]]

    tickets = []
    current_ticket = []
    current_q = 0
    for quantity, name in items:
        if current_q + quantity < max_items_per_ticket:
            current_ticket.append((quantity, name))
            current_q += quantity
        else:
            while current_q + quantity >= max_items_per_ticket:
                q = max_items_per_ticket - current_q
                current_ticket.append((q, name))
                tickets.append(current_ticket)
                current_ticket = []
                current_q = 0
                quantity -= q

            if quantity:
                current_ticket.append((quantity, name))
                current_q += quantity

    if current_ticket:
        tickets.append(current_ticket)

    for i, ticket in enumerate(tickets):
        my_printer.cut(mode="PART")
        title = f"Commande {order_id}"
        if len(tickets) > 1:
            title += f" - {i+1}/{len(tickets)}"
        my_printer.text(title + "\n")

        for j, (q, name) in enumerate(ticket):
            my_printer.text(f"{q} x {name}" + ("\n" if j < len(ticket) - 1 else ""))

    my_printer.text("\n\n")
    my_printer.cut(mode="FULL")


def print_order(order, my_printer=None):
    try:
        print_order_(order, my_printer)
    except escpos.exceptions.Error as e:
        print("=== [ESCPOS ERROR] ===", e)
        global g_printer
        g_printer = None


if __name__ == "__main__":

    class MockPrinter:
        def set(self, *args, **kwargs):
            pass

        def text(self, msg):
            print("print " + msg)

        def cut(self, mode="FULL"):
            print("print ================")

    # mock_printer = MockPrinter()
    mock_printer = None
    print_order(
        {
            "id_in_day": 1,
            "items": [
                {"quantity": 1, "name": "A"},
                {"quantity": 2, "name": "B"},
                {"quantity": 1, "name": "C"},
                {"quantity": 1, "name": "D"},
                {"quantity": 7, "name": "E"},
            ],
        },
        mock_printer,
    )
