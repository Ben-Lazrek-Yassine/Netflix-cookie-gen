from flask import Flask, render_template, request
import json
from os import listdir
from random import choice
from threading import Lock, Thread
from random import randbytes
from time import time, sleep

db_lock = Lock()

app = Flask(__name__)
app.secret_key = randbytes(128).hex()

def get_gens() -> list:
    return [gen.lower().replace(".txt", "") for gen in listdir("Accounts")]

def get_ip(request) -> str:
    isCloudflare = request.headers.get('Cf-Connecting-Ip')
    ip = request.remote_addr if not isCloudflare else isCloudflare
    return ip

def remove_chosen_cookie(gen_name, cookie):
    with db_lock:
        with open(f"Accounts/{gen_name}.txt", "r", errors='ignore') as f:
            accounts = f.read().split("###")
        accounts.remove(cookie)
        new_content = "###".join(accounts)
        with open(f"Accounts/{gen_name}.txt", "w", errors='ignore') as f:
            f.write(new_content)

def save_cookie_json(cookie):
    try:
        with open("JSON-Cookie.txt", "w") as f:
            json.dump([cookie], f)
    except Exception as e:
        print(f"Error saving JSON cookie: {e}")

Cooldowns = {}  # Array for managing cooldowns
def cooldown_manager():
    while True:
        for ip in Cooldowns.copy():
            if Cooldowns[ip] < time():
                Cooldowns.pop(ip)
        sleep(0.1)
Thread(target=cooldown_manager, daemon=True).start()

@app.route("/")
def mainpage():
    return render_template("index.html", gens=get_gens())

@app.route("/gen")
def get_account():
    ip = get_ip(request)
    if ip in Cooldowns:
        return "Generating too fast", 429

    gens = get_gens()
    gen_name = request.args.get('name', '').lower()
    if gen_name not in gens:
        return f"An error occurred: Gen not found!", 404

    needs_cookie = request.args.get('Netscape-Cookie', '').lower() == 'true'
    needs_json = request.args.get('JSON-Cookie', '').lower() == 'true'
    with db_lock:
        with open(f"Accounts/{gen_name}.txt", errors='ignore') as f:
            accounts = f.read().split("###")
        if not accounts[0]:
            return "Out of stock", 202

        if needs_cookie:
            account = accounts[0]
            accounts.pop(0)  # Remove the chosen account
            remove_chosen_cookie(gen_name, account)  # Remove the chosen account from file
            if needs_json:
                save_cookie_json(account)  # Save the cookie as JSON
        else:
            account = choice(accounts)
            accounts.remove(account)

        new_content = "###".join(accounts)

        if not needs_cookie:
            with open(f"Accounts/{gen_name}.txt", "w", errors='ignore') as f:
                f.write(new_content)

    Cooldowns[ip] = time() + 5

    return account

@app.route("/stock")
def get_stock():
    gens = get_gens()
    gen_name = request.args.get('name', '').lower()
    if gen_name not in gens:
        return f"An error occurred: Gen not found!", 404
    
    with db_lock:
        with open(f"Accounts/{gen_name}.txt", errors='ignore') as f:
            stock = len(f.read().splitlines())
    if not stock:
        return '0', 202


if __name__ == "__main__":
    app.run("0.0.0.0", 80)
