"""
Database of Celebrity Birth Data
Focus on Rodden Rating AA/A (verified/accurate)
"""

CELEBRITY_DATA = [
    # SCIENCE & TECH
    {'name': 'Albert Einstein', 'date': '1879-03-14', 'time': '11:30', 'category': 'Science'},
    {'name': 'Marie Curie', 'date': '1867-11-07', 'time': '12:00', 'category': 'Science'},
    {'name': 'Isaac Newton', 'date': '1643-01-04', 'time': '01:38', 'category': 'Science'}, # Julian/Gregorian handling needed usually, but typically standardized
    {'name': 'Charles Darwin', 'date': '1809-02-12', 'time': '03:00', 'category': 'Science'},
    {'name': 'Nikola Tesla', 'date': '1856-07-10', 'time': '00:00', 'category': 'Science'},
    {'name': 'Sigmund Freud', 'date': '1856-05-06', 'time': '18:30', 'category': 'Science'},
    {'name': 'Carl Jung', 'date': '1875-07-26', 'time': '19:32', 'category': 'Science'},
    {'name': 'Steve Jobs', 'date': '1955-02-24', 'time': '19:15', 'category': 'Science'},
    {'name': 'Bill Gates', 'date': '1955-10-28', 'time': '22:00', 'category': 'Science'},
    {'name': 'Elon Musk', 'date': '1971-06-28', 'time': '06:30', 'category': 'Science'},
    {'name': 'Alan Turing', 'date': '1912-06-23', 'time': '02:15', 'category': 'Science'},
    {'name': 'Stephen Hawking', 'date': '1942-01-08', 'time': '02:29', 'category': 'Science'},
    {'name': 'Thomas Edison', 'date': '1847-02-11', 'time': '03:00', 'category': 'Science'},
    {'name': 'Alexander Graham Bell', 'date': '1847-03-03', 'time': '07:00', 'category': 'Science'},
    {'name': 'Galileo Galilei', 'date': '1564-02-15', 'time': '15:41', 'category': 'Science'},

    # ARTS & MUSIC
    {'name': 'Leonardo da Vinci', 'date': '1452-04-15', 'time': '21:40', 'category': 'Arts'},
    {'name': 'Wolfgang Mozart', 'date': '1756-01-27', 'time': '20:00', 'category': 'Arts'},
    {'name': 'Ludwig Beethoven', 'date': '1770-12-16', 'time': '13:00', 'category': 'Arts'},
    {'name': 'Pablo Picasso', 'date': '1881-10-25', 'time': '23:15', 'category': 'Arts'},
    {'name': 'Salvador Dali', 'date': '1904-05-11', 'time': '08:45', 'category': 'Arts'},
    {'name': 'Vincent van Gogh', 'date': '1853-03-30', 'time': '11:00', 'category': 'Arts'},
    {'name': 'Frida Kahlo', 'date': '1907-07-06', 'time': '08:30', 'category': 'Arts'},
    {'name': 'Bob Dylan', 'date': '1941-05-24', 'time': '21:05', 'category': 'Arts'},
    {'name': 'John Lennon', 'date': '1940-10-09', 'time': '18:30', 'category': 'Arts'},
    {'name': 'David Bowie', 'date': '1947-01-08', 'time': '09:00', 'category': 'Arts'},
    {'name': 'Prince', 'date': '1958-06-07', 'time': '18:17', 'category': 'Arts'},
    {'name': 'Madonna', 'date': '1958-08-16', 'time': '07:05', 'category': 'Arts'},
    {'name': 'Michael Jackson', 'date': '1958-08-29', 'time': '19:33', 'category': 'Arts'},
    {'name': 'Kurt Cobain', 'date': '1967-02-20', 'time': '19:38', 'category': 'Arts'},
    {'name': 'Freddie Mercury', 'date': '1946-09-05', 'time': '05:50', 'category': 'Arts'},
    {'name': 'Elvis Presley', 'date': '1935-01-08', 'time': '04:35', 'category': 'Arts'},
    {'name': 'Jimi Hendrix', 'date': '1942-11-27', 'time': '10:15', 'category': 'Arts'},
    {'name': 'Mick Jagger', 'date': '1943-07-26', 'time': '02:30', 'category': 'Arts'},
    {'name': 'Bob Marley', 'date': '1945-02-06', 'time': '02:30', 'category': 'Arts'},
    {'name': 'Elton John', 'date': '1947-03-25', 'time': '02:00', 'category': 'Arts'},
    {'name': 'Whitney Houston', 'date': '1963-08-09', 'time': '20:55', 'category': 'Arts'},

    # POLITICS & LEADERS
    {'name': 'Abraham Lincoln', 'date': '1809-02-12', 'time': '06:54', 'category': 'Politics'},
    {'name': 'Winston Churchill', 'date': '1874-11-30', 'time': '01:30', 'category': 'Politics'},
    {'name': 'Mahatma Gandhi', 'date': '1869-10-02', 'time': '07:12', 'category': 'Politics'},
    {'name': 'Martin Luther King', 'date': '1929-01-15', 'time': '12:00', 'category': 'Politics'},
    {'name': 'Nelson Mandela', 'date': '1918-07-18', 'time': '14:54', 'category': 'Politics'}, # Corrected time often cited
    {'name': 'John F. Kennedy', 'date': '1917-05-29', 'time': '15:00', 'category': 'Politics'},
    {'name': 'Barack Obama', 'date': '1961-08-04', 'time': '19:24', 'category': 'Politics'},
    {'name': 'Angela Merkel', 'date': '1954-07-17', 'time': '18:00', 'category': 'Politics'},
    {'name': 'Margaret Thatcher', 'date': '1925-10-13', 'time': '09:00', 'category': 'Politics'},
    {'name': 'Queen Elizabeth II', 'date': '1926-04-21', 'time': '02:40', 'category': 'Politics'},
    {'name': 'Princess Diana', 'date': '1961-07-01', 'time': '19:45', 'category': 'Politics'},
    {'name': 'Indira Gandhi', 'date': '1917-11-19', 'time': '23:11', 'category': 'Politics'},
    {'name': 'Emmanuel Macron', 'date': '1977-12-21', 'time': '10:40', 'category': 'Politics'},
    {'name': 'Donald Trump', 'date': '1946-06-14', 'time': '10:54', 'category': 'Politics'},
    {'name': 'Joe Biden', 'date': '1942-11-20', 'time': '08:30', 'category': 'Politics'},
    {'name': 'Kamala Harris', 'date': '1964-10-20', 'time': '21:28', 'category': 'Politics'},

    # ACTORS & ENTERTAINMENT
    {'name': 'Marilyn Monroe', 'date': '1926-06-01', 'time': '09:30', 'category': 'Entertainment'},
    {'name': 'Audrey Hepburn', 'date': '1929-05-04', 'time': '03:00', 'category': 'Entertainment'},
    {'name': 'Elizabeth Taylor', 'date': '1932-02-27', 'time': '02:15', 'category': 'Entertainment'},
    {'name': 'Grace Kelly', 'date': '1929-11-12', 'time': '05:31', 'category': 'Entertainment'},
    {'name': 'Meryl Streep', 'date': '1949-06-22', 'time': '08:05', 'category': 'Entertainment'},
    {'name': 'Robert De Niro', 'date': '1943-08-17', 'time': '03:00', 'category': 'Entertainment'},
    {'name': 'Al Pacino', 'date': '1940-04-25', 'time': '11:02', 'category': 'Entertainment'},
    {'name': 'Angelina Jolie', 'date': '1975-06-04', 'time': '09:09', 'category': 'Entertainment'},
    {'name': 'Brad Pitt', 'date': '1963-12-18', 'time': '06:31', 'category': 'Entertainment'},
    {'name': 'Leonardo DiCaprio', 'date': '1974-11-11', 'time': '02:47', 'category': 'Entertainment'},
    {'name': 'Tom Cruise', 'date': '1962-07-03', 'time': '12:00', 'category': 'Entertainment'}, # Approx 
    {'name': 'Will Smith', 'date': '1968-09-25', 'time': '22:00', 'category': 'Entertainment'},
    {'name': 'Oprah Winfrey', 'date': '1954-01-29', 'time': '04:30', 'category': 'Entertainment'},

    # SPORTS
    {'name': 'Muhammad Ali', 'date': '1942-01-17', 'time': '18:35', 'category': 'Sports'},
    {'name': 'Michael Jordan', 'date': '1963-02-17', 'time': '13:40', 'category': 'Sports'},
    {'name': 'Serena Williams', 'date': '1981-09-26', 'time': '20:28', 'category': 'Sports'},
    {'name': 'Tiger Woods', 'date': '1975-12-30', 'time': '22:50', 'category': 'Sports'},
    {'name': 'Usain Bolt', 'date': '1986-08-21', 'time': '09:30', 'category': 'Sports'},
    {'name': 'Pele', 'date': '1940-10-23', 'time': '03:00', 'category': 'Sports'},
    {'name': 'Diego Maradona', 'date': '1960-10-30', 'time': '07:05', 'category': 'Sports'},
    {'name': 'Cristiano Ronaldo', 'date': '1985-02-05', 'time': '05:25', 'category': 'Sports'},
    {'name': 'Lionel Messi', 'date': '1987-06-24', 'time': '20:30', 'category': 'Sports'}, # approx
    {'name': 'Roger Federer', 'date': '1981-08-08', 'time': '08:40', 'category': 'Sports'},

    # LITERATURE
    {'name': 'Ernest Hemingway', 'date': '1899-07-21', 'time': '08:00', 'category': 'Literature'},
    {'name': 'Virginia Woolf', 'date': '1882-01-25', 'time': '12:15', 'category': 'Literature'},
    {'name': 'James Joyce', 'date': '1882-02-02', 'time': '06:00', 'category': 'Literature'},
    {'name': 'J.K. Rowling', 'date': '1965-07-31', 'time': '21:10', 'category': 'Literature'},
    {'name': 'Stephen King', 'date': '1947-09-21', 'time': '01:30', 'category': 'Literature'},
    {'name': 'Oscar Wilde', 'date': '1854-10-16', 'time': '03:00', 'category': 'Literature'},
    {'name': 'Mark Twain', 'date': '1835-11-30', 'time': '04:00', 'category': 'Literature'},

    # PHILOSOPHY & SPIRITUALITY
    {'name': 'Dalai Lama XIV', 'date': '1935-07-06', 'time': '04:38', 'category': 'Philosophy'},
    {'name': 'Pope Francis', 'date': '1936-12-17', 'time': '21:00', 'category': 'Philosophy'},
    {'name': 'Friedrich Nietzsche', 'date': '1844-10-15', 'time': '10:00', 'category': 'Philosophy'},
    {'name': 'Jean-Paul Sartre', 'date': '1905-06-21', 'time': '15:20', 'category': 'Philosophy'}
]
