import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

flashcards = []
current_flashcard = 1
json_file = "flashcards.json"

def update_char_count(*args):
    example1 = example1_entry.get("1.0", "end-1c")
    example2 = example2_entry.get("1.0", "end-1c")
    total_example_chars = len(example1) + len(example2)
    char_count.set(f"{total_example_chars}/130")
    if total_example_chars > 130:
        char_count_label.config(foreground="red")
    else:
        char_count_label.config(foreground="black")
    
    definition_text = definition_entry.get("1.0", "end-1c")
    pronunciation_text = pronunciation_entry.get("1.0", "end-1c")
    total_def_pron_chars = len(definition_text) + len(pronunciation_text)
    def_pron_char_count.set(f"{total_def_pron_chars}/180")
    if total_def_pron_chars > 180:
        def_pron_char_count_label.config(foreground="red")
    else:
        def_pron_char_count_label.config(foreground="black")

def generate_html():
    global current_flashcard
    word = word_entry.get("1.0", "end-1c").strip()
    topic = topic_entry.get("1.0", "end-1c").strip()
    definition = definition_entry.get("1.0", "end-1c").strip()
    example1 = example1_entry.get("1.0", "end-1c").strip()
    example2 = example2_entry.get("1.0", "end-1c").strip()
    pronunciation = pronunciation_entry.get("1.0", "end-1c").strip()

    if len(example1) + len(example2) > 130:
        messagebox.showerror("Error", "Examples combined length exceeds 130 characters.")
        return

    if len(definition) + len(pronunciation) > 180:
        messagebox.showerror("Error", "Definition and pronunciation combined length exceeds 180 characters.")
        return

    example1 = example1.replace(word, f"<strong>{word}</strong>")
    example2 = example2.replace(word, f"<strong>{word}</strong>")

    flashcard = f"""
    <div class="word-card">
      <div class="word"><strong>Word: </strong>{word}</div>
      <div class="topic"><strong>Topic: </strong>{topic}</div>
      <div class="definition-and-pronunciation"><em>[ {pronunciation} ]</em> {definition}</div>
      <div class="examples">
        <strong>Examples: </strong>
        <li>{example1}</li>
        <li>{example2}</li>
      </div>
    </div>
    """

    flashcards.append(flashcard)
    if len(flashcards) == 15:
        write_html_file()
        flashcards.clear()
        current_flashcard = 1
    else:
        current_flashcard += 1

    update_flashcard_label()

def write_html_file():
    file_name = file_name_entry.get("1.0", "end-1c").strip()
    if not file_name:
        file_name = "flashcards"

    html_content = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>A4</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Zilla+Slab:ital,wght@0,300;0,400;0,500;0,600;0,700&display=swap");

      * {{
        font-family: "Zilla Slab";
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        line-height: 0.9;
        list-style: none;
      }}

      body {{
        background: rgb(204, 204, 204);
      }}

      .a4-div > p,
      span,
      li,
      td {{
        font-size: 13.5pt;
      }}

      .a4-div {{
        display: flex;
        flex-direction: column;
        background: white;
        margin: 0 auto;
        margin-bottom: 0.5cm;
        box-shadow: 0 0 0.5cm rgba(0, 0, 0, 0.5);
        flex-wrap: wrap;
        gap: 1px; /* Set a small gap between items */
        padding: 0; /* Ensure no extra padding */
        width: 21cm; /* Explicitly set width */
        height: 29.7cm; /* Explicitly set height */
      }}

      .a4-div[size="A4"] {{
        width: 21cm;
        height: 29.7cm;
      }}

      .a4-div[size="A4"][layout="portrait"] {{
        width: 29.7cm;
        height: 21cm;
      }}

      @media print {{
        body,
        page {{
          margin: 0;
          box-shadow: 0;
        }}
      }}

      .word-card {{
        width: calc(33.33% - 1px); /* Adjust width to account for gap */
        height: calc(20% - 1px); /* Adjust height to account for gap */
        border: 1px solid black;
        background-color: rgb(239, 239, 239);
        box-sizing: border-box;
      }}

      .word {{
        display: flex;
        justify-content: space-between;
        font-weight: bold;
        border-bottom: 1px solid black;
        padding-bottom: 2px;
        margin-bottom: 2px;
      }}

      .topic {{
        font-style: italic;
        border-bottom: 1px solid black;
        padding-bottom: 2px;
        margin-bottom: 2px;
      }}

      .definition-and-pronunciation {{
        border-bottom: 1px solid black;
        padding-bottom: 2px;
        margin-bottom: 2px;
      }}

      .examples {{
        line-height: 0.9;
      }}

      .examples li {{
        margin-bottom: 1px;
      }}
    </style>
  </head>
  <body>
    <div class="a4-div" size="A4">
      {" ".join(flashcards)}
    </div>
  </body>
</html>'''

    with open(f"{file_name}_{current_flashcard//15}.html", "w") as file:
        file.write(html_content)
    messagebox.showinfo("Success", "HTML file generated successfully!")

def update_flashcard_label():
    flashcard_label.config(text=f"Creating Flashcard: {current_flashcard}/15")

def save_progress():
    global flashcards, current_flashcard
    data = {
        "flashcards": flashcards,
        "current_flashcard": current_flashcard
    }
    with open(json_file, "w") as file:
        json.dump(data, file)
    messagebox.showinfo("Success", "Progress saved successfully!")

def load_progress():
    global flashcards, current_flashcard
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
            flashcards = data.get("flashcards", [])
            current_flashcard = data.get("current_flashcard", 1)
            update_flashcard_label()

def clear_progress():
    global flashcards, current_flashcard
    if os.path.exists(json_file):
        os.remove(json_file)
    flashcards.clear()
    current_flashcard = 1
    update_flashcard_label()
    messagebox.showinfo("Success", "Progress cleared successfully!")

def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")
    return 'break'

def copy(event):
    event.widget.event_generate('<<Copy>>')
    return 'break'

def paste(event):
    event.widget.event_generate('<<Paste>>')
    return 'break'

def undo(event):
    event.widget.edit_undo()
    return 'break'

root = tk.Tk()
root.title("Flashcard Generator")

root.geometry("800x600")
root.minsize(600, 400)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

for i in range(2):
    root.columnconfigure(i, weight=1)

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), foreground="blue")
style.configure("TButton", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="white")
style.configure("TFrame", background="#f0f0f0")

frame.configure(style="TFrame")

ttk.Label(frame, text="Word:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
word_entry = tk.Text(frame, width=50, height=2, wrap='word', undo=True, font=("Helvetica", 12))
word_entry.grid(row=0, column=1, pady=5, sticky="ew")

ttk.Label(frame, text="Topic:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
topic_entry = tk.Text(frame, width=50, height=2, wrap='word', undo=True, font=("Helvetica", 12))
topic_entry.grid(row=1, column=1, pady=5, sticky="ew")

ttk.Label(frame, text="Definition:", style="TLabel").grid(row=2, column=0, sticky=tk.W)
definition_entry = tk.Text(frame, width=50, height=2, wrap='word', undo=True, font=("Helvetica", 12))
definition_entry.grid(row=2, column=1, pady=5, sticky="ew")

ttk.Label(frame, text="Example 1:", style="TLabel").grid(row=3, column=0, sticky=tk.W)
example1_entry = tk.Text(frame, width=50, height=2, wrap='word', undo=True, font=("Helvetica", 12))
example1_entry.grid(row=3, column=1, pady=5, sticky="ew")
example1_entry.bind("<KeyRelease>", update_char_count)

ttk.Label(frame, text="Example 2:", style="TLabel").grid(row=4, column=0, sticky=tk.W)
example2_entry = tk.Text(frame, width=50, height=2, wrap='word', undo=True, font=("Helvetica", 12))
example2_entry.grid(row=4, column=1, pady=5, sticky="ew")
example2_entry.bind("<KeyRelease>", update_char_count)

ttk.Label(frame, text="Pronunciation:", style="TLabel").grid(row=5, column=0, sticky=tk.W)
pronunciation_entry = tk.Text(frame, width=50, height=2, wrap='word', undo=True, font=("Helvetica", 12))
pronunciation_entry.grid(row=5, column=1, pady=5, sticky="ew")
pronunciation_entry.bind("<KeyRelease>", update_char_count)

char_count = tk.StringVar()
char_count_label = ttk.Label(frame, textvariable=char_count, style="TLabel")
char_count_label.grid(row=6, column=1, sticky=tk.W)
char_count.set("0/130")

def_pron_char_count = tk.StringVar()
def_pron_char_count_label = ttk.Label(frame, textvariable=def_pron_char_count, style="TLabel")
def_pron_char_count_label.grid(row=7, column=1, sticky=tk.W)
def_pron_char_count.set("0/180")

ttk.Label(frame, text="HTML File Name:", style="TLabel").grid(row=8, column=0, sticky=tk.W)
file_name_entry = tk.Text(frame, width=50, height=1, wrap='word', undo=True, font=("Helvetica", 12))
file_name_entry.grid(row=8, column=1, pady=5, sticky="ew")

flashcard_label = ttk.Label(frame, text=f"Creating Flashcard: {current_flashcard}/15", style="TLabel")
flashcard_label.grid(row=9, column=0, columnspan=2, pady=5)

ttk.Button(frame, text="Generate HTML", command=generate_html).grid(row=10, column=1, sticky=tk.E, pady=5)
ttk.Button(frame, text="Save Progress", command=save_progress).grid(row=10, column=0, sticky=tk.W, pady=5)
ttk.Button(frame, text="Clear Progress", command=clear_progress).grid(row=11, column=0, sticky=tk.W, pady=5)
ttk.Button(frame, text="Load Progress", command=load_progress).grid(row=11, column=1, sticky=tk.E, pady=5)

update_flashcard_label()

for widget in [word_entry, topic_entry, definition_entry, example1_entry, example2_entry, pronunciation_entry]:
    widget.bind('<Control-a>', select_all)
    widget.bind('<Control-A>', select_all)
    widget.bind('<Control-c>', copy)
    widget.bind('<Control-C>', copy)
    widget.bind('<Control-v>', paste)
    widget.bind('<Control-V>', paste)
    widget.bind('<Control-z>', undo)
    widget.bind('<Control-Z>', undo)

load_progress()
root.mainloop()