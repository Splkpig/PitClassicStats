accountsSplk = ["Splkpig", "Splkion", "NPCBehavior", "SweatySharkBers"]


def isOwnerAccount(player):
    for ign in accountsSplk:
        if player.lower() == ign.lower():
            return 1
