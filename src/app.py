from threading import Thread, Event
from datetime import datetime, UTC
from plyer import notification
from YumiaCode import Playbox as pb
import requests, time, pathlib, sys

stop_event = Event()

curr_path = pathlib.Path(__file__).resolve().parent


def get_icon_path() -> pathlib.Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return pathlib.Path(sys._MEIPASS) / "warframe.ico"
    return curr_path / "warframe.ico"


def formatExpiry(srcDateTime:str) -> str:
    mDate = srcDateTime.split("-")[:2]
    mDate.append(srcDateTime.split("T")[0][8:10])
    mTime = "".join(srcDateTime.split("T")[1][0:5])
    return f"{mDate[1]}/{mDate[2]}/{mDate[0]} ({mTime})"

def getDateTime(utcTimeStr:str) -> str:
    utc_datetime = datetime.strptime(utcTimeStr, "%m/%d/%Y (%H:%M)").replace(tzinfo=UTC)
    local_datetime = utc_datetime.astimezone()
    return local_datetime.strftime("%d/%m/%Y (%H:%M)")

def getArchon():
    url = f"https://api.warframestat.us/pc/archonHunt"
    
    while not stop_event.is_set():
        currentDateTime = datetime.now().strftime("%x (%H:%M)")

        try:
            res = requests.get(url, timeout=45)
        except requests.exceptions.RequestException as error:
            print(f"{currentDateTime}: Couldn't fetch archon hunt ({error})")
            stop_event.wait(1800)
            continue
                
        # fail function if 'status' is not 'OK' (200)
        if res.status_code != 200:
            # note status code '521' could potentially suggest your connection IP was banned
            # however, this being the case is very unlikely... even with a VPN
            msg = "API down" if res.status_code == 521 else f"Couldn't fetch archon hunt"
            print(f"{currentDateTime}: {msg} (S:{res.status_code})")
            stop_event.wait(1800)# check again in 30 minutes
            continue

        data = res.json()
        missions = tuple(pb.map(data["missions"], lambda m: m["type"]))
        date_time = getDateTime(formatExpiry(data["expiry"]))
        

        notif_message = f"{date_time}: {missions[0]} → {missions[1]} → {missions[2]} | {data["boss"]}"
        match(data["boss"]):
            case "Archon Boreal":
                hunt_title = "Azure Shard Hunt (Earth)"
            case "Archon Amar":
                hunt_title = "Crimson Shard Hunt (Mars)"
            case "Archon Nira":
                hunt_title = "Topaz Shard Hunt (Jupiter)"

        sendNotification(hunt_title, notif_message)
        print(f"[{hunt_title}]: {notif_message}")

        stop_event.wait(57600)# check every 16 hours

def sendNotification(title, notif_message) -> None:
    notification.notify(
        title = title,
        message = notif_message,
        timeout = 3600,
        app_name = "Your.Warframe",
        app_icon = str(get_icon_path())
    )


def getFissures():
    url = f"https://api.warframestat.us/pc/fissures"

    while not stop_event.is_set():
        currentDateTime = datetime.now().strftime("%x (%H:%M)")

        try:
            res = requests.get(url, timeout=45)
        except requests.exceptions.RequestException as error:
            print(f"{currentDateTime}: Couldn't fetch fissures ({error})")
            stop_event.wait(1800)
            continue
        
        # fail function if 'status' is not 'OK' (200)
        if res.status_code != 200:
            # note status code '521' could potentially suggest your connection IP was banned
            # however, this being the case is very unlikely... even with a VPN
            msg = "API down" if res.status_code == 521 else f"Couldn't fetch fissures"
            print(f"{currentDateTime}: {msg} (S:{res.status_code})")
            stop_event.wait(1800)# check again in 30 minutes
            continue
    
        # API fetch returned as 'dict' generated from parsed JSON data
        data = res.json()
        BASE_PATH = tuple(pb.filter(data, lambda f: not f["isHard"] and f["tier"] == "Omnia"))
        STEEL_PATH = tuple(pb.filter(data, lambda f: f["isHard"] and f["tier"] == "Omnia"))
        IDEAL_FISSURES = ("Survival", "Void Cascade")

        node:str
        mission_type:str
        date_time:str
        notif_message:str
        title:str
        
        for m in BASE_PATH:
            node = m["node"]
            mission_type = m["missionType"]
            date_time = getDateTime(formatExpiry(m["expiry"]))
            title = f"{mission_type} Fissure"
            notif_message = f"{node} — {mission_type} (Omnia)\nEnds at {date_time}"

            if mission_type in IDEAL_FISSURES:
                sendNotification(title, notif_message)
                print(f"{node} — {mission_type} (Omnia)\nEnds at {date_time}\n")

        for m in STEEL_PATH:
            node = m["node"]
            mission_type = m["missionType"]
            date_time = getDateTime(formatExpiry(m["expiry"]))
            title = f"Steel Path {mission_type} Fissure"
            notif_message = f"{node} — {mission_type} (Omnia)\nEnds at {date_time}"

            if mission_type in IDEAL_FISSURES:
                sendNotification(title, notif_message)
                print(f"Steel Path {node} — {mission_type} (Omnia)\nEnds at {date_time}\n")

        stop_event.wait(1800)# checks fissures every 30 minutes



def main():
    threads = [
        Thread(target=getFissures, name="Fissure Tracker", daemon=True),
        Thread(target=getArchon, name="Archon Tracker", daemon=True)
    ]

    LAUNCH_TIME = datetime.now().strftime("%d/%m/%Y (%H:%M)")

    print("Your.Warframe Online!\n")
    print(f"[tracking starts]: {LAUNCH_TIME}\n")
    for t in threads:
        t.start()
        print(f"[launched {t.name}]\n")
        time.sleep(1)

        try:
            stop_event.wait()
        except KeyboardInterrupt as e:
            END_TIME = datetime.now().strftime("%d/%m/%Y (%H:%M)")

            print("Your.Warframe Offline! (window will close itself)\n")
            print(f"[tracking ran from: {LAUNCH_TIME} to {END_TIME}]")
            stop_event.set()
        except RuntimeError as e:
            pass

        for thread in threads:
            thread.join()
        time.sleep(10)
        sys.exit()



if __name__ == "__main__":
    main()