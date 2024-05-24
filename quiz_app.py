import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
# Define user data and quiz data
user_data_file = 'users.json'
quiz_data_file = 'quiz.json'

# Load user data
if os.path.exists(user_data_file):
    with open(user_data_file, 'r') as f:
        users = json.load(f)
else:
    users = {
        'teacher': {'password': 'teacher123', 'role': 'teacher'},
        'student': {'password': 'student123', 'role': 'student'}
    }
    with open(user_data_file, 'w') as f:
        json.dump(users, f)

# Load quiz data
if os.path.exists(quiz_data_file):
    with open(quiz_data_file, 'r') as f:
        quiz_data = json.load(f)
else:
    quiz_data = {
        'questions': [
            {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "answer": "Paris"
            },
            {
                "question": "What is the largest planet in our Solar System?",
                "options": ["Earth", "Mars", "Jupiter", "Saturn"],
                "answer": "Jupiter"
            },
            {
                "question": "Who wrote 'Hamlet'?",
                "options": ["Charles Dickens", "William Shakespeare", "J.K. Rowling", "Mark Twain"],
                "answer": "William Shakespeare"
            }
        ],
        'scores': {}
    }
    with open(quiz_data_file, 'w') as f:
        json.dump(quiz_data, f)
class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quiz")
        self.current_user = None

        self.create_login_page()

    def create_login_page(self):
        self.clear_window()
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=10)

        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=10)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username]['password'] == password:
            self.current_user = username
            role = users[username]['role']
            if role == 'teacher':
                self.create_teacher_page()
            elif role == 'student':
                self.create_student_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_teacher_page(self):
        self.clear_window()
        tk.Label(self.root, text="Teacher Page").pack(pady=10)
        tk.Button(self.root, text="Manage Questions", command=self.manage_questions).pack(pady=10)
        tk.Button(self.root, text="View Scores", command=self.view_scores).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.create_login_page).pack(pady=10)

    def manage_questions(self):
        self.clear_window()
        tk.Label(self.root, text="Manage Questions").pack(pady=10)

        self.question_listbox = tk.Listbox(self.root)
        self.question_listbox.pack(pady=10)
        self.load_questions()

        tk.Button(self.root, text="Add Question", command=self.add_question).pack(pady=5)
        tk.Button(self.root, text="Edit Question", command=self.edit_question).pack(pady=5)
        tk.Button(self.root, text="Delete Question", command=self.delete_question).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_teacher_page).pack(pady=10)

    def load_questions(self):
        self.question_listbox.delete(0, tk.END)
        for q in quiz_data['questions']:
            self.question_listbox.insert(tk.END, q['question'])

    def add_question(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        options = [
            simpledialog.askstring("Input", "Option 1:"),
            simpledialog.askstring("Input", "Option 2:"),
            simpledialog.askstring("Input", "Option 3:"),
            simpledialog.askstring("Input", "Option 4:")
        ]
        answer = simpledialog.askstring("Input", "Enter the correct answer:")
        quiz_data['questions'].append({"question": question, "options": options, "answer": answer})
        self.save_quiz_data()
        self.load_questions()

    def edit_question(self):
        selected_index = self.question_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Select a question to edit")
            return
        index = selected_index[0]
        question = quiz_data['questions'][index]
        new_question = simpledialog.askstring("Input", "Edit the question:", initialvalue=question['question'])
        new_options = [
            simpledialog.askstring("Input", "Option 1:", initialvalue=question['options'][0]),
            simpledialog.askstring("Input", "Option 2:", initialvalue=question['options'][1]),
            simpledialog.askstring("Input", "Option 3:", initialvalue=question['options'][2]),
            simpledialog.askstring("Input", "Option 4:", initialvalue=question['options'][3])
        ]
        new_answer = simpledialog.askstring("Input", "Edit the correct answer:", initialvalue=question['answer'])
        quiz_data['questions'][index] = {"question": new_question, "options": new_options, "answer": new_answer}
        self.save_quiz_data()
        self.load_questions()

    def delete_question(self):
        selected_index = self.question_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Select a question to delete")
            return
        index = selected_index[0]
        del quiz_data['questions'][index]
        self.save_quiz_data()
        self.load_questions()

    def view_scores(self):
        self.clear_window()
        tk.Label(self.root, text="Student Scores").pack(pady=10)
        score_listbox = tk.Listbox(self.root)
        score_listbox.pack(pady=10)
        for student, score in quiz_data['scores'].items():
            score_listbox.insert(tk.END, f"{student}: {score}")
        tk.Button(self.root, text="Back", command=self.create_teacher_page).pack(pady=10)

    def create_student_page(self):
        self.clear_window()
        tk.Label(self.root, text="Student Page").pack(pady=10)
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.create_login_page).pack(pady=10)

    def start_quiz(self):
        self.clear_window()
        self.quiz = Quiz(self.root, quiz_data['questions'], self.current_user, self.quiz_completed)

    def quiz_completed(self, score):
        quiz_data['scores'][self.current_user] = score
        self.save_quiz_data()
        self.create_student_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def save_quiz_data(self):
        with open(quiz_data_file, 'w') as f:
            json.dump(quiz_data, f)
class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quiz")
        self.current_user = None

        self.create_login_page()

    def create_login_page(self):
        self.clear_window()
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=10)

        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=10)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username]['password'] == password:
            self.current_user = username
            role = users[username]['role']
            if role == 'teacher':
                self.create_teacher_page()
            elif role == 'student':
                self.create_student_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_teacher_page(self):
        self.clear_window()
        tk.Label(self.root, text="Teacher Page").pack(pady=10)
        tk.Button(self.root, text="Manage Questions", command=self.manage_questions).pack(pady=10)
        tk.Button(self.root, text="View Scores", command=self.view_scores).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.create_login_page).pack(pady=10)

    def manage_questions(self):
        self.clear_window()
        tk.Label(self.root, text="Manage Questions").pack(pady=10)

        self.question_listbox = tk.Listbox(self.root)
        self.question_listbox.pack(pady=10)
        self.load_questions()

        tk.Button(self.root, text="Add Question", command=self.add_question).pack(pady=5)
        tk.Button(self.root, text="Edit Question", command=self.edit_question).pack(pady=5)
        tk.Button(self.root, text="Delete Question", command=self.delete_question).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_teacher_page).pack(pady=10)

    def load_questions(self):
        self.question_listbox.delete(0, tk.END)
        for q in quiz_data['questions']:
            self.question_listbox.insert(tk.END, q['question'])

    def add_question(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        options = [
            simpledialog.askstring("Input", "Option 1:"),
            simpledialog.askstring("Input", "Option 2:"),
            simpledialog.askstring("Input", "Option 3:"),
            simpledialog.askstring("Input", "Option 4:")
        ]
        answer = simpledialog.askstring("Input", "Enter the correct answer:")
        quiz_data['questions'].append({"question": question, "options": options, "answer": answer})
        self.save_quiz_data()
        self.load_questions()

    def edit_question(self):
        selected_index = self.question_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Select a question to edit")
            return
        index = selected_index[0]
        question = quiz_data['questions'][index]
        new_question = simpledialog.askstring("Input", "Edit the question:", initialvalue=question['question'])
        new_options = [
            simpledialog.askstring("Input", "Option 1:", initialvalue=question['options'][0]),
            simpledialog.askstring("Input", "Option 2:", initialvalue=question['options'][1]),
            simpledialog.askstring("Input", "Option 3:", initialvalue=question['options'][2]),
            simpledialog.askstring("Input", "Option 4:", initialvalue=question['options'][3])
        ]
        new_answer = simpledialog.askstring("Input", "Edit the correct answer:", initialvalue=question['answer'])
        quiz_data['questions'][index] = {"question": new_question, "options": new_options, "answer": new_answer}
        self.save_quiz_data()
        self.load_questions()

    def delete_question(self):
        selected_index = self.question_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Select a question to delete")
            return
        index = selected_index[0]
        del quiz_data['questions'][index]
        self.save_quiz_data()
        self.load_questions()

    def view_scores(self):
        self.clear_window()
        tk.Label(self.root, text="Student Scores").pack(pady=10)
        score_listbox = tk.Listbox(self.root)
        score_listbox.pack(pady=10)
        for student, score in quiz_data['scores'].items():
            score_listbox.insert(tk.END, f"{student}: {score}")
        tk.Button(self.root, text="Back", command=self.create_teacher_page).pack(pady=10)

    def create_student_page(self):
        self.clear_window()
        tk.Label(self.root, text="Student Page").pack(pady=10)
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.create_login_page).pack(pady=10)

    def start_quiz(self):
        self.clear_window()
        self.quiz = Quiz(self.root, quiz_data['questions'], self.current_user, self.quiz_completed)

    def quiz_completed(self, score):
        quiz_data['scores'][self.current_user] = score
        self.save_quiz_data()
        self.create_student_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def save_quiz_data(self):
        with open(quiz_data_file, 'w') as f:
            json.dump(quiz_data, f)
class Quiz:
    def __init__(self, root, questions, username, on_complete):
        self.root = root
        self.questions = questions
        self.username = username
        self.on_complete = on_complete
        self.score = 0
        self.current_question = 0
        self.user_answers = []

        # Configure the quiz window
        self.root.title("Quiz")
        self.question_label = tk.Label(root, text="", wraplength=350)
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.option_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(root, text="", variable=self.var, value="", command=self.on_select)
            btn.pack(anchor='w')
            self.option_buttons.append(btn)

        self.next_button = tk.Button(root, text="Next", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=20)

        self.display_question()

    def display_question(self):
        question = self.questions[self.current_question]
        self.question_label.config(text=f"Q{self.current_question + 1}: {question['question']}")
        self.var.set(None)
        for i, option in enumerate(question['options']):
            self.option_buttons[i].config(text=option, value=option)
        self.next_button.config(state=tk.DISABLED)

    def on_select(self):
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        user_answer = self.var.get()
        self.user_answers.append(user_answer)
        if user_answer == self.questions[self.current_question]['answer']:
            self.score += 1

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.on_complete(self.score)

# Initialize the main application
root = tk.Tk()
app = Application(root)
root.mainloop()
