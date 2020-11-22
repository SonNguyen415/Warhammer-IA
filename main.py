from story import *

currScene = 1
gameContinue = True

# Make the game
print_intro()
time.sleep(WAIT_TIME)
while gameContinue:
    Player = render_menu()
    if in_database(Player.charID):
        currScene = get_curr_progress(Player.charID)
    Player.check_stats()
    start_game()
    game_progress(currScene, Player)
    gameContinue = end_game()

exit_game()

