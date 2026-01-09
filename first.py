import logging
import sys
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

# Set up logging to file and console
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            # Set default leverage to 1 for safety on testnet
            self.client.futures_change_leverage(symbol='BTCUSDT', leverage=1)
            logging.info("BasicBot initialized successfully with testnet.")
        except Exception as e:
            logging.error(f"Error initializing BasicBot: {e}")
            raise

    def place_market_order(self, symbol, side, quantity):
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be 'BUY' or 'SELL'")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logging.info(f"Market order placed successfully: {order}")
            print(f"Order placed: {order}")
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error(f"API Error placing market order: {e}")
            print(f"API Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error placing market order: {e}")
            print(f"Unexpected Error: {e}")

    def place_limit_order(self, symbol, side, quantity, price):
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be 'BUY' or 'SELL'")
        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive")
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'
            )
            logging.info(f"Limit order placed successfully: {order}")
            print(f"Order placed: {order}")
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error(f"API Error placing limit order: {e}")
            print(f"API Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error placing limit order: {e}")
            print(f"Unexpected Error: {e}")

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be 'BUY' or 'SELL'")
        if quantity <= 0 or price <= 0 or stop_price <= 0:
            raise ValueError("Quantity, price, and stop_price must be positive")
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce='GTC'
            )
            logging.info(f"Stop-Limit order placed successfully: {order}")
            print(f"Order placed: {order}")
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error(f"API Error placing stop-limit order: {e}")
            print(f"API Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error placing stop-limit order: {e}")
            print(f"Unexpected Error: {e}")

def main():
    try:
        api_key = input("Enter your Binance Testnet API Key: ").strip()
        api_secret = input("Enter your Binance Testnet API Secret: ").strip()
        if not api_key or not api_secret:
            raise ValueError("API Key and Secret are required")
        bot = BasicBot(api_key, api_secret)
        logging.info("Bot started and ready for commands.")
        print("Bot initialized. Enter commands below.")
        
        while True:
            print("\nChoose order type:")
            print("1. Market Order")
            print("2. Limit Order")
            print("3. Stop-Limit Order (Bonus)")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '4':
                print("Exiting bot.")
                logging.info("Bot exited by user.")
                break
            
            if choice not in ['1', '2', '3']:
                print("Invalid choice. Please select 1-4.")
                continue
            
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            if not symbol:
                print("Symbol is required.")
                continue
            
            side = input("Enter side (BUY/SELL): ").strip().upper()
            if side not in ['BUY', 'SELL']:
                print("Side must be BUY or SELL.")
                continue
            
            try:
                quantity = float(input("Enter quantity: ").strip())
            except ValueError:
                print("Invalid quantity. Must be a number.")
                continue
            
            if choice == '1':
                bot.place_market_order(symbol, side, quantity)
            elif choice == '2':
                try:
                    price = float(input("Enter price: ").strip())
                    bot.place_limit_order(symbol, side, quantity, price)
                except ValueError:
                    print("Invalid price. Must be a number.")
                    continue
            elif choice == '3':
                try:
                    price = float(input("Enter price: ").strip())
                    stop_price = float(input("Enter stop price: ").strip())
                    bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                except ValueError:
                    print("Invalid price or stop price. Must be numbers.")
                    continue
    except KeyboardInterrupt:
        print("\nBot interrupted by user.")
        logging.info("Bot interrupted.")
    except Exception as e:
        logging.error(f"Error in main: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()