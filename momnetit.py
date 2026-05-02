#!/usr/bin/env python3
"""
THE MOMNE TIT - Connection Killer Library
"One look is all you get."

Author: WinterGate Intelligence Collective
"""

import os,sys,time,socket,struct,subprocess,threading,random,hashlib
from collections import defaultdict
from datetime import datetime
from typing import Tuple,Optional,List,Dict

def _a()->str:
    try:
        _b=subprocess.run(["ip","route","show","default"],capture_output=True,text=True)
        for _c in _b.stdout.split():
            if "dev" in _c:
                _d=_b.stdout.split().index("dev")
                if _d+1<len(_b.stdout.split()):
                    return _b.stdout.split()[_d+1]
    except:pass
    try:
        _e=subprocess.run(["ip","link","show","up"],capture_output=True,text=True)
        for _f in _e.stdout.split("\n"):
            if "LOOPBACK" not in _f and "state UP" in _f:
                _g=_f.split(":")
                if len(_g)>=2:
                    return _g[1].strip()
    except:pass
    return "eth0"

_B={}
_L=threading.Lock()
_T=None
_R=False
_I=_a()

def _h(_i:str)->int:
    return struct.unpack("!I",socket.inet_aton(_i))[0]
def _j(_k:int)->str:
    return socket.inet_ntoa(struct.pack("!I",_k))
def _l(_m:str,_n:int=24)->str:
    _o=_h(_m)
    _p=(0xFFFFFFFF<<(32-_n))&0xFFFFFFFF
    return f"{_j(_o&_p)}/{_n}"

def burn_ip(_q:str,_n:int=24,_r:bool=True)->bool:
    global _B,_I
    _s=_l(_q,_n)
    if not _s:
        return False
    with _L:
        if _s in _B:
            return False
        _B[_s]={
            "trigger_ip":_q,
            "prefix":_n,
            "burned_at":datetime.now(),
            "permanent":_r
        }
        try:
            subprocess.run([
                "iptables","-A","INPUT",
                "-i",_I,
                "-s",_s,
                "-j","DROP"
            ],check=True,capture_output=True)
        except:
            try:
                subprocess.run([
                    "iptables","-A","INPUT",
                    "-s",_s,
                    "-j","DROP"
                ],check=True,capture_output=True)
            except:
                return False
    return True

def is_burned(_t:str,_n:int=24)->bool:
    _s=_l(_t,_n)
    if not _s:
        return False
    with _L:
        if _s in _B:
            return True
        for _u in _B.keys():
            try:
                import ipaddress
                if ipaddress.ip_address(_t) in ipaddress.ip_network(_u,strict=False):
                    return True
            except:
                pass
    return False

def list_burned()->List[Dict]:
    with _L:
        return [
            {
                "cidr":_v,
                "trigger_ip":_w["trigger_ip"],
                "burned_at":_w["burned_at"].isoformat()
            }
            for _v,_w in _B.items()
        ]

def clear_burned(_x:str=None)->int:
    global _B
    _y=0
    try:
        _z=subprocess.run(
            ["iptables","-L","INPUT","--line-numbers","-n","-S"],
            capture_output=True,
            text=True
        )
        _10=[]
        for _11 in _z.stdout.split("\n"):
            if "-s" in _11 and "-j DROP" in _11:
                _12=_11.split()
                for _13,_14 in enumerate(_12):
                    if _14=="-s" and _13+1<len(_12):
                        _15=_12[_13+1]
                        if _x is None or _15==_x:
                            _16=_11.split()
                            if _16 and _16[0].replace("-A","").isdigit():
                                _10.append(int(_16[0]))
        for _17 in sorted(_10,reverse=True):
            try:
                subprocess.run(["iptables","-D","INPUT",str(_17)],capture_output=True)
                _y+=1
            except:
                pass
    except:
        pass
    with _L:
        if _x:
            _B.pop(_x,None)
        else:
            _B.clear()
    return _y

def get_stats()->Dict:
    with _L:
        return {
            "total_burned":len(_B),
            "active":_R,
            "interface":_I
        }

def _18():
    global _R
    try:
        _19=socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(0x0003))
        while _R:
            _1a=_19.recv(65535)
            if len(_1a)<14:
                continue
            if struct.unpack("!H",_1a[12:14])[0]!=0x0800:
                continue
            if len(_1a)<34:
                continue
            _1b=(_1a[14]&0x0F)*4
            if _1a[14+9]!=6:
                continue
            _1c=socket.inet_ntoa(_1a[14+12:14+16])
            _1d=14+_1b
            if len(_1a)<_1d+13:
                continue
            _1e=_1a[_1d+13]
            if (_1e&0x02) and not (_1e&0x10):
                if not is_burned(_1c):
                    burn_ip(_1c)
    except Exception:
        pass
    finally:
        try:
            _19.close()
        except:
            pass

def start_killer(_1f:bool=True)->bool:
    global _R,_T
    if os.geteuid()!=0:
        print("ERROR: Momne Tit requires root (sudo)")
        return False
    _R=True
    if _1f:
        _T=threading.Thread(target=_18,daemon=True)
        _T.start()
    else:
        _18()
    return True

def stop_killer()->bool:
    global _R
    _R=False
    return True

class MomneTit:
    def __init__(self,verbose:bool=False):
        self.v=verbose
        self._r=False
    def arm(self):
        if start_killer():
            self._r=True
            if self.v:
                print("⚡ THE MOMNE TIT IS ARMED")
                print('"One look is all you get."')
        return self
    def disarm(self):
        stop_killer()
        self._r=False
        return self
    def burn(self,ip:str):
        r=burn_ip(ip)
        if self.v and r:
            print(f"💀 Burned: {_l(ip)}")
        return r
    def check(self,ip:str):
        return is_burned(ip)
    def stats(self):
        return get_stats()
    def list(self):
        return list_burned()
    def __enter__(self):
        return self.arm()
    def __exit__(self,*_):
        self.disarm()

def quick_burn(ip:str)->bool:
    return burn_ip(ip)
def quick_check(ip:str)->bool:
    return is_burned(ip)

if __name__=="__main__":
    import argparse
    _1g=argparse.ArgumentParser(description="THE MOMNE TIT")
    _1g.add_argument("-v","--verbose",action="store_true")
    _1h=_1g.add_subparsers(dest="cmd")
    _1h.add_parser("arm",help="Arm killer")
    _1h.add_parser("stop",help="Stop killer")
    _1i=_1h.add_parser("burn",help="Burn IP range")
    _1i.add_argument("ip")
    _1j=_1h.add_parser("check",help="Check IP")
    _1j.add_argument("ip")
    _1h.add_parser("list",help="List burned")
    _1h.add_parser("stats",help="Statistics")
    _1h.add_parser("clear",help="Clear all")
    _1k=_1g.parse_args()
    if os.geteuid()!=0:
        print("Need root. Run with sudo.")
        sys.exit(1)
    if _1k.cmd=="arm":
        print(f"⚡ Arming on {_I}")
        start_killer(background=False)
    elif _1k.cmd=="burn":
        if quick_burn(_1k.ip):
            print(f"💀 Burned: {_l(_1k.ip)}")
        else:
            print("Already burned or error")
    elif _1k.cmd=="check":
        if quick_check(_1k.ip):
            print("🔥 Burned")
        else:
            print("✅ Clean")
    elif _1k.cmd=="list":
        for _1l in list_burned():
            print(f"{_1l['cidr']} - by {_1l['trigger_ip']}")
    elif _1k.cmd=="stats":
        _1m=get_stats()
        print(f"Burned: {_1m['total_burned']}")
        print(f"Interface: {_1m['interface']}")
    elif _1k.cmd=="clear":
        _1n=clear_burned()
        print(f"Cleared {_1n} ranges")
    else:
        _1g.print_help()
