import datetime


def refine_patdata(s : str):
    if "진료비 하이패스" in s:
        hosp = "B"
        s=s.replace("직원가족", "").replace("직원", "").replace("진료비 하이패스 서비스 대상자입니다.", "/").replace(" ", "/")
        s_spl = s.split("/")
        # 00711411/구본길/K-TAS/4/남/68Y1M
        pnum = s_spl[0]
        KTAS_idx = s_spl.index("K-TAS")
        pname = " ".join(s_spl[1:KTAS_idx])
        sex = "M" if s_spl[KTAS_idx+2]=="남" else "F"
        age_str = s_spl[KTAS_idx+3]
        age = ""
        if "Y" not in age_str:
            age = age_str[:-1]+"mo"
        else:
            age = age_str.split("Y")[0]

        return pnum, pname.strip(), sex.strip(), age

   

def now_timestamp(dividor="-", add=0):
    time = datetime.datetime.now() + datetime.timedelta(minutes=add)
    return time.strftime("%Y%m%d_%H%M%S".format(d=dividor))


def today_timestamp(dividor="-"):
    # return "{Y}{d}{M}{d}{D}".format(Y=2022, M=11, D=14, d=dividor)
    return datetime.datetime.now().strftime("%Y{d}%m{d}%d".format(d=dividor))

def strip_multyline(raw : str) -> str:
    raw = raw.split("\n")
    for i in range(len(raw)):
        raw[i] = raw[i].strip()
    return "\n".join(raw)