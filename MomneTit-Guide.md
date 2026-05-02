# THE MOMNE TIT

"One look is all you get."

---

## INSTALL

pip install momnetit

---

## QUICK START

sudo momnetit arm

That's it. The killer runs. Attackers die.

---

## COMMANDS

Command          | Action
-----------------|------------------
sudo momnetit arm     | Arm the killer
sudo momnetit stop    | Stop the killer
sudo momnetit burn IP | Burn IP range
sudo momnetit check IP| Check if burned
sudo momnetit list     | List burned ranges
sudo momnetit stats    | Show statistics
sudo momnetit clear    | Clear all burns

---

## PYTHON USE

from momnetit import quick_burn, quick_check, MomneTit

quick_burn("45.33.22.11")
print(quick_check("45.33.22.11"))

with MomneTit(verbose=True) as tit:
    tit.burn("192.168.1.1")

---

## REQUIREMENTS

- Python 3.8+
- Linux
- Root (sudo)

---

## WARNING

Once burned, stays burned. No undo.

---

"We tried to scan. The Momne Tit saw us. We no longer exist."
