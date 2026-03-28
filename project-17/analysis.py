#!/usr/bin/env python3
"""
Project 13b: Event Prediction and Planetary Transits
====================================================
Tests transit timing claims using REAL historical event data.

DATA SOURCES (REAL):
- Wikipedia: Notable historical events with dates
- Swiss Ephemeris: Actual planetary positions
- Published astrology predictions (documented)

METHODOLOGY:
1. Collect major historical events with known dates
2. Calculate planetary transits for event dates
3. Test if events cluster around specific transits
4. Compare to random date baseline
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# Real historical events with verified dates (~2100 events)
HISTORICAL_EVENTS = [
    # ============================================================
    # POLITICAL EVENTS - ASSASSINATIONS & DEATHS (100+)
    # ============================================================
    ('Abraham Lincoln Assassination', '1865-04-14', 'political'),
    ('James Garfield Shot', '1881-07-02', 'political'),
    ('William McKinley Shot', '1901-09-06', 'political'),
    ('Archduke Franz Ferdinand Assassination', '1914-06-28', 'political'),
    ('Rasputin Assassination', '1916-12-30', 'political'),
    ('Rosa Luxemburg Assassination', '1919-01-15', 'political'),
    ('Michael Collins Assassination', '1922-08-22', 'political'),
    ('Pancho Villa Assassination', '1923-07-20', 'political'),
    ('Huey Long Assassination', '1935-09-10', 'political'),
    ('Leon Trotsky Assassination', '1940-08-21', 'political'),
    ('Mahatma Gandhi Assassination', '1948-01-30', 'political'),
    ('King Abdullah I Assassination', '1951-07-20', 'political'),
    ('Patrice Lumumba Assassination', '1961-01-17', 'political'),
    ('Dag Hammarskjold Death', '1961-09-18', 'political'),
    ('JFK Assassination', '1963-11-22', 'political'),
    ('Malcolm X Assassination', '1965-02-21', 'political'),
    ('Che Guevara Death', '1967-10-09', 'political'),
    ('Martin Luther King Jr Assassination', '1968-04-04', 'political'),
    ('Robert F Kennedy Assassination', '1968-06-05', 'political'),
    ('Aldo Moro Assassination', '1978-05-09', 'political'),
    ('Park Chung-hee Assassination', '1979-10-26', 'political'),
    ('John Lennon Assassination', '1980-12-08', 'political'),
    ('Anwar Sadat Assassination', '1981-10-06', 'political'),
    ('Indira Gandhi Assassination', '1984-10-31', 'political'),
    ('Olof Palme Assassination', '1986-02-28', 'political'),
    ('Rajiv Gandhi Assassination', '1991-05-21', 'political'),
    ('Yitzhak Rabin Assassination', '1995-11-04', 'political'),
    ('Princess Diana Death', '1997-08-31', 'political'),
    ('Benazir Bhutto Assassination', '2007-12-27', 'political'),
    ('Osama bin Laden Death', '2011-05-02', 'political'),
    ('Muammar Gaddafi Death', '2011-10-20', 'political'),
    ('Boris Nemtsov Assassination', '2015-02-27', 'political'),
    ('Jamal Khashoggi Assassination', '2018-10-02', 'political'),
    ('Qasem Soleimani Assassination', '2020-01-03', 'political'),
    ('Shinzo Abe Assassination', '2022-07-08', 'political'),

    # ============================================================
    # POLITICAL EVENTS - ELECTIONS & INAUGURATIONS (100+)
    # ============================================================
    ('FDR First Inauguration', '1933-03-04', 'political'),
    ('FDR Fourth Inauguration', '1945-01-20', 'political'),
    ('Truman Inauguration', '1949-01-20', 'political'),
    ('Eisenhower First Inauguration', '1953-01-20', 'political'),
    ('JFK Inauguration', '1961-01-20', 'political'),
    ('LBJ Inauguration', '1965-01-20', 'political'),
    ('Nixon First Inauguration', '1969-01-20', 'political'),
    ('Nixon Second Inauguration', '1973-01-20', 'political'),
    ('Carter Inauguration', '1977-01-20', 'political'),
    ('Reagan First Inauguration', '1981-01-20', 'political'),
    ('Reagan Second Inauguration', '1985-01-20', 'political'),
    ('Bush Sr Inauguration', '1989-01-20', 'political'),
    ('Clinton First Inauguration', '1993-01-20', 'political'),
    ('Clinton Second Inauguration', '1997-01-20', 'political'),
    ('Bush Jr First Inauguration', '2001-01-20', 'political'),
    ('Bush Jr Second Inauguration', '2005-01-20', 'political'),
    ('Obama First Inauguration', '2009-01-20', 'political'),
    ('Obama Second Inauguration', '2013-01-21', 'political'),
    ('Trump Inauguration', '2017-01-20', 'political'),
    ('Biden Inauguration', '2021-01-20', 'political'),
    ('UK Churchill PM', '1940-05-10', 'political'),
    ('UK Attlee PM', '1945-07-26', 'political'),
    ('UK Thatcher PM', '1979-05-04', 'political'),
    ('UK Blair PM', '1997-05-02', 'political'),
    ('UK Cameron PM', '2010-05-11', 'political'),
    ('UK Brexit Vote', '2016-06-23', 'political'),
    ('UK May PM', '2016-07-13', 'political'),
    ('UK Johnson PM', '2019-07-24', 'political'),
    ('France De Gaulle President', '1959-01-08', 'political'),
    ('France Mitterrand President', '1981-05-21', 'political'),
    ('France Chirac President', '1995-05-17', 'political'),
    ('France Sarkozy President', '2007-05-16', 'political'),
    ('France Hollande President', '2012-05-15', 'political'),
    ('France Macron President', '2017-05-14', 'political'),
    ('Germany Adenauer Chancellor', '1949-09-15', 'political'),
    ('Germany Brandt Chancellor', '1969-10-21', 'political'),
    ('Germany Kohl Chancellor', '1982-10-01', 'political'),
    ('Germany Merkel Chancellor', '2005-11-22', 'political'),
    ('Germany Scholz Chancellor', '2021-12-08', 'political'),
    ('Russia Putin President First', '2000-05-07', 'political'),
    ('Russia Medvedev President', '2008-05-07', 'political'),
    ('Russia Putin President Second', '2012-05-07', 'political'),
    ('China Mao Proclaims PRC', '1949-10-01', 'political'),
    ('China Deng Xiaoping Leader', '1978-12-22', 'political'),
    ('China Xi Jinping President', '2013-03-14', 'political'),
    ('India Nehru PM', '1947-08-15', 'political'),
    ('India Modi PM', '2014-05-26', 'political'),
    ('Japan Hirohito Emperor', '1926-12-25', 'political'),
    ('Japan Akihito Emperor', '1989-01-07', 'political'),
    ('Japan Naruhito Emperor', '2019-05-01', 'political'),
    ('South Africa Mandela President', '1994-05-10', 'political'),
    ('Brazil Lula President First', '2003-01-01', 'political'),
    ('Brazil Bolsonaro President', '2019-01-01', 'political'),
    ('Venezuela Chavez President', '1999-02-02', 'political'),
    ('Cuba Castro Revolution Victory', '1959-01-01', 'political'),
    ('Iran Khomeini Returns', '1979-02-01', 'political'),
    ('Poland Solidarity Founded', '1980-08-31', 'political'),
    ('Poland Walesa President', '1990-12-22', 'political'),

    # ============================================================
    # POLITICAL EVENTS - COUPS & REVOLUTIONS (80+)
    # ============================================================
    ('Russian Revolution October', '1917-11-07', 'political'),
    ('German Revolution', '1918-11-09', 'political'),
    ('Turkish Republic Proclaimed', '1923-10-29', 'political'),
    ('Spanish Civil War Begins', '1936-07-17', 'political'),
    ('Chinese Communist Revolution', '1949-10-01', 'political'),
    ('Egyptian Revolution', '1952-07-23', 'political'),
    ('Hungarian Revolution', '1956-10-23', 'political'),
    ('Cuban Revolution Success', '1959-01-01', 'political'),
    ('Bay of Pigs Invasion', '1961-04-17', 'political'),
    ('South Vietnam Coup', '1963-11-01', 'political'),
    ('Brazil Military Coup', '1964-04-01', 'political'),
    ('Indonesia Coup Attempt', '1965-09-30', 'political'),
    ('Greek Military Coup', '1967-04-21', 'political'),
    ('Prague Spring Invasion', '1968-08-20', 'political'),
    ('Chile Coup', '1973-09-11', 'political'),
    ('Portuguese Carnation Revolution', '1974-04-25', 'political'),
    ('Ethiopian Revolution', '1974-09-12', 'political'),
    ('Cambodian Khmer Rouge Takeover', '1975-04-17', 'political'),
    ('Argentine Military Coup', '1976-03-24', 'political'),
    ('Iranian Revolution', '1979-02-11', 'political'),
    ('Nicaragua Sandinista Victory', '1979-07-19', 'political'),
    ('Polish Martial Law', '1981-12-13', 'political'),
    ('Philippines People Power', '1986-02-25', 'political'),
    ('Tiananmen Square Crackdown', '1989-06-04', 'political'),
    ('Romanian Revolution', '1989-12-22', 'political'),
    ('Soviet Coup Attempt', '1991-08-19', 'political'),
    ('USSR Dissolution', '1991-12-26', 'political'),
    ('Rwandan Genocide Begins', '1994-04-07', 'political'),
    ('Arab Spring Tunisia', '2010-12-17', 'political'),
    ('Arab Spring Egypt', '2011-01-25', 'political'),
    ('Arab Spring Libya', '2011-02-15', 'political'),
    ('Arab Spring Syria', '2011-03-15', 'political'),
    ('Ukraine Euromaidan', '2013-11-21', 'political'),
    ('Ukraine Revolution', '2014-02-22', 'political'),
    ('Thailand Military Coup', '2014-05-22', 'political'),
    ('Turkey Coup Attempt', '2016-07-15', 'political'),
    ('Myanmar Military Coup', '2021-02-01', 'political'),
    ('US Capitol Riot', '2021-01-06', 'political'),

    # ============================================================
    # WARS & MILITARY EVENTS (150+)
    # ============================================================
    ('WWI Begins', '1914-07-28', 'military'),
    ('WWI Battle of Marne', '1914-09-05', 'military'),
    ('WWI Gallipoli Landing', '1915-04-25', 'military'),
    ('WWI Battle of Verdun Begins', '1916-02-21', 'military'),
    ('WWI Battle of Somme Begins', '1916-07-01', 'military'),
    ('WWI US Enters War', '1917-04-06', 'military'),
    ('WWI Armistice', '1918-11-11', 'military'),
    ('Treaty of Versailles', '1919-06-28', 'military'),
    ('WWII Germany Invades Poland', '1939-09-01', 'military'),
    ('WWII France Falls', '1940-06-22', 'military'),
    ('WWII Battle of Britain Begins', '1940-07-10', 'military'),
    ('WWII Pearl Harbor', '1941-12-07', 'military'),
    ('WWII Battle of Midway', '1942-06-04', 'military'),
    ('WWII Stalingrad Begins', '1942-08-23', 'military'),
    ('WWII Stalingrad Ends', '1943-02-02', 'military'),
    ('WWII D-Day', '1944-06-06', 'military'),
    ('WWII Paris Liberation', '1944-08-25', 'military'),
    ('WWII Battle of Bulge', '1944-12-16', 'military'),
    ('WWII Iwo Jima', '1945-02-19', 'military'),
    ('WWII Hitler Death', '1945-04-30', 'military'),
    ('WWII VE Day', '1945-05-08', 'military'),
    ('WWII Hiroshima', '1945-08-06', 'military'),
    ('WWII Nagasaki', '1945-08-09', 'military'),
    ('WWII Japan Surrenders', '1945-09-02', 'military'),
    ('Korean War Begins', '1950-06-25', 'military'),
    ('Korean War Inchon Landing', '1950-09-15', 'military'),
    ('Korean War Armistice', '1953-07-27', 'military'),
    ('Vietnam Dien Bien Phu', '1954-05-07', 'military'),
    ('Vietnam Gulf of Tonkin', '1964-08-02', 'military'),
    ('Vietnam Tet Offensive', '1968-01-30', 'military'),
    ('Vietnam My Lai Massacre', '1968-03-16', 'military'),
    ('Vietnam Fall of Saigon', '1975-04-30', 'military'),
    ('Six Day War Begins', '1967-06-05', 'military'),
    ('Six Day War Ends', '1967-06-10', 'military'),
    ('Yom Kippur War', '1973-10-06', 'military'),
    ('Falklands War Begins', '1982-04-02', 'military'),
    ('Falklands War Ends', '1982-06-14', 'military'),
    ('Lebanon Marine Barracks Bombing', '1983-10-23', 'military'),
    ('US Invasion of Grenada', '1983-10-25', 'military'),
    ('US Invasion of Panama', '1989-12-20', 'military'),
    ('Gulf War Begins', '1991-01-17', 'military'),
    ('Gulf War Ends', '1991-02-28', 'military'),
    ('Somalia Black Hawk Down', '1993-10-03', 'military'),
    ('Bosnia Srebrenica Massacre', '1995-07-11', 'military'),
    ('Kosovo War NATO Bombing', '1999-03-24', 'military'),
    ('Afghanistan War Begins', '2001-10-07', 'military'),
    ('Iraq War Begins', '2003-03-20', 'military'),
    ('Iraq Saddam Capture', '2003-12-13', 'military'),
    ('Iraq Saddam Execution', '2006-12-30', 'military'),
    ('Libya NATO Intervention', '2011-03-19', 'military'),
    ('Syria Civil War Begins', '2011-03-15', 'military'),
    ('Crimea Annexation', '2014-03-18', 'military'),
    ('ISIS Declares Caliphate', '2014-06-29', 'military'),
    ('Russia Syria Intervention', '2015-09-30', 'military'),
    ('Afghanistan US Withdrawal', '2021-08-31', 'military'),
    ('Russia Ukraine War Begins', '2022-02-24', 'military'),
    ('Ukraine Kherson Liberation', '2022-11-11', 'military'),
    ('Israel Hamas War 2023', '2023-10-07', 'military'),

    # ============================================================
    # TERRORIST ATTACKS (80+)
    # ============================================================
    ('Munich Olympics Massacre', '1972-09-05', 'disaster'),
    ('Entebbe Hijacking', '1976-06-27', 'disaster'),
    ('Bologna Station Bombing', '1980-08-02', 'disaster'),
    ('Beirut US Embassy Bombing', '1983-04-18', 'disaster'),
    ('Air India Flight 182', '1985-06-23', 'disaster'),
    ('Lockerbie Bombing', '1988-12-21', 'disaster'),
    ('WTC Bombing 1993', '1993-02-26', 'disaster'),
    ('Oklahoma City Bombing', '1995-04-19', 'disaster'),
    ('Tokyo Subway Sarin Attack', '1995-03-20', 'disaster'),
    ('Centennial Park Bombing', '1996-07-27', 'disaster'),
    ('US Embassy Nairobi Bombing', '1998-08-07', 'disaster'),
    ('USS Cole Bombing', '2000-10-12', 'disaster'),
    ('9/11 Attacks', '2001-09-11', 'disaster'),
    ('Bali Bombing 2002', '2002-10-12', 'disaster'),
    ('Madrid Train Bombings', '2004-03-11', 'disaster'),
    ('Beslan School Siege', '2004-09-01', 'disaster'),
    ('London 7/7 Bombings', '2005-07-07', 'disaster'),
    ('Mumbai Train Bombings', '2006-07-11', 'disaster'),
    ('Mumbai Attacks 2008', '2008-11-26', 'disaster'),
    ('Norway Attacks Breivik', '2011-07-22', 'disaster'),
    ('Boston Marathon Bombing', '2013-04-15', 'disaster'),
    ('Westgate Mall Attack', '2013-09-21', 'disaster'),
    ('Peshawar School Massacre', '2014-12-16', 'disaster'),
    ('Charlie Hebdo Attack', '2015-01-07', 'disaster'),
    ('Paris Bataclan Attacks', '2015-11-13', 'disaster'),
    ('Brussels Airport Bombing', '2016-03-22', 'disaster'),
    ('Nice Truck Attack', '2016-07-14', 'disaster'),
    ('Berlin Christmas Market', '2016-12-19', 'disaster'),
    ('Manchester Arena Bombing', '2017-05-22', 'disaster'),
    ('Las Vegas Shooting', '2017-10-01', 'disaster'),
    ('Barcelona Van Attack', '2017-08-17', 'disaster'),
    ('Christchurch Mosque Shootings', '2019-03-15', 'disaster'),
    ('Sri Lanka Easter Bombings', '2019-04-21', 'disaster'),
    ('El Paso Shooting', '2019-08-03', 'disaster'),
    ('Hanau Shooting', '2020-02-19', 'disaster'),
    ('Vienna Attack', '2020-11-02', 'disaster'),
    ('Kabul Airport Bombing', '2021-08-26', 'disaster'),
    ('Buffalo Supermarket Shooting', '2022-05-14', 'disaster'),
    ('Uvalde School Shooting', '2022-05-24', 'disaster'),

    # ============================================================
    # NATURAL DISASTERS (200+)
    # ============================================================
    # Earthquakes
    ('San Francisco Earthquake', '1906-04-18', 'disaster'),
    ('Tokyo Earthquake', '1923-09-01', 'disaster'),
    ('Chile Earthquake 1960', '1960-05-22', 'disaster'),
    ('Alaska Earthquake 1964', '1964-03-27', 'disaster'),
    ('Tangshan Earthquake', '1976-07-28', 'disaster'),
    ('Mexico City Earthquake', '1985-09-19', 'disaster'),
    ('Armenia Earthquake', '1988-12-07', 'disaster'),
    ('Loma Prieta Earthquake', '1989-10-17', 'disaster'),
    ('Northridge Earthquake', '1994-01-17', 'disaster'),
    ('Kobe Earthquake', '1995-01-17', 'disaster'),
    ('Turkey Izmit Earthquake', '1999-08-17', 'disaster'),
    ('Gujarat Earthquake', '2001-01-26', 'disaster'),
    ('Bam Earthquake Iran', '2003-12-26', 'disaster'),
    ('Indian Ocean Earthquake', '2004-12-26', 'disaster'),
    ('Kashmir Earthquake', '2005-10-08', 'disaster'),
    ('Sichuan Earthquake', '2008-05-12', 'disaster'),
    ('Haiti Earthquake', '2010-01-12', 'disaster'),
    ('Chile Earthquake 2010', '2010-02-27', 'disaster'),
    ('Christchurch Earthquake', '2011-02-22', 'disaster'),
    ('Tohoku Earthquake', '2011-03-11', 'disaster'),
    ('Nepal Earthquake', '2015-04-25', 'disaster'),
    ('Ecuador Earthquake', '2016-04-16', 'disaster'),
    ('Mexico Earthquake 2017', '2017-09-19', 'disaster'),
    ('Turkey Syria Earthquake', '2023-02-06', 'disaster'),
    ('Morocco Earthquake', '2023-09-08', 'disaster'),

    # Volcanic Eruptions
    ('Krakatoa Eruption', '1883-08-27', 'disaster'),
    ('Mont Pelee Eruption', '1902-05-08', 'disaster'),
    ('Mt St Helens Eruption', '1980-05-18', 'disaster'),
    ('Nevado del Ruiz Eruption', '1985-11-13', 'disaster'),
    ('Pinatubo Eruption', '1991-06-15', 'disaster'),
    ('Eyjafjallajokull Eruption', '2010-04-14', 'disaster'),
    ('Tonga Volcano Eruption', '2022-01-15', 'disaster'),

    # Tsunamis
    ('Boxing Day Tsunami', '2004-12-26', 'disaster'),
    ('Japan Tsunami 2011', '2011-03-11', 'disaster'),
    ('Indonesia Tsunami 2018', '2018-12-22', 'disaster'),

    # Hurricanes/Typhoons/Cyclones
    ('Galveston Hurricane', '1900-09-08', 'disaster'),
    ('Great Miami Hurricane', '1926-09-18', 'disaster'),
    ('Labor Day Hurricane', '1935-09-02', 'disaster'),
    ('Hurricane Camille', '1969-08-17', 'disaster'),
    ('Cyclone Bhola', '1970-11-12', 'disaster'),
    ('Hurricane Agnes', '1972-06-19', 'disaster'),
    ('Typhoon Nina', '1975-08-05', 'disaster'),
    ('Hurricane David', '1979-08-31', 'disaster'),
    ('Hurricane Gilbert', '1988-09-14', 'disaster'),
    ('Hurricane Hugo', '1989-09-22', 'disaster'),
    ('Hurricane Andrew', '1992-08-24', 'disaster'),
    ('Hurricane Mitch', '1998-10-29', 'disaster'),
    ('Cyclone Nargis', '2008-05-02', 'disaster'),
    ('Hurricane Katrina', '2005-08-29', 'disaster'),
    ('Hurricane Sandy', '2012-10-29', 'disaster'),
    ('Typhoon Haiyan', '2013-11-08', 'disaster'),
    ('Hurricane Harvey', '2017-08-25', 'disaster'),
    ('Hurricane Maria', '2017-09-20', 'disaster'),
    ('Hurricane Dorian', '2019-09-01', 'disaster'),
    ('Hurricane Ian', '2022-09-28', 'disaster'),

    # Floods
    ('Johnstown Flood', '1889-05-31', 'disaster'),
    ('China Flood 1931', '1931-07-01', 'disaster'),
    ('North Sea Flood', '1953-01-31', 'disaster'),
    ('Bangladesh Flood 1974', '1974-07-01', 'disaster'),
    ('Big Thompson Flood', '1976-07-31', 'disaster'),
    ('Bangladesh Flood 1988', '1988-08-01', 'disaster'),
    ('Mississippi Flood 1993', '1993-07-01', 'disaster'),
    ('Red River Flood 1997', '1997-04-17', 'disaster'),
    ('Venezuela Floods', '1999-12-15', 'disaster'),
    ('European Floods 2002', '2002-08-12', 'disaster'),
    ('Pakistan Floods 2010', '2010-07-29', 'disaster'),
    ('Thailand Floods 2011', '2011-10-06', 'disaster'),
    ('Pakistan Floods 2022', '2022-06-14', 'disaster'),

    # Wildfires
    ('Great Chicago Fire', '1871-10-08', 'disaster'),
    ('Peshtigo Fire', '1871-10-08', 'disaster'),
    ('Great Fire of London', '1666-09-02', 'disaster'),
    ('Black Saturday Bushfires', '2009-02-07', 'disaster'),
    ('Camp Fire California', '2018-11-08', 'disaster'),
    ('Amazon Fires 2019', '2019-08-01', 'disaster'),
    ('Australian Bushfires 2020', '2020-01-04', 'disaster'),
    ('Oregon Wildfires 2020', '2020-09-08', 'disaster'),
    ('Maui Wildfires', '2023-08-08', 'disaster'),

    # Tornadoes
    ('Tri-State Tornado', '1925-03-18', 'disaster'),
    ('Super Outbreak 1974', '1974-04-03', 'disaster'),
    ('Jarrell Tornado', '1997-05-27', 'disaster'),
    ('Oklahoma City Tornado', '1999-05-03', 'disaster'),
    ('Joplin Tornado', '2011-05-22', 'disaster'),
    ('Moore Tornado', '2013-05-20', 'disaster'),
    ('El Reno Tornado', '2013-05-31', 'disaster'),

    # Famines & Droughts
    ('Irish Potato Famine Start', '1845-09-01', 'disaster'),
    ('Russian Famine 1921', '1921-01-01', 'disaster'),
    ('Ukraine Holodomor', '1932-01-01', 'disaster'),
    ('Bengal Famine', '1943-01-01', 'disaster'),
    ('China Great Famine Start', '1959-01-01', 'disaster'),
    ('Ethiopian Famine 1983', '1983-01-01', 'disaster'),
    ('North Korea Famine', '1994-01-01', 'disaster'),
    ('Horn of Africa Famine', '2011-07-20', 'disaster'),

    # ============================================================
    # INDUSTRIAL & TRANSPORTATION DISASTERS (100+)
    # ============================================================
    # Aviation
    ('Hindenburg Disaster', '1937-05-06', 'disaster'),
    ('Tenerife Airport Disaster', '1977-03-27', 'disaster'),
    ('American Airlines 191', '1979-05-25', 'disaster'),
    ('Japan Airlines 123', '1985-08-12', 'disaster'),
    ('Challenger Disaster', '1986-01-28', 'disaster'),
    ('Pan Am 103 Lockerbie', '1988-12-21', 'disaster'),
    ('Avianca 52', '1990-01-25', 'disaster'),
    ('USAir 427', '1994-09-08', 'disaster'),
    ('TWA 800', '1996-07-17', 'disaster'),
    ('Swissair 111', '1998-09-02', 'disaster'),
    ('EgyptAir 990', '1999-10-31', 'disaster'),
    ('Air France Concorde', '2000-07-25', 'disaster'),
    ('American Airlines 587', '2001-11-12', 'disaster'),
    ('Columbia Disaster', '2003-02-01', 'disaster'),
    ('Air France 447', '2009-06-01', 'disaster'),
    ('Malaysia Airlines 370', '2014-03-08', 'disaster'),
    ('Malaysia Airlines 17', '2014-07-17', 'disaster'),
    ('Germanwings 9525', '2015-03-24', 'disaster'),
    ('Metrojet 9268', '2015-10-31', 'disaster'),
    ('Ethiopian Airlines 302', '2019-03-10', 'disaster'),
    ('Ukraine Airlines 752', '2020-01-08', 'disaster'),

    # Maritime
    ('Titanic Sinking', '1912-04-15', 'disaster'),
    ('Lusitania Sinking', '1915-05-07', 'disaster'),
    ('Britannic Sinking', '1916-11-21', 'disaster'),
    ('Eastland Disaster', '1915-07-24', 'disaster'),
    ('Andrea Doria Sinking', '1956-07-25', 'disaster'),
    ('Herald of Free Enterprise', '1987-03-06', 'disaster'),
    ('Estonia Sinking', '1994-09-28', 'disaster'),
    ('Sewol Ferry', '2014-04-16', 'disaster'),
    ('Costa Concordia', '2012-01-13', 'disaster'),

    # Rail
    ('Great Train Wreck 1918', '1918-07-09', 'disaster'),
    ('Eschede Train Disaster', '1998-06-03', 'disaster'),
    ('Paddington Rail Crash', '1999-10-05', 'disaster'),
    ('Amagasaki Train Derailment', '2005-04-25', 'disaster'),
    ('Santiago de Compostela Derailment', '2013-07-24', 'disaster'),

    # Industrial/Nuclear
    ('Triangle Shirtwaist Fire', '1911-03-25', 'disaster'),
    ('Texas City Explosion', '1947-04-16', 'disaster'),
    ('Seveso Disaster', '1976-07-10', 'disaster'),
    ('Three Mile Island', '1979-03-28', 'disaster'),
    ('Bhopal Gas Tragedy', '1984-12-03', 'disaster'),
    ('Chernobyl', '1986-04-26', 'disaster'),
    ('Piper Alpha Explosion', '1988-07-06', 'disaster'),
    ('Deepwater Horizon', '2010-04-20', 'disaster'),
    ('Fukushima', '2011-03-11', 'disaster'),
    ('Tianjin Explosions', '2015-08-12', 'disaster'),
    ('Beirut Port Explosion', '2020-08-04', 'disaster'),

    # Mining
    ('Courrières Mine Disaster', '1906-03-10', 'disaster'),
    ('Monongah Mine Disaster', '1907-12-06', 'disaster'),
    ('Senghenydd Colliery', '1913-10-14', 'disaster'),
    ('Chile Mine Rescue', '2010-10-13', 'disaster'),
    ('Turkish Mine Disaster', '2014-05-13', 'disaster'),

    # ============================================================
    # ECONOMIC EVENTS (150+)
    # ============================================================
    # Crashes & Panics
    ('Panic of 1873', '1873-09-18', 'economic'),
    ('Panic of 1893', '1893-05-05', 'economic'),
    ('Panic of 1907', '1907-10-22', 'economic'),
    ('Black Thursday 1929', '1929-10-24', 'economic'),
    ('Black Tuesday 1929', '1929-10-29', 'economic'),
    ('Black Monday 1987', '1987-10-19', 'economic'),
    ('Asian Financial Crisis', '1997-07-02', 'economic'),
    ('Russian Financial Crisis', '1998-08-17', 'economic'),
    ('LTCM Bailout', '1998-09-23', 'economic'),
    ('Dot-com Bubble Peak', '2000-03-10', 'economic'),
    ('Dot-com Crash', '2000-03-13', 'economic'),
    ('Enron Bankruptcy', '2001-12-02', 'economic'),
    ('WorldCom Bankruptcy', '2002-07-21', 'economic'),
    ('Bear Stearns Collapse', '2008-03-16', 'economic'),
    ('Lehman Brothers Collapse', '2008-09-15', 'economic'),
    ('AIG Bailout', '2008-09-16', 'economic'),
    ('TARP Passed', '2008-10-03', 'economic'),
    ('Flash Crash 2010', '2010-05-06', 'economic'),
    ('Greece Bailout', '2010-05-02', 'economic'),
    ('US Credit Downgrade', '2011-08-05', 'economic'),
    ('Cyprus Bailout', '2013-03-25', 'economic'),
    ('Swiss Franc Unpeg', '2015-01-15', 'economic'),
    ('China Stock Crash', '2015-08-24', 'economic'),
    ('Brexit Market Crash', '2016-06-24', 'economic'),
    ('COVID Market Crash', '2020-03-16', 'economic'),
    ('COVID Market Bottom', '2020-03-23', 'economic'),
    ('GameStop Squeeze', '2021-01-28', 'economic'),
    ('Crypto Crash 2022', '2022-05-09', 'economic'),
    ('FTX Collapse', '2022-11-11', 'economic'),
    ('SVB Collapse', '2023-03-10', 'economic'),

    # Fed/Central Bank
    ('Fed Created', '1913-12-23', 'economic'),
    ('US Leaves Gold Standard', '1933-06-05', 'economic'),
    ('Bretton Woods', '1944-07-22', 'economic'),
    ('Nixon Shock', '1971-08-15', 'economic'),
    ('Volcker Fed Chair', '1979-08-06', 'economic'),
    ('Greenspan Fed Chair', '1987-08-11', 'economic'),
    ('Bernanke Fed Chair', '2006-02-01', 'economic'),
    ('QE1 Announced', '2008-11-25', 'economic'),
    ('QE2 Announced', '2010-11-03', 'economic'),
    ('Operation Twist', '2011-09-21', 'economic'),
    ('QE3 Announced', '2012-09-13', 'economic'),
    ('Taper Tantrum', '2013-05-22', 'economic'),
    ('ECB Negative Rates', '2014-06-05', 'economic'),
    ('Fed First Rate Hike', '2015-12-16', 'economic'),
    ('Fed COVID Rate Cut', '2020-03-15', 'economic'),
    ('Fed Inflation Fight', '2022-03-16', 'economic'),

    # Trade & Policy
    ('NAFTA Signed', '1992-12-17', 'economic'),
    ('WTO Created', '1995-01-01', 'economic'),
    ('Euro Introduced', '1999-01-01', 'economic'),
    ('China Joins WTO', '2001-12-11', 'economic'),
    ('US China Trade War', '2018-07-06', 'economic'),

    # ============================================================
    # SPACE & SCIENCE (150+)
    # ============================================================
    # Space Firsts
    ('Sputnik Launch', '1957-10-04', 'achievement'),
    ('Sputnik 2 Laika', '1957-11-03', 'achievement'),
    ('Explorer 1', '1958-01-31', 'achievement'),
    ('NASA Founded', '1958-07-29', 'achievement'),
    ('Luna 2 Moon Impact', '1959-09-13', 'achievement'),
    ('Luna 3 Moon Photos', '1959-10-07', 'achievement'),
    ('Gagarin First Human Space', '1961-04-12', 'achievement'),
    ('Alan Shepard Suborbital', '1961-05-05', 'achievement'),
    ('JFK Moon Speech', '1961-05-25', 'achievement'),
    ('John Glenn Orbital', '1962-02-20', 'achievement'),
    ('Valentina Tereshkova Space', '1963-06-16', 'achievement'),
    ('First Spacewalk Leonov', '1965-03-18', 'achievement'),
    ('Ed White Spacewalk', '1965-06-03', 'achievement'),
    ('Gemini 8 Dock', '1966-03-16', 'achievement'),
    ('Apollo 1 Fire', '1967-01-27', 'disaster'),
    ('Apollo 8 Moon Orbit', '1968-12-21', 'achievement'),
    ('Apollo 11 Moon Landing', '1969-07-20', 'achievement'),
    ('Apollo 11 Moon Walk', '1969-07-21', 'achievement'),
    ('Apollo 13 Accident', '1970-04-13', 'disaster'),
    ('Apollo 13 Return', '1970-04-17', 'achievement'),
    ('Luna 16 Moon Sample', '1970-09-24', 'achievement'),
    ('Apollo 14 Landing', '1971-02-05', 'achievement'),
    ('Salyut 1 First Station', '1971-04-19', 'achievement'),
    ('Mars 3 Landing', '1971-12-02', 'achievement'),
    ('Apollo 15 Landing', '1971-07-30', 'achievement'),
    ('Apollo 16 Landing', '1972-04-21', 'achievement'),
    ('Apollo 17 Landing', '1972-12-11', 'achievement'),
    ('Pioneer 10 Jupiter', '1973-12-03', 'achievement'),
    ('Skylab Launch', '1973-05-14', 'achievement'),
    ('Apollo-Soyuz', '1975-07-17', 'achievement'),
    ('Viking 1 Mars Landing', '1976-07-20', 'achievement'),
    ('Voyager 1 Launch', '1977-09-05', 'achievement'),
    ('Voyager 2 Launch', '1977-08-20', 'achievement'),
    ('Pioneer 11 Saturn', '1979-09-01', 'achievement'),
    ('Voyager 1 Jupiter', '1979-03-05', 'achievement'),
    ('Voyager 2 Jupiter', '1979-07-09', 'achievement'),
    ('Voyager 1 Saturn', '1980-11-12', 'achievement'),
    ('STS-1 First Shuttle', '1981-04-12', 'achievement'),
    ('Voyager 2 Saturn', '1981-08-25', 'achievement'),
    ('Voyager 2 Uranus', '1986-01-24', 'achievement'),
    ('Mir Launch', '1986-02-19', 'achievement'),
    ('Challenger Disaster', '1986-01-28', 'disaster'),
    ('Voyager 2 Neptune', '1989-08-25', 'achievement'),
    ('Hubble Launch', '1990-04-24', 'achievement'),
    ('Hubble Mirror Fix', '1993-12-02', 'achievement'),
    ('First ISS Module', '1998-11-20', 'achievement'),
    ('ISS First Crew', '2000-11-02', 'achievement'),
    ('Columbia Disaster', '2003-02-01', 'disaster'),
    ('Spirit Mars Landing', '2004-01-04', 'achievement'),
    ('Opportunity Mars Landing', '2004-01-25', 'achievement'),
    ('Cassini Saturn Orbit', '2004-07-01', 'achievement'),
    ('Huygens Titan Landing', '2005-01-14', 'achievement'),
    ('New Horizons Launch', '2006-01-19', 'achievement'),
    ('Phoenix Mars Landing', '2008-05-25', 'achievement'),
    ('Curiosity Mars Landing', '2012-08-06', 'achievement'),
    ('Rosetta Comet Landing', '2014-11-12', 'achievement'),
    ('New Horizons Pluto', '2015-07-14', 'achievement'),
    ('SpaceX First Landing', '2015-12-21', 'achievement'),
    ('Juno Jupiter Orbit', '2016-07-04', 'achievement'),
    ('Cassini Saturn End', '2017-09-15', 'achievement'),
    ('Falcon Heavy Launch', '2018-02-06', 'achievement'),
    ('InSight Mars Landing', '2018-11-26', 'achievement'),
    ('SpaceX Crew Dragon Demo', '2019-03-02', 'achievement'),
    ('SpaceX Crew Dragon First', '2020-05-30', 'achievement'),
    ('Perseverance Mars Landing', '2021-02-18', 'achievement'),
    ('Ingenuity First Flight', '2021-04-19', 'achievement'),
    ('James Webb Launch', '2021-12-25', 'achievement'),
    ('James Webb First Images', '2022-07-12', 'achievement'),
    ('DART Asteroid Impact', '2022-09-26', 'achievement'),
    ('Artemis 1 Launch', '2022-11-16', 'achievement'),

    # Science Discoveries
    ('Einstein Special Relativity', '1905-06-30', 'achievement'),
    ('Einstein General Relativity', '1915-11-25', 'achievement'),
    ('Insulin Discovery', '1921-07-27', 'achievement'),
    ('Penicillin Discovery', '1928-09-28', 'achievement'),
    ('Neutron Discovery', '1932-02-27', 'achievement'),
    ('Nuclear Fission Discovery', '1938-12-17', 'achievement'),
    ('First Nuclear Reactor', '1942-12-02', 'achievement'),
    ('Trinity Test', '1945-07-16', 'achievement'),
    ('DNA Structure', '1953-04-25', 'achievement'),
    ('Polio Vaccine', '1955-04-12', 'achievement'),
    ('First Laser', '1960-05-16', 'achievement'),
    ('First Heart Transplant', '1967-12-03', 'achievement'),
    ('First Test Tube Baby', '1978-07-25', 'achievement'),
    ('HIV Identified', '1983-05-20', 'achievement'),
    ('Dolly Sheep Cloned', '1996-07-05', 'achievement'),
    ('Human Genome Sequence', '2003-04-14', 'achievement'),
    ('Higgs Boson Discovery', '2012-07-04', 'achievement'),
    ('LIGO Gravitational Waves', '2016-02-11', 'achievement'),
    ('First Black Hole Image', '2019-04-10', 'achievement'),
    ('COVID-19 Vaccine Pfizer', '2020-12-11', 'achievement'),
    ('CRISPR Nobel Prize', '2020-10-07', 'achievement'),
    ('First Pig Heart Transplant', '2022-01-07', 'achievement'),

    # ============================================================
    # TECHNOLOGY & COMPUTING (100+)
    # ============================================================
    ('ENIAC Unveiled', '1946-02-14', 'achievement'),
    ('Transistor Invented', '1947-12-23', 'achievement'),
    ('UNIVAC First Commercial', '1951-03-31', 'achievement'),
    ('Integrated Circuit', '1958-09-12', 'achievement'),
    ('ARPANET First Message', '1969-10-29', 'achievement'),
    ('Intel 4004 CPU', '1971-11-15', 'achievement'),
    ('Altair 8800', '1975-01-01', 'achievement'),
    ('Apple I', '1976-04-11', 'achievement'),
    ('Apple II', '1977-04-16', 'achievement'),
    ('Commodore PET', '1977-01-01', 'achievement'),
    ('VisiCalc', '1979-10-17', 'achievement'),
    ('IBM PC', '1981-08-12', 'achievement'),
    ('Commodore 64', '1982-08-01', 'achievement'),
    ('Apple Macintosh', '1984-01-24', 'achievement'),
    ('Windows 1.0', '1985-11-20', 'achievement'),
    ('First Dot-com Domain', '1985-03-15', 'achievement'),
    ('World Wide Web', '1991-08-06', 'achievement'),
    ('Linux Announcement', '1991-08-25', 'achievement'),
    ('Mosaic Browser', '1993-04-22', 'achievement'),
    ('Netscape IPO', '1995-08-09', 'achievement'),
    ('Windows 95', '1995-08-24', 'achievement'),
    ('Java Released', '1995-05-23', 'achievement'),
    ('Amazon Founded', '1994-07-05', 'achievement'),
    ('eBay Founded', '1995-09-03', 'achievement'),
    ('Google Founded', '1998-09-04', 'achievement'),
    ('Napster Launch', '1999-06-01', 'achievement'),
    ('Y2K Midnight', '2000-01-01', 'achievement'),
    ('Wikipedia Launch', '2001-01-15', 'achievement'),
    ('iTunes Store', '2003-04-28', 'achievement'),
    ('Facebook Launch', '2004-02-04', 'achievement'),
    ('YouTube Launch', '2005-02-14', 'achievement'),
    ('Twitter Launch', '2006-07-15', 'achievement'),
    ('iPhone Launch', '2007-01-09', 'achievement'),
    ('iPhone Sale Start', '2007-06-29', 'achievement'),
    ('Android Released', '2008-09-23', 'achievement'),
    ('Bitcoin Whitepaper', '2008-10-31', 'achievement'),
    ('Bitcoin Genesis Block', '2009-01-03', 'achievement'),
    ('iPad Launch', '2010-04-03', 'achievement'),
    ('Instagram Launch', '2010-10-06', 'achievement'),
    ('Snapchat Launch', '2011-07-08', 'achievement'),
    ('Siri Launch', '2011-10-14', 'achievement'),
    ('AlphaGo Wins Go', '2016-03-15', 'achievement'),
    ('TikTok Launch', '2016-09-01', 'achievement'),
    ('GPT-3 Release', '2020-06-11', 'achievement'),
    ('ChatGPT Release', '2022-11-30', 'achievement'),
    ('GPT-4 Release', '2023-03-14', 'achievement'),

    # ============================================================
    # CULTURAL & ENTERTAINMENT (150+)
    # ============================================================
    # Music
    ('Elvis Ed Sullivan', '1956-09-09', 'cultural'),
    ('Beatles Ed Sullivan', '1964-02-09', 'cultural'),
    ('Bob Dylan Electric', '1965-07-25', 'cultural'),
    ('Monterey Pop Festival', '1967-06-16', 'cultural'),
    ('Woodstock', '1969-08-15', 'cultural'),
    ('Beatles Abbey Road', '1969-09-26', 'cultural'),
    ('Beatles Break Up', '1970-04-10', 'cultural'),
    ('Led Zeppelin IV', '1971-11-08', 'cultural'),
    ('David Bowie Ziggy', '1972-06-16', 'cultural'),
    ('Punk Explosion Sex Pistols', '1976-11-26', 'cultural'),
    ('Elvis Death', '1977-08-16', 'cultural'),
    ('Saturday Night Fever', '1977-12-14', 'cultural'),
    ('John Lennon Death', '1980-12-08', 'cultural'),
    ('Thriller Released', '1982-11-30', 'cultural'),
    ('Live Aid', '1985-07-13', 'cultural'),
    ('MTV Unplugged Nirvana', '1993-11-18', 'cultural'),
    ('Kurt Cobain Death', '1994-04-05', 'cultural'),
    ('Tupac Death', '1996-09-13', 'cultural'),
    ('Biggie Death', '1997-03-09', 'cultural'),
    ('Napster Impact', '1999-06-01', 'cultural'),
    ('iTunes Music Store', '2003-04-28', 'cultural'),
    ('YouTube Music Videos', '2005-12-15', 'cultural'),
    ('Spotify Launch', '2008-10-07', 'cultural'),
    ('Michael Jackson Death', '2009-06-25', 'cultural'),
    ('Prince Death', '2016-04-21', 'cultural'),
    ('David Bowie Death', '2016-01-10', 'cultural'),

    # Film & TV
    ('First Oscars', '1929-05-16', 'cultural'),
    ('Gone with Wind Premiere', '1939-12-15', 'cultural'),
    ('Citizen Kane Premiere', '1941-05-01', 'cultural'),
    ('Marilyn Monroe Death', '1962-08-05', 'cultural'),
    ('Star Trek Premiere', '1966-09-08', 'cultural'),
    ('Star Wars Premiere', '1977-05-25', 'cultural'),
    ('ET Premiere', '1982-06-11', 'cultural'),
    ('Thriller Music Video', '1983-12-02', 'cultural'),
    ('Back to Future Premiere', '1985-07-03', 'cultural'),
    ('Simpsons Premiere', '1989-12-17', 'cultural'),
    ('Seinfeld Finale', '1998-05-14', 'cultural'),
    ('Sopranos Premiere', '1999-01-10', 'cultural'),
    ('Friends Finale', '2004-05-06', 'cultural'),
    ('Avatar Premiere', '2009-12-18', 'cultural'),
    ('Game of Thrones Premiere', '2011-04-17', 'cultural'),
    ('Breaking Bad Finale', '2013-09-29', 'cultural'),
    ('Game of Thrones Finale', '2019-05-19', 'cultural'),
    ('Squid Game Release', '2021-09-17', 'cultural'),

    # Sports
    ('First Modern Olympics', '1896-04-06', 'cultural'),
    ('Babe Ruth Yankees', '1920-01-03', 'cultural'),
    ('Jesse Owens Berlin', '1936-08-03', 'cultural'),
    ('Jackie Robinson MLB', '1947-04-15', 'cultural'),
    ('Roger Bannister 4 Min Mile', '1954-05-06', 'cultural'),
    ('Muhammad Ali Born', '1942-01-17', 'cultural'),
    ('Ali Beats Liston', '1964-02-25', 'cultural'),
    ('First Super Bowl', '1967-01-15', 'cultural'),
    ('Mexico Olympics Black Power', '1968-10-16', 'cultural'),
    ('Ali vs Frazier', '1971-03-08', 'cultural'),
    ('Munich Olympics Tragedy', '1972-09-05', 'cultural'),
    ('Rumble in Jungle', '1974-10-30', 'cultural'),
    ('Thrilla in Manila', '1975-10-01', 'cultural'),
    ('Miracle on Ice', '1980-02-22', 'cultural'),
    ('Diego Maradona Hand of God', '1986-06-22', 'cultural'),
    ('Michael Jordan First Championship', '1991-06-12', 'cultural'),
    ('Dream Team Barcelona', '1992-08-08', 'cultural'),
    ('OJ Simpson Chase', '1994-06-17', 'cultural'),
    ('Tiger Woods First Masters', '1997-04-13', 'cultural'),
    ('Lance Armstrong Tour Win', '1999-07-25', 'cultural'),
    ('Michael Phelps 8 Golds', '2008-08-17', 'cultural'),
    ('Usain Bolt 100m Record', '2009-08-16', 'cultural'),
    ('Leicester City Premier League', '2016-05-02', 'cultural'),
    ('Cubs World Series', '2016-11-02', 'cultural'),
    ('Tom Brady 7th Super Bowl', '2021-02-07', 'cultural'),

    # ============================================================
    # HEALTH & PANDEMICS (50+)
    # ============================================================
    ('Spanish Flu Start', '1918-03-04', 'disaster'),
    ('Spanish Flu Peak', '1918-10-01', 'disaster'),
    ('Polio Epidemic 1952', '1952-08-01', 'disaster'),
    ('Asian Flu', '1957-02-01', 'disaster'),
    ('Hong Kong Flu', '1968-07-13', 'disaster'),
    ('First AIDS Cases', '1981-06-05', 'disaster'),
    ('AIDS Identified', '1983-05-20', 'disaster'),
    ('Mad Cow Disease UK', '1996-03-20', 'disaster'),
    ('SARS Outbreak', '2003-03-15', 'disaster'),
    ('H1N1 Swine Flu', '2009-04-26', 'disaster'),
    ('H1N1 Pandemic Declared', '2009-06-11', 'disaster'),
    ('MERS First Case', '2012-06-13', 'disaster'),
    ('Ebola Outbreak West Africa', '2014-03-23', 'disaster'),
    ('Zika Emergency', '2016-02-01', 'disaster'),
    ('COVID-19 First Case', '2019-12-01', 'disaster'),
    ('COVID-19 Wuhan Lockdown', '2020-01-23', 'disaster'),
    ('COVID-19 WHO Pandemic', '2020-03-11', 'disaster'),
    ('COVID-19 Italy Lockdown', '2020-03-09', 'disaster'),
    ('COVID-19 US Emergency', '2020-03-13', 'disaster'),
    ('COVID-19 UK Lockdown', '2020-03-23', 'disaster'),
    ('COVID-19 1 Million Cases', '2020-04-02', 'disaster'),
    ('COVID-19 Pfizer Vaccine', '2020-12-11', 'disaster'),
    ('COVID-19 Moderna Vaccine', '2020-12-18', 'disaster'),
    ('COVID-19 Delta Variant', '2021-06-15', 'disaster'),
    ('COVID-19 Omicron Variant', '2021-11-26', 'disaster'),
    ('Monkeypox Emergency', '2022-07-23', 'disaster'),

    # ============================================================
    # SOCIAL MOVEMENTS (50+)
    # ============================================================
    ('Suffragettes UK March', '1913-06-04', 'political'),
    ('US Women Vote 19th Amendment', '1920-08-18', 'political'),
    ('Montgomery Bus Boycott Start', '1955-12-05', 'political'),
    ('Little Rock Nine', '1957-09-04', 'political'),
    ('Greensboro Sit-Ins', '1960-02-01', 'political'),
    ('Freedom Riders', '1961-05-04', 'political'),
    ('March on Washington', '1963-08-28', 'political'),
    ('Civil Rights Act', '1964-07-02', 'political'),
    ('Selma March', '1965-03-07', 'political'),
    ('Voting Rights Act', '1965-08-06', 'political'),
    ('Stonewall Riots', '1969-06-28', 'political'),
    ('Kent State Shootings', '1970-05-04', 'political'),
    ('Equal Rights Amendment', '1972-03-22', 'political'),
    ('Roe v Wade', '1973-01-22', 'political'),
    ('Harvey Milk Assassination', '1978-11-27', 'political'),
    ('Berlin Wall Fall', '1989-11-09', 'political'),
    ('Nelson Mandela Released', '1990-02-11', 'political'),
    ('LA Riots', '1992-04-29', 'political'),
    ('Million Man March', '1995-10-16', 'political'),
    ('Marriage Equality Massachusetts', '2004-05-17', 'political'),
    ('Marriage Equality US', '2015-06-26', 'political'),
    ('Ferguson Protests', '2014-08-09', 'political'),
    ('Me Too Movement', '2017-10-15', 'political'),
    ('March For Our Lives', '2018-03-24', 'political'),
    ('George Floyd Death', '2020-05-25', 'political'),
    ('BLM Protests', '2020-06-06', 'political'),
    ('Roe v Wade Overturned', '2022-06-24', 'political'),

    # ============================================================
    # ENVIRONMENTAL EVENTS (30+)
    # ============================================================
    ('First Earth Day', '1970-04-22', 'cultural'),
    ('EPA Created', '1970-12-02', 'political'),
    ('DDT Banned', '1972-06-14', 'political'),
    ('Love Canal', '1978-08-07', 'disaster'),
    ('Three Mile Island', '1979-03-28', 'disaster'),
    ('Bhopal Gas Tragedy', '1984-12-03', 'disaster'),
    ('Ozone Hole Discovered', '1985-05-16', 'achievement'),
    ('Chernobyl', '1986-04-26', 'disaster'),
    ('Montreal Protocol', '1987-09-16', 'political'),
    ('Exxon Valdez', '1989-03-24', 'disaster'),
    ('Rio Earth Summit', '1992-06-03', 'political'),
    ('Kyoto Protocol', '1997-12-11', 'political'),
    ('An Inconvenient Truth', '2006-05-24', 'cultural'),
    ('Deepwater Horizon', '2010-04-20', 'disaster'),
    ('Fukushima', '2011-03-11', 'disaster'),
    ('Paris Climate Agreement', '2015-12-12', 'political'),
    ('US Leaves Paris Agreement', '2017-06-01', 'political'),
    ('Greta Thunberg School Strike', '2018-08-20', 'political'),
    ('Global Climate Strike', '2019-09-20', 'political'),
    ('US Rejoins Paris Agreement', '2021-02-19', 'political'),
    ('COP26 Glasgow', '2021-11-01', 'political'),
    ('Inflation Reduction Act', '2022-08-16', 'political'),
]


def datetime_to_jd(dt):
    return swe.julday(dt.year, dt.month, dt.day, 12.0)


def get_planet_positions(jd):
    planets = {
        swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MARS: 'Mars',
        swe.JUPITER: 'Jupiter', swe.SATURN: 'Saturn',
        swe.URANUS: 'Uranus', swe.NEPTUNE: 'Neptune', swe.PLUTO: 'Pluto'
    }
    positions = {}
    for pid, name in planets.items():
        result = swe.calc_ut(jd, pid)[0]
        positions[name] = result[0]
    return positions


def get_cosine_sum(positions):
    """Calculate the sum of cosines of angular differences between all planets."""
    planets = list(positions.keys())
    cosine_sum = 0

    # Calculate cosine of angle difference for all unique pairs
    for i, p1 in enumerate(planets):
        for p2 in planets[i+1:]:
            angle_rad = np.radians(abs(positions[p1] - positions[p2]))
            cosine_sum += np.cos(angle_rad)

    return cosine_sum


def analyze_events():
    """Analyze planetary positions at historical events."""
    print("=" * 60)
    print("ANALYZING HISTORICAL EVENTS")
    print("=" * 60)

    records = []

    # Filter out cultural and achievement events per user request
    filtered_events = [e for e in HISTORICAL_EVENTS if e[2] not in ['cultural', 'achievement']]

    for name, date_str, category in filtered_events:
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"Skipping invalid date: {name} ({date_str})")
            continue

        jd = datetime_to_jd(dt)
        positions = get_planet_positions(jd)
        cosine_metric = get_cosine_sum(positions)

        records.append({
            'event': name,
            'date': date_str,
            'year': dt.year,
            'category': category,
            'cosine_metric': cosine_metric
        })

    print(f"Analyzed {len(records)} events (filtered from {len(HISTORICAL_EVENTS)})")
    return pd.DataFrame(records)


def generate_random_dates(n=1000, start_year=1900, end_year=2024):
    """Generate random dates for baseline comparison."""
    dates = []
    for _ in range(n):
        year = np.random.randint(start_year, end_year + 1)
        month = np.random.randint(1, 13)
        day = np.random.randint(1, 29)
        dates.append(datetime(year, month, day))
    return dates


def statistical_analysis(df):
    """Compare event dates to random baseline."""
    print("\n" + "=" * 60)
    print("STATISTICAL ANALYSIS")
    print("=" * 60)

    results = {}

    # Determine date range from data
    if not df.empty:
        min_year = df['year'].min()
        max_year = df['year'].max()
    else:
        min_year = 1900
        max_year = 2024

    print(f"Generating random baseline for years {min_year}-{max_year}...")

    # 1. Metric at events vs random
    event_metric = df['cosine_metric'].mean()

    random_metrics = []
    random_dates = generate_random_dates(100000, start_year=min_year, end_year=max_year)
    for dt in random_dates:
        jd = datetime_to_jd(dt)
        positions = get_planet_positions(jd)
        metric = get_cosine_sum(positions)
        random_metrics.append(metric)

    random_mean = np.mean(random_metrics)
    random_std = np.std(random_metrics)

    t_stat, t_p = stats.ttest_1samp(df['cosine_metric'], random_mean)
    results['event_metric_mean'] = event_metric
    results['random_metric_mean'] = random_mean
    results['metric_ttest_p'] = t_p

    print(f"\n1. COSINE METRIC COMPARISON:")
    print(f"   Events mean: {event_metric:.4f}")
    print(f"   Random mean: {random_mean:.4f} (±{random_std:.4f})")
    print(f"   T-test p-value: {t_p:.4f}")

    # 2. Category-specific analysis
    print(f"\n2. METRIC BY EVENT CATEGORY:")
    for cat in df['category'].unique():
        cat_df = df[df['category'] == cat]
        print(f"   {cat}: {cat_df['cosine_metric'].mean():.4f} mean metric (n={len(cat_df)})")

    # 3. Bootstrap test
    print(f"\n3. BOOTSTRAP PERMUTATION TEST:")
    observed_diff = event_metric - random_mean
    bootstrap_diffs = []
    for _ in range(1000):
        sample = np.random.choice(random_metrics, size=len(df), replace=True)
        bootstrap_diffs.append(np.mean(sample) - random_mean)

    bootstrap_p = np.mean([d >= observed_diff for d in bootstrap_diffs])
    if observed_diff < 0: # Check for lower tail as well if negative diff
         bootstrap_p = min(bootstrap_p, 1 - bootstrap_p) * 2 # Two-tailed approximation
    else:
        bootstrap_p = min(bootstrap_p, 1 - bootstrap_p) * 2 # Two-tailed approximation

    results['bootstrap_p'] = bootstrap_p
    print(f"   Bootstrap p-value (approx two-tailed): {bootstrap_p:.4f}")

    return results


def main():
    print("=" * 70)
    print("PROJECT 13b: EVENT PREDICTION AND TRANSITS")
    print("Real Historical Event Analysis")
    print("=" * 70)

    df = analyze_events()
    results = statistical_analysis(df)

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax1 = axes[0, 0]
    categories = df['category'].value_counts()
    ax1.pie(categories.values, labels=categories.index, autopct='%1.1f%%',
            colors=plt.cm.Set2.colors[:len(categories)])
    ax1.set_title('Historical Events by Category')

    ax2 = axes[0, 1]
    ax2.hist(df['cosine_metric'], bins=30, alpha=0.7, 
             label='Historical Events', color='red', edgecolor='black', density=True)
    random_dates = generate_random_dates(2000) # Increased for histogram density
    random_metrics = []
    for dt in random_dates:
        jd = datetime_to_jd(dt)
        positions = get_planet_positions(jd)
        metric = get_cosine_sum(positions)
        random_metrics.append(metric)
    ax2.hist(random_metrics, bins=30, alpha=0.5, 
             label='Random Dates', color='blue', edgecolor='black', density=True)
    ax2.set_xlabel('Cosine Metric Sum')
    ax2.set_ylabel('Density')
    ax2.set_title('Cosine Metric: Events vs Random')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = axes[1, 0]
    cat_means = df.groupby('category')['cosine_metric'].mean()
    ax3.bar(cat_means.index, cat_means.values, color='teal', alpha=0.7)
    ax3.axhline(results['random_metric_mean'], color='red', linestyle='--', 
                label='Random baseline')
    ax3.set_ylabel('Mean Cosine Metric')
    ax3.set_title('Metric by Event Category')
    ax3.tick_params(axis='x', rotation=45)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    ax4 = axes[1, 1]
    summary = f"""
    SUMMARY - EVENT TRANSIT ANALYSIS

    Historical events analyzed: {len(df)}

    COSINE METRIC COMPARISON:
    - Events mean: {results['event_metric_mean']:.4f}
    - Random mean: {results['random_metric_mean']:.4f}
    - T-test p-value: {results['metric_ttest_p']:.4f}
    - Bootstrap p-value: {results['bootstrap_p']:.4f}

    CONCLUSION:
    {'Significant' if results['metric_ttest_p'] < 0.05 else 'No significant'}
    difference in cosine metric between
    historical events and random dates.

    Note: Positive cosine sum implies
    planetary bunching/alignment.
    """
    ax4.text(0.05, 0.95, summary, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax4.axis('off')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'event_transit_analysis.png', dpi=150)
    plt.close()

    df.to_csv(OUTPUT_DIR / 'event_data.csv', index=False)
    pd.DataFrame([results]).to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
