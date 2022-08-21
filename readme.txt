app_class explain :

include main def : __init__ and run 
- __init__ def is create attributes necessary for this programme
- run def is make game can work 

there are some group def to use in this programme : Helper functions, intro functions, playing functions, and game over functions


-helper functions :
 	draw_text help we can create a text in screen easier 
	load is assign function that it will assign variable from maze.png and walls.txt
	make_enemeis is create 4 ghosts from enemy position 
	reset is a function that at end of game when you be killed or eat coin , if you want to play again ,it will active to make the variable be initial variable


- intro function :
	the functions include what programme will do at start of game 
	start_events : lead programme to right play option (player, bfs or a* ) 
	start_draw will draw these option to screen and you need to choose 


- playing functions :
	there have function relate to playing :
	playing_events : return quit decision or direction you want pacman go to
	playing_update : update if enemy kill pacman pacman be die
	playing_draw : draw to screen running time and step number in top of screen 
	remove_life : if pacman die , pacman.lives be minus 1 and game over
	draw_coins : draw coin to screen


- game over functions :
	there include what programme do in game over state 
	game_over_events : if you want play again , put space else if you want to quit game you put ESC
	game_over_draw : draw infomation and decision out to screen


player_class.py explain :

include there is 2 algorithm (BFS , A*) and functions ralate to move of pacman in game

group 1 : update , draw , on_coin , eat_coin , move , get_pix_pos  there all are function relate to game play 

group 2 :BFS and ASTAR is 2 algorithm we code in our programme and 2 function to give pacman direction to go to coin


A* explain :

-Start with creating a grid to simulate a maze.
-"queue" is a list used to "define" Pacman's current position 
-"path" is a list to store node expanded 
-"visited" is a list used to avoid previously expanded locations

 in first while loop: 
-the first for loop used to arrange priority positions (which vectors will lead to smaller H (X) positions)
-the second for loop used to fine the next position 

the second while loop is use to get the "real path" to the coin


BFS explain :
same with  A* at begin we create a grid and 3 list "queue" , "path" , "visited"

-in first while loop :
the loop expand node until pacman catch coin and stop

in second while loop
- from coin , path run back to start point and return a solve path


function give pacman direction : get_path_direction and find_next_cell_in_path 
from strategies search we have path to lead pacman from start point to coin position
find_next_cell_in_path return next cell at normal condition and nearly ghost 
get_path_direction : give a direction that make pacman can go to next cell in path

enemy_class* explain:
in this part, it's just some simple function,so i will divide it into 2 main groups:

+group 1: it's contanin time_to_move function, get_direction function, move function, get_pix_pos function, and the last is update function.
	group 1 towards the calculation, updating the location of the ghosts in the next steps.
+group 2: contain all of another function.
	group 2 is just to "draw" enemy.


settings.py :
there include some finger of programme