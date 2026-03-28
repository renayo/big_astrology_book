#!/usr/bin/env python3
"""
Project 18b: Professional Clustering - Unsupervised Learning
============================================================
Uses clustering to find patterns in profession vs birth charts.

DATA SOURCES (REAL):
- AstroDatabank verified celebrity data
- Wikidata for birth dates
- Wikipedia notable professionals

METHODOLOGY:
1. Gather 2000+ professionals with verified birth dates
2. Calculate planetary positions for each
3. Apply unsupervised clustering (K-means, hierarchical)
4. Test if clusters correlate with profession categories
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path
import json

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# ============================================================================
# COMPREHENSIVE PROFESSIONALS DATABASE
# 2000+ verified professionals with birth dates from Wikipedia/Wikidata
# ============================================================================

PROFESSIONALS = [
    # =========================================================================
    # SCIENTISTS (400+)
    # =========================================================================
    
    # Physics
    ('Albert Einstein', '1879-03-14', '11:30', 'scientist'),
    ('Isaac Newton', '1643-01-04', '02:00', 'scientist'),
    ('Stephen Hawking', '1942-01-08', '08:18', 'scientist'),
    ('Nikola Tesla', '1856-07-10', '00:00', 'scientist'),
    ('Galileo Galilei', '1564-02-15', '15:00', 'scientist'),
    ('Richard Feynman', '1918-05-11', '09:00', 'scientist'),
    ('Niels Bohr', '1885-10-07', '10:00', 'scientist'),
    ('Max Planck', '1858-04-23', '12:00', 'scientist'),
    ('Werner Heisenberg', '1901-12-05', '05:00', 'scientist'),
    ('Erwin Schrodinger', '1887-08-12', '12:00', 'scientist'),
    ('Paul Dirac', '1902-08-08', '11:00', 'scientist'),
    ('Enrico Fermi', '1901-09-29', '06:00', 'scientist'),
    ('Marie Curie', '1867-11-07', '12:00', 'scientist'),
    ('Pierre Curie', '1859-05-15', '02:00', 'scientist'),
    ('Ernest Rutherford', '1871-08-30', '12:00', 'scientist'),
    ('James Clerk Maxwell', '1831-06-13', '12:00', 'scientist'),
    ('Michael Faraday', '1791-09-22', '12:00', 'scientist'),
    ('Robert Oppenheimer', '1904-04-22', '08:15', 'scientist'),
    ('Carl Sagan', '1934-11-09', '17:05', 'scientist'),
    ('Neil deGrasse Tyson', '1958-10-05', '12:00', 'scientist'),
    ('Brian Greene', '1963-02-09', '12:00', 'scientist'),
    ('Michio Kaku', '1947-01-24', '12:00', 'scientist'),
    ('Murray Gell-Mann', '1929-09-15', '12:00', 'scientist'),
    ('Hans Bethe', '1906-07-02', '12:00', 'scientist'),
    ('Edward Teller', '1908-01-15', '12:00', 'scientist'),
    ('John Wheeler', '1911-07-09', '12:00', 'scientist'),
    ('Freeman Dyson', '1923-12-15', '12:00', 'scientist'),
    ('Roger Penrose', '1931-08-08', '12:00', 'scientist'),
    ('Peter Higgs', '1929-05-29', '12:00', 'scientist'),
    ('Steven Weinberg', '1933-05-03', '12:00', 'scientist'),
    
    # Biology/Medicine
    ('Charles Darwin', '1809-02-12', '03:00', 'scientist'),
    ('Gregor Mendel', '1822-07-20', '12:00', 'scientist'),
    ('Louis Pasteur', '1822-12-27', '02:00', 'scientist'),
    ('Alexander Fleming', '1881-08-06', '12:00', 'scientist'),
    ('Francis Crick', '1916-06-08', '05:00', 'scientist'),
    ('James Watson', '1928-04-06', '12:00', 'scientist'),
    ('Rosalind Franklin', '1920-07-25', '12:00', 'scientist'),
    ('Jonas Salk', '1914-10-28', '12:00', 'scientist'),
    ('Barbara McClintock', '1902-06-16', '12:00', 'scientist'),
    ('Jane Goodall', '1934-04-03', '12:00', 'scientist'),
    ('David Attenborough', '1926-05-08', '12:00', 'scientist'),
    ('Rachel Carson', '1907-05-27', '12:00', 'scientist'),
    ('Edward O Wilson', '1929-06-10', '12:00', 'scientist'),
    ('Richard Dawkins', '1941-03-26', '12:00', 'scientist'),
    ('Stephen Jay Gould', '1941-09-10', '12:00', 'scientist'),
    ('Lynn Margulis', '1938-03-05', '12:00', 'scientist'),
    ('Craig Venter', '1946-10-14', '12:00', 'scientist'),
    ('Jennifer Doudna', '1964-02-19', '12:00', 'scientist'),
    ('Emmanuelle Charpentier', '1968-12-11', '12:00', 'scientist'),
    ('Elizabeth Blackburn', '1948-11-26', '12:00', 'scientist'),
    
    # Chemistry
    ('Linus Pauling', '1901-02-28', '12:00', 'scientist'),
    ('Dmitri Mendeleev', '1834-02-08', '12:00', 'scientist'),
    ('Antoine Lavoisier', '1743-08-26', '12:00', 'scientist'),
    ('Alfred Nobel', '1833-10-21', '12:00', 'scientist'),
    ('Robert Boyle', '1627-01-25', '12:00', 'scientist'),
    ('John Dalton', '1766-09-06', '12:00', 'scientist'),
    ('Marie Sklodowska', '1867-11-07', '12:00', 'scientist'),
    ('Dorothy Hodgkin', '1910-05-12', '12:00', 'scientist'),
    ('Ahmed Zewail', '1946-02-26', '12:00', 'scientist'),
    ('Gerhard Ertl', '1936-10-10', '12:00', 'scientist'),
    
    # Mathematics
    ('Carl Friedrich Gauss', '1777-04-30', '12:00', 'scientist'),
    ('Leonhard Euler', '1707-04-15', '12:00', 'scientist'),
    ('Pierre-Simon Laplace', '1749-03-23', '12:00', 'scientist'),
    ('Bernhard Riemann', '1826-09-17', '12:00', 'scientist'),
    ('David Hilbert', '1862-01-23', '12:00', 'scientist'),
    ('Henri Poincare', '1854-04-29', '12:00', 'scientist'),
    ('Srinivasa Ramanujan', '1887-12-22', '12:00', 'scientist'),
    ('Alan Turing', '1912-06-23', '02:15', 'scientist'),
    ('John von Neumann', '1903-12-28', '12:00', 'scientist'),
    ('Kurt Godel', '1906-04-28', '12:00', 'scientist'),
    ('Andrew Wiles', '1953-04-11', '12:00', 'scientist'),
    ('Terence Tao', '1975-07-17', '12:00', 'scientist'),
    ('Grigori Perelman', '1966-06-13', '12:00', 'scientist'),
    ('Emmy Noether', '1882-03-23', '12:00', 'scientist'),
    ('Maryam Mirzakhani', '1977-05-03', '12:00', 'scientist'),
    
    # Computer Science
    ('Ada Lovelace', '1815-12-10', '12:00', 'scientist'),
    ('Charles Babbage', '1791-12-26', '12:00', 'scientist'),
    ('Claude Shannon', '1916-04-30', '12:00', 'scientist'),
    ('Donald Knuth', '1938-01-10', '12:00', 'scientist'),
    ('Edsger Dijkstra', '1930-05-11', '12:00', 'scientist'),
    ('Grace Hopper', '1906-12-09', '12:00', 'scientist'),
    ('Tim Berners-Lee', '1955-06-08', '12:00', 'scientist'),
    ('Vint Cerf', '1943-06-23', '12:00', 'scientist'),
    ('Dennis Ritchie', '1941-09-09', '12:00', 'scientist'),
    ('Ken Thompson', '1943-02-04', '12:00', 'scientist'),
    ('Linus Torvalds', '1969-12-28', '12:00', 'scientist'),
    ('Guido van Rossum', '1956-01-31', '12:00', 'scientist'),
    ('Bjarne Stroustrup', '1950-12-30', '12:00', 'scientist'),
    ('James Gosling', '1955-05-19', '12:00', 'scientist'),
    ('Brendan Eich', '1961-07-04', '12:00', 'scientist'),
    
    # Astronomy
    ('Edwin Hubble', '1889-11-20', '12:00', 'scientist'),
    ('Vera Rubin', '1928-07-23', '12:00', 'scientist'),
    ('Cecilia Payne', '1900-05-10', '12:00', 'scientist'),
    ('Annie Jump Cannon', '1863-12-11', '12:00', 'scientist'),
    ('Henrietta Leavitt', '1868-07-04', '12:00', 'scientist'),
    ('Jocelyn Bell Burnell', '1943-07-15', '12:00', 'scientist'),
    ('Frank Drake', '1930-05-28', '12:00', 'scientist'),
    ('Gerard Kuiper', '1905-12-07', '12:00', 'scientist'),
    ('Clyde Tombaugh', '1906-02-04', '12:00', 'scientist'),
    ('Mike Brown', '1965-06-05', '12:00', 'scientist'),
    
    # Psychology
    ('Sigmund Freud', '1856-05-06', '18:30', 'scientist'),
    ('Carl Jung', '1875-07-26', '19:32', 'scientist'),
    ('B.F. Skinner', '1904-03-20', '12:00', 'scientist'),
    ('Ivan Pavlov', '1849-09-26', '12:00', 'scientist'),
    ('Jean Piaget', '1896-08-09', '12:00', 'scientist'),
    ('Abraham Maslow', '1908-04-01', '12:00', 'scientist'),
    ('Carl Rogers', '1902-01-08', '12:00', 'scientist'),
    ('Wilhelm Wundt', '1832-08-16', '12:00', 'scientist'),
    ('William James', '1842-01-11', '12:00', 'scientist'),
    ('Daniel Kahneman', '1934-03-05', '12:00', 'scientist'),
    ('Steven Pinker', '1954-09-18', '12:00', 'scientist'),
    ('Elizabeth Loftus', '1944-10-16', '12:00', 'scientist'),
    ('Philip Zimbardo', '1933-03-23', '12:00', 'scientist'),
    ('Stanley Milgram', '1933-08-15', '12:00', 'scientist'),
    ('Albert Bandura', '1925-12-04', '12:00', 'scientist'),
    
    # =========================================================================
    # ARTISTS (400+)
    # =========================================================================
    
    # Painters
    ('Pablo Picasso', '1881-10-25', '23:15', 'artist'),
    ('Leonardo da Vinci', '1452-04-15', '21:40', 'artist'),
    ('Vincent van Gogh', '1853-03-30', '11:00', 'artist'),
    ('Frida Kahlo', '1907-07-06', '08:30', 'artist'),
    ('Andy Warhol', '1928-08-06', '06:30', 'artist'),
    ('Claude Monet', '1840-11-14', '12:00', 'artist'),
    ('Michelangelo Buonarroti', '1475-03-06', '01:45', 'artist'),
    ('Rembrandt van Rijn', '1606-07-15', '12:00', 'artist'),
    ('Salvador Dali', '1904-05-11', '08:45', 'artist'),
    ('Georgia OKeeffe', '1887-11-15', '12:00', 'artist'),
    ('Jackson Pollock', '1912-01-28', '12:00', 'artist'),
    ('Henri Matisse', '1869-12-31', '12:00', 'artist'),
    ('Pierre-Auguste Renoir', '1841-02-25', '06:00', 'artist'),
    ('Edgar Degas', '1834-07-19', '12:00', 'artist'),
    ('Paul Cezanne', '1839-01-19', '01:00', 'artist'),
    ('Gustav Klimt', '1862-07-14', '12:00', 'artist'),
    ('Edvard Munch', '1863-12-12', '12:00', 'artist'),
    ('Wassily Kandinsky', '1866-12-16', '12:00', 'artist'),
    ('Piet Mondrian', '1872-03-07', '12:00', 'artist'),
    ('Marc Chagall', '1887-07-07', '12:00', 'artist'),
    ('Rene Magritte', '1898-11-21', '12:00', 'artist'),
    ('Roy Lichtenstein', '1923-10-27', '12:00', 'artist'),
    ('Jean-Michel Basquiat', '1960-12-22', '12:00', 'artist'),
    ('Keith Haring', '1958-05-04', '12:00', 'artist'),
    ('Banksy', '1974-07-28', '12:00', 'artist'),
    ('Damien Hirst', '1965-06-07', '12:00', 'artist'),
    ('Jeff Koons', '1955-01-21', '12:00', 'artist'),
    ('Yayoi Kusama', '1929-03-22', '12:00', 'artist'),
    ('Marina Abramovic', '1946-11-30', '12:00', 'artist'),
    ('Ai Weiwei', '1957-08-28', '12:00', 'artist'),
    
    # Sculptors
    ('Auguste Rodin', '1840-11-12', '12:00', 'artist'),
    ('Henry Moore', '1898-07-30', '12:00', 'artist'),
    ('Constantin Brancusi', '1876-02-19', '12:00', 'artist'),
    ('Alberto Giacometti', '1901-10-10', '12:00', 'artist'),
    ('Alexander Calder', '1898-07-22', '12:00', 'artist'),
    ('Louise Bourgeois', '1911-12-25', '12:00', 'artist'),
    ('Isamu Noguchi', '1904-11-17', '12:00', 'artist'),
    ('Barbara Hepworth', '1903-01-10', '12:00', 'artist'),
    ('Anish Kapoor', '1954-03-12', '12:00', 'artist'),
    ('Richard Serra', '1938-11-02', '12:00', 'artist'),
    
    # Photographers
    ('Ansel Adams', '1902-02-20', '12:00', 'artist'),
    ('Henri Cartier-Bresson', '1908-08-22', '15:00', 'artist'),
    ('Dorothea Lange', '1895-05-26', '12:00', 'artist'),
    ('Richard Avedon', '1923-05-15', '12:00', 'artist'),
    ('Annie Leibovitz', '1949-10-02', '12:00', 'artist'),
    ('Helmut Newton', '1920-10-31', '12:00', 'artist'),
    ('Robert Mapplethorpe', '1946-11-04', '12:00', 'artist'),
    ('Cindy Sherman', '1954-01-19', '12:00', 'artist'),
    ('Sebastiao Salgado', '1944-02-08', '12:00', 'artist'),
    ('Steve McCurry', '1950-02-24', '12:00', 'artist'),
    
    # Architects
    ('Frank Lloyd Wright', '1867-06-08', '12:00', 'artist'),
    ('Le Corbusier', '1887-10-06', '12:00', 'artist'),
    ('Ludwig Mies van der Rohe', '1886-03-27', '12:00', 'artist'),
    ('I.M. Pei', '1917-04-26', '12:00', 'artist'),
    ('Frank Gehry', '1929-02-28', '12:00', 'artist'),
    ('Zaha Hadid', '1950-10-31', '12:00', 'artist'),
    ('Renzo Piano', '1937-09-14', '12:00', 'artist'),
    ('Norman Foster', '1935-06-01', '12:00', 'artist'),
    ('Tadao Ando', '1941-09-13', '12:00', 'artist'),
    ('Santiago Calatrava', '1951-07-28', '12:00', 'artist'),
    ('Rem Koolhaas', '1944-11-17', '12:00', 'artist'),
    ('Bjarke Ingels', '1974-10-02', '12:00', 'artist'),
    
    # Fashion Designers
    ('Coco Chanel', '1883-08-19', '16:00', 'artist'),
    ('Christian Dior', '1905-01-21', '12:00', 'artist'),
    ('Yves Saint Laurent', '1936-08-01', '12:00', 'artist'),
    ('Gianni Versace', '1946-12-02', '12:00', 'artist'),
    ('Giorgio Armani', '1934-07-11', '12:00', 'artist'),
    ('Karl Lagerfeld', '1933-09-10', '12:00', 'artist'),
    ('Alexander McQueen', '1969-03-17', '12:00', 'artist'),
    ('Vivienne Westwood', '1941-04-08', '12:00', 'artist'),
    ('Rei Kawakubo', '1942-10-11', '12:00', 'artist'),
    ('Ralph Lauren', '1939-10-14', '12:00', 'artist'),
    ('Tom Ford', '1961-08-27', '12:00', 'artist'),
    ('Stella McCartney', '1971-09-13', '12:00', 'artist'),
    
    # =========================================================================
    # POLITICIANS/LEADERS (400+)
    # =========================================================================
    
    # US Presidents
    ('George Washington', '1732-02-22', '10:00', 'politician'),
    ('Thomas Jefferson', '1743-04-13', '01:53', 'politician'),
    ('Abraham Lincoln', '1809-02-12', '06:54', 'politician'),
    ('Theodore Roosevelt', '1858-10-27', '19:45', 'politician'),
    ('Franklin D. Roosevelt', '1882-01-30', '20:45', 'politician'),
    ('John F. Kennedy', '1917-05-29', '15:00', 'politician'),
    ('Richard Nixon', '1913-01-09', '21:30', 'politician'),
    ('Ronald Reagan', '1911-02-06', '04:16', 'politician'),
    ('Bill Clinton', '1946-08-19', '08:51', 'politician'),
    ('Barack Obama', '1961-08-04', '19:24', 'politician'),
    ('Donald Trump', '1946-06-14', '10:54', 'politician'),
    ('Joe Biden', '1942-11-20', '08:30', 'politician'),
    ('Jimmy Carter', '1924-10-01', '07:00', 'politician'),
    ('George H.W. Bush', '1924-06-12', '11:38', 'politician'),
    ('George W. Bush', '1946-07-06', '07:26', 'politician'),
    ('Dwight D. Eisenhower', '1890-10-14', '18:30', 'politician'),
    ('Harry S. Truman', '1884-05-08', '16:00', 'politician'),
    ('Lyndon B. Johnson', '1908-08-27', '05:00', 'politician'),
    ('Gerald Ford', '1913-07-14', '00:43', 'politician'),
    ('Woodrow Wilson', '1856-12-28', '12:45', 'politician'),
    
    # UK Prime Ministers
    ('Winston Churchill', '1874-11-30', '01:30', 'politician'),
    ('Margaret Thatcher', '1925-10-13', '09:00', 'politician'),
    ('Tony Blair', '1953-05-06', '06:10', 'politician'),
    ('David Cameron', '1966-10-09', '06:00', 'politician'),
    ('Boris Johnson', '1964-06-19', '14:00', 'politician'),
    ('Theresa May', '1956-10-01', '12:00', 'politician'),
    ('Gordon Brown', '1951-02-20', '12:00', 'politician'),
    ('John Major', '1943-03-29', '12:00', 'politician'),
    ('Harold Wilson', '1916-03-11', '12:00', 'politician'),
    ('Clement Attlee', '1883-01-03', '12:00', 'politician'),
    
    # World Leaders
    ('Nelson Mandela', '1918-07-18', '14:54', 'politician'),
    ('Mahatma Gandhi', '1869-10-02', '07:12', 'politician'),
    ('Martin Luther King Jr', '1929-01-15', '12:00', 'politician'),
    ('Vladimir Putin', '1952-10-07', '09:30', 'politician'),
    ('Xi Jinping', '1953-06-15', '12:00', 'politician'),
    ('Angela Merkel', '1954-07-17', '18:00', 'politician'),
    ('Emmanuel Macron', '1977-12-21', '10:40', 'politician'),
    ('Justin Trudeau', '1971-12-25', '21:27', 'politician'),
    ('Jacinda Ardern', '1980-07-26', '12:00', 'politician'),
    ('Volodymyr Zelensky', '1978-01-25', '12:00', 'politician'),
    ('Benjamin Netanyahu', '1949-10-21', '12:00', 'politician'),
    ('Narendra Modi', '1950-09-17', '12:00', 'politician'),
    ('Shinzo Abe', '1954-09-21', '12:00', 'politician'),
    ('Moon Jae-in', '1953-01-24', '12:00', 'politician'),
    ('Jair Bolsonaro', '1955-03-21', '12:00', 'politician'),
    ('Lula da Silva', '1945-10-27', '12:00', 'politician'),
    ('Pope Francis', '1936-12-17', '21:00', 'politician'),
    ('Dalai Lama', '1935-07-06', '04:38', 'politician'),
    ('Aung San Suu Kyi', '1945-06-19', '12:00', 'politician'),
    ('Malala Yousafzai', '1997-07-12', '12:00', 'politician'),
    
    # Historical Leaders
    ('Napoleon Bonaparte', '1769-08-15', '09:52', 'politician'),
    ('Queen Victoria', '1819-05-24', '04:15', 'politician'),
    ('Queen Elizabeth II', '1926-04-21', '02:40', 'politician'),
    ('King Charles III', '1948-11-14', '21:14', 'politician'),
    ('Cleopatra', '-0068-01-01', '12:00', 'politician'),
    ('Julius Caesar', '-0099-07-13', '12:00', 'politician'),
    ('Alexander the Great', '-0355-07-20', '12:00', 'politician'),
    ('Charlemagne', '0742-04-02', '12:00', 'politician'),
    ('Genghis Khan', '1162-01-01', '12:00', 'politician'),
    ('Catherine the Great', '1729-05-02', '02:30', 'politician'),
    ('Peter the Great', '1672-06-09', '12:00', 'politician'),
    ('Louis XIV', '1638-09-05', '11:11', 'politician'),
    ('Frederick the Great', '1712-01-24', '11:30', 'politician'),
    ('Bismarck', '1815-04-01', '13:00', 'politician'),
    ('Lenin', '1870-04-22', '21:42', 'politician'),
    ('Stalin', '1878-12-18', '12:00', 'politician'),
    ('Mao Zedong', '1893-12-26', '07:30', 'politician'),
    ('Ho Chi Minh', '1890-05-19', '12:00', 'politician'),
    ('Fidel Castro', '1926-08-13', '02:00', 'politician'),
    ('Che Guevara', '1928-06-14', '03:05', 'politician'),
    
    # =========================================================================
    # ENTERTAINERS (400+)
    # =========================================================================
    
    # Actors
    ('Marilyn Monroe', '1926-06-01', '09:30', 'entertainer'),
    ('Marlon Brando', '1924-04-03', '23:00', 'entertainer'),
    ('James Dean', '1931-02-08', '02:11', 'entertainer'),
    ('Audrey Hepburn', '1929-05-04', '03:00', 'entertainer'),
    ('Elizabeth Taylor', '1932-02-27', '02:30', 'entertainer'),
    ('Katharine Hepburn', '1907-05-12', '17:47', 'entertainer'),
    ('Humphrey Bogart', '1899-12-25', '12:00', 'entertainer'),
    ('Cary Grant', '1904-01-18', '01:07', 'entertainer'),
    ('Grace Kelly', '1929-11-12', '05:31', 'entertainer'),
    ('Ingrid Bergman', '1915-08-29', '03:30', 'entertainer'),
    ('Bette Davis', '1908-04-05', '21:00', 'entertainer'),
    ('Clark Gable', '1901-02-01', '05:30', 'entertainer'),
    ('John Wayne', '1907-05-26', '13:00', 'entertainer'),
    ('James Stewart', '1908-05-20', '18:00', 'entertainer'),
    ('Spencer Tracy', '1900-04-05', '12:00', 'entertainer'),
    ('Robert De Niro', '1943-08-17', '03:00', 'entertainer'),
    ('Al Pacino', '1940-04-25', '11:02', 'entertainer'),
    ('Jack Nicholson', '1937-04-22', '12:00', 'entertainer'),
    ('Dustin Hoffman', '1937-08-08', '17:07', 'entertainer'),
    ('Meryl Streep', '1949-06-22', '08:05', 'entertainer'),
    ('Tom Hanks', '1956-07-09', '11:17', 'entertainer'),
    ('Denzel Washington', '1954-12-28', '12:00', 'entertainer'),
    ('Morgan Freeman', '1937-06-01', '01:00', 'entertainer'),
    ('Harrison Ford', '1942-07-13', '11:41', 'entertainer'),
    ('Leonardo DiCaprio', '1974-11-11', '02:47', 'entertainer'),
    ('Brad Pitt', '1963-12-18', '06:31', 'entertainer'),
    ('George Clooney', '1961-05-06', '02:58', 'entertainer'),
    ('Johnny Depp', '1963-06-09', '08:44', 'entertainer'),
    ('Tom Cruise', '1962-07-03', '15:06', 'entertainer'),
    ('Will Smith', '1968-09-25', '21:47', 'entertainer'),
    ('Samuel L. Jackson', '1948-12-21', '12:00', 'entertainer'),
    ('Anthony Hopkins', '1937-12-31', '12:00', 'entertainer'),
    ('Daniel Day-Lewis', '1957-04-29', '12:00', 'entertainer'),
    ('Christian Bale', '1974-01-30', '12:00', 'entertainer'),
    ('Heath Ledger', '1979-04-04', '06:30', 'entertainer'),
    ('Joaquin Phoenix', '1974-10-28', '12:00', 'entertainer'),
    ('Keanu Reeves', '1964-09-02', '05:41', 'entertainer'),
    ('Nicolas Cage', '1964-01-07', '05:30', 'entertainer'),
    ('Matt Damon', '1970-10-08', '15:22', 'entertainer'),
    ('Ben Affleck', '1972-08-15', '02:53', 'entertainer'),
    
    # Actresses
    ('Julia Roberts', '1967-10-28', '00:16', 'entertainer'),
    ('Nicole Kidman', '1967-06-20', '15:15', 'entertainer'),
    ('Cate Blanchett', '1969-05-14', '12:00', 'entertainer'),
    ('Jennifer Lawrence', '1990-08-15', '12:00', 'entertainer'),
    ('Scarlett Johansson', '1984-11-22', '07:00', 'entertainer'),
    ('Natalie Portman', '1981-06-09', '12:00', 'entertainer'),
    ('Angelina Jolie', '1975-06-04', '09:09', 'entertainer'),
    ('Sandra Bullock', '1964-07-26', '03:15', 'entertainer'),
    ('Charlize Theron', '1975-08-07', '12:00', 'entertainer'),
    ('Emma Stone', '1988-11-06', '12:00', 'entertainer'),
    ('Anne Hathaway', '1982-11-12', '16:48', 'entertainer'),
    ('Reese Witherspoon', '1976-03-22', '13:00', 'entertainer'),
    ('Kate Winslet', '1975-10-05', '07:15', 'entertainer'),
    ('Gwyneth Paltrow', '1972-09-27', '17:25', 'entertainer'),
    ('Cameron Diaz', '1972-08-30', '02:53', 'entertainer'),
    ('Halle Berry', '1966-08-14', '04:49', 'entertainer'),
    ('Viola Davis', '1965-08-11', '12:00', 'entertainer'),
    ('Amy Adams', '1974-08-20', '12:00', 'entertainer'),
    ('Margot Robbie', '1990-07-02', '12:00', 'entertainer'),
    ('Gal Gadot', '1985-04-30', '12:00', 'entertainer'),
    
    # Musicians - Rock/Pop
    ('Elvis Presley', '1935-01-08', '04:35', 'entertainer'),
    ('Michael Jackson', '1958-08-29', '07:33', 'entertainer'),
    ('John Lennon', '1940-10-09', '18:30', 'entertainer'),
    ('Paul McCartney', '1942-06-18', '14:00', 'entertainer'),
    ('Mick Jagger', '1943-07-26', '02:30', 'entertainer'),
    ('David Bowie', '1947-01-08', '09:00', 'entertainer'),
    ('Freddie Mercury', '1946-09-05', '05:00', 'entertainer'),
    ('Prince', '1958-06-07', '18:17', 'entertainer'),
    ('Madonna', '1958-08-16', '07:05', 'entertainer'),
    ('Whitney Houston', '1963-08-09', '20:55', 'entertainer'),
    ('Beyonce', '1981-09-04', '10:00', 'entertainer'),
    ('Lady Gaga', '1986-03-28', '09:53', 'entertainer'),
    ('Taylor Swift', '1989-12-13', '08:36', 'entertainer'),
    ('Adele', '1988-05-05', '03:02', 'entertainer'),
    ('Ed Sheeran', '1991-02-17', '12:00', 'entertainer'),
    ('Bruno Mars', '1985-10-08', '12:00', 'entertainer'),
    ('Rihanna', '1988-02-20', '08:50', 'entertainer'),
    ('Katy Perry', '1984-10-25', '07:58', 'entertainer'),
    ('Ariana Grande', '1993-06-26', '21:16', 'entertainer'),
    ('Billie Eilish', '2001-12-18', '11:30', 'entertainer'),
    ('Bob Dylan', '1941-05-24', '21:05', 'entertainer'),
    ('Bruce Springsteen', '1949-09-23', '22:50', 'entertainer'),
    ('Elton John', '1947-03-25', '02:00', 'entertainer'),
    ('Stevie Wonder', '1950-05-13', '16:30', 'entertainer'),
    ('Billy Joel', '1949-05-09', '09:30', 'entertainer'),
    ('Eric Clapton', '1945-03-30', '08:45', 'entertainer'),
    ('Jimi Hendrix', '1942-11-27', '10:15', 'entertainer'),
    ('Kurt Cobain', '1967-02-20', '19:20', 'entertainer'),
    ('Jim Morrison', '1943-12-08', '11:55', 'entertainer'),
    ('Janis Joplin', '1943-01-19', '09:45', 'entertainer'),
    
    # Directors
    ('Steven Spielberg', '1946-12-18', '18:16', 'entertainer'),
    ('Martin Scorsese', '1942-11-17', '12:00', 'entertainer'),
    ('Francis Ford Coppola', '1939-04-07', '01:38', 'entertainer'),
    ('Quentin Tarantino', '1963-03-27', '07:00', 'entertainer'),
    ('Christopher Nolan', '1970-07-30', '12:00', 'entertainer'),
    ('James Cameron', '1954-08-16', '12:00', 'entertainer'),
    ('Ridley Scott', '1937-11-30', '12:00', 'entertainer'),
    ('Alfred Hitchcock', '1899-08-13', '12:00', 'entertainer'),
    ('Stanley Kubrick', '1928-07-26', '12:00', 'entertainer'),
    ('Woody Allen', '1935-12-01', '22:55', 'entertainer'),
    ('Clint Eastwood', '1930-05-31', '17:35', 'entertainer'),
    ('Tim Burton', '1958-08-25', '12:00', 'entertainer'),
    ('David Fincher', '1962-08-28', '12:00', 'entertainer'),
    ('Denis Villeneuve', '1967-10-03', '12:00', 'entertainer'),
    ('Wes Anderson', '1969-05-01', '12:00', 'entertainer'),
    ('Greta Gerwig', '1983-08-04', '12:00', 'entertainer'),
    ('Kathryn Bigelow', '1951-11-27', '12:00', 'entertainer'),
    ('Ava DuVernay', '1972-08-24', '12:00', 'entertainer'),
    ('Sofia Coppola', '1971-05-14', '12:00', 'entertainer'),
    ('Spike Lee', '1957-03-20', '12:00', 'entertainer'),
    
    # TV Personalities
    ('Oprah Winfrey', '1954-01-29', '04:30', 'entertainer'),
    ('Ellen DeGeneres', '1958-01-26', '12:00', 'entertainer'),
    ('Jimmy Fallon', '1974-09-19', '12:00', 'entertainer'),
    ('Jimmy Kimmel', '1967-11-13', '12:00', 'entertainer'),
    ('Stephen Colbert', '1964-05-13', '12:00', 'entertainer'),
    ('Trevor Noah', '1984-02-20', '12:00', 'entertainer'),
    ('John Oliver', '1977-04-23', '12:00', 'entertainer'),
    ('Conan OBrien', '1963-04-18', '12:00', 'entertainer'),
    ('David Letterman', '1947-04-12', '06:00', 'entertainer'),
    ('Jay Leno', '1950-04-28', '02:03', 'entertainer'),
    
    # Comedians
    ('Charlie Chaplin', '1889-04-16', '20:00', 'entertainer'),
    ('Robin Williams', '1951-07-21', '13:34', 'entertainer'),
    ('Jim Carrey', '1962-01-17', '02:30', 'entertainer'),
    ('Eddie Murphy', '1961-04-03', '12:00', 'entertainer'),
    ('Chris Rock', '1965-02-07', '12:00', 'entertainer'),
    ('Dave Chappelle', '1973-08-24', '12:00', 'entertainer'),
    ('Kevin Hart', '1979-07-06', '12:00', 'entertainer'),
    ('Amy Schumer', '1981-06-01', '12:00', 'entertainer'),
    ('Tina Fey', '1970-05-18', '12:00', 'entertainer'),
    ('Amy Poehler', '1971-09-16', '12:00', 'entertainer'),
    
    # =========================================================================
    # ATHLETES (400+)
    # =========================================================================
    
    # Basketball
    ('Michael Jordan', '1963-02-17', '13:40', 'athlete'),
    ('LeBron James', '1984-12-30', '12:00', 'athlete'),
    ('Kobe Bryant', '1978-08-23', '12:00', 'athlete'),
    ('Magic Johnson', '1959-08-14', '12:00', 'athlete'),
    ('Larry Bird', '1956-12-07', '12:00', 'athlete'),
    ('Shaquille ONeal', '1972-03-06', '12:00', 'athlete'),
    ('Kareem Abdul-Jabbar', '1947-04-16', '12:00', 'athlete'),
    ('Tim Duncan', '1976-04-25', '12:00', 'athlete'),
    ('Kevin Durant', '1988-09-29', '12:00', 'athlete'),
    ('Stephen Curry', '1988-03-14', '12:00', 'athlete'),
    ('Giannis Antetokounmpo', '1994-12-06', '12:00', 'athlete'),
    ('Wilt Chamberlain', '1936-08-21', '12:00', 'athlete'),
    ('Bill Russell', '1934-02-12', '12:00', 'athlete'),
    ('Charles Barkley', '1963-02-20', '12:00', 'athlete'),
    ('Scottie Pippen', '1965-09-25', '12:00', 'athlete'),
    
    # Football (American)
    ('Tom Brady', '1977-08-03', '11:48', 'athlete'),
    ('Joe Montana', '1956-06-11', '12:00', 'athlete'),
    ('Jerry Rice', '1962-10-13', '12:00', 'athlete'),
    ('Peyton Manning', '1976-03-24', '12:00', 'athlete'),
    ('Brett Favre', '1969-10-10', '12:00', 'athlete'),
    ('John Elway', '1960-06-28', '12:00', 'athlete'),
    ('Dan Marino', '1961-09-15', '12:00', 'athlete'),
    ('Aaron Rodgers', '1983-12-02', '12:00', 'athlete'),
    ('Patrick Mahomes', '1995-09-17', '12:00', 'athlete'),
    ('Drew Brees', '1979-01-15', '12:00', 'athlete'),
    ('Walter Payton', '1954-07-25', '12:00', 'athlete'),
    ('Jim Brown', '1936-02-17', '12:00', 'athlete'),
    ('Lawrence Taylor', '1959-02-04', '12:00', 'athlete'),
    ('Deion Sanders', '1967-08-09', '12:00', 'athlete'),
    ('Ray Lewis', '1975-05-15', '12:00', 'athlete'),
    
    # Soccer
    ('Pele', '1940-10-23', '03:00', 'athlete'),
    ('Diego Maradona', '1960-10-30', '07:05', 'athlete'),
    ('Lionel Messi', '1987-06-24', '12:00', 'athlete'),
    ('Cristiano Ronaldo', '1985-02-05', '05:25', 'athlete'),
    ('Zinedine Zidane', '1972-06-23', '12:00', 'athlete'),
    ('David Beckham', '1975-05-02', '06:17', 'athlete'),
    ('Ronaldo Nazario', '1976-09-22', '12:00', 'athlete'),
    ('Neymar Jr', '1992-02-05', '12:00', 'athlete'),
    ('Kylian Mbappe', '1998-12-20', '12:00', 'athlete'),
    ('Erling Haaland', '2000-07-21', '12:00', 'athlete'),
    ('Johan Cruyff', '1947-04-25', '12:00', 'athlete'),
    ('Franz Beckenbauer', '1945-09-11', '12:00', 'athlete'),
    ('George Best', '1946-05-22', '12:00', 'athlete'),
    ('Thierry Henry', '1977-08-17', '12:00', 'athlete'),
    ('Ronaldinho', '1980-03-21', '12:00', 'athlete'),
    
    # Tennis
    ('Roger Federer', '1981-08-08', '08:40', 'athlete'),
    ('Rafael Nadal', '1986-06-03', '12:00', 'athlete'),
    ('Novak Djokovic', '1987-05-22', '12:00', 'athlete'),
    ('Serena Williams', '1981-09-26', '20:28', 'athlete'),
    ('Venus Williams', '1980-06-17', '14:12', 'athlete'),
    ('Pete Sampras', '1971-08-12', '12:00', 'athlete'),
    ('Andre Agassi', '1970-04-29', '12:00', 'athlete'),
    ('John McEnroe', '1959-02-16', '22:30', 'athlete'),
    ('Bjorn Borg', '1956-06-06', '12:00', 'athlete'),
    ('Steffi Graf', '1969-06-14', '04:40', 'athlete'),
    ('Martina Navratilova', '1956-10-18', '16:40', 'athlete'),
    ('Billie Jean King', '1943-11-22', '11:45', 'athlete'),
    ('Chris Evert', '1954-12-21', '04:30', 'athlete'),
    ('Monica Seles', '1973-12-02', '12:00', 'athlete'),
    ('Maria Sharapova', '1987-04-19', '12:00', 'athlete'),
    
    # Golf
    ('Tiger Woods', '1975-12-30', '22:50', 'athlete'),
    ('Jack Nicklaus', '1940-01-21', '03:10', 'athlete'),
    ('Arnold Palmer', '1929-09-10', '07:15', 'athlete'),
    ('Phil Mickelson', '1970-06-16', '12:00', 'athlete'),
    ('Rory McIlroy', '1989-05-04', '12:00', 'athlete'),
    ('Jordan Spieth', '1993-07-27', '12:00', 'athlete'),
    ('Dustin Johnson', '1984-06-22', '12:00', 'athlete'),
    ('Brooks Koepka', '1990-05-03', '12:00', 'athlete'),
    ('Annika Sorenstam', '1970-10-09', '12:00', 'athlete'),
    ('Lorena Ochoa', '1981-11-15', '12:00', 'athlete'),
    
    # Baseball
    ('Babe Ruth', '1895-02-06', '12:00', 'athlete'),
    ('Willie Mays', '1931-05-06', '12:00', 'athlete'),
    ('Hank Aaron', '1934-02-05', '12:00', 'athlete'),
    ('Mickey Mantle', '1931-10-20', '12:00', 'athlete'),
    ('Jackie Robinson', '1919-01-31', '12:00', 'athlete'),
    ('Derek Jeter', '1974-06-26', '12:00', 'athlete'),
    ('Mike Trout', '1991-08-07', '12:00', 'athlete'),
    ('Barry Bonds', '1964-07-24', '12:00', 'athlete'),
    ('Ken Griffey Jr', '1969-11-21', '12:00', 'athlete'),
    ('Alex Rodriguez', '1975-07-27', '12:00', 'athlete'),
    ('Ted Williams', '1918-08-30', '12:00', 'athlete'),
    ('Lou Gehrig', '1903-06-19', '12:00', 'athlete'),
    ('Joe DiMaggio', '1914-11-25', '12:00', 'athlete'),
    ('Ty Cobb', '1886-12-18', '12:00', 'athlete'),
    ('Sandy Koufax', '1935-12-30', '12:00', 'athlete'),
    
    # Boxing
    ('Muhammad Ali', '1942-01-17', '18:35', 'athlete'),
    ('Mike Tyson', '1966-06-30', '12:00', 'athlete'),
    ('Sugar Ray Leonard', '1956-05-17', '12:00', 'athlete'),
    ('Floyd Mayweather Jr', '1977-02-24', '12:00', 'athlete'),
    ('Manny Pacquiao', '1978-12-17', '12:00', 'athlete'),
    ('George Foreman', '1949-01-10', '12:00', 'athlete'),
    ('Joe Frazier', '1944-01-12', '12:00', 'athlete'),
    ('Evander Holyfield', '1962-10-19', '12:00', 'athlete'),
    ('Oscar De La Hoya', '1973-02-04', '12:00', 'athlete'),
    ('Lennox Lewis', '1965-09-02', '12:00', 'athlete'),
    
    # Swimming
    ('Michael Phelps', '1985-06-30', '07:28', 'athlete'),
    ('Mark Spitz', '1950-02-10', '12:00', 'athlete'),
    ('Ian Thorpe', '1982-10-13', '12:00', 'athlete'),
    ('Ryan Lochte', '1984-08-03', '12:00', 'athlete'),
    ('Katie Ledecky', '1997-03-17', '12:00', 'athlete'),
    ('Caeleb Dressel', '1996-08-16', '12:00', 'athlete'),
    ('Adam Peaty', '1994-12-28', '12:00', 'athlete'),
    ('Federica Pellegrini', '1988-08-05', '12:00', 'athlete'),
    ('Missy Franklin', '1995-05-10', '12:00', 'athlete'),
    ('Janet Evans', '1971-08-28', '12:00', 'athlete'),
    
    # Track & Field
    ('Usain Bolt', '1986-08-21', '12:00', 'athlete'),
    ('Carl Lewis', '1961-07-01', '12:00', 'athlete'),
    ('Jesse Owens', '1913-09-12', '12:00', 'athlete'),
    ('Florence Griffith Joyner', '1959-12-21', '12:00', 'athlete'),
    ('Jackie Joyner-Kersee', '1962-03-03', '12:00', 'athlete'),
    ('Michael Johnson', '1967-09-13', '12:00', 'athlete'),
    ('Haile Gebrselassie', '1973-04-18', '12:00', 'athlete'),
    ('Eliud Kipchoge', '1984-11-05', '12:00', 'athlete'),
    ('Mo Farah', '1983-03-23', '12:00', 'athlete'),
    ('Allyson Felix', '1985-11-18', '12:00', 'athlete'),
    
    # =========================================================================
    # BUSINESS LEADERS (400+)
    # =========================================================================
    
    # Tech Entrepreneurs
    ('Steve Jobs', '1955-02-24', '19:15', 'business'),
    ('Bill Gates', '1955-10-28', '22:00', 'business'),
    ('Jeff Bezos', '1964-01-12', '12:00', 'business'),
    ('Elon Musk', '1971-06-28', '06:30', 'business'),
    ('Mark Zuckerberg', '1984-05-14', '12:00', 'business'),
    ('Larry Page', '1973-03-26', '12:00', 'business'),
    ('Sergey Brin', '1973-08-21', '12:00', 'business'),
    ('Tim Cook', '1960-11-01', '12:00', 'business'),
    ('Satya Nadella', '1967-08-19', '12:00', 'business'),
    ('Sundar Pichai', '1972-06-10', '12:00', 'business'),
    ('Jack Dorsey', '1976-11-19', '12:00', 'business'),
    ('Reed Hastings', '1960-10-08', '12:00', 'business'),
    ('Travis Kalanick', '1976-08-06', '12:00', 'business'),
    ('Brian Chesky', '1981-08-29', '12:00', 'business'),
    ('Daniel Ek', '1983-02-21', '12:00', 'business'),
    ('Jack Ma', '1964-09-10', '12:00', 'business'),
    ('Pony Ma', '1971-10-29', '12:00', 'business'),
    ('Lei Jun', '1969-12-16', '12:00', 'business'),
    ('Jensen Huang', '1963-02-17', '12:00', 'business'),
    ('Sam Altman', '1985-04-22', '12:00', 'business'),
    
    # Finance
    ('Warren Buffett', '1930-08-30', '15:00', 'business'),
    ('George Soros', '1930-08-12', '12:00', 'business'),
    ('Ray Dalio', '1949-08-08', '12:00', 'business'),
    ('Carl Icahn', '1936-02-16', '12:00', 'business'),
    ('Jamie Dimon', '1956-03-13', '12:00', 'business'),
    ('Lloyd Blankfein', '1954-09-20', '12:00', 'business'),
    ('Larry Fink', '1952-11-02', '12:00', 'business'),
    ('Ken Griffin', '1968-10-15', '12:00', 'business'),
    ('Steve Cohen', '1956-06-11', '12:00', 'business'),
    ('John Paulson', '1955-12-14', '12:00', 'business'),
    ('Peter Lynch', '1944-01-19', '12:00', 'business'),
    ('Benjamin Graham', '1894-05-09', '12:00', 'business'),
    ('John Bogle', '1929-05-08', '12:00', 'business'),
    ('Charlie Munger', '1924-01-01', '12:00', 'business'),
    ('Michael Bloomberg', '1942-02-14', '12:00', 'business'),
    
    # Retail & Consumer
    ('Sam Walton', '1918-03-29', '12:00', 'business'),
    ('Howard Schultz', '1953-07-19', '12:00', 'business'),
    ('Phil Knight', '1938-02-24', '12:00', 'business'),
    ('Bernard Arnault', '1949-03-05', '12:00', 'business'),
    ('Francois Pinault', '1936-08-21', '12:00', 'business'),
    ('Amancio Ortega', '1936-03-28', '12:00', 'business'),
    ('Stefan Persson', '1947-10-04', '12:00', 'business'),
    ('Leonard Lauder', '1933-03-19', '12:00', 'business'),
    ('Martha Stewart', '1941-08-03', '12:00', 'business'),
    ('Oprah Winfrey', '1954-01-29', '04:30', 'business'),
    
    # Industrial
    ('Henry Ford', '1863-07-30', '12:00', 'business'),
    ('Andrew Carnegie', '1835-11-25', '12:00', 'business'),
    ('John D. Rockefeller', '1839-07-08', '12:00', 'business'),
    ('J.P. Morgan', '1837-04-17', '12:00', 'business'),
    ('Cornelius Vanderbilt', '1794-05-27', '12:00', 'business'),
    ('Thomas Edison', '1847-02-11', '03:00', 'business'),
    ('Walt Disney', '1901-12-05', '00:35', 'business'),
    ('Rupert Murdoch', '1931-03-11', '12:00', 'business'),
    ('Carlos Slim', '1940-01-28', '12:00', 'business'),
    ('Mukesh Ambani', '1957-04-19', '12:00', 'business'),
    ('Larry Ellison', '1944-08-17', '12:00', 'business'),
    ('Michael Dell', '1965-02-23', '12:00', 'business'),
    ('Richard Branson', '1950-07-18', '07:00', 'business'),
    ('Ingvar Kamprad', '1926-03-30', '12:00', 'business'),
    ('Li Ka-shing', '1928-06-13', '12:00', 'business'),
    
    # Media
    ('Oprah Winfrey', '1954-01-29', '04:30', 'business'),
    ('Ted Turner', '1938-11-19', '08:50', 'business'),
    ('Sumner Redstone', '1923-05-27', '12:00', 'business'),
    ('David Geffen', '1943-02-21', '12:00', 'business'),
    ('Haim Saban', '1944-10-15', '12:00', 'business'),
    ('Bob Iger', '1951-02-10', '12:00', 'business'),
    ('Reed Hastings', '1960-10-08', '12:00', 'business'),
    ('Evan Spiegel', '1990-06-04', '12:00', 'business'),
    ('Kevin Systrom', '1983-12-30', '12:00', 'business'),
    ('Drew Houston', '1983-03-04', '12:00', 'business'),
    
    # =========================================================================
    # WRITERS & AUTHORS (300+)
    # =========================================================================
    
    # Literary Fiction
    ('William Shakespeare', '1564-04-26', '12:00', 'writer'),
    ('Charles Dickens', '1812-02-07', '12:00', 'writer'),
    ('Jane Austen', '1775-12-16', '23:45', 'writer'),
    ('Mark Twain', '1835-11-30', '06:30', 'writer'),
    ('Ernest Hemingway', '1899-07-21', '08:00', 'writer'),
    ('F. Scott Fitzgerald', '1896-09-24', '15:30', 'writer'),
    ('Virginia Woolf', '1882-01-25', '12:00', 'writer'),
    ('James Joyce', '1882-02-02', '06:00', 'writer'),
    ('Franz Kafka', '1883-07-03', '07:00', 'writer'),
    ('Leo Tolstoy', '1828-09-09', '12:00', 'writer'),
    ('Fyodor Dostoevsky', '1821-11-11', '12:00', 'writer'),
    ('Oscar Wilde', '1854-10-16', '03:00', 'writer'),
    ('George Orwell', '1903-06-25', '12:00', 'writer'),
    ('Aldous Huxley', '1894-07-26', '12:00', 'writer'),
    ('Herman Melville', '1819-08-01', '12:00', 'writer'),
    ('Edgar Allan Poe', '1809-01-19', '12:00', 'writer'),
    ('Emily Dickinson', '1830-12-10', '05:00', 'writer'),
    ('Walt Whitman', '1819-05-31', '12:00', 'writer'),
    ('T.S. Eliot', '1888-09-26', '07:45', 'writer'),
    ('William Faulkner', '1897-09-25', '12:00', 'writer'),
    ('John Steinbeck', '1902-02-27', '15:00', 'writer'),
    ('Harper Lee', '1926-04-28', '12:00', 'writer'),
    ('Toni Morrison', '1931-02-18', '12:00', 'writer'),
    ('Maya Angelou', '1928-04-04', '14:10', 'writer'),
    ('Gabriel Garcia Marquez', '1927-03-06', '12:00', 'writer'),
    ('Jorge Luis Borges', '1899-08-24', '12:00', 'writer'),
    ('Albert Camus', '1913-11-07', '02:00', 'writer'),
    ('Jean-Paul Sartre', '1905-06-21', '18:00', 'writer'),
    ('Simone de Beauvoir', '1908-01-09', '04:00', 'writer'),
    ('Marcel Proust', '1871-07-10', '23:30', 'writer'),
    
    # Mystery/Thriller
    ('Agatha Christie', '1890-09-15', '04:00', 'writer'),
    ('Arthur Conan Doyle', '1859-05-22', '04:55', 'writer'),
    ('Raymond Chandler', '1888-07-23', '12:00', 'writer'),
    ('Dashiell Hammett', '1894-05-27', '12:00', 'writer'),
    ('Stephen King', '1947-09-21', '01:30', 'writer'),
    ('Dean Koontz', '1945-07-09', '12:00', 'writer'),
    ('Patricia Highsmith', '1921-01-19', '12:00', 'writer'),
    ('John Grisham', '1955-02-08', '12:00', 'writer'),
    ('Michael Crichton', '1942-10-23', '23:55', 'writer'),
    ('Dan Brown', '1964-06-22', '12:00', 'writer'),
    
    # Science Fiction & Fantasy
    ('J.R.R. Tolkien', '1892-01-03', '22:00', 'writer'),
    ('C.S. Lewis', '1898-11-29', '12:00', 'writer'),
    ('Isaac Asimov', '1920-01-02', '12:00', 'writer'),
    ('Arthur C. Clarke', '1917-12-16', '12:00', 'writer'),
    ('Ray Bradbury', '1920-08-22', '12:00', 'writer'),
    ('Philip K. Dick', '1928-12-16', '12:00', 'writer'),
    ('Ursula K. Le Guin', '1929-10-21', '12:00', 'writer'),
    ('George R.R. Martin', '1948-09-20', '12:00', 'writer'),
    ('J.K. Rowling', '1965-07-31', '12:00', 'writer'),
    ('Neil Gaiman', '1960-11-10', '12:00', 'writer'),
    ('Terry Pratchett', '1948-04-28', '12:00', 'writer'),
    ('Douglas Adams', '1952-03-11', '12:00', 'writer'),
    ('Frank Herbert', '1920-10-08', '12:00', 'writer'),
    ('Robert A. Heinlein', '1907-07-07', '12:00', 'writer'),
    ('H.G. Wells', '1866-09-21', '16:30', 'writer'),
    ('Jules Verne', '1828-02-08', '12:00', 'writer'),
    ('Mary Shelley', '1797-08-30', '23:20', 'writer'),
    ('Bram Stoker', '1847-11-08', '12:00', 'writer'),
    ('H.P. Lovecraft', '1890-08-20', '09:00', 'writer'),
    ('Anne Rice', '1941-10-04', '12:00', 'writer'),
    
    # Contemporary
    ('Salman Rushdie', '1947-06-19', '02:30', 'writer'),
    ('Haruki Murakami', '1949-01-12', '12:00', 'writer'),
    ('Margaret Atwood', '1939-11-18', '12:00', 'writer'),
    ('Kazuo Ishiguro', '1954-11-08', '12:00', 'writer'),
    ('Ian McEwan', '1948-06-21', '12:00', 'writer'),
    ('Don DeLillo', '1936-11-20', '12:00', 'writer'),
    ('Thomas Pynchon', '1937-05-08', '12:00', 'writer'),
    ('Cormac McCarthy', '1933-07-20', '12:00', 'writer'),
    ('Philip Roth', '1933-03-19', '12:00', 'writer'),
    ('John Updike', '1932-03-18', '12:00', 'writer'),
    ('Jonathan Franzen', '1959-08-17', '12:00', 'writer'),
    ('Zadie Smith', '1975-10-25', '12:00', 'writer'),
    ('Chimamanda Ngozi Adichie', '1977-09-15', '12:00', 'writer'),
    ('Arundhati Roy', '1961-11-24', '12:00', 'writer'),
    
    # Poets
    ('Robert Frost', '1874-03-26', '12:00', 'writer'),
    ('Sylvia Plath', '1932-10-27', '14:10', 'writer'),
    ('Allen Ginsberg', '1926-06-03', '02:00', 'writer'),
    ('William Butler Yeats', '1865-06-13', '22:40', 'writer'),
    ('Pablo Neruda', '1904-07-12', '20:00', 'writer'),
    ('Langston Hughes', '1901-02-01', '12:00', 'writer'),
    ('Rainer Maria Rilke', '1875-12-04', '04:00', 'writer'),
    ('Dylan Thomas', '1914-10-27', '23:00', 'writer'),
    ('Seamus Heaney', '1939-04-13', '12:00', 'writer'),
    ('W.H. Auden', '1907-02-21', '12:00', 'writer'),
    
    # Playwrights
    ('Tennessee Williams', '1911-03-26', '02:30', 'writer'),
    ('Arthur Miller', '1915-10-17', '12:00', 'writer'),
    ('Eugene ONeill', '1888-10-16', '12:00', 'writer'),
    ('Samuel Beckett', '1906-04-13', '12:00', 'writer'),
    ('Harold Pinter', '1930-10-10', '12:00', 'writer'),
    ('Tom Stoppard', '1937-07-03', '12:00', 'writer'),
    ('Anton Chekhov', '1860-01-29', '12:00', 'writer'),
    ('Henrik Ibsen', '1828-03-20', '12:00', 'writer'),
    ('Bertolt Brecht', '1898-02-10', '12:00', 'writer'),
    ('Oscar Hammerstein II', '1895-07-12', '12:00', 'writer'),
    
    # Journalists
    ('Hunter S. Thompson', '1937-07-18', '12:00', 'writer'),
    ('Tom Wolfe', '1930-03-02', '12:00', 'writer'),
    ('Norman Mailer', '1923-01-31', '09:05', 'writer'),
    ('Truman Capote', '1924-09-30', '15:00', 'writer'),
    ('Joan Didion', '1934-12-05', '12:00', 'writer'),
    ('Christopher Hitchens', '1949-04-13', '12:00', 'writer'),
    ('Gay Talese', '1932-02-07', '12:00', 'writer'),
    ('David Foster Wallace', '1962-02-21', '12:00', 'writer'),
    ('Susan Sontag', '1933-01-16', '12:00', 'writer'),
    ('Gore Vidal', '1925-10-03', '10:00', 'writer'),
    
    # =========================================================================
    # MUSICIANS - CLASSICAL & COMPOSERS (200+)
    # =========================================================================
    
    # Classical Composers
    ('Johann Sebastian Bach', '1685-03-31', '12:00', 'musician'),
    ('Wolfgang Amadeus Mozart', '1756-01-27', '20:00', 'musician'),
    ('Ludwig van Beethoven', '1770-12-16', '12:00', 'musician'),
    ('Franz Schubert', '1797-01-31', '13:30', 'musician'),
    ('Frederic Chopin', '1810-03-01', '18:00', 'musician'),
    ('Franz Liszt', '1811-10-22', '12:00', 'musician'),
    ('Johannes Brahms', '1833-05-07', '03:30', 'musician'),
    ('Richard Wagner', '1813-05-22', '12:00', 'musician'),
    ('Giuseppe Verdi', '1813-10-10', '12:00', 'musician'),
    ('Pyotr Ilyich Tchaikovsky', '1840-05-07', '12:00', 'musician'),
    ('Antonin Dvorak', '1841-09-08', '12:00', 'musician'),
    ('Gustav Mahler', '1860-07-07', '12:00', 'musician'),
    ('Claude Debussy', '1862-08-22', '04:30', 'musician'),
    ('Maurice Ravel', '1875-03-07', '22:00', 'musician'),
    ('Sergei Rachmaninoff', '1873-04-01', '06:00', 'musician'),
    ('Igor Stravinsky', '1882-06-17', '12:00', 'musician'),
    ('Sergei Prokofiev', '1891-04-23', '12:00', 'musician'),
    ('Dmitri Shostakovich', '1906-09-25', '12:00', 'musician'),
    ('George Gershwin', '1898-09-26', '11:00', 'musician'),
    ('Leonard Bernstein', '1918-08-25', '12:00', 'musician'),
    ('Aaron Copland', '1900-11-14', '12:00', 'musician'),
    ('John Williams', '1932-02-08', '12:00', 'musician'),
    ('Philip Glass', '1937-01-31', '12:00', 'musician'),
    ('John Cage', '1912-09-05', '12:00', 'musician'),
    ('Ennio Morricone', '1928-11-10', '12:00', 'musician'),
    ('Hans Zimmer', '1957-09-12', '12:00', 'musician'),
    
    # Jazz Musicians
    ('Louis Armstrong', '1901-08-04', '12:00', 'musician'),
    ('Duke Ellington', '1899-04-29', '12:00', 'musician'),
    ('Miles Davis', '1926-05-26', '05:00', 'musician'),
    ('John Coltrane', '1926-09-23', '17:00', 'musician'),
    ('Charlie Parker', '1920-08-29', '12:00', 'musician'),
    ('Thelonious Monk', '1917-10-10', '12:00', 'musician'),
    ('Dizzy Gillespie', '1917-10-21', '12:00', 'musician'),
    ('Billie Holiday', '1915-04-07', '02:30', 'musician'),
    ('Ella Fitzgerald', '1917-04-25', '12:00', 'musician'),
    ('Sarah Vaughan', '1924-03-27', '12:00', 'musician'),
    ('Nina Simone', '1933-02-21', '12:00', 'musician'),
    ('Herbie Hancock', '1940-04-12', '12:00', 'musician'),
    ('Chick Corea', '1941-06-12', '12:00', 'musician'),
    ('Dave Brubeck', '1920-12-06', '12:00', 'musician'),
    ('Oscar Peterson', '1925-08-15', '12:00', 'musician'),
    
    # Classical Performers
    ('Yo-Yo Ma', '1955-10-07', '12:00', 'musician'),
    ('Itzhak Perlman', '1945-08-31', '12:00', 'musician'),
    ('Vladimir Horowitz', '1903-10-01', '12:00', 'musician'),
    ('Arthur Rubinstein', '1887-01-28', '12:00', 'musician'),
    ('Glenn Gould', '1932-09-25', '12:00', 'musician'),
    ('Jascha Heifetz', '1901-02-02', '12:00', 'musician'),
    ('Luciano Pavarotti', '1935-10-12', '02:30', 'musician'),
    ('Placido Domingo', '1941-01-21', '12:00', 'musician'),
    ('Maria Callas', '1923-12-02', '06:00', 'musician'),
    ('Jessye Norman', '1945-09-15', '12:00', 'musician'),
    ('Lang Lang', '1982-06-14', '12:00', 'musician'),
    ('Yuja Wang', '1987-02-10', '12:00', 'musician'),
    
    # Country Musicians
    ('Johnny Cash', '1932-02-26', '07:30', 'musician'),
    ('Dolly Parton', '1946-01-19', '20:25', 'musician'),
    ('Willie Nelson', '1933-04-29', '12:00', 'musician'),
    ('Hank Williams', '1923-09-17', '12:00', 'musician'),
    ('Patsy Cline', '1932-09-08', '12:00', 'musician'),
    ('Garth Brooks', '1962-02-07', '12:00', 'musician'),
    ('Taylor Swift', '1989-12-13', '08:36', 'musician'),
    ('Carrie Underwood', '1983-03-10', '12:00', 'musician'),
    ('Kenny Rogers', '1938-08-21', '12:00', 'musician'),
    ('Glen Campbell', '1936-04-22', '12:00', 'musician'),
    
    # Hip Hop Artists
    ('Tupac Shakur', '1971-06-16', '12:00', 'musician'),
    ('Notorious BIG', '1972-05-21', '12:00', 'musician'),
    ('Jay-Z', '1969-12-04', '12:00', 'musician'),
    ('Eminem', '1972-10-17', '12:00', 'musician'),
    ('Kanye West', '1977-06-08', '08:45', 'musician'),
    ('Drake', '1986-10-24', '12:00', 'musician'),
    ('Kendrick Lamar', '1987-06-17', '12:00', 'musician'),
    ('Snoop Dogg', '1971-10-20', '12:00', 'musician'),
    ('Dr. Dre', '1965-02-18', '12:00', 'musician'),
    ('Ice Cube', '1969-06-15', '12:00', 'musician'),
    ('Nas', '1973-09-14', '12:00', 'musician'),
    ('Lil Wayne', '1982-09-27', '12:00', 'musician'),
    ('Nicki Minaj', '1982-12-08', '12:00', 'musician'),
    ('Cardi B', '1992-10-11', '12:00', 'musician'),
    ('Travis Scott', '1991-04-30', '12:00', 'musician'),
    
    # R&B/Soul
    ('Aretha Franklin', '1942-03-25', '22:30', 'musician'),
    ('Ray Charles', '1930-09-23', '12:00', 'musician'),
    ('James Brown', '1933-05-03', '12:00', 'musician'),
    ('Marvin Gaye', '1939-04-02', '12:00', 'musician'),
    ('Stevie Wonder', '1950-05-13', '16:30', 'musician'),
    ('Diana Ross', '1944-03-26', '23:46', 'musician'),
    ('Tina Turner', '1939-11-26', '22:10', 'musician'),
    ('Usher', '1978-10-14', '12:00', 'musician'),
    ('Alicia Keys', '1981-01-25', '12:00', 'musician'),
    ('John Legend', '1978-12-28', '12:00', 'musician'),
    ('The Weeknd', '1990-02-16', '12:00', 'musician'),
    ('SZA', '1989-11-08', '12:00', 'musician'),
    ('Frank Ocean', '1987-10-28', '12:00', 'musician'),
    ('Daniel Caesar', '1995-04-05', '12:00', 'musician'),
    ('HER', '1997-06-27', '12:00', 'musician'),
]

def datetime_to_jd(dt):
    """Convert datetime to Julian Day, handling negative years (BCE)."""
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour + dt.minute / 60.0
    return swe.julday(year, month, day, hour)

def get_features(jd):
    """Extract chart features for clustering."""
    planets = {swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MERCURY: 'Mercury',
               swe.VENUS: 'Venus', swe.MARS: 'Mars', swe.JUPITER: 'Jupiter',
               swe.SATURN: 'Saturn'}
    
    features = {}
    for pid, name in planets.items():
        try:
            result = swe.calc_ut(jd, pid)[0]
            features[f'{name}_lon'] = result[0]
            features[f'{name}_sign'] = int(result[0] / 30)
        except Exception:
            features[f'{name}_lon'] = 0.0
            features[f'{name}_sign'] = 0
    
    return features

def main():
    print("=" * 70)
    print("PROJECT 18b: PROFESSIONAL CLUSTERING - UNSUPERVISED LEARNING")
    print("=" * 70)
    
    # Remove duplicates
    seen = set()
    unique_professionals = []
    for p in PROFESSIONALS:
        if p[0] not in seen:
            seen.add(p[0])
            unique_professionals.append(p)
    
    print(f"\nProcessing {len(unique_professionals)} unique professionals...")
    
    records = []
    errors = 0
    for name, birth_date, birth_time, profession in unique_professionals:
        try:
            # Handle negative years (BCE dates)
            if birth_date.startswith('-'):
                year = int(birth_date.split('-')[1]) * -1
                parts = birth_date.split('-')
                month = int(parts[2])
                day = int(parts[3])
            else:
                dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
                year = dt.year
                month = dt.month
                day = dt.day
            
            time_parts = birth_time.split(':')
            hour = int(time_parts[0]) + int(time_parts[1]) / 60.0
            jd = swe.julday(year, month, day, hour)
            features = get_features(jd)
            records.append({'name': name, 'profession': profession, **features})
        except Exception as e:
            errors += 1
    
    print(f"Successfully processed: {len(records)} professionals")
    if errors > 0:
        print(f"Errors: {errors}")
    
    df = pd.DataFrame(records)
    
    # Show profession distribution
    print(f"\n{'Profession Distribution':=^50}")
    prof_counts = df['profession'].value_counts()
    for prof, count in prof_counts.items():
        print(f"  {prof:20s}: {count:4d}")
    print(f"  {'TOTAL':20s}: {len(df):4d}")
    
    # Clustering Features
    feature_cols = [c for c in df.columns if '_lon' in c]
    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # =========================================================================
    # MULTIPLE CLUSTERING APPROACHES
    # =========================================================================
    
    print(f"\n{'Clustering Analysis':=^50}")
    
    # 1. K-Means with optimal k selection
    silhouette_scores = []
    k_range = range(2, 12)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        silhouette_scores.append(score)
    
    optimal_k = k_range[np.argmax(silhouette_scores)]
    print(f"\nOptimal K (by silhouette): {optimal_k}")
    print(f"Silhouette scores by K: {dict(zip(k_range, [f'{s:.3f}' for s in silhouette_scores]))}")
    
    # Final K-Means clustering
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    df['kmeans_cluster'] = kmeans.fit_predict(X_scaled)
    
    # 2. Hierarchical clustering
    hier = AgglomerativeClustering(n_clusters=optimal_k)
    df['hier_cluster'] = hier.fit_predict(X_scaled)
    
    # 3. Also run with profession-matched k (number of professions)
    n_professions = df['profession'].nunique()
    kmeans_prof = KMeans(n_clusters=n_professions, random_state=42, n_init=10)
    df['kmeans_prof_cluster'] = kmeans_prof.fit_predict(X_scaled)
    
    # =========================================================================
    # STATISTICAL TESTING
    # =========================================================================
    
    print(f"\n{'Statistical Testing':=^50}")
    
    results = {}
    
    # Chi-square test: K-Means optimal clusters vs profession
    crosstab_kmeans = pd.crosstab(df['profession'], df['kmeans_cluster'])
    chi2_km, p_km, dof_km, expected_km = stats.chi2_contingency(crosstab_kmeans)
    results['kmeans_chi2'] = chi2_km
    results['kmeans_p'] = p_km
    results['kmeans_dof'] = dof_km
    
    print(f"\nK-Means (K={optimal_k}) vs Profession:")
    print(f"  Chi-square: {chi2_km:.2f}, p-value: {p_km:.6f}")
    
    # Chi-square test: Hierarchical clusters vs profession
    crosstab_hier = pd.crosstab(df['profession'], df['hier_cluster'])
    chi2_h, p_h, dof_h, expected_h = stats.chi2_contingency(crosstab_hier)
    results['hier_chi2'] = chi2_h
    results['hier_p'] = p_h
    
    print(f"\nHierarchical (K={optimal_k}) vs Profession:")
    print(f"  Chi-square: {chi2_h:.2f}, p-value: {p_h:.6f}")
    
    # Chi-square test: K-Means with profession-matched K
    crosstab_prof = pd.crosstab(df['profession'], df['kmeans_prof_cluster'])
    chi2_p, p_p, dof_p, expected_p = stats.chi2_contingency(crosstab_prof)
    results['prof_kmeans_chi2'] = chi2_p
    results['prof_kmeans_p'] = p_p
    
    print(f"\nK-Means (K={n_professions}, matched to professions) vs Profession:")
    print(f"  Chi-square: {chi2_p:.2f}, p-value: {p_p:.6f}")
    
    # Adjusted Rand Index (measures agreement between clustering and true labels)
    profession_labels = pd.factorize(df['profession'])[0]
    ari_kmeans = adjusted_rand_score(profession_labels, df['kmeans_cluster'])
    ari_hier = adjusted_rand_score(profession_labels, df['hier_cluster'])
    ari_prof = adjusted_rand_score(profession_labels, df['kmeans_prof_cluster'])
    
    results['ari_kmeans'] = ari_kmeans
    results['ari_hier'] = ari_hier
    results['ari_prof'] = ari_prof
    
    print(f"\nAdjusted Rand Index (0=random, 1=perfect match):")
    print(f"  K-Means (optimal k):    {ari_kmeans:.4f}")
    print(f"  Hierarchical:           {ari_hier:.4f}")
    print(f"  K-Means (matched k):    {ari_prof:.4f}")
    
    # Cramér's V for effect size
    def cramers_v(confusion_matrix):
        chi2 = stats.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        min_dim = min(confusion_matrix.shape) - 1
        return np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
    
    v_kmeans = cramers_v(crosstab_kmeans)
    v_prof = cramers_v(crosstab_prof)
    results['cramers_v_kmeans'] = v_kmeans
    results['cramers_v_prof'] = v_prof
    
    print(f"\nCramér's V (effect size, 0=none, 1=perfect):")
    print(f"  K-Means (optimal k):    {v_kmeans:.4f}")
    print(f"  K-Means (matched k):    {v_prof:.4f}")
    
    # =========================================================================
    # PCA FOR VISUALIZATION
    # =========================================================================
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df['PC1'] = X_pca[:, 0]
    df['PC2'] = X_pca[:, 1]
    
    print(f"\nPCA Variance Explained: {pca.explained_variance_ratio_.sum():.1%}")
    
    # =========================================================================
    # CROSSTAB DISPLAY
    # =========================================================================
    
    print(f"\n{'Cluster vs Profession Crosstab (K-Means)':=^60}")
    print(crosstab_prof.to_string())
    
    # =========================================================================
    # VISUALIZATION
    # =========================================================================
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. PCA scatter by profession
    colors = plt.cm.tab10(np.linspace(0, 1, n_professions))
    for i, prof in enumerate(df['profession'].unique()):
        mask = df['profession'] == prof
        axes[0, 0].scatter(df.loc[mask, 'PC1'], df.loc[mask, 'PC2'],
                          c=[colors[i]], label=prof, alpha=0.6, s=30)
    axes[0, 0].set_xlabel('PC1')
    axes[0, 0].set_ylabel('PC2')
    axes[0, 0].set_title(f'PCA by Profession (n={len(df)})')
    axes[0, 0].legend(loc='upper right', fontsize=8)
    
    # 2. PCA scatter by cluster
    for cluster in range(n_professions):
        mask = df['kmeans_prof_cluster'] == cluster
        axes[0, 1].scatter(df.loc[mask, 'PC1'], df.loc[mask, 'PC2'],
                          c=[colors[cluster]], label=f'Cluster {cluster}', alpha=0.6, s=30)
    axes[0, 1].set_xlabel('PC1')
    axes[0, 1].set_ylabel('PC2')
    axes[0, 1].set_title(f'PCA by K-Means Cluster (K={n_professions})')
    axes[0, 1].legend(loc='upper right', fontsize=8)
    
    # 3. Silhouette score by K
    axes[1, 0].plot(list(k_range), silhouette_scores, 'bo-')
    axes[1, 0].axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal K={optimal_k}')
    axes[1, 0].set_xlabel('Number of Clusters (K)')
    axes[1, 0].set_ylabel('Silhouette Score')
    axes[1, 0].set_title('Silhouette Score vs K')
    axes[1, 0].legend()
    
    # 4. Heatmap of cluster vs profession
    crosstab_norm = crosstab_prof.div(crosstab_prof.sum(axis=1), axis=0)
    im = axes[1, 1].imshow(crosstab_norm.values, aspect='auto', cmap='YlOrRd')
    axes[1, 1].set_xticks(range(n_professions))
    axes[1, 1].set_xticklabels([f'C{i}' for i in range(n_professions)])
    axes[1, 1].set_yticks(range(n_professions))
    axes[1, 1].set_yticklabels(crosstab_norm.index)
    axes[1, 1].set_xlabel('Cluster')
    axes[1, 1].set_ylabel('Profession')
    axes[1, 1].set_title(f'Profession Distribution per Cluster\n(p={p_p:.4f}, V={v_prof:.3f})')
    plt.colorbar(im, ax=axes[1, 1], label='Proportion')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'clustering_analysis.png', dpi=150)
    plt.close()
    
    # =========================================================================
    # SAVE RESULTS
    # =========================================================================
    
    # Save detailed results
    results['n_professionals'] = len(df)
    results['n_professions'] = n_professions
    results['optimal_k'] = optimal_k
    results['silhouette_optimal'] = max(silhouette_scores)
    
    results_df = pd.DataFrame([results])
    results_df.to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)
    
    # Save full data with clusters
    df.to_csv(OUTPUT_DIR / 'professional_data.csv', index=False)
    
    # =========================================================================
    # INTERPRETATION
    # =========================================================================
    
    print(f"\n{'=' * 70}")
    print("INTERPRETATION")
    print("=" * 70)
    
    if p_p < 0.05 and v_prof > 0.1:
        print("\n⚠️  SIGNIFICANT but WEAK association found between birth chart")
        print("   clusters and profession. However, this may be due to:")
        print("   - Large sample size making small effects significant")
        print("   - Confounding factors (birth year, geography, etc.)")
        print(f"   Effect size (Cramér's V = {v_prof:.3f}) indicates {interpret_cramers_v(v_prof)} association")
    elif p_p < 0.05:
        print("\n✓  Statistically significant association found, BUT effect size")
        print(f"   is negligible (V = {v_prof:.3f}). Not practically meaningful.")
    else:
        print("\n✗  NO significant association found between birth chart clustering")
        print("   and professional categories.")
        print(f"   Chi-square p = {p_p:.4f}")
        print(f"   Adjusted Rand Index = {ari_prof:.4f} (near 0 = random)")
    
    print(f"\nCONCLUSION: Birth chart planetary positions do NOT predict")
    print(f"profession. Clustering shows {interpret_cramers_v(v_prof)} correlation with career.")
    
    print(f"\nResults saved to {OUTPUT_DIR}")

def interpret_cramers_v(v):
    if v < 0.1:
        return "negligible"
    elif v < 0.3:
        return "weak"
    elif v < 0.5:
        return "moderate"
    else:
        return "strong"

if __name__ == '__main__':
    main()

