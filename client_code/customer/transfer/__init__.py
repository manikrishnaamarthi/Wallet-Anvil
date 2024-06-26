from ._anvil_designer import transferTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class transfer(transferTemplate):
    def __init__(self, user=None, **properties):
        # Initialize self.user as a dictionary 
        self.init_components(**properties) 
        self.user = user
        # Set Form properties and Data Bindings.
        username = anvil.server.call('get_username', self.user['users_phone'])
        self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        currencies=anvil.server.call('get_user_currency',self.user['users_phone'])
        self.drop_down_2.items= [str(row['users_balance_currency_type']) for row in currencies]
        self.display()
     

    def drop_down_1_change(self, **event_args):
      self.display()

    def display(self, **event_args):
      acc = self.drop_down_2.selected_value

    def button_1_click(self, **event_args):
        current_datetime = datetime.now()
        receiver_phone_number = float(self.text_box_2.text)
        transfer_amount = float(self.text_box_3.text)
        cur=self.drop_down_2.selected_value
        depositor_phone_number = self.user['users_phone']
        
        # Use the entered phone number to identify the receiver's account
        receiver_balance = app_tables.wallet_users_balance.get(users_balance_phone=receiver_phone_number,users_balance_currency_type=cur)
        if self.user :
          depositor_balance = app_tables.wallet_users_balance.get(users_balance_phone=self.user['users_phone'],users_balance_currency_type=cur)
          print(depositor_balance['users_balance'])
          
          money_value = transfer_amount if transfer_amount else 0.0
          if depositor_balance['users_balance'] >=money_value:
            if receiver_balance is not None:
              depositor_balance['users_balance'] -= money_value
              receiver_balance['users_balance']+= money_value
              new_transaction = app_tables.wallet_users_transaction.add_row(
                users_transaction_phone=self.user['users_phone'],
                users_transaction_fund=money_value,
                users_transaction_currency=cur,
                users_transaction_date=current_datetime,
                users_transaction_type="Debit",
                users_transaction_status="transfered-to",
                users_transaction_receiver_phone=self.user['users_phone']
            )
              new_transaction = app_tables.wallet_users_transaction.add_row(
                users_transaction_phone=self.user['users_phone'],
                users_transaction_fund=money_value,
                users_transaction_currency=cur,
                users_transaction_date=current_datetime,
                users_transaction_type="Credit",
                users_transaction_status="recieved-from",
                users_transaction_receiver_phone=self.user['users_phone']
            )
              self.label_4.text = "Money transferred successfully to the account."
            else:
              reciver = app_tables.wallet_users.get(users_phone=receiver_phone_number)
              if reciver:
                depositor_balance['users_balance'] -= money_value
                balance = app_tables.wallet_users_balance.add_row(
                      users_balance_currency_type=cur,  # Replace with the actual currency type
                      users_balance=money_value,
                      users_balance_phone=receiver_phone_number
                  )
                new_transaction = app_tables.wallet_users_transaction.add_row(
                  users_transaction_phone=self.user['users_phone'],
                users_transaction_fund=money_value,
                users_transaction_currency=cur,
                users_transaction_date=current_datetime,
                users_transaction_type="Debit",
                users_transaction_status="transfered-to",
                users_transaction_receiver_phone=self.user['users_phone']
              )
                new_transaction = app_tables.wallet_users_transaction.add_row(
                  users_transaction_phone=self.user['users_phone'],
                users_transaction_fund=money_value,
                users_transaction_currency=cur,
                users_transaction_date=current_datetime,
                users_transaction_type="Credit",
                users_transaction_status="recieved-from",
                users_transaction_receiver_phone=self.user['users_phone']
              )
                self.label_4.text = "Money transferred successfully to the account."
              else:
                anvil.alert("User does not exist")
          else:
            anvil.alert("Insufficient balance. Please add funds.")
        else:
          self.label_4.text = "Error: No matching accounts found for the user or invalid account number."
        open_form('customer.transfer',user=self.user)  
          
    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.deposit",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transfer",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.withdraw",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer_page",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")





