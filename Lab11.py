import sys, matplotlib.pyplot as plt

import re

def load_students(filename):
    students = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            match = re.match(r"(\d+)(.+)", line)
            if match:
                student_id = int(match.group(1))
                name = match.group(2).strip()
                students[student_id] = name
    return students

def load_assignments(filename):
    assignments = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            assignment_id = int(lines[i+1].strip())
            points = int(lines[i+2].strip())
            assignments[assignment_id] = {'name': name, 'points': points}
    return assignments

def load_submissions():
    import os
    submissions = []
    for filename in os.listdir('data'):
        if filename.endswith('.txt') and filename != "students.txt" and filename != "assignments.txt":
            with open(f'data/{filename}', 'r') as file:
                for line in file:
                    student_id, assignment_id, percentage = map(int, line.strip().split('|'))
                    submissions.append({'student_id': student_id, 'assignment_id': assignment_id, 'percentage': percentage})
    return submissions

# 2.  Calculation Functions
def calculate_student_grade(student_name, students, assignments, submissions):

    student_grade = 0
    total_points = 0
    student_found = False

    for student_id, name in students.items():
        if name == student_name:
            student_found = True
            for submission in submissions:
                if submission['student_id'] == student_id:
                    assignment = assignments.get(submission['assignment_id'])
                    if assignment:
                        student_grade += (submission['percentage'] / 100) * assignment['points']
                        total_points += assignment['points']
            break

    if not student_found:
        return "Student not found"
    else:
        return round((student_grade / total_points) * 100) if total_points > 0 else 0

def calculate_assignment_stats(assignment_name, assignments, submissions):

    scores = []
    assignment_found = False

    for assignment_id, assignment in assignments.items():
        if assignment['name'] == assignment_name:
            assignment_found = True
            for submission in submissions:
                if submission['assignment_id'] == assignment_id:
                    scores.append(submission['percentage'])
            break

    if not assignment_found:
        return "Assignment not found"
    elif scores:
        return {
            "Min": round(min(scores)),
            "Avg": round(sum(scores) / len(scores)),
            "Max": round(max(scores))
        }
    else:
        return {"Min": 0, "Avg": 0, "Max": 0}

def display_assignment_graph(assignment_name, assignments, submissions):
    
    scores = []
    assignment_found = False

    for assignment_id, assignment in assignments.items():
        if assignment['name'] == assignment_name:
            assignment_found = True
            for submission in submissions:
                if submission['assignment_id'] == assignment_id:
                    scores.append(submission['percentage'])
            break

    if not assignment_found:
        print("Assignment not found")
    elif scores:
        plt.hist(scores, bins=[0, 25, 50, 75, 100])
        plt.title(f'Assignment Scores for {assignment_name}')
        plt.xlabel('Percentage')
        plt.ylabel('Number of Students')
        plt.show()
    else:
        print("No scores found for this assignment.")

# 3.  Menu and User Interaction
def display_menu():
    """Displays the menu and gets user input."""
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    return input("Enter your selection: ")

# 4.  Main Function
def main():
    students = load_students('data/students.txt')
    assignments = load_assignments('data/assignments.txt')
    submissions = load_submissions()

    while True:
        choice = display_menu()

        if choice == '1':
            student_name = input("What is the student's name: ")
            grade = calculate_student_grade(student_name, students, assignments, submissions)
            print(grade)
            break
        elif choice == '2':
            assignment_name = input("What is the assignment name: ")
            stats = calculate_assignment_stats(assignment_name, assignments, submissions)
            if isinstance(stats, dict):
                print(f"Min: {stats['Min']}%")
                print(f"Avg: {stats['Avg']}%")
                print(f"Max: {stats['Max']}%")
            else:
                print(stats)
            break
        elif choice == '3':
            assignment_name = input("What is the assignment name: ")
            display_assignment_graph(assignment_name, assignments, submissions)
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
