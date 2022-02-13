import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
import time

dev_address = "AINOI2AZRTE5BG2OVP5EFSGFLRUI6NHINEZZAO7OI5ULPOH7D4H6YPI3ZY"
dev_pk = "o7yQ3alvLfdad7knDJDNO4LX9iz1bpGntgWC9CzV9/ECGuRoGYzJ0JtOq/pCyMVcaI806GkzkDvuR2i3uP8fDw=="
def create_account():
  #Connecting to the testnet
  algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  algod_address = "http://localhost:4001"
  algod_client = algod.AlgodClient(algod_token, algod_address)

  #Generate new account for this transaction
  secret_key, my_address = account.generate_account()
  m = mnemonic.from_private_key(secret_key)
  print("My address: {}".format(my_address))

  # Check your balance. It should be 0 microAlgos
  account_info = algod_client.account_info(my_address)
  print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

  #Fund the created account
  print('Go to the below link to fund the created account using testnet faucet: \n https://dispenser.testnet.aws.algodev.network/?account={}'.format(my_address))

  completed = ""
  while completed.lower() != 'yes':
    completed = input("Type 'yes' once you funded the account: ");

  print('Fund transfer in process...')
  # Wait for the faucet to transfer funds
  time.sleep(10)
  
  print('Fund transferred!')
  # Check your balance. It should be 10000000 microAlgos
  account_info = algod_client.account_info(my_address)
  print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

  return m

# utility for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1;
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))
