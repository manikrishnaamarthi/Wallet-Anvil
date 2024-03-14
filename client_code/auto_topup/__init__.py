from ._anvil_designer import auto_topupTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime#, timedelta, timezone
import anvil.http
class auto_topup(auto_topupTemplate):

    def __init__(self,user=None, **properties):
        # Initialize self.user as a dictionary
      self.init_components(**properties)
      self.user = user
      # Set Form properties and Data Bindings.
      username = anvil.server.call('get_username', self.user['phone'])
      self.label_1.text = f"Welcome to Green Gate Financial, {username}"
      currencies = anvil.server.call('get_user_currency', self.user['phone'])
      #self.drop_down_1.items = [str(row['bank_name']) for row in bank_names]
      self.drop_down_2.items= [str(row['currency_type']) for row in currencies]
      self.display()
      self.card_2.visible = False
      self.button_5.visible=False
      self.label_4.visible=False
      self.card_3.visible = False
      self.button_6.visible= False
      self.label_5.visible=False
      #self.minimum_balance_topup.visible=False
      #self.timely_topup.visible=False
      self.button_off_visible = False
      self.button_on_visible= True
      if self.user['auto_topup']== True:
        self.button_on.visible= False
      else:
        self.button_off.visible= False
        

    def display(self, **event_args):
        acc = self.drop_down_1.selected_value

    def button_1_click(self, **event_args):
      self.text_box_1.text = 100

    def button_2_click(self, **event_args):
      self.text_box_1.text = 200

    def button_3_click(self, **event_args):
      self.text_box_1.text = 500

    def button_4_click(self, **event_args):
      self.text_box_1.text = 1000

    def button_13_click(self, **event_args):
      self.text_box_2.text = 100

    def button_14_click(self, **event_args):
      self.text_box_2.text = 200

    def button_15_click(self, **event_args):
      self.text_box_2.text = 500
      
    def button_16_click(self, **event_args):
      self.text_box_2.text = 1000

    def button_5_click(self, **event_args):
      if self.user['auto_topup']== True:
        current_datetime = datetime.now()
        w_bal = self.drop_down_1.selected_value
        cur= self.drop_down_2.selected_value
        money = float(self.text_box_1.text)
        endpoint = 'convert'
        api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'
        # Set base currency and any other parameters (replace 'USD' with your desired base currency)
        base_currency = 'INR'
        resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={cur}&amount={money}&api_key={api_key}", json=True)
        money_value=resp['response']['value']
        if self.user :
          # Check if a balance row already exists for the user
          existing_balance = app_tables.wallet_users_balance.get(phone=self.user['phone'],currency_type=cur) 
          if existing_balance['balance'] < int(w_bal):
            self.user['minimum_topup'] = True
            existing_balance['balance'] += money_value
            new_transaction = app_tables.wallet_users_transaction.add_row(
                  phone=self.user['phone'],
                  fund=money_value,
                  date=current_datetime,
                  transaction_type=f"{cur} - Credit",
                  transaction_status="Minimum-Topup",
                  receiver_phone=None
              )
            #self.label_4.text = "Minimum-topup payment has been successfully added to your account."
            alert("Minimum-topup payment has been successfully added to your account.")
            self.text_box_1.text = ""
            print("minimum topup added") 
            open_form('customer', user=self.user)
          else:
            # No minimum top-up required
            self.user['minimum_topup'] = False
            #self.user['auto_topup'] = False
            anvil.alert("Auto-topup is not required.")
            print("Your balance is not below the limit")
            open_form('customer', user=self.user)
        else:
          self.label_4.text = "Error: No matching accounts found for the user or invalid account number."
          #open_form('customer', user=self.user)
      else:
        alert("Please enable the auto-topup switch to proceed.")
      


    def button_6_click(self, **event_args):
      if self.user['auto_topup']== True:
        from datetime import datetime, timezone
        current_datetime = datetime.now().replace(tzinfo=timezone.utc)
        frequency = self.drop_down_3.selected_value
        cur= self.drop_down_2.selected_value
        money = float(self.text_box_2.text)
        endpoint = 'convert'
        api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'
        # Set base currency and any other parameters 
        base_currency = 'INR'
        resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={cur}&amount={money}&api_key={api_key}", json=True)
        money_value=resp['response']['value']
        print(f"Your entered amount is {money_value}")
        if self.user :
          # Check if a balance row already exists for the user
          existing_balance = app_tables.wallet_users_balance.get(phone=self.user['phone'],currency_type=cur)         
          
          # Calculate the time interval based on the frequency
          if frequency == "Every Week":
              interval_days = 1
          elif frequency == "Every Month":
              interval_days = 30 
          elif frequency == "Every 3 Months":
              interval_days = 90  
          elif frequency == "Every 6 Months":
              interval_days = 180  
          else:
              interval_days = 0 
          
          # Check if the required time duration has elapsed or if the frequency is different
          if (self.user['last_auto_topup_time'] is None) or ((current_datetime - self.user['last_auto_topup_time']).days >= interval_days):
            self.user['timely_topup'] = True
            self.user['timely_topup_interval'] = frequency
            existing_balance['balance'] += money_value
            new_transaction = app_tables.wallet_users_transaction.add_row(
                  phone=self.user['phone'],
                  fund=money_value,
                  date=current_datetime,
                  transaction_type=f"{cur} - Credit",
                  transaction_status="Timely-Topup",
                  receiver_phone=None
              )
            self.label_5.text = f"{frequency}-topup payment has been successfully added to your account."
            # Update the last auto-topup time in user data
            self.user['last_auto_topup_time'] = current_datetime
            open_form('customer', user=self.user)  
          else:
            self.user['auto_topup'] = False
            anvil.alert("Auto-topup is inactive until the required time duration has expired.")
            print("Your balance is not below the limit")
            open_form('customer', user=self.user)  
        else:
          self.label_5.text = "Error: No matching accounts found for the user or invalid account number."
      else:
        alert("Please enable the auto-topup switch to proceed.")    
        
    def button_on_click(self, **event_args):
      self.user['auto_topup']= True
      self.user.update()
      self.button_on.visible = False
      self.button_off.visible = True
  
    def button_off_click(self, **event_args):
      self.user['auto_topup']= False
      self.user.update()
      self.button_on.visible = True
      self.button_off.visible = False
      self.minimum_balance_topup.visible=True
      self.timely_topup.visible=True
      self.card_2.visible = False
      self.button_5.visible = False
      self.label_4.visible= False
      self.card_3.visible = False
      self.button_6.visible = False
      self.label_5.visible=False
      self.timely_topup.enabled=True
      self.minimum_balance_topup.enabled=True
     
    def link_1_click(self, **event_args):
      open_form('customer',user=self.user)

    def minimum_balance_topup_click(self, **event_args):
      self.minimum_balance_topup.enabled=True
      self.timely_topup.enabled=False
      self.card_2.visible = True
      self.button_5.visible = True
      self.label_4.visible= True
      self.card_3.visible = False
      self.button_6.visible = False
      self.label_5.visible=False

    def timely_topup_click(self, **event_args):
      self.timely_topup.enabled=True
      self.minimum_balance_topup.enabled=False
      self.card_3.visible = True
      self.button_6.visible = True
      self.label_5.visible= True
      self.card_2.visible = False
      self.button_5.visible = False
      self.label_4.visible= False