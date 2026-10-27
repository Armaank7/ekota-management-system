import os, sys, random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EkotaFootballClub.settings')

import django
django.setup()

from django.contrib.auth.models import User
from accounts.models import Staff, Player
from matches.models import Match, MatchAppearance
from training.models import Training, TrainingAttendance

# WIPE
MatchAppearance.objects.all().delete()
TrainingAttendance.objects.all().delete()
Match.objects.all().delete()
Training.objects.all().delete()
Player.objects.all().delete()
Staff.objects.all().delete()
User.objects.all().delete()
print("Wiped.")

# No staff account is seeded - register one through the staff registration page
print("No staff account created (register one on the site).")

# 18 PLAYERS
pdata = [
    ("Raheem","Osei",date(2007,3,15),"GK"),
    ("Jayden","Brooks",date(2008,1,22),"GK"),
    ("Khalid","Hassan",date(2007,6,10),"DEF"),
    ("Tyler","Morgan",date(2007,9,3),"DEF"),
    ("Aiden","Chukwu",date(2008,2,14),"DEF"),
    ("Zain","Malik",date(2007,11,28),"DEF"),
    ("Reece","Palmer",date(2008,4,7),"DEF"),
    ("Ibrahim","Diallo",date(2007,5,19),"MID"),
    ("Marcus","Bennett",date(2007,8,25),"MID"),
    ("Daniel","Okafor",date(2008,1,3),"MID"),
    ("Ryan","Hughes",date(2007,12,11),"MID"),
    ("Kofi","Mensah",date(2008,3,29),"MID"),
    ("Ethan","Clarke",date(2007,7,16),"MID"),
    ("Jamal","Adebayo",date(2007,4,22),"FWD"),
    ("Leo","Santos",date(2008,2,8),"FWD"),
    ("Nathan","Wright",date(2007,10,14),"FWD"),
    ("Yusuf","Ahmed",date(2007,6,30),"FWD"),
    ("Cameron","Stewart",date(2008,1,9),"FWD"),
]
players = []
for i, (f, l, d, p) in enumerate(pdata, 1):
    uname = f.lower() + "." + l.lower()
    pu = User.objects.create_user(username=uname, password="Matchday2026!", first_name=f, last_name=l)
    players.append(Player.objects.create(first_name=f, last_name=l, date_of_birth=d, position=p, playerID="PLY"+str(i).zfill(3), user=pu, must_change_password=True))
print(str(len(players)) + " players created (with login accounts).")

# 8 MATCHES
mdata = [
    ("Barking United",date(2026,1,4),"League","Home","Mayfield",3,1),
    ("Redbridge City",date(2026,1,18),"League","Away","Redbridge Sports Ground",1,1),
    ("Dagenham Youth",date(2026,1,25),"Cup","Home","Mayfield",2,0),
    ("Ilford Town",date(2026,2,15),"League","Home","Mayfield",4,1),
    ("Hackney Rovers",date(2026,2,22),"Friendly","Neutral","Victoria Park",2,2),
    ("East Ham FC",date(2026,3,1),"League","Home","Mayfield",1,0),
    ("Stratford Lions",date(2026,3,15),"Cup","Away","Stratford Community Pitch",3,2),
    ("Canning Town FC",date(2026,3,22),"League","Home","Mayfield",2,1),
]
matches = []
for o, d, mt, vt, loc, us, ts in mdata:
    matches.append(Match.objects.create(opponent_name=o, match_date=d, match_type=mt, venue_type=vt, location=loc, our_score=us, opponent_score=ts))
print(str(len(matches)) + " matches created.")

# MATCH APPEARANCES
ad = {
    0: [(0,0,0,90),(2,0,0,90),(3,0,0,90),(4,0,0,90),(5,0,1,90),(7,1,0,90),(8,0,1,90),(9,0,0,75),(12,0,0,65),(13,1,0,90),(15,1,1,90)],
    1: [(0,0,0,90),(2,0,0,90),(3,0,0,90),(4,0,0,90),(5,0,0,90),(7,0,1,90),(8,0,0,90),(10,0,0,70),(13,1,0,90),(15,0,0,80),(14,0,0,20)],
    2: [(0,0,0,90),(2,0,0,90),(3,1,0,90),(4,0,0,90),(6,0,0,90),(7,0,1,90),(8,0,0,90),(9,0,0,60),(13,1,1,90),(16,0,0,90),(12,0,0,30)],
    3: [(0,0,0,90),(2,0,0,90),(3,0,0,90),(4,0,1,90),(5,0,0,90),(7,1,1,90),(8,0,1,90),(9,1,0,80),(13,2,0,90),(15,0,1,90),(16,0,0,20)],
    4: [(1,0,0,90),(2,0,0,90),(6,0,0,90),(5,0,0,90),(3,0,0,45),(7,0,0,90),(11,1,0,90),(10,0,1,90),(14,1,0,90),(17,0,1,75),(16,0,0,45)],
    5: [(0,0,0,90),(2,0,0,90),(3,0,0,90),(4,0,0,90),(5,0,0,90),(7,0,0,90),(8,0,1,90),(10,0,0,80),(13,1,0,90),(15,0,0,85),(11,0,0,10)],
    6: [(0,0,0,90),(2,0,0,90),(3,0,0,90),(4,0,0,90),(6,0,0,90),(7,1,0,90),(8,0,1,90),(9,0,1,75),(13,1,0,90),(16,1,0,85),(15,0,1,65)],
    7: [(0,0,0,90),(2,0,0,90),(3,0,0,90),(4,0,0,90),(5,0,0,90),(7,0,1,90),(8,1,0,90),(12,0,0,90),(13,1,0,90),(15,0,1,90),(17,0,0,20)],
}
ta = 0
for mi, al in ad.items():
    for pi, g, a, m in al:
        MatchAppearance.objects.create(player=players[pi], match=matches[mi], goals=g, assists=a, minutes_played=m)
        ta += 1
print(str(ta) + " appearances created.")

# 8 TRAINING SESSIONS
tdata = [
    (date(2026,1,3),90,"Attacking","Ran 3v3 attacking drills focusing on quick transitions and finishing in the box"),
    (date(2026,1,17),75,"Defending","Worked on defending corners and free kick set pieces"),
    (date(2026,1,24),90,"Match Sim","Full 11v7 match simulation to prepare for the cup tie against Dagenham"),
    (date(2026,2,14),90,"Passing","Short passing triangles and practised building up play from the back"),
    (date(2026,2,21),75,"Attacking","Crossing and finishing drills with the wingers and strikers"),
    (date(2026,2,28),90,"Defending","Worked on pressing triggers and holding defensive shape in a 4-3-3"),
    (date(2026,3,14),60,"Fitness","Agility ladder work and keeper reflex drills"),
    (date(2026,3,21),90,"Match Sim","Full match simulation focusing on set piece routines for corners and free kicks"),
]
sessions = []
for d, dur, tt, n in tdata:
    sessions.append(Training.objects.create(training_date=d, duration=dur, training_type=tt, notes=n))
print(str(len(sessions)) + " training sessions created.")

# TRAINING ATTENDANCE
random.seed(42)
tc = 0
good_notes = ["Arrived 10 minutes late","Left early with a tight hamstring","Excellent work rate today","Looked sharp in the drills","Struggled with the fitness drills but kept going","Good communication with the back line","Needs to work on first touch","Strong performance in the session","Picked up a minor knock but carried on","Great attitude throughout","Keeper made some brilliant saves in practice","Took on extra shooting practice after the session"]
bad_notes = ["Injured","Unavailable","Family commitment","School exam"]
for s in sessions:
    absent = set(random.sample(range(18), random.randint(1, 5)))
    for i, p in enumerate(players):
        present = i not in absent
        note = ""
        if present and random.random() < 0.3:
            note = random.choice(good_notes)
        elif not present and random.random() < 0.4:
            note = random.choice(bad_notes)
        TrainingAttendance.objects.create(player=p, training=s, is_present=present, player_notes=note)
        tc += 1
print(str(tc) + " attendance records created.")
print("ALL DONE! Player login (any): firstname.lastname / Matchday2026!  |  Staff: register on the site")
