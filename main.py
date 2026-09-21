# Система учета запчастей на СТО

from datetime import date

# --- Данные о запчасти и заказе (простые типы) ---
part_name = "Масляный фильтр"       # str — название запчасти
article = "OF-2041"                 # str — артикул
price = 850.5                       # float — цена за штуку, руб.
stock = 12                          # int — остаток на складе
min_stock = 5                       # int — минимальный остаток
received_amount = 20                # int — принято от поставщика
write_off_amount = 4                # int — списано в заказ на ремонт
labor_cost = 1500.0                 # float — стоимость работы, руб.
discount_percent = 10               # int — скидка клиенту, %
is_original = True                  # bool — оригинальная запчасть
today = date.today()                # дата операции


def get_part_info(name: str, art: str, unit_price: float) -> str:
    """Учет запчастей: карточка запчасти одной строкой."""
    return f"{name} (арт. {art}), цена: {unit_price:.2f} руб."


def change_stock(current: int, amount: int, operation: str) -> int:
    """Прием и списание: новый остаток ("receive" или "write_off")."""
    if operation == "receive":
        return current + amount
    elif operation == "write_off":
        return current - amount
    else:
        return current


def get_stock_status(quantity: int, minimum: int) -> str:
    """Отчеты по складу: статус позиции по остатку."""
    if quantity == 0:
        return "Нет в наличии"
    elif quantity <= minimum:
        return "Заканчивается: нужно заказать у поставщика"
    else:
        return "В наличии"


def calculate_order_cost(
    unit_price: float, quantity: int, labor: float, discount: int
) -> float:
    """Расчет стоимости: запчасти + работа, минус скидка."""
    parts_cost = unit_price * quantity
    total = parts_cost + labor
    if discount > 0:
        total = total - total * discount / 100
    return round(total, 2)


# --- Сценарий: приемка запчастей и заказ на ремонт ---
print(get_part_info(part_name, article, price))
print(f"Дата: {today}")
print(f"Оригинал: {'да' if is_original else 'нет'}")
print(f"Остаток на складе: {stock} шт.")

# Приемка партии от поставщика
stock = change_stock(stock, received_amount, "receive")
print(f"Принято {received_amount} шт., остаток: {stock} шт.")

# Списание в заказ на ремонт
if write_off_amount > stock:
    print("Списание невозможно: на складе недостаточно запчастей")
    stock_after = stock
else:
    stock_after = change_stock(stock, write_off_amount, "write_off")
    print(f"Списано {write_off_amount} шт., остаток: {stock_after} шт.")

print(f"Статус: {get_stock_status(stock_after, min_stock)}")

# Стоимость заказа (преобразование типа: округляем до целых рублей)
order_cost = calculate_order_cost(
    price, write_off_amount, labor_cost, discount_percent
)

order_cost_int = int(round(order_cost))

print(f"Стоимость заказа со скидкой {discount_percent}%: "
      f"{order_cost_int} руб.")