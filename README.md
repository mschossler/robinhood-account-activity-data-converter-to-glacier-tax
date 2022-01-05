# Robinhood-account-acctivity-data-converter-to-Glacier-tax
This application converts data from account activity from Robinhood (and other stock brokers that use similar format) to the shape required by Glacier tax.

You may find difficult to retrieve the information from the 1099-B form from Robinhood and add it to Glacier if you buy and sell stoks frequently. This application was created to facilitate this process. Here are the steps you have to follow:

1- Contact Robinhood (or other stock brokers) to obatin an account acctivity (or transaction history) from your first transaction untill 12/31/2021 in csv format with heads:
Activity,Date,Process,Date,Settle,Date,Account,Type,Instrument,Description,Trans,Code,Quantity,Price,Amount,Suppressed

2- Bring the file account_acctivity.csv (with this name) to the same folder as the file taxes2021.ipynb. 

3- Run the code using Jupyter (check item 4 if you can't use Jupyter) and you should obtain a file 2021tax1099-B.csv with heads:
name,acquired,sold,proceeds,cost

4- If you don't have Jupyter installed in your machine you may upload taxes2021.ipynb and account_acctivity.csv to Google Colab (https://colab.research.google.com/?utm_source=scs-index#scrollTo=0cE_xvj-KuHw). The files must be in the same folder. Run the code. you may convert the file to .py and run with your favorite python compiler as well.

5- Follow the instructions to use the plugging from https://github.com/JiahaoShan/Glacier-tax-1099-B-Stock-Transactions-Helper to upload the file 2021tax1099-B.csv to glaciertax.com.

Cheers!
