#TASK 2- Quiz application
#Date- 10/09/2023
#Programmer- Saumya singh(saumyasingh635@gmail.com)


from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import json
#setting the credential for user name and password
teacher_credentials = {"teacher_username": "teacher_password"}
class quiz_app:
    def __init__(self,root):
        self.root=root
        self.root.title("Quiz app")
        self.root.iconbitmap("")
        self.root.geometry("860x800")
        self.root.resizable(TRUE,TRUE)
        #designing frames
        self.frame_=Frame(self.root,height=800,width=800,bg='beige',highlightbackground="burlywood4", highlightcolor="burlywood", highlightthickness=5)
        self.frame_.pack_configure(side=TOP)
        self.login_frame =Frame(self.root,height=800,width=800,bg='beige',highlightbackground="burlywood4", highlightcolor="burlywood", highlightthickness=5)
        self.quiz_frame =Frame(self.root,height=800,width=800,bg='beige',highlightbackground="burlywood4", highlightcolor="burlywood", highlightthickness=5)
        self.questions=[]
        self.current_question=0

        self.selected_option = IntVar()
        self.quiz_home()

    #creating the home page for the quiz application
    def quiz_home(self):  
        if self.quiz_frame:
            self.quiz_frame.destroy()
        #heading 
        head=Label(self.frame_,text="\t\t\tQuiz \t\t\t",font="Times 20 italic bold",bg="antiquewhite3")
        head.pack_configure()
        login=Label(self.frame_,text="\t\t\tlogin\t\t\t",font="Times 15 italic")
        login.pack_configure()
        admin_login=Button(self.frame_,text='Admin ',padx=20,pady=10,cursor='hand2',background='deepskyblue',highlightcolor='burlywood4',command=self.teacher_login)
        admin_login.pack_configure()
        student_login=Button(self.frame_,text='Player',padx=20,pady=10,cursor='hand2',background='deepskyblue',highlightcolor='burlywood4',command=self.show_student_dashboard)
        student_login.pack_configure()
    #login page for the teacher
    def teacher_login(self):
        if self.frame_:
            self.frame_.destroy()
        self.login_frame = Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)
        self.username_label =Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry =Entry(self.login_frame)
        self.username_entry.pack()
        self.password_label = Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.pack()
        #passing control to login function through login button
        self.login_button = Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

    
    #login function to check the validity of the username and password
    def login(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        #setting default username as "teacher" and default password as "password"
        if username == "teacher" and password == "password":
            self.current_user = "teacher"
            self.show_teacher_dashboard()
        elif username in teacher_credentials and teacher_credentials[username] == password:
            self.current_user = "teacher"
            self.show_teacher_dashboard()
        elif username != "" and password != "":
            self.current_user = "student"
            self.show_student_dashboard()
        else:
            #shows the message box if credentials are left empty
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")
     #teacher dashbord
    def show_teacher_dashboard(self):
        if self.login_frame:
            self.login_frame.destroy()
        
        self.quiz_frame =Frame(self.root)
        self.quiz_frame.pack(padx=20, pady=20)

        self.create_quiz_button = Button(self.quiz_frame, text="Create Quiz", command=self.create_quiz)
        self.create_quiz_button.pack()
    
    #student dashbord
    def show_student_dashboard(self):
        if self.frame_:
            self.frame_.destroy()
        
        self.quiz_frame = Frame(self.root)
        self.quiz_frame.pack(padx=20, pady=20)

        self.take_quiz_button = Button(self.quiz_frame, text="Take Quiz", command=self.load_quiz)
        self.take_quiz_button.pack()

    #Quiz creation gui menu
    def create_quiz(self):
             self.question_label = Label(self.root, text="Enter a question:")
             self.question_label.pack()

             self.question_entry = Entry(self.root, width=50)
             self.question_entry.pack()

             self.option_labels = []
             self.option_entries = []

             for i in range(4):
                 option_label = Label(self.root, text=f"Option {i + 1}:")
                 option_label.pack()
                 self.option_labels.append(option_label)

                 option_entry = Entry(self.root, width=50)
                 option_entry.pack()
                 self.option_entries.append(option_entry)

             self.add_question_button = Button(self.root, text="Add Question", command=self.add_question)
             self.add_question_button.pack()

             self.save_quiz_button = Button(self.root, text="Save Quiz", command=self.save_quiz)
             self.save_quiz_button.pack()
             self.home_button=Button(self.root, text="Save Quiz", command=self.quiz_home)
             self.home_button.pack()
    def add_question(self):
        question_text = self.question_entry.get()
        options = [entry.get() for entry in self.option_entries]

        if question_text and all(options):
            question_data = {
                "question": question_text,
                "options": options
            }
            self.questions.append(question_data)
            # Clear the input fields
            self.question_entry.delete(0, END)
            for entry in self.option_entries:
                entry.delete(0, END)
        else:
            messagebox.showerror("Error", "Please enter a question and all four options.")

    def save_quiz(self):
        if not self.questions:
            messagebox.showerror("Error", "No questions added to the quiz.")
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if file_path:
                try:
                    # Write the quiz data to the chosen JSON file
                    with open(file_path, 'a') as file:
                        json.dump(self.questions, file, indent=4)

                    messagebox.showinfo("Quiz Saved", "Quiz has been saved.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save the quiz: {str(e)}")

    def load_quiz(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                # Load the quiz data from the chosen JSON file
                with open(file_path, 'r') as file:
                    self.questions = json.load(file)
                self.current_question=0
                self.take_quiz()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the quiz: {str(e)}")


    def take_quiz(self):
        if self.questions:
            self.quiz_frame.destroy()
            #self.next_ques()
            if self.current_question < len(self.questions):
                # Clear the previous question interface
                for widget in self.root.winfo_children():
                    widget.destroy()
                question_data = self.questions[self.current_question]
                question_text = question_data["question"]
                options = question_data["options"]
                self.question_label = Label(self.root, text=question_text, font=("Arial", 12))
                self.question_label.pack(pady=10)
                self.option_buttons = []
                for i, option in enumerate(options):
                    option_button = Radiobutton(self.root, text=option, variable=self.selected_option, value=i)
                    option_button.pack(pady=5)
                    self.option_buttons.append(option_button) 
                self.current_question+=1
                self.next_button=Button(self.root,text="Next",command=self.take_quiz)  
                self.next_button.pack()
            else:   
                self.submit_button=Button(self.root,text="Submit",command=self.save_quiz)  
                self.submit_button.pack()
        else:
            messagebox.showerror("Error", "No quiz questions loaded.")
        
                


if __name__ == "__main__":
    root = Tk()
    app = quiz_app(root)
    
    root.mainloop()       