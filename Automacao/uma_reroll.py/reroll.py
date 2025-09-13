#!/usr/bin/env python3
# ───────────────────────────────────────────────────────────────
#  Uma Musume Steam build – automatic reroll macro 
#  Requires:  pip install pyautogui pygetwindow
# ───────────────────────────────────────────────────────────────
import pyautogui as pg, pygetwindow as gw, time, random, sys

pg.FAILSAFE = True                      # drag mouse to a screen corner to abort

WINDOW_TITLE  = "Umamusume"             # substring found in the title bar
CLICK_DELAY   = (0.25, 0.45)            # random delay between taps
FAST_SPAM_GAP = 0.15                    # for rapid Skip mashing

# ───────────────────────────────────────────────────────────────
#  Coordinates dictionary  (duplicates merged, snake-case keys)
# ───────────────────────────────────────────────────────────────
C = {
    # System / menus
    "menu"               : (1547, 858),
    "delete"             : (1050, 667),
    "close"              : ( 961, 654),

    # Launch consent
    "click3_view1"       : (1092, 506),
    "view2"              : (1096, 580),
    "agree"              : (1043, 706),
    "change_country"     : (1094, 568),
    "ok_country"         : (1050, 702),
    "ok2"                : (1048, 653),

    # Birthdate
    "select_date"        : ( 958, 565),
    "ok_date"            : (1051, 654),

    # Trainer name
    "skip_tutorial"      : (1046, 661),
    "trainer_name"       : ( 965, 518),
    "under_name"         : ( 950, 603),
    "register"           : ( 962, 658),
    "ok_name"            : (1047, 650),

    # Generic skip & gifts
    "skip"               : ( 920, 893),
    "gift"               : ( 853, 704),
    "collect_all"        : ( 776, 861),

    # Guaranteed pulls
    "scout_section"      : ( 850, 889),
    "left_banner"        : ( 503, 630),
    "scout_guaranteed"   : ( 688, 767),
    "confirm_scout"      : ( 770, 661),
    "ok_guarantee"       : ( 682, 702),

    # 10-pulls
    "right_banner"       : ( 870, 630),
    "scout10"            : ( 808, 773),
    "scout_again"        : ( 776, 868),

    # Post-pull screens
    "back_from_pulls"    : ( 603, 870),
    "enhance_section"    : ( 529, 886),
    "support_cards"      : ( 756, 665),
    "uncap_section"      : ( 756, 614),
    "close_popup"        : ( 682, 871),
}

# ────────────────────────── helpers
def bring_to_front() -> None:
    """Activate the game window by title substring."""
    for t in gw.getAllTitles():
        if WINDOW_TITLE.lower() in t.lower():
            gw.getWindowsWithTitle(t)[0].activate()
            time.sleep(0.3)
            return
    sys.exit(f"✖  No window with “{WINDOW_TITLE}” found.")

def rnd_pause(low=CLICK_DELAY[0], high=CLICK_DELAY[1]):
    time.sleep(random.uniform(low, high))

def click(key: str, wait: float = 0.0, times: int = 1, gap: float = 0.3):
    """Click coordinate `key` `times`, waiting after."""
    x, y = C[key]
    for _ in range(times):
        pg.click(x, y)
        rnd_pause(gap, gap + 0.05)
    if wait:
        time.sleep(wait)

def hotkey(*keys: str):
    pg.hotkey(*keys)
    rnd_pause()

def typewrite(text: str, speed: float = 0.05):
    pg.typewrite(text, interval=speed)
    rnd_pause()

# ────────────────────────── one full reroll flow
def reroll_once(n: int):
    print(f"\n=== Cycle {n} ===")
    bring_to_front()

    # (1) Terms & region screens
    click("click3_view1")
    hotkey("alt", "tab")            # switch once
    click("view2")
    hotkey("alt", "tab")            # switch back
    click("agree")
    click("change_country")
    click("ok_country")
    click("ok2")

    # (2) Set birthday -> 1990-01-01
    click("select_date")
    typewrite("199001")
    click("ok_date", wait=15)

    # (3) Skip tutorial, input trainer name
    click("skip_tutorial")
    click("trainer_name")
    typewrite("LuckyBoi")
    click("under_name")
    click("register", wait=8)
    click("ok_name")

    # 20 × generic Skip
    click("skip", times=20, gap=1.0)

    # (4) Collect gifts
    click("gift", wait=8)
    click("collect_all", wait=4)
    click("skip", times=2, gap=1.0)

    # (5) Guaranteed scouts
    click("scout_section", wait=7)
    click("left_banner")
    click("scout_guaranteed")
    click("confirm_scout", wait=6)
    click("skip", times=2, gap=0.5)

    click("skip")                   # same coord as “ScoutAgain_Guarantee”
    click("confirm_scout", wait=6)
    click("skip", times=2, gap=0.5)
    click("ok_guarantee", wait=8)

    # (6) Right banner + first 10-pull
    click("right_banner", times=2, gap=0.5)
    click("scout10")
    click("confirm_scout", wait=6)
    click("skip", times=7, gap=FAST_SPAM_GAP)

    # (7) Nine extra 10-pulls
    for i in range(9):
        click("scout_again")
        click("confirm_scout", wait=6)
        click("skip", times=7, gap=FAST_SPAM_GAP)

    # (8) Navigate to Uncap for manual SSR check
    click("back_from_pulls", wait=8)
    click("enhance_section", wait=1.5)
    click("support_cards",   wait=1.5)
    click("uncap_section",   wait=2.0)
    click("close_popup")

    print("▲  Manual check: review cards, then close game or Ctrl-C to stop.")

# ────────────────────────── run forever (Ctrl-C to break)
if __name__ == "__main__":
    try:
        for cycle in range(1, 9999):
            reroll_once(cycle)
    except KeyboardInterrupt:
        print("\nStopped by user – goodbye!")
