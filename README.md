#  Robinhood account activity data converter to Glacier Tax
This application converts data from account activity from Robinhood (and other stockbrokers that use a similar format) to the shape required by Glacier tax. It finds and matches stocks that were sold in 2020 with stocks previously bought to calculate the profit and ultimately the income taxes for stock transactions for nonresident aliens. It also exports the data in the format required to be uploaded into glaciertax.com.

You may find it difficult to retrieve the information from the 1099-B form from Robinhood and add it to Glacier if you buy and sell stocks frequently. This application was created to facilitate this process. Here are the steps you have to follow:

1- Contact Robinhood (or other stockbrokers) to obtain account activity (or transaction history) from your first transaction until 12/31/2020 in CSV file with heads (this is the standard heads for Robinhood): Activity,Date,Process,Date,Settle,Date,Account,Type,Instrument,Description,Trans,Code,Quantity,Price,Amount,Suppressed

2- Bring the file account_activity.csv (with this name) to the same folder as the file taxes2020.py (or taxes2020.ipynb).

3- Run the python script (check item 4 to use Jupyter) and you should obtain a file 2020tax1099-B.csv with heads: name,acquired,sold,proceeds,cost

4- If you want to use Jupyter the file taxes2020.ipynb is ready for you. If you don't have Jupyter installed in your machine you may upload taxes2020.ipynb and account_acctivity.csv to Google Colab (https://colab.research.google.com/?utm_source=scs-index#scrollTo=0cE_xvj-KuHw). The files must be in the same folder. Run the code.

5- Follow the instructions to use the javascript plugin from https://github.com/JiahaoShan/Glacier-tax-1099-B-Stock-Transactions-Helper to upload the file 2020tax1099-B.csv to glaciertax.com.

Updates and generalizations will be made available for 2021 tax returns and beyond.

Enjoy!
