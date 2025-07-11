import os
import time

import pandas as pd

from tinkoff.invest import Client
from tinkoff.invest import (
    OrderBookInstrument,
    MarketDataRequest,
    SubscribeOrderBookRequest,
    SubscriptionAction,
)

TOKEN = ""

tickers = ['RU000A10BBW8', 'RU000A105QX1', 'RU000A105BY1', 'RU000A105RZ4',
           'RU000A105WH2', 'RU000A101EQ0', 'RU000A102QN9', 'RU000A103S97', 'RU000A103SA0']  # , 'MOEX' , 'POSI'


def instr():
    instr = {}
    with Client(TOKEN) as client:
        for ticker in tickers:
            # print(ticker)
            r = client.instruments.find_instrument(query=ticker)
            for i in r.instruments:
                if i.ticker == ticker and i.class_code == 'TQCB':
                    instr[i.figi] = {'ticker': i.ticker}
    return instr


def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v:
    :return:
    """
    return v.units + v.nano / 1e9  # nano - 9 нулей


def main():
    partition_counter = 0
    generation_counter = 1
    df = pd.DataFrame(columns=["ticker", "time", "ask", "ask_vol", "bid", "bid_vol"])
    os.mkdir("data")
    instrr = instr()
    instr_ob = []
    for key in instrr.keys():
        instr_ob.append(OrderBookInstrument(
                        figi=key, depth=1))

    def request_iterator():
        yield MarketDataRequest(
            subscribe_order_book_request=SubscribeOrderBookRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=instr_ob
            )
        )
        while True:
            time.sleep(1)

    with Client(TOKEN) as client:
        for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):

            if marketdata.orderbook:
                data = {'ticker': instrr[marketdata.orderbook.figi]['ticker'],
                        'time': marketdata.orderbook.time,
                        'ask': cast_money(marketdata.orderbook.asks[0].price),
                        'ask_vol': marketdata.orderbook.asks[0].quantity,
                        'bid': cast_money(marketdata.orderbook.bids[0].price),
                        'bid_vol': marketdata.orderbook.bids[0].quantity,
                        }

                df.loc[len(df)] = data
                partition_counter += 1

                if partition_counter == 1000:
                    output_path = f'data/orlog_bonds_{generation_counter}.csv'
                    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)
                    df.drop(df.index, inplace=True)
                    generation_counter += 1
                    partition_counter = 0
                    print(f"Generated {generation_counter} document")


if __name__ == "__main__":
    main()
