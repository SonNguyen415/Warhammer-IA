from story import *

currScene = 1


# Make the game
print_intro()
while True:
    Player = render_menu()
    if not_in_database(Player.charID):
        currScene = 1
    else:
        currScene = get_curr_progress(Player.charID)
    Player.check_stats()
    start_game()
    currScene = game_progress(currScene, Player)
    end_game()



