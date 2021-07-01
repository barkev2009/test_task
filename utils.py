def exchange_into_rub(money_data):
    rubbles = euros = dollars = 0
    for item in money_data:
        if item[1] == 'RUB':
            rubbles += item[0]
        elif item[1] == 'USD':
            dollars += item[0]
        elif item[1] == 'EUR':
            euros += item[0]
    return rubbles + 70 * dollars + 80 * euros