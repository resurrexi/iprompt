import sqlite3
conn = sqlite3.connect('smsproto.db')

c = conn.cursor()

# Create tables
print("Creating answers table...")
c.execute("CREATE TABLE answers (question integer, phone text, answer integer, dt text)")

# TODO: Rename to answers_meta
print("Creating questions_meta table...")
c.execute("CREATE TABLE questions_meta (question integer, answer_choice text, answer_text text, value integer)")

# TODO: Rename to questions_meta and add a max_value field
print("Creating question_text table...")
c.execute("CREATE TABLE question_text (question integer, prompt text)")

print("Creating question_pointer table...")
c.execute("CREATE TABLE question_pointer (id integer primary key, question integer)")

print("Inserting default pointer...")
c.execute("INSERT INTO question_pointer VALUES (1, 0)")

print("Done!")
conn.commit()

conn.close()
