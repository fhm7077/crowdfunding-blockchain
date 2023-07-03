from web3 import Web3,HTTPProvider
blockchain_address="http://127.0.0.1:7545"
web3=Web3(HTTPProvider(blockchain_address))
if web3.isConnected():


    acc1="0x1490458B3cc38D303A48d8DCa17cE4A51179D3A8"
    acc2="0xE465072A2276Cd69a5d8B4226375bA98305Cd46e"


    prvkey="0x572a7b3ec551c727edac423ab45cc14065b68121bb81208fff390bfb62bcde8a"
    nonce= web3.eth.getTransactionCount(acc1)

    abcd = web3.eth.get_balance(acc1)
    abcd=web3.fromWei(abcd,'ether')
    print(abcd)


    tx={
        'nonce':nonce,
        'to':acc2,
        'value':web3.toWei(90,'ether'),
        'gas':200000,
        'gasPrice':web3.toWei('50','gwei')
    }
    signedtx=web3.eth.account.sign_transaction(tx,prvkey)
    hashx=web3.eth.send_raw_transaction(signedtx.rawTransaction)
    print(web3.toHex(hashx))