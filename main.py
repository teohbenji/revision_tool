import os
import random
import re
import time
import db
import firebase_db

def home_page():
    """Creates home page CLI
    
    Includes options to start program, access settings or exit program"""
    clear_screen()
    print("""---------------\nHome page
    1 - Start
    2 - Settings
    3 - Exit""")
    print("---------------")

    user_response = input("Please enter 1 to choose a game mode, 2 to go to settings or 3 to exit the game: ")

    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "Start" and user_response != "start" and \
          user_response != "2" and user_response != "Settings" and user_response != "settings" and \
          user_response != "3" and user_response != "Exit" and user_response != "exit":

        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to choose a game mode, 2 to go to settings or 3 to exit the game: ")

    #Redirects user based on user_response
    if user_response == "1" or user_response == "Start" or user_response == "start":
        mode_page()
    elif user_response == "2" or user_response == "Settings" or user_response == "settings":
        settings_page()
    elif user_response == "3" or user_response == "Exit" or user_response == "exit":
        clear_screen()
        print("Thank you for playing! :)")
        time.sleep(2)
        clear_screen()
        quit()

def settings_page():
    """Creates settings page CLI
    
    Includes options to add question or return to home page"""
    clear_screen()
    print("""---------------\nSettings page
    1 - Add a question
    2 - Remove a question
    3 - Reset program
    # - Back to Home page""")
    print("---------------")

    user_response = input("Please enter 1 to add a question, 2 to remove a question, 3 to reset program or # to go back to Home page: ")

    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "Add a question" and user_response != "add a question" and \
          user_response != "2" and user_response != "Remove a question" and user_response != "remove a question" and \
          user_response != "3" and user_response != "Reset Program" and user_response != "reset Program" and \
          user_response != "#" and user_response != "Back to Home page" and user_response != "back to Home page":

        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to add a question, 2 to remove a question, 3 to reset program or # to go back to Home page: ")

    #Redirects user based on user_response
    if user_response == "1" or user_response == "Add a question" or user_response == "add a question":
        add_new_question_page()
    elif user_response == "2" or user_response == "Remove a question" or user_response == "remove a question":
        remove_question_home_page()
    elif user_response == "3" or user_response == "Reset Program" or user_response == "reset Program":
        reset_page()         
    elif user_response == "#" or user_response == "Back to Home page" or user_response == "back to Home page":
        home_page()

def reset_page():
    """Creates reset data CLI
    
    Includes options to confirm reset database or return to settings page"""
    clear_screen()
    #Warns user before resetting database
    print("WARNING: Are you sure you want to reset the program?")
    print("ALL PROGRESS WILL BE LOST, including new questions created and the highscores in campaign and sudden death mode.\n")

    user_response = input("Please enter 1 to confirm or # to go back to the settings page: ")

    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "#":
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to confirm, # to go back to the settings page: ")

    #Resets database
    if user_response == "1":
        clear_screen()
        db.setup()
        print("\n---------------------------------------------------")
        print("Reset success! Returning you to the settings page")
        print("---------------------------------------------------\n")
        time.sleep(1)
        settings_page()

    elif user_response == "#":
        settings_page()

def mode_page():
    """Creates mode select page CLI
    
    Includes options to play campaign, sudden death or return to home page"""
    clear_screen()
    print("---------------")
    print("""Mode Select
    1 - Campaign (Play on to move to the next chapter)
    2 - Sudden death (One wrong answer and you lose...)
    # - Back to Home page""")
    print("---------------")

    user_response = input("Please enter 1 to choose Campaign mode, 2 to choose Sudden death Mode or # to go back to Home page: ")

    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "Campaign" and user_response != "campaign" and \
          user_response != "2" and user_response != "Sudden death" and user_response != "sudden death" and \
          user_response != "#" and user_response != "Back to Home page" and user_response != "back to Home page":
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to choose Campaign mode, 2 to choose Sudden death Mode or # to go back to Home page: ")

    #Redirects user based on user_response
    if user_response == "1" or user_response == "Campaign" or user_response == "campaign":
        chapter_select_page()
    elif user_response == "2" or user_response == "Sudden death" or user_response == "sudden death":
        sudden_death_page()
    elif user_response == "#" or user_response == "Back to Home page" or user_response == "back to Home page":
        home_page()

def chapter_select_page():
    """Creates chapter select page CLI
    
    Only unlocked chapters are available for user to select. Best score out of previous attempts are shown"""
    clear_screen()
    print("---------------")
    print("Welcome to Campaign mode!")

    unlocked_chap_nums_list = db.get_unlocked_chap_nums()
    locked_chap_nums_list = db.get_locked_chap_nums()

    #Valid inputs refer to inputs with correct chapter numbers, and invalid inputs refers to inputs with wrong chapter numbers
    correct_inputs_list = []
    wrong_inputs_list = []

    for chap_num in unlocked_chap_nums_list:
        correct_inputs_list += [str(chap_num), "Chapter {}".format(str(chap_num)), "chapter {}".format(str(chap_num))]
        print("{} - Chapter {} ({}) * Highscore: {} / 5 *".format(chap_num, chap_num, "Unlocked", db.get_chapter_high_score(chap_num)))

    for chap_num in locked_chap_nums_list:
        wrong_inputs_list += [str(chap_num), "Chapter {}".format(str(chap_num)), "chapter {}".format(str(chap_num))]
        print("{} - Chapter {} ({})".format(chap_num, chap_num, "Locked" ))
    
    print("# - Back to Mode page")
    print("---------------")

    chapter_select_page_input_validation(correct_inputs_list, wrong_inputs_list)

def chapter_select_page_input_validation(valid_inputs_list, invalid_inputs_list):
    """Validates user input when selecting chapter
    
        If user selects unlocked chapter, user is redirected to campaign.
        If user selects mode, user is redirected to mode page
        Depending on whether user selects locked chapter or types wrong input, different messages are output 
        and user has to select chapter again
    """
    user_response = input("Please enter 1 to choose Chapter 1, 2 to choose Chapter 2, so on and so forth or # to go back to Mode Select page: ")
    #Redirects user based on user_response
    if user_response in valid_inputs_list:
        chap_num = int(user_response[-1])
        campaign(chap_num)
    elif user_response == "#" or user_response == "Back to Mode page" or user_response == "back to Mode page":
        mode_page()

    #Reprompts user for valid user_response input
    elif user_response in invalid_inputs_list:
        chap_num = int(user_response[-1])
        print("\nChapter {} is locked.".format(chap_num))
        print("Please choose an unlocked chapter instead.")
        chapter_select_page_input_validation(valid_inputs_list, invalid_inputs_list)
    else:
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        chapter_select_page_input_validation(valid_inputs_list, invalid_inputs_list)

def campaign_scorecard_page(score, result_list, chap_num):
    """Creates scorecard page CLI. 
    
    Result of each question is printed. If score >3 /5, prints Success. Else prints Try again!
    
    Args:
        score: User score for chapter
        result_list: List of user results for each question
        chap_num: Chapter number
    """
    clear_screen()
    print("\n----Chap {} Scorecard----".format(chap_num))
    for i in range(5):
        print("       Q{} - {}".format(i + 1, result_list[i]))
    
    print("------------------------")
        
    if score >= 4:
        print("\nResult: {}/5 Success!\n".format(score))
    else:
        print("\nResult: {}/5 Try again!\n".format(score))

def campaign(chap_num):
    """Handles logic for campaign chapter, where user has to attempt 5 questions from selected chapter.

    Args:
        chap_num: chapter number
    """
    (current_score, result_list) = grade_campaign_questions(chap_num)

    # Get high score of chapter from database
    # If user's current score > database high score
    # Update high score
    # Update next chapter score
    # If not dont do anything

    campaign_scorecard_page(current_score, result_list, chap_num)

    chap_high_score = db.get_chapter_high_score(chap_num)
    
    #Update high score if user beats highscore
    if current_score > chap_high_score:
        db.update_chapter_high_score(chap_num, current_score)
        print("Congratulations, you just got a new highscore of {}/5!".format(current_score))
    
    # UI for new chapter being unlocked
    if current_score >= 4:
        db.update_chapter_unlocked(chap_num + 1)

        if chap_num < 7:
            print("Congratulations! You have unlocked chapter {}!".format(chap_num + 1))

            user_response = input("Please enter 1 to attempt the next chapter, 2 to try this chapter again or # to go back to home page: ")
            
            #Reprompts user for valid user_response input
            while user_response != "1" and user_response != "2" and user_response != "#":
                print("\nYou entered an invalid command: {}.".format(user_response))
                print("Please enter a valid command.")
                user_response = input("Please enter 1 to attempt the next chapter, 2 to try this chapter again or # to go back to home page: ")

            #Redirects user based on user_response
            if user_response == "1":
                campaign(chap_num + 1)
            elif user_response == "2":
                campaign(chap_num)
            elif user_response == "#":
                home_page()

        else:
            print("Congratulations! You have completed campaign mode!")

            user_response = input("Please enter 1 to try this chapter again or # to go back to home page: ")

            #Reprompts user for valid user_response input
            while user_response != "1" and user_response != "#":
                print("\nYou entered an invalid command: {}.".format(user_response))
                print("Please enter a valid command.")
                user_response = input("Please enter 1 to try again or # to go back to home page: ")

            #Redirects user based on user_response
            if user_response == "1":
                campaign(chap_num)
            elif user_response == "#":
                home_page()
    
    #UI for failed attempt. Prompt to try again or return to home page
    else:
        if chap_num < 7:
            #If next chapter already unlocked
            if chap_high_score >= 4:
                user_response = input("Please enter 1 to attempt the next chapter, 2 to try this chapter again or # to go back to home page: ")
                
                #Reprompts user for valid user_response input
                while user_response != "1" and user_response != "2" and user_response != "#":
                    print("\nYou entered an invalid command: {}.".format(user_response))
                    print("Please enter a valid command.")
                    user_response = input("Please enter 1 to attempt the next chapter, 2 to try this chapter again or # to go back to home page: ")

                #Redirects user based on user_response
                if user_response == "1":
                    campaign(chap_num + 1)
                elif user_response == "2":
                    campaign(chap_num)
                elif user_response == "#":
                    home_page()
                    
            # If next chapter not unlocked
            else: 
                print("\nYou failed to unlock the next chapter. :(")
                user_response = input("Please enter 1 to try again or # to go back to home page: ")

                #Reprompts user for valid user_response inputs
                while user_response != "1" and user_response != "#":
                    print("\nYou entered an invalid command: {}.".format(user_response))
                    print("Please enter a valid command.")
                    user_response = input("Please enter 1 to try again or # to go back to home page: ")

                #Redirects user based on user_response
                if user_response == "1":
                    campaign(chap_num)
                elif user_response == "#":
                    home_page()
        # If chapter 7, and score < 4
        else:
            user_response = input("Please enter 1 to try again or # to go back to home page: ")

            #Reprompts user for valid user_response inputs
            while user_response != "1" and user_response != "#":
                print("\nYou entered an invalid command: {}.".format(user_response))
                print("Please enter a valid command.")
                user_response = input("Please enter 1 to try again or # to go back to home page: ")

            #Redirects user based on user_response
            if user_response == "1":
                campaign(chap_num)
            elif user_response == "#":
                home_page()

def sudden_death_page():
    """Creates scorecard page CLI."""
    clear_screen()
    print("---------------\nWelcome to Sudden death mode!\
    \n1 - Start\
    \n2 - View highscores")
    print("---------------")
    user_response = input("Please enter 1 to begin the sudden death game mode, 2 to view the top 5 highscores or # to go back to Mode Select page: ")

    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "2" and user_response != "#":
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to begin the sudden death game mode, 2 to view the top 5 highscores or # to go back to Home page: ")

    #Redirects user based on user_response
    if user_response == "1":
        grade_sudden_death()

    elif user_response == "#":
        mode_page()

    elif user_response == "2":
        highscores_page()
        
def highscores_page():
    """Creates CLI for local and global (firebase) highscores"""
    clear_screen()
    print("\nThese are your champions:")
    local_highscores = db.get_highscores()
    global_highscores = firebase_db.get_highscores()
    place = 1

    #Print local highscores
    print("\n----Local----")

    if len(local_highscores) == 0:
        print("No highscores yet! Are you worthy to be the next champion???")
    else:
        for score in local_highscores:
            print("{}) {} - {}".format(place, score._name, score._score))
            place += 1
    
    #Print global highscores
    print("\n----Global----")
    place = 1

    if len(global_highscores) == 0:
        print("No highscores yet! Be the first ever champion!")
    else:
        for score in global_highscores:
            print("{}) {} - {}".format(place, score._name, score._score))
            place += 1

    user_response = input("\nPlease enter 1 to attempt the sudden death game mode or # to go back to home page: ")
    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "#":
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to try again or # to go back to home page: ")

    #Redirects user based on user_response
    if user_response == "1":
        grade_sudden_death()
        
    elif user_response == "#":
        home_page()
 
def grade_sudden_death():
    """Handles logic for sudden death mode.

    User answers every question in questions table. If user gets question wrong, the mode ends.
    """
    clear_screen()
    print("\nSudden death is starting now. One wrong move you loseeeeeeee.")
    time.sleep(1)
    clear_screen()

    correct_qns_num = 0
    questions_list = db.get_all_questions()
    question_num = 0 

    while len(questions_list) > 0:
        question_num += 1

        question = random.choice(questions_list)
        answers_list = db.get_answers_by_question_id(question._id)
        isAnswerCorrect = grade_question_page(question_num, question, answers_list)

        #User gets answer right
        if isAnswerCorrect:
            correct_qns_num += 1
            questions_list.pop(questions_list.index(question))

        #User gets answer wrong    
        else:
            clear_screen()
            if correct_qns_num == 0:
                print("You didnt get any question correct:(".format(correct_qns_num))
            elif correct_qns_num == 1:
                print("You got 1 question correct!".format(correct_qns_num))
            else:
                print("You got {} questions correct!".format(correct_qns_num))
            save_score_page(correct_qns_num)
            
    #User gets every question correct
    complete_sudden_death_page(correct_qns_num)

def save_score_page(correct_qns_num):
    """Creates CLI for saving sudden death score
    
    Args:
        correct_qns_num: Number of correct questions
    """
    user_name = input("What name would you like to save this score under?: ")
    
    save_score(user_name, correct_qns_num)

    user_response = input("Please enter 1 to try again, 2 to go back to sudden death page, 3 to view highscores or # to go back to home page: ")
    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "2" and user_response != "3" and user_response != "#":
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to try again, 2 to go back to sudden death page, 3 to view highscores or # to go back to home page: ")

    #Redirects user based on user_response
    if user_response == "1":
        grade_sudden_death()

    elif user_response == "2":
        sudden_death_page()

    elif user_response == "3":
        highscores_page()

    elif user_response == "#":
        home_page()

def save_score(user_name, correct_qns_num):
    """Saves sudden death score into local db and online db
    
    Args:
        
    """
    score = db.Score("", user_name, correct_qns_num)
    db.add_score(score)
    firebase_db.add_score(score)

def complete_sudden_death_page(correct_qns_num):
    """CLI displayed after user gets every sudden death question correct
    
    Args:
        correct_qns_num: Number of questions user answered correctly
    
    """
    clear_screen()
    print("Congratulations! You have completed the sudden death gamemode! You got all {} questions right!".format(correct_qns_num))
    save_score_page(correct_qns_num)

def grade_campaign_questions(chap_num):
    """Checks results of user attempting 5 questions from selected chapter.

    Args:
        chap_num: chapter number

    Returns:
        current_score: User score out of 5
        result_list: List of length 5 containing user results. Either "Correct" or "Wrong"
    """

    current_score = 0
    result_list = []
    questions_list = db.get_questions_by_chap_num(chap_num)
    
    #Choose random 5 questions from all the questions in the chapter
    random_questions_list = random.sample(questions_list, 5)
    question_num = 0

    for question in random_questions_list:
        answers_list = []
        answers_list = db.get_answers_by_question_id(question._id)
        question_num += 1

        isResultTrue = grade_question_page(question_num, question, answers_list)

        if isResultTrue:
            result_list.append("Correct")
            current_score += 1
        else:
            result_list.append("Wrong")
    
    return current_score, result_list

def grade_question_page(question_num, question, answers_list,):
    """Creates question grading CLI

    Prints question, then prints different lines depending on user input. If user answer is wrong, prints out all possible answers

    Args:
        question_no: Question number
        question: Question object
        answers_list: list of Answer objects
        
    Returns:
        True if correct answer, False if wrong answer
    """
    clear_screen()
    grading = "wrong"
    print("\n\nQuestion {}:\n{}".format(question_num, question._name))
    print("\n")
    user_answer = input("Your answer: ")
    
    for answer in answers_list:
        is_ans_regex = "\s*" in answer._name #check if answer contains regex

        #If answer is regex, use match. Else do str comparison 
        if is_ans_regex:
            is_user_ans_correct = isinstance(re.search(answer._name, user_answer), re.Match) 
        else:
            is_user_ans_correct = user_answer == answer._name

        if is_user_ans_correct:
            grading = "right"
            print("You got it {}!".format(grading))
            input("Press enter to continue")

            return True

    print("You got it {}!".format(grading))
    print("\nCorrect answer(s): ")

    #Prints out all correct answers
    for answer in answers_list:
        answer_name = answer._name

        #remove regex chars from answer name
        if is_ans_regex:
            answer_name = remove_regex_from_str(answer_name)

        print(answer_name)

    input("Press enter to continue")

    return False

def remove_regex_from_str(regex_str):
    """Removes regex chars from string
    
    Args:
        regex_str: Str containing regex

    Returns:
        cleaned_str: Str without regex
    """
    cleaned_str = regex_str.replace("[(]", "(").replace("[)]", ")")
    chars_list = ["\s*", "^", "$"]
        
    for char in chars_list:
        cleaned_str = cleaned_str.replace(char, "")

    return cleaned_str

def add_new_question_page():
    """Creates add new question CLI"""
    clear_screen()
    print("Hello, you are about to add a new question. Enter # at anytime to quit back to Settings page")
    chap_num = input("\nWhich chapter from Chapters 1-7 is the new question from: ")

    #Reprompts user for valid chap_num input
    while chap_num not in [str(i) for i in range(1,8)] and chap_num != '#':
        print("\nYou entered an invalid command: {}.".format(chap_num))
        chap_num = input("Please enter a valid Chapter number from 1 - 7: ")

    if chap_num in [str(i) for i in range(1,8)]:
        print("\nYou will add a question under Chapter {}".format(chap_num))
    
    #Returns user to settings page
    elif chap_num == '#':
        settings_page()
    
    qn_type = input("\nIs your question an mcq or open-ended question?\n1 - MCQ\n2 - Open-ended\nEnter 1 or 2: ")

    #Reprompts user for valid qn_type input
    while qn_type != '1' and qn_type != '2' and qn_type != '#':
        print("\nYou entered an invalid command: {}.".format(qn_type))
        qn_type = input("\nIs your question an mcq or open-ended question?\n1 - MCQ\n2 - Open-ended\nEnter 1 or 2: ")

    #Creates mcq question
    if qn_type == '1':
        add_mcq_question_page(chap_num)
    
    #Creates open_ended question
    elif qn_type == '2':
        add_open_ended_question_page(chap_num)

    #Returns user to settings page
    elif qn_type == '#':
        settings_page()

def add_mcq_question_page(chap_num):
    """Creates add mcq question CLI

    Args: 
        chap_num: Chapter number of new question
    
    """
    clear_screen()
    print("\nYou have chosen to add an MCQ question")
    question_name = input("Input your new question: ")

    if question_name == '#':
        settings_page()

    option_number = [str(i) for i in range(1,100)]
    answer_options = []
    add_another_option = '1'
    question_name += "\n(To answer, enter 1 for Option 1, enter 2 for Option 2 etc.)"

    #Prompts user to add new answer option
    while add_another_option != '2' and add_another_option != '#':
        new_mcq_option = input("\nAdd your MCQ Option: ")

        #Returns user to settings page
        if new_mcq_option =='#':
            settings_page()
        
        current_option = option_number.pop(0)
        #Adds answer options to question name
        answer_options.append(current_option)
        question_name += "\nOption {}".format(current_option) + " - " + new_mcq_option
        print("\nYou have entered:\nChapter number: {}\nQuestion: {}".format(chap_num, question_name))

        add_another_option = input("\nDo you want to add another MCQ Option?\n1 - Yes\n2 - No\nEnter 1 or 2: ")

        #Reprompts user for valid add_another_option input
        while add_another_option != '1' and add_another_option != '2' and add_another_option != '#':
            print("\nYou entered an invalid command: {}.".format(add_another_option))
            add_another_option = input("Do you want to add another MCQ Option?\n1 - Yes\n2 - No\nEnter 1 or 2: ")

    #Returns user to settings page
    if add_another_option =='#':
        settings_page()

    answer_name = input("\nInput your answer to the question (Eg. Enter 1 for Option 1, Enter 2 for Option 2): ")

    #Reprompts user for valid answer_name input
    while answer_name not in answer_options and answer_name != '#':
        print("\nYou entered an invalid option: {}.".format(answer_name))
        answer_name = input("\nInput your answer to the question (Eg. Enter 1 for Option 1, Enter 2 for Option 2): ")
    
    #Returns user to settings page
    if answer_name == '#':
        settings_page()

    confirm_add_question_page(chap_num, question_name, answer_name)

def add_open_ended_question_page(chap_num):
    """Creates add open ended question CLI

    Args: 
        chap_num: Chapter number of new question
    """
    clear_screen()
    print("\nYou have chosen to add an open-ended question")
    question_name = input("Input your new question: ")

    #Returns user to settings page
    if question_name == '#':
        settings_page()

    print("\nYou have entered:\nChapter number: {}\nQuestion: {}".format(chap_num, question_name))

    answer_name = input("\nInput your answer to the question: ")

    #Returns user to settings page
    if answer_name == '#':
        settings_page()
    
    confirm_add_question_page(chap_num, question_name, answer_name)

def confirm_add_question_page(chap_num, question_name, answer_name):
    """Creates CLI for confirmation of adding question

    Includes options to confirm add question or return to settings page
    
    Args:
        chap_num: Chapter number of new question
        question_name: Name of question to be added
        answer_name: Name of answer to be added
    """
    clear_screen()
    print("\nYou have entered:\nChapter number: {}\nQuestion: {}\nAnswer: {}".format(chap_num, question_name, answer_name))

    confirmation = input("\nTo confirm the addition of the above question, please enter 1: ")
    
    #Reprompts user for valid confirmation input
    while confirmation != '1' and confirmation != '#':
        print("\nYou entered an invalid command: {}.".format(confirmation))
        confirmation = input("Please enter 1 to confirm your new question and answer or # to quit: ")

    if confirmation == "1":
        question = db.Question('', int(chap_num), question_name)
        db.add_question(question)

        answer = db.Answer("", db.get_newest_question_id(), answer_name)
        db.add_answer(answer)

        print("------------------------------------------\nYou have successfully added the question and answer.")
        print("You will be redirected to Settings page.------------------------------------------\n")
        settings_page()

    #Returns user to settings page
    elif confirmation == '#':
        settings_page()

def remove_question_home_page():
    """Creates remove question home page CLI
    
    Includes options for remove question, show all questions and return to settings page"""
    clear_screen()
    print("""---------------\nRemove question page
    1 - Remove specific question (Based on unique question id number. If you do not know the unique question id, pick option 2.)
    2 - Show all unique question id, question and answer
    # - Go back to Settings page""")
    print("---------------")

    user_response = input("Please enter 1 to remove a question, 2 to show all questions and answers, or # to return to the Settings page: ")

    #Reprompts user for valid user_response input
    while user_response != "1" and user_response != "2" and user_response != "#":
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Please enter 1 to remove a question, 2 to show all questions and answers, or # to return to the Settings page: ")

    if user_response == "1":
        remove_question_page()

    elif user_response == "#":
        settings_page()

    elif user_response == "2":
        print_qns_and_answers_of_chap_page(1)

def print_qns_and_answers_of_chap_page(chap_num):
    """Creates CLI to display questions and answers for each chapter
    
    Q&A from only one chapter is shown at a time. Options to view next chapter, view prev chapter, delete qn or return to remove question homepage"""
    clear_screen()
    chapter_question_list = db.get_questions_sorted_by_chapter()
    chapter_answer_list = sort_answer_by_chapter(chapter_question_list)
    question_list = chapter_question_list[chap_num - 1]
    list_of_answers_list = chapter_answer_list[chap_num - 1]
    num_of_chaps = len(chapter_question_list) 

    print("--------------------------------")
    print("Chapter {} Questions\n".format(chap_num))

    #Print questions and answers of chapter
    for i in range(len(question_list)):
        print_question_and_answers(question_list[i], list_of_answers_list[i])

    print("--------------------------------")

    #First chapter
    if chap_num == 1:
        prompt = "\nPlease enter 1 to view next chapter or # to return to the Remove question page: "

    #Last chapter
    elif chap_num == num_of_chaps:
        prompt = "\nPlease enter 1 to view previous chapter or # to return to the Remove question page: "
    
    else: 
        prompt = "\nPlease enter 1 to view next chapter, 2 to view previous chapter or # to return to the Remove question page: "
    
    user_response = input(prompt)

    #Reprompts user for valid user_response input
    # First chapter, option 1 is for next chapter 
    if chap_num == 1:
        while user_response != "1" and user_response != "#":
            print("\nYou entered an invalid command: {}.".format(user_response))
            print("Please enter a valid command.")
            user_response = input(prompt)

        if user_response == "1":
            print_qns_and_answers_of_chap_page(chap_num + 1)

        elif user_response == "#":
            remove_question_home_page()

    # Last chapter, option 1 is for prev chapter 
    elif chap_num == num_of_chaps:
        while user_response != "1" and user_response != "#":
            print("\nYou entered an invalid command: {}.".format(user_response))
            print("Please enter a valid command.")
            user_response = input(prompt)

        if user_response == "1":
            print_qns_and_answers_of_chap_page(chap_num - 1)

        elif user_response == "#":
            remove_question_home_page()

    #If not first or last chapter, so option 2 is available
    else:
        while user_response != "1" and user_response != "2" and user_response != "#":
            print("\nYou entered an invalid command: {}.".format(user_response))
            print("Please enter a valid command.")
            user_response = input(prompt)
        
        if user_response == "1":
            print_qns_and_answers_of_chap_page(chap_num + 1)

        elif user_response == "2":
            print_qns_and_answers_of_chap_page(chap_num - 1)

        elif user_response == "#":
            remove_question_home_page()

def format_multiple_answer_str(answer_list):
    """Format multiple answers of a question into a single string for display

    Args:
        answer_list: List of answer objects

    Returns: 
        multiple_answer_str: Formatted str including all answers of question
    """
    multiple_answer_str = ""

    for i in range(len(answer_list)):
        answer_name = answer_list[i]._name

        is_ans_regex = "\s*" in answer_name #check if answer contains regex

        #remove regex chars from answer name
        if is_ans_regex:
            answer_name = remove_regex_from_str(answer_name)

        if i < len(answer_list) - 1:
            multiple_answer_str += "{} / ".format(answer_name)
        else:
            multiple_answer_str += "{}".format(answer_name)

    return multiple_answer_str

def sort_answer_by_chapter(chapter_question_list):
    """Sorts answer objects by chapter

    Args:
        chapter_question_list: List of questions sorted by chapter

    Returns:
        chapter_answer_list: List of lists, where each nested list contains answers from the same chapter
    """
    chapter_answer_list = []
    for chapter in chapter_question_list:
        answer_list = []
        for question in chapter:
            answer = db.get_answers_by_question_id(question._id)
            answer_list.append(answer)
            
        chapter_answer_list.append(answer_list)
        
    return chapter_answer_list

def remove_question_page():
    """Generates CLI for question removal"""
    clear_screen()
    qn_id = input("\nPlease enter the unique ID number of the question you wish to remove: ")
    valid_qn_id_list = db.get_all_question_ids()

    #Reprompts user for valid qn_id input
    while qn_id not in valid_qn_id_list and qn_id != '#':
        print("\nYou entered an invalid command: {}.".format(qn_id))
        print("Please enter a valid command.")

        qn_id = input("Enter # to go back to Settings. If not, please enter a valid unique ID number of the question you wish to remove: ")

    if qn_id == "#":
        settings_page()

    elif qn_id in valid_qn_id_list:
        confirm_remove_question_page(qn_id)

def confirm_remove_question_page(qn_id):
    """Creates CLI for confirmation of question removal"""
    clear_screen()
    question = db.get_question_by_id(qn_id)
    answer_list = db.get_answers_by_question_id(qn_id)
    print_question_and_answers(question, answer_list)
    
    user_response = input("Enter 1 to confirm deletion of question. Enter 2 to remove a different question. If not, please enter # to go back to Remove question: ")

    #Reprompts user for valid qn_id input
    while user_response not in ["1", "2", '#']:
        print("\nYou entered an invalid command: {}.".format(user_response))
        print("Please enter a valid command.")
        user_response = input("Enter 1 to confirm deletion of question. Enter 2 to remove a different question. If not, please enter # to go back to Remove question: ")

    if user_response == "1":
        remove_question(qn_id)
    elif user_response == "2":
        remove_question_page()
    elif user_response == "#":
        remove_question_home_page()

def print_question_and_answers(question, answer_list):
    """Displays question and answer(s)
    
    Args:
        question: Question object to be displayed
        answer_list: List of Answer object(s) of question
    """
    answer_display_str = "Answer" if len(answer_list) == 1 else "Answers" 
    multiple_answer_str = format_multiple_answer_str(answer_list)

    print("\nQuestion Unique ID: {} \
                \nQuestion: {} \
                \n\n{}: {}\n".format(question._id, question._name, answer_display_str, multiple_answer_str))
        
def remove_question(qn_id):
    """Removes question by user id
    
    Args:
        qn_id: Question id
    """
    db.remove_question_by_id(int(qn_id))
    db.remove_answer_by_question_id(int(qn_id))
    
    clear_screen()
    print("------------------------------------------------------------------------")
    print("\nYou have successfully deleted the question and answer with unique id: {}".format(qn_id))
    print("Returning you to the settings page\n")
    print("------------------------------------------------------------------------")
    time.sleep(2)
    settings_page()

def clear_screen():
    """Clears terminal output.
       
    Code taken from: https://stackoverflow.com/questions/2084508/clear-terminal-in-python"""

    os.system('cls' if os.name == 'nt' else 'clear')

def initial_setup():
    """Setups if main.db doesn't exist"""
    is_db_created = os.path.exists('main.db')

    if not is_db_created:
        db.setup()

def main():
    """Main logic of program"""
    initial_setup()
    home_page()

if __name__ == '__main__':
    main()