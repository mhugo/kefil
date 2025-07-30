from escpos import printer

my_printer = printer.File("/dev/usb/lp0")


def print_order(order):
    my_printer.set(custom_size=True, height=2, width=2, bold=True)
    my_printer.text(f"Commande n°{order['id']}")
    my_printer.cut(mode="PART")
    my_printer.text(f"#{order['id']}\n")
    for item in order["items"]:
        my_printer.text(f"{item['quantity']} x {item['name']}\n")
    my_printer.cut()
