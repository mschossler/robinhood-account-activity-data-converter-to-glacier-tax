import pandas as pd, io
import io

pd.set_option("display.max_rows", 20, "display.max_columns", 20)
import datetime

file_data = pd.read_csv("account_acctivity.csv")

renam_data = file_data.rename(columns={'Activity Date': 'date', 'Instrument': 'instrument', 'Amount': 'amount', 'Trans Code': 'code', 'Quantity': 'st_quantity', 'Price': 'price'})
renam_data = renam_data.drop(['Process Date', 'Settle Date', 'Account Type', 'Description', 'Suppressed'], axis=1)
renam_data = renam_data.loc[(renam_data.code == 'SELL') | (renam_data.code == 'BUY')]
renam_data = renam_data.reset_index(drop=True)

# ____________________________converts strings to float and integers__________________________________

length = len(renam_data.loc[:, 'st_quantity'])
ntmp = [float(renam_data.loc[j, 'st_quantity']) for j in range(length)]
renam_data['quantity'] = pd.Series(ntmp)


def float_part(string):
    return float(''.join([i for i in list(string) if i.isdigit()])) / 100


ntmp = [float_part(renam_data.loc[j, 'price']) for j in range(length)]
renam_data['float_price'] = pd.Series(ntmp)

ntmp = [float_part(renam_data.loc[j, 'amount']) for j in range(length)]
renam_data['float_amount'] = pd.Series(ntmp)

renam_data = renam_data.drop(['st_quantity', 'price', 'amount'], axis=1)

# _________________sort data by stock and date selecting only for stocks relevant for 2019 or 2020 taxes__________________


renam_data['date'] = pd.to_datetime(renam_data['date'], format='%m/%d/%Y')

# selects data for 2019
data2019 = renam_data
for i in list(data2019.index.values):
    if data2019.loc[i, 'date'] >= datetime.datetime(2020, 1, 1):
        data2019 = data2019.drop(i)

    # selects data for 2020, but missing some 'BUY' trades from 2018
data2020 = renam_data
for i in list(data2020.index.values):
    if (data2020.loc[i, 'date'] < datetime.datetime(2020, 1, 1) or data2020.loc[i, 'date'] >= datetime.datetime(2021, 1, 1)):
        data2020 = data2020.drop(i)

data2019 = data2019.sort_values(by=['instrument', 'date'])
data2020 = data2020.sort_values(by=['instrument', 'date'])

grouped = data2019.groupby('instrument')

for stock in grouped.groups:
    for i in reversed(grouped.get_group(stock).index):
        if data2019.loc[i, 'code'] == 'BUY':
            data2020 = data2020.append(data2019.loc[i], ignore_index=True)  # gets missing 'BUY' trades from 2018 to data2020
            data2019 = data2019.drop(i)  # drop irrelevent 'BUY' tradings from 2019 data
        else:
            break

data2020 = data2020.sort_values(by=['instrument', 'date'])
stocktmp = 'none'  # prints data for the stock defined here. none is to hide this data


# print(data2020)
def manipulate_data(data_frame):  # returns the data in a format as required by glacier - associating sell's and buy's
    grouped = data_frame.groupby('instrument')

    for stock in grouped.groups:
        indexlist = [i for i in reversed(grouped.get_group(stock).index)]
        for i in indexlist:
            if data_frame.loc[i, 'code'] == 'BUY':
                data_frame = data_frame.drop(i)  # drop irrelevent 'BUY' tradings from 2020 data - data must be sorted before
            else:
                break

    data_frame = data_frame.sort_values(by=['instrument', 'date', 'float_amount']).reset_index(drop=True)  # sort by float_amount is for day trading with profit - does not work with loss

    processed_data = []

    def add_data(processed_data, i_b, i_s, qtt_b, qtt_s):
        processed_data.append([data_frame.loc[i_b, 'instrument'], qtt_b, data_frame.loc[i_b, 'date'], data_frame.loc[i_s, 'date'],
                               qtt_s * data_frame.loc[i_s, 'float_price'], qtt_b * data_frame.loc[i_b, 'float_price']])

    grouped = data_frame.groupby('instrument')
    processed_data = [];

    for stock in grouped.groups:
        indexlist = [i for i in grouped.get_group(stock).index]
        l = [[i, data_frame.loc[i, 'quantity']] for i in indexlist]

        if stock == stocktmp:
            print(stock, l)
        l_b = [row for row in l if row[1] > 0]
        l_s = [row for row in l if row[1] < 0]
        l = l_b + l_s

        if stock == stocktmp:
            print(stock, l_b, l_s, '\n lenght of l', len(l))

        loop = 1;
        while l_b and l_s:
            b_index = l_b[0][0]
            s_index = l_s[0][0]
            # if loop==1:
            qtt_b = abs(l_b[0][1])
            qtt_s = abs(l_s[0][1])
            if stock == stocktmp:
                print(loop, qtt_b, qtt_s, 'here0')
            if qtt_b > qtt_s:  # first case where quantity of buys is larger than quantity of sells for a given stock/operation
                if stock == stocktmp:
                    print(loop, stock, l_b, l_s, 'here1')
                add_data(processed_data, b_index, s_index, qtt_s, qtt_s)
                l_b[0][1] = qtt_b - qtt_s
                del l_s[0]
            elif qtt_s > qtt_b:  # first case where quantity of buys is leser than quantity of sells for a given stock/operation
                if stock == stocktmp:
                    print(loop, stock, l_b, l_s, 'here2')
                add_data(processed_data, b_index, s_index, qtt_b, qtt_b)
                l_s[0][1] = -(qtt_s - qtt_b)
                del l_b[0]
            elif qtt_s == qtt_b:  # first case where quantity of buys is equal as quantity of sells for a given stock/operation
                if stock == stocktmp:
                    print(loop, stock, l_b, l_s, 'here3')
                if len(l_b + l_s) > 1:
                    # if stock==stocktmp:
                    # print(stock, l, '\n lenght of l',len(l))
                    add_data(processed_data, b_index, s_index, qtt_b, qtt_s)
                    del l_s[0]
                    del l_b[0]
                elif len(l_b + l_s) == 1:
                    l_b = [];
                    l_s = [];
            loop += 1
            l = l_b + l_s
        if stock == stocktmp:
            print(stock, l)

    # print(type(grouped.get_group('CCL').index))
    # print(grouped.groups.keys())

    final_data = pd.DataFrame(processed_data, columns=['instrument', 'qtt', 'buy_date', 'sale_date', 'sale_price', 'cost'])
    return final_data


final_data = manipulate_data(data2020)

# ____________________________export data to file__________________________________

exp_data = final_data.drop(['qtt'], axis=1).rename(columns={'instrument': 'name', 'buy_date': 'acquired', 'sale_date': 'sold', 'sale_price': 'proceeds'})

# convert date formats
exp_data['acquired'] = exp_data.acquired.map(lambda p: p.strftime('%m/%d/%Y'))
exp_data['sold'] = exp_data.sold.map(lambda p: p.strftime('%m/%d/%Y'))

for i in list(exp_data.index.values):  # set the floats in the exported data with two digits of precision
    costtmp = round(exp_data.loc[i, 'cost'], 2)
    proceedtmp = round(exp_data.loc[i, 'proceeds'], 2)
    # profittmp=round(exp_data.loc[i,'profit'],2)
    exp_data.loc[i, 'cost'] = costtmp
    exp_data.loc[i, 'proceeds'] = proceedtmp
    # exp_data.loc[i,'profit']=profittmp

exp_data.to_csv(r'2020tax1099-B.csv', index=False, header=True)

#print(exp_data.proceeds.sum(), exp_data.cost.sum())

# ________________________________calculates the profits__________________________________________________________
exp_data['profit'] = pd.Series([exp_data.loc[i, 'proceeds'] - exp_data.loc[i, 'cost'] for i in range(len(exp_data))])
lost = 0
gain = 0
for i in list(exp_data.index.values):
    if exp_data.loc[i, 'profit'] <= 0:
        lost = lost + exp_data.loc[i, 'profit']
    else:
        gain = gain + exp_data.loc[i, 'profit']
# print(lost, gain, gain + lost)
print(exp_data)
