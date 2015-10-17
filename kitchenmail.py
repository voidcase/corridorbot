#!/usr/bin/python3
import requests, time, math, datetime, json
def send_message(profile,content):
    keyfile = open("key","rt")
    apikey = keyfile.read().replace("\n","")
    keyfile.close();
    return requests.post(
            "https://api.mailgun.net/v3/sandboxe8c945081cc6485e857b525aebd3bab3.mailgun.org/messages",
            auth=("api",apikey),
            data={"from": "Corridor bot <postmaster@sandboxe8c945081cc6485e857b525aebd3bab3.mailgun.org>",
                "to": profile["name"] + " <" + profile["email"] + ">",
                "subject": "corridor cleaning reminder",
                "text": content
                }
            )

tasks = [
    'tables/surfaces - Clean the black countertops as well as the sofa tables.',
    'floor - Sweep and mop the corridor floor, the kitchen floor, and the sofa-half of the common room floor.',
    'dish racks - Empty the dish racks of dishes and put them back where they belong.',
    'Wednesday trash - Take out the trashbags under the sinks on wednesday if they are full or semi-full',
    'Sunday trash - Take out the trashbags under the sinks on sunday if they are full or semi-full',
    'carton recycling - Take out the carton recycling once near the end of the week.',
    'plastic/glass/metal recycling - Take out the plastic/glass/metal recycling once near the end of the week.',
    'inventory - Keep the cleaning cupboard somewhat tidy and if we have less than 3 of any of the items listed below, go buy a bunch of them. Give the reciept to the corridor contact for reimbursement.',
    'sinks - Make sure the sinks and metal area around them are clean.',
    'launder towels - Book a washingmachine and launder the towels, 60 degrees <b>without</b> softener.'
]

def get_week():
    t = time.time()
    one_week = 1/60/60/24/7
    dt = t - 1441584000
    w = dt*one_week
    return math.floor(w)

def get_task(roomID):
    week = get_week()
    return tasks[(roomID+week)%10]

def get_people():
    with open("people.json") as json_file:
        json_data = json.load(json_file)
        return json_data['people']


def send_all():
    people = get_people()
    for p in people:
        content = "Hello " + p["name"] + ". This is your kitchen task this week:\n"
        content += get_task(p["room"]) + "\n"
        content += "next week: " + get_task((p["room"]+1)%10) + "\n\n regards, the corridor bot."
        send_message(p,content)

def send_one(name):
    people = get_people()
    p = [a for a in people if a["name"]==name][0]
    content = "Hello " + p["name"] + ". This is your kitchen task this week:\n"
    content += get_task(p["room"]) + "\n"
    content += "next week: " + get_task((p["room"]+1)%10) + "\n\n regards, the corridor bot."
    send_message(p,content)
    print("sent message to",name)

def start():
    while True:
        weekday = datetime.datetime.today().weekday()
        one_day = 60*60*24
        if weekday == 0:
            send_all()
        now = datetime.datetime.now()
        ssmn = (now - now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        time.sleep(one_day*(7-weekday)-ssmn+17*60*60)

send_one("Isak")
