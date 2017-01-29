import sqlite3
conn = sqlite3.connect('smsproto.db')

c = conn.cursor()

# Dump values into table
print("Populating questions_meta...")
# question, answer_choice, answer_text, value
values = [(1, 'a', 'Coefficients', 0),
          (1, 'b', 'Residuals', 0),
          (1, 'c', 'SSE (Sum squared errors)', 1),
          (1, 'd', 'R-squared value', 0),
          (2, 'a', 'Supervised', 0),
          (2, 'b', 'Unsupervised', 1),
          (3, 'a', 'Overfit', 1),
          (3, 'b', 'Underfit', 0),
          (4, 'a', '[-1, 1]', 0),
          (4, 'b', '[0, 1]', 1),
          (5, 'a', 'Left skewed (long tail on left)', 1),
          (5, 'b', 'Right skewed (long tail on right)', 0),
          (6, 'a', 'None', 0),
          (6, 'b', '1', 1),
          (6, 'c', '2', 2),
          (6, 'd', '3', 3),
          (6, 'e', '4', 4),
          (6, 'f', '5', 5),
          (6, 'g', 'All of them', 6),
          (7, 'a', 'Neither', 0),
          (7, 'b', 'Only Python', 1),
          (7, 'c', 'Only R', 1),
          (7, 'd', 'Both', 2)]

c.executemany("INSERT INTO questions_meta VALUES (?,?,?,?)", values)

print("Populating question_text...")
# question, prompt
values = [(1, 'When building a linear regression model in a machine learning context, you want to apply gradient descent on the _____.'),
          (2, 'Clustering is _____.'),
          (3, 'A model with high variance indicates _____.'),
          (4, 'When the logistic function is used as the activation function for building an artificial neural network, then normalizing the inputs to the range _____ is preferred.'),
          (5, 'If the median is greater than the mean, then the population is _____.'),
          (6, 'How many of these technologies/services listed below are you comfortable working with?<br><br>Cloud (AWS, Azure, Google Cloud)<br>Git/GitHub<br>NoSQL<br>Hadoop<br>REST APIs<br>Linux/Unix command line'),
          (7, 'Can you build a model in Python or R?')]

c.executemany("INSERT INTO question_text VALUES (?,?)", values)

print("Done!")
conn.commit()

conn.close()
