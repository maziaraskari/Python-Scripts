import os
import sys
import fileinput



range = []
range2 =[]




print("Enter lower number to search for:")

lower = input("> ")

print("Enter highest number to search for:")

upper = input("> ")



print("Enter lower number range to change to:")

lower1 = input("> ")

print("Enter highest number range to cahgne to for:")

upper1 = input("> ")



# Read in the file
with open('file.txt', 'r') as file:
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('abcd', 'ram')

# Write the file out again
with open('file.txt', 'w') as file:
  file.write(filedata)