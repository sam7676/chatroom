# chatroom

This is a web-based chatroom project that allowed me to experiment with Django, HTML, CSS, JavaScript and databases as an introduction to complex web design. 
It is a classic database-oriented application in which users can create unlimited chatrooms and connect and talk to others.
There is a command-line interface embedded in the application which allows simple room customisation, including leaving, closing and locking a room. 

The link to an online version of this chatroom can be found at https://quickchat.pythonanywhere.com/.

Commands:  
leave                       Leaves the current room and returns to the home page.  
unlock                      Unlocks the room if it is locked.  
lock                        Locks the room so that no users can join from the home page.  
lock [password]             Locks the room with a specific password so users can join from the home page only if they enter the correct password.  
close                       Closes the room and deletes all messages. Requires there to be only one user currently in the room.  
colour [colour]             Changes the colour of the page text. This can either a colour code (#abcdef or abcdef) or a specific colour name.  
color [colour]              Changes the colour of the page text. This can either a colour code (#abcdef or abcdef) or a specific colour name.  
fg [colour]                 Changes the colour of the page text. This can either a colour code (#abcdef or abcdef) or a specific colour name.  
background [colour]         Changes the colour of the background text. This can either a colour code (#abcdef or abcdef) or a specific colour name.  
bg [colour]                 Changes the colour of the background text. This can either a colour code (#abcdef or abcdef) or a specific colour name.  
All specific colour names can be found at https://en.wikipedia.org/wiki/List_of_colors_(alphabetical).
