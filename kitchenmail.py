#!/usr/bin/python3
import requests, time, math, datetime, json
def send_message(profile,subject,content):
    keyfile = open("key","rt")
    apikey = keyfile.read().replace("\n","")
    keyfile.close();
    return requests.post(
            "https://api.mailgun.net/v3/sandboxe8c945081cc6485e857b525aebd3bab3.mailgun.org/messages",
            auth=("api",apikey),
            data={"from": "Corridor bot <postmaster@sandboxe8c945081cc6485e857b525aebd3bab3.mailgun.org>",
                "to": profile["name"] + " <" + profile["email"] + ">",
                "subject": subject,
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

dailies = """
    take out the trash if it's full.
    empty the dishracks if they are full.
    clean the surfaces if they are dirty.
    clean the stoves if they are dirty.
    clean the sinks if they are dirty.
"""

weeklies = """
    take out the recycling.
    sweep and mop the floors. (in the corridor, kitchen, and half of the common room facing the parking lot.)
    make sure we are not running out of supplies (wash-up liquid, grumme såpa, paper towels). Take the reciept to the corridor contact for reimbursement.
    launder the kitchen towels. 60 degrees. NO softener.
"""

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

def notify():
    people = get_people()
    week = get_week()
    c1 = people[(week)%len(people)]
    c2 = people[(week+1)%len(people)]
    m1 = """Hello human_"""+str(c1['room'])+""". You have been assigned to this weeks daily kitchen duties.
        Simply follow this checklist once each day:
        """ + str(dailies) + """
        Best regards, the corridor bot."""
    m2 = """Hello human_"""+str(c2['room'])+""". You have been assigned to this weeks weekly kitchen duties.
        Simply get the following items done before the end of the week:
        """ + str(weeklies) + """
        Also know that you have the daily duties next week, if you will be away then, ask someone to switch week with you.
        Best regards, the corridor bot."""
    send_message(c1,"cleaning reminder",m1)
    print("mailed", c1['name'], "(daily)", datetime.datetime.now())
    send_message(c2,"cleaning reminder",m2)
    print("mailed", c2['name'], "(weekly)", datetime.datetime.now())
    
    # heads up
    # c3 = people[(week+2)%len(people)]
    # send_message(c3,"cleaning heads up","""
    #         Hello human_"""+str(c3['room'])+""". I am notifying you that you have the weekly kitchen duties next week. If you will be away, ask someone else to switch week with you.
    #         Best regards, the corridor bot.""")
    # print("headsup", c3['name'], datetime.datetime.now())

    

def send_all():
    people = get_people()
    for p in people:
        content = "Hello " + p["name"] + ". This is your kitchen task this week:\n"
        content += get_task(p["room"]) + "\n"
        content += "next week: " + get_task((p["room"]+1)%10) + "\n\n regards, the corridor bot."
        send_message(p,"cleaning reminder",content)

def send_one(name):
    people = get_people()
    p = [a for a in people if a["name"]==name][0]
    content = "Hello " + p["name"] + ". This is your kitchen task this week:\n"
    content += get_task(p["room"]) + "\n"
    content += "next week: " + get_task((p["room"]+1)%10) + "\n\n regards, the corridor bot."
    send_message(p,"cleaning reminder",content)
    print("sent message to",name)

def start():
    while True:
        weekday = datetime.datetime.today().weekday()
        one_day = 60*60*24
        if weekday == 0:
            notify()
        now = datetime.datetime.now()
        ssmn = (now - now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        time.sleep(one_day*(7-weekday)-ssmn+17*60*60)
