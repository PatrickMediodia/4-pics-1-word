"""
========================================================= 
=                                                       =
=           Project by : Patrick Mediodia               =
=           Section : a51                               =
=           Project title: 4pics1word                   =
=           Finished on : July 1,2020                   =
=           Submitted on : July 1,2020                  =
=           Submitted to: Sir Terrence Lim              =
=           Subject: IT101-L/2                          =   
=                                                       =
=========================================================
"""

from tkinter import *
import random
import string
import ctypes

class game(Frame):
    coins = 0
    level = 0
    pic_answer = []
    word = ''
    letter_index = 0 
    

    def __init__(self, root, save):
        super().__init__()
        self['bg'] = 'gray30'
        self.save = save

        game.coins = self.save.coins
        game.level = self.save.level

        global pic_answer
        pic_answer = self.get_pic_list()

        #Label and coins
        self.level_frame = Frame(self,width = 468,height = 50, bg = 'gray20')
        self.lbl_level = Label(self.level_frame, text = f'Level: {game.level}',fg = 'white', bg = 'gray20', font='Arial 20 bold', padx = 15)

        self.img_coin = PhotoImage(file='assets/coin.png')
        self.lbl_coin = Label(self.level_frame, image=self.img_coin, bg = 'gray20')
        self.lbl_coin_amt = Label(self.level_frame, text = game.coins, bg = 'gray20', fg='white', font='Arial 20 bold', padx = 15)

        self.lbl_level.pack(side = LEFT)
        self.lbl_coin_amt.pack(side = RIGHT)
        self.lbl_coin.pack(side = RIGHT)
        self.level_frame.pack_propagate(0)
        self.level_frame.pack()

        #Image
        self.img = PhotoImage(file=f'pics/{pic_answer[game.level-1]}.png')
        self.lblpic = Label(self,image = self.img)

        self.lblpic.pack(pady = 10)

        #Label Status
        self.lbl_status = Label(self, font='Arial 12 bold', fg = 'white', bg = 'gray30')
        self.lbl_status.pack(pady= 5)

        #Letter Placements
        self.letter_placement_frame = Frame(self, bg = 'gray30')
        self.letter_placement_list = self.letter_placement_creator()

        self.letter_placement_frame.pack()

        #Scambled Letters
        self.scrambled_letters_frame = Frame(self, bg = 'gray30')
        self.scrambled_letter_list = self.scrambled_letter_creator()

        self.scrambled_letters_frame.pack(pady = 15)

        #Hint
        self.img_lightbulb = PhotoImage(file='assets/light_bulb_2.png') 
        self.btn_lightbulb = Button(self.letter_placement_frame, image=self.img_lightbulb, bg = 'gray30', border = 0, command = self.hint_function)
        self.btn_lightbulb.grid(row = 0, column = len(self.letter_placement_list))

        #Pass Button
        self.img_pass = PhotoImage(file='assets/pass_button.png')
        self.btn_pass= Button(self.scrambled_letters_frame, image = self.img_pass, command = self.pass_level, bg='gray30')
        self.btn_pass['border'] = 0
        self.btn_pass.grid(row = 0, column = 7, rowspan = 2)
        
        self.hint_given = list(pic_answer[game.level-1])
        self.list_game_word = [ '' for x in range(len(self.letter_placement_list))]
        self.hint_index = set()
        self.pack()


    def letter_placement_creator(self):
        #Creates buttons where the clicked letters will spwan

        current_level = list(game.pic_answer[game.level-1])
        self.image_border = PhotoImage(file=f'assets/letter_border.png')
        self.labels = []

        for index in range(len(current_level)):
            self.labels.append(LetterButton(self.letter_placement_frame))
            self.labels[index].grid(row = 0, column = index)

        return self.labels


    def scrambled_letter_creator(self):
        #Creates buttons of the 12 scrambled letters used to guess the word

        scrambled_list = self.return_12_letters()
        self.buttons = []
        index = 0
        
        for x in range(2):
            for y in range(6):
                self.buttons.append(LetterButton(self.scrambled_letters_frame))
                self.buttons[index]['text'] = scrambled_list[index].upper()
                self.buttons[index]['command'] = lambda arg1 = self.buttons[index]: self.button_function(arg1)
                self.buttons[index].grid(row = x, column = y)
                index+=1

        self.save.update_record_list(game.level, game.coins)

        return self.buttons


    def pass_level(self):
        #pass level - 10 coins

        game.coins-=10

        if game.coins < 0:
            self.lbl_status['text'] =  'Insufficient Coins'
            game.coins+=10  
            return None
            
        self.change_level()


    def next_level(self):
        #next level after guessing word corretly

        game.coins+=10

        self.change_level()
        

    def change_level(self):
        #change level is used when pass_level or next_level is called
        #changes widgets, picture and answer to next level
        
        if game.level == 50:
            game.create_pop_up('You have finished the game!', 'CONGRATULATIONS!')
            game.level = 0
            game.coins = 100

        game.level += 1
        game.word = ''
        game.letter_index = 0
        self.hint_given = list(pic_answer[game.level-1])
        self.hint_index = set()
        self.save.update_record_list(game.level, game.coins)
        
        self.lbl_coin_amt['text'] = game.coins
        self.lbl_level['text'] = f'Level: {game.level}'
        self.img['file'] = f'pics/{pic_answer[game.level-1]}.png'
        self.lblpic['image'] = self.img
        self.lbl_status['text'] = ''
        self.destroy_and_create_wdigets()

        self.btn_lightbulb.grid(row=0, column = len(self.letter_placement_list))
        self.list_game_word = [ '' for x in range(len(self.letter_placement_list))]


    def button_function(self, button_object):
        #is called when scrambled letters are clicked
        #used to identify the pointer at which the clicked letter with spwan

        self.lbl_status['text'] = ''

        for box in self.letter_placement_list:
            if box['text'] == '':
                game.letter_index = self.letter_placement_list.index(box)
                break
        else: 
            self.lbl_status['text'] = 'Incorrect word!'
            return None

        self.change_button_and_word(button_object)


    def hint_function(self):
        #called when hint button is clicked
        #Get correct wors, filter to which index of word has not been used for hint then change button and word function will be called

        game.coins-=2
        if game.coins < 0:
            self.lbl_status['text'] =  'Insufficient Coins'
            game.coins+=2
            return  None

        self.lbl_coin_amt['text'] = game.coins

        word = game.pic_answer[game.level-1]
        indices  = list(filter(lambda x : x not in self.hint_index, range(len(word))))

        hintIndex = random.choice(indices)
        self.hint_index.add(hintIndex)
        letter = word[hintIndex]
        
        for index, button in enumerate(self.scrambled_letter_list):
            if button['text'].lower() == letter and button.clicked is False:
                button.clicked = True
                button_object = button
                break

        game.letter_index = hintIndex
        self.save.update_record_list(game.level, game.coins)

        self.change_button_and_word(button_object)


    def change_button_and_word(self, button_object):
        #used to change button state and value

        self.list_game_word[game.letter_index] = button_object['text']
        game.word = ''.join(self.list_game_word)
        button_object['state'] = DISABLED

        letter_object = self.letter_placement_list[game.letter_index]

        letter_object['text'] = button_object['text']
        letter_object['command'] = lambda arg1 = button_object, arg2 = letter_object: self.selected_letter_function(arg1,arg2)
            
        if game.word == pic_answer[game.level-1].upper():
            self.next_level()


    def selected_letter_function(self ,button_object, letter_object):
        #command of the letters that has been selected from scrambled letters

        letter_object['text'] = ''
        button_object['state'] = NORMAL
        
        index = self.letter_placement_list.index(letter_object)

        self.list_game_word[index] = ''
        game.word = ''.join(self.list_game_word)


    def destroy_and_create_wdigets(self):
        #used to destory and create new widgets when next level is called

        self.destroy_widgets(self.letter_placement_frame)
        self.destroy_widgets(self.scrambled_letters_frame)

        self.letter_placement_list = self.letter_placement_creator()
        self.scrambled_letter_list = self.scrambled_letter_creator()


    def return_12_letters(self):
        #correct letters and more random letters will be added until it reaches 12

        current_level = list(game.pic_answer[game.level-1])

        while len(current_level) < 12:
            alphabet = string.ascii_uppercase
            current_level.append(random.choice(alphabet))

        random.shuffle(current_level)
        return current_level


    def destroy_widgets(self, delete_frame):
        #destroy widgets of frame

        for widget in delete_frame.winfo_children():
            if widget is not self.btn_pass and widget is not self.btn_lightbulb: 
                widget.destroy()


    def create_pop_up(msg,title):
        #creates pop up messages,  takes in message and title 

        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, msg, title, 0)


    def get_pic_list(self):
        #gets picList of correct answers and their index

        try:
            with open("pics/picList.txt","r") as f:
                pics = f.readlines()
                for pic in pics:
                    pic_split = pic.strip().split(';')
                    game.pic_answer.append(pic_split[1])
                
            return game.pic_answer

        except:
            game.error_pop_up()

    def error_pop_up():
        #this is called when an error has been raised regarding missing files
        
        game.create_pop_up(f"""\nMake sure that the 4pics1word directory is correct:\n
                    Directory:\n
                        /4pics1word
                        |______/assets
                                    |______records.txt
                        |______/pics
                                    |______picList.txt
                        |______4pics1word_.py""", 'ERROR! Please Check Game Files')
        exit(0)


#Class for scrambled letter and letter placement buttons
class LetterButton(Button):
    def __init__(self,parent):
        Button.__init__(self,parent)
        self.image_border = PhotoImage(file=f'assets/letter_border.png')
        self.clicked = False
        self['image']= self.image_border
        self['compound'] = CENTER
        self['font']= 'Arial 12 bold'
        self['border'] = 0


#Class that stores game save of user
class game_save():
    def __init__(self):
        self.records = self.get_record_list()
        self.level = int(self.records[0])
        self.coins = int(self.records[1])
    
    def get_record_list(self):
        #gets record list containing level and coins
        try:
            with open("assets/record.txt","r") as f:
                records = f.readlines()
                for record in records:
                    record_split = record.strip().split(';')
            return record_split[0], record_split[1]

        except:
            #self.update_record_list(game.level, game.coins)
            game.error_pop_up()
    
    def update_record_list(self, level, coins):
        #updates record list when called
        with open("assets/record.txt","w") as f:
            f.write(f'{level};{coins}')

 
def main():
    root = Tk()
    root.title("4 PICS 1 WORD")
    root.geometry(f'{468}x{624}')
    root.maxsize(468,624)
    root['bg'] = 'gray30'
    
    save = game_save()
    four_pics_one_word = game(root,save)

    root.mainloop()

if __name__ == "__main__":
    main()
