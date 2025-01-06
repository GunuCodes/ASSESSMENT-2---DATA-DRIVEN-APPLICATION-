import os
import html
import requests
from tkinter import *

# Set up colors and visual settings for the app
THEME_COLOR = "#2C3E50"
SECONDARY_COLOR = "#F6BE00"
TERTIARY_COLOR = "#B58B00"
TEXT_COLOR = "#ECF0F1"
CORRECT_COLOR = "#27AE60"
WRONG_COLOR = "#E74C3C"
START_BG_COLOR = "#34495E"
FONT_NAME = "Arial"
TITLE_COLORS = ["#3498DB", "#E67E22", "#E91E63", "#27AE60"] 

# Dictionary mapping category names to their API ID numbers
CATEGORIES = {
    "General Knowledge": 9,
    "History": 23,
    "Geography": 22,
    "Animals": 27,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Video Games": 15,
    "Science & Nature": 17,
    "Computer Science": 18
}

# Simple class to store each question and its answer
class Question:
    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer

# Handles the quiz logic (scoring, question progression)
class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    # Check if there are more questions to ask
    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    # Get the next question in the quiz
    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    # Check if user's answer is correct and update score
    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False

# Main quiz interface where questions are displayed
class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain, window):
        self.quiz = quiz_brain
        self.window = window
        
        # Update window configuration
        self.window.config(padx=40, pady=40, bg=THEME_COLOR)
        
        # Main container to center everything
        main_container = Frame(self.window, bg=THEME_COLOR)
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights to center the container
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Question Counter Frame
        question_frame = Frame(main_container, bg=THEME_COLOR)
        question_frame.pack(fill=X, pady=(0, 10))
        
        # Center container for question counter
        question_container = Frame(question_frame, bg=THEME_COLOR)
        question_container.pack(expand=True)
        
        question_text = Label(
            question_container,
            text="Question:",
            fg=TEXT_COLOR,
            bg=THEME_COLOR,
            font=(FONT_NAME, 14)
        )
        question_text.pack(side=LEFT, padx=5)
        
        self.question_number = Label(
            question_container,
            text="0/10",
            fg=SECONDARY_COLOR,
            bg=THEME_COLOR,
            font=(FONT_NAME, 24, "bold")
        )
        self.question_number.pack(side=LEFT)
        
        # Score Frame
        score_frame = Frame(main_container, bg=THEME_COLOR)
        score_frame.pack(fill=X, pady=(0, 20))
        
        # Center container for score
        score_container = Frame(score_frame, bg=THEME_COLOR)
        score_container.pack(expand=True)
        
        score_text = Label(
            score_container,
            text="Score:",
            fg=TEXT_COLOR,
            bg=THEME_COLOR,
            font=(FONT_NAME, 14)
        )
        score_text.pack(side=LEFT, padx=5)
        
        self.score_label = Label(
            score_container,
            text="0",
            fg=SECONDARY_COLOR,
            bg=THEME_COLOR,
            font=(FONT_NAME, 24, "bold")
        )
        self.score_label.pack(side=LEFT)
        
        # Canvas
        self.canvas = Canvas(
            main_container,
            width=400,
            height=250,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.pack(pady=30)

        self.background_rectangle = self.create_rounded_rectangle(10, 10, 390, 240, 20, fill="white")

        self.question_text = self.canvas.create_text(
            200,
            125,
            width=350,
            text="Question goes here",
            fill=THEME_COLOR,
            font=(FONT_NAME, 18, "bold"),
            justify="center"
        )

        # Button frame
        button_frame = Frame(main_container, bg=THEME_COLOR)
        button_frame.pack(pady=20)

        true_image = PhotoImage(file="images/true.png")
        false_image = PhotoImage(file="images/false.png")

        self.true_button = Button(
            button_frame,
            image=true_image,
            command=self.true_pressed,
            bg=THEME_COLOR,
            activebackground=THEME_COLOR,
            borderwidth=0,
            cursor="hand2"
        )
        self.true_button.image = true_image
        self.true_button.pack(side=LEFT, padx=20)

        self.false_button = Button(
            button_frame,
            image=false_image,
            command=self.false_pressed,
            bg=THEME_COLOR,
            activebackground=THEME_COLOR,
            borderwidth=0,
            cursor="hand2"
        )
        self.false_button.image = false_image
        self.false_button.pack(side=LEFT, padx=20)

        self.get_next_question()
        self.window.mainloop()

    # Creates rounded corners for the question box
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    # Shows next question or final score if quiz is done
    def get_next_question(self):
        self.canvas.itemconfig(self.background_rectangle, fill="white")
        self.score_label.config(fg=SECONDARY_COLOR)  # Reset to orange

        if self.quiz.still_has_questions():
            # Update question counter
            self.question_number.config(
                text=f"{self.quiz.question_number}/{len(self.quiz.question_list)}"
            )
            
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")
        else:
            # Final score screen
            self.question_number.config(text="10/10")
            final_score = f"{self.quiz.score}/{len(self.quiz.question_list)}"
            self.score_label.config(
                text=final_score,
                fg=CORRECT_COLOR if self.quiz.score > len(self.quiz.question_list)/2 
                else WRONG_COLOR
            )
            
            final_text = (
                f"Congratulations!\n\n"
                f"You got {self.quiz.score} out of {len(self.quiz.question_list)} "
                f"questions correct!"
            )
            self.canvas.itemconfig(
                self.question_text,
                text=final_text,
                font=(FONT_NAME, 24, "bold")
            )
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    # Shows if answer was correct/wrong and updates score
    def give_feedback(self, is_right):
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        
        # Update score color based on answer
        self.score_label.config(
            text=str(self.quiz.score),
            fg=CORRECT_COLOR if is_right else WRONG_COLOR
        )
        
        color = CORRECT_COLOR if is_right else WRONG_COLOR
        self.canvas.itemconfig(self.background_rectangle, fill=color)
        self.window.after(1000, self.get_next_question)

    # Handles when True button is clicked
    def true_pressed(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    # Handles when False button is clicked
    def false_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

# Gets questions from the trivia API based on chosen category
def get_question_data(category=9):
    parameters = {
        "amount": 10,
        "type": "boolean",
        "category": category
    }
    try:
        response = requests.get("https://opentdb.com/api.php", params=parameters)
        response.raise_for_status()
        data = response.json()
        
        if not data["results"]:
            raise ValueError("No questions available for selected category")
            
        return data["results"]
        
    except (requests.RequestException, ValueError) as e:
        return None

# Welcome screen with colorful title and start button
class StartScreen:
    def __init__(self):
        self.window = Tk()
        self.window.title("Open Trivia Quizzer")
        self.window.config(padx=40, pady=40, bg=START_BG_COLOR)
        self.window.resizable(False, False)
        
        # Title Frame
        title_frame = Frame(self.window, bg=START_BG_COLOR)
        title_frame.grid(row=0, column=0, pady=(0, 10))
        
        # "Open Trivia" with alternating colors
        top_title = "Open Trivia"
        for i, char in enumerate(top_title):
            if char != " ":
                Label(
                    title_frame,
                    text=char,
                    fg=TITLE_COLORS[i % 4],
                    bg=START_BG_COLOR,
                    font=(FONT_NAME, 24, "bold")
                ).grid(row=0, column=i, padx=1)
            else:
                Label(
                    title_frame,
                    text=" ",
                    bg=START_BG_COLOR,
                    font=(FONT_NAME, 24)
                ).grid(row=0, column=i, padx=1)
        
        # "QUIZ" in white
        Label(
            title_frame,
            text="QUIZZER",
            fg=TEXT_COLOR,
            bg=START_BG_COLOR,
            font=(FONT_NAME, 60, "bold")
        ).grid(row=1, column=0, columnspan=len(top_title), pady=(0, 20))
        
        # Description
        desc_label = Label(
            self.window,
            text="Test your knowledge about trivia of different\ncategories with 10 simple questions!",
            fg=TEXT_COLOR,
            bg=START_BG_COLOR,
            font=(FONT_NAME, 14),
            justify="center"
        )
        desc_label.grid(row=2, column=0, pady=(0, 40))
        
        # Start Button
        start_button = Button(
            self.window,
            text="Start Quiz",
            command=self.start_quiz,
            font=(FONT_NAME, 16, "bold"),
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR,
            padx=30,
            pady=10,
            borderwidth=0,
            cursor="hand2",
            activebackground=TERTIARY_COLOR,
            activeforeground=TEXT_COLOR
        )
        start_button.grid(row=3, column=0)
        
    # Switches to category selection when start is clicked
    def start_quiz(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        category_screen = CategoryScreen(self.window)

# Screen for selecting quiz category
class CategoryScreen:
    def __init__(self, window):
        self.window = window
        self.selected_category = StringVar(value="General Knowledge")
        
        # Main container
        main_container = Frame(self.window, bg=START_BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Title
        title_label = Label(
            main_container,
            text="Select Category",
            fg=TEXT_COLOR,
            bg=START_BG_COLOR,
            font=(FONT_NAME, 32, "bold")
        )
        title_label.pack(pady=(0, 40))
        
        # Category Selection
        category_label = Label(
            main_container,
            text="Choose your quiz category:",
            fg=TEXT_COLOR,
            bg=START_BG_COLOR,
            font=(FONT_NAME, 14)
        )
        category_label.pack(pady=(0, 10))
        
        category_menu = OptionMenu(
            main_container,
            self.selected_category,
            *CATEGORIES.keys()
        )
        category_menu.config(
            font=(FONT_NAME, 12),
            bg=THEME_COLOR,
            fg=TEXT_COLOR,
            activebackground=SECONDARY_COLOR,
            activeforeground=TEXT_COLOR,
            highlightthickness=0,
            borderwidth=0,
            padx=20,
            pady=5
        )
        category_menu["menu"].config(
            bg=THEME_COLOR,
            fg=TEXT_COLOR,
            activebackground=SECONDARY_COLOR,
            activeforeground=TEXT_COLOR,
            font=(FONT_NAME, 12)
        )
        category_menu.pack(pady=(0, 40))
        
        # Start Quiz button
        start_button = Button(
            main_container,
            text="Start Quiz",
            command=self.start_quiz,
            font=(FONT_NAME, 16, "bold"),
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR,
            padx=30,
            pady=10,
            borderwidth=0,
            cursor="hand2",
            activebackground=TERTIARY_COLOR,
            activeforeground=TEXT_COLOR
        )
        start_button.pack()
    
    # Starts the quiz with selected category
    def start_quiz(self):
        category_id = CATEGORIES[self.selected_category.get()]
        question_data = get_question_data(category_id)
        
        # Show error if no questions available
        if question_data is None or len(question_data) == 0:
            error_label = Label(
                self.window,
                text="No questions available for this category.\nPlease try a different one.",
                fg=WRONG_COLOR,
                bg=START_BG_COLOR,
                font=(FONT_NAME, 14),
                justify="center"
            )
            error_label.place(relx=0.5, rely=0.8, anchor=CENTER)
            self.window.after(3000, error_label.destroy)
            return
        
        # Create questions and start quiz if successful
        question_bank = []
        for question in question_data:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            question_bank.append(new_question)
        
        if question_bank:
            for widget in self.window.winfo_children():
                widget.destroy()
            
            quiz = QuizBrain(question_bank)
            quiz_ui = QuizInterface(quiz, self.window)

# Start the application
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    start_screen = StartScreen()
    start_screen.window.mainloop()
