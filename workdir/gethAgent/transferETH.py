from web3 import Web3
my_provider = Web3.HTTPProvider("http://127.0.0.1:8080") #8545, 30303
w3 = Web3(my_provider)


class transferETH():

    def createFunds(to: str, amount: int):
        transaction = { 'from' : w3.eth.defaultAccount, 'to' : to, 'value' : amount }
        w3.geth.personal.sendTransaction(transaction, 'Password1!')

    def sendFunds(fro: str, to: str, amount: int):
        transaction = { 'from' : fro, 'to' : to, 'value' : amount }
        print('Sending ETH transaction...')
        w3.eth.sendTransaction(transaction)
        print('Sending ETH transaction...complete')

    def getFunds(account: str):
        balance = w3.eth.getBalance(account)
        print('[{0}]: Balance: {1}'.format(account, balance))
        return balance

    def makeAcc(pword: str):
        account = w3.geth.personal.newAccount(pword)
        return account

    def getAccs():
        accounts = w3.geth.personal.listAccounts()
        return accounts

    def convertFET(amount: int):
        multiplier = 0.0003123
        return amount*multiplier

    w3.eth.defaultAccount = "0x41FD089BD912da31b704fc36fdE2d1486E1551B1"

    getFunds(w3.eth.defaultAccount)

'''
    makeAcc('pword1')
    makeAcc('pword2')
    accounts = []
    accounts = getAccs()
    for i in accounts:
        getFunds(i)
'''
