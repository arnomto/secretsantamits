import streamlit as st
import random
import requests
import json

st.set_page_config(page_title="Secret Santa", page_icon="🎅", layout="centered")


st.title("🎅 Secret Santa")
st.write("Pick your name and confirm to reveal your Secret Santa!")
st.write("**FOR THE LOVE OF GOD JUST DO YOURS <3**")

names = [
"AARON SAM","ADVAITH SANTHOSH","AISHWARYA SREESH","AKHILESH PRAMOD","ANNE MARIA ELDO",
"ARCHANA K A","CILEN GEORGE ANIL","GAYATHRI S","HAMDHA FATHIMA SHANAVAS",
"JONATHAN GIBOY PANICKER","MATHEW GEORGE","MOHAMMED RIZWAN K S",
"NEVIL JOE JOY","SREEDEV K P","SANIYA SAM","ABHINAV J CHEMMANNOOR",
"ABHINAV S SUNIL","ABHIRAJ S","ADWAITH P V","AISWARYA C","ANGELINE RAJ",
"ANUSHREE PRASANNAN","APARNA K A","ARCHA RAJEEV NAIR","ARDHRA JAYACHANDRAN",
"ARON DEVASSY","ARYAN ARUN M","ASWAL SINDHUMOL AJAY","ASWIN KRISHNA A",
"ATHULRAJ R","BENJAMIN CHACKO","BENNET CHACKO","DEERAJ P D",
"DEVANANDA R","DIWON DAVID ALEX","DIYA SUSAN MANU","FAHEEM AHAMED M S",
"FATHIMA NAHAN A","FEBA P BIJU","GAUTHAMI NANDAN","HAFEEZ MOHAMMED SHAJI",
"HARRY NOBLE","HRITHIKA S","JASSIL MUHAMMED MOOPPAN","JINOY FREDY",
"JOEL JOSSEY JACOB","JOHN JOHNSON","KAMAL U","MUHAMMAD AL SABITH",
"NIDHI BIJURAJ","NUAN NELSON","P GAUTHAM KRISHNA","PRANAV SHYJU",
"RANA ANJUM ASHRAF","SHIFA O S","SHIVANI MANOJ","SONA PHILO SOJI",
"STEVE MATHEW RAJESH","SWATHI RAJENDRAN","THERESA SABIN","VYDHEHI DEVI",
"WASEEM NIYAS KALATHIL","ABIJITH AJAY CHERAMMEL","AKZA TREESA MATHEWS",
"ALISHA SHAJI KURIAN","DHAKSHINA HARIKUMAR","DIYA A CHANDRAN",
"HELEN JOY","MARIA SIJU","NIRANJANA SATISH KUMAR","PARVANA DEV T K",
"SAMUEL BABY","SREYA SUSAN SAJU"
]

API_BASE = "https://api.jsonbin.io/v3/b"
BIN_ID = "6937150c43b1c97be9e03502"
MASTER_KEY = "$2a$10$Wq4M8p2e3wne6/qgZZ2ihuTskrzkIutYO8c3BzxGXxfOLIJw1tqDG"
headers = {"X-Master-Key": MASTER_KEY, "Content-Type": "application/json"}

def load_data():
    try:
        r = requests.get(f"{API_BASE}/{BIN_ID}/latest", headers=headers, params={"meta":"false"})
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {}

def save_data(data):
    try:
        requests.put(f"{API_BASE}/{BIN_ID}", headers=headers, data=json.dumps(data))
    except:
        st.warning("⚠️ Unable to sync with server")

data = load_data()

if "assignments" not in data or "revealed" not in data:
    receivers = names.copy()
    while True:
        random.shuffle(receivers)
        if all(g != r for g, r in zip(names, receivers)):
            break
    data = {"assignments": dict(zip(names, receivers)), "revealed": []}
    save_data(data)

assignments = data["assignments"]
revealed = set(data.get("revealed", []))

selected_name = st.selectbox("Select your name:", names)

if "confirming" not in st.session_state:
    st.session_state.confirming = False

if st.button("Reveal🎁"):
    st.session_state.confirming = True

if st.session_state.confirming:
    st.warning(f"are you sure you want to reveal Secret Santa for **{selected_name}**?")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("Yes, reveal"):
            assigned = assignments.get(selected_name)

            if assigned:
                st.success(f"🎄 Your Secret Santa is: **{assigned}** 🎅")
                st.balloons()

                revealed.add(selected_name)
                data["revealed"] = list(revealed)
                save_data(data)
            else:
                st.error("Error: No assignment found")

            st.session_state.confirming = False

    with c2:
        if st.button("Cancel"):
            st.session_state.confirming = False

