
def calculate_total(marks):
    """Returns the sum of all marks in the marks dictionary."""
    return sum(marks.values())

def calculate_average(marks):
    """Returns the average rounded to 2 decimals using calculate_total."""
    if not marks:
        return 0.0
    return round(calculate_total(marks) / len(marks), 2)

def get_grade(average):
    """Returns letter grade based on the average mark."""
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"

def check_result(marks, pass_mark=40):
    """Returns 'Pass' only if every subject is at least the pass mark, otherwise 'Fail'."""
    for mark in marks.values():
        if mark < pass_mark:
            return "Fail"
    return "Pass"

def student_summary(student):
    """Takes one student dictionary and returns a new dictionary with name, total, average, grade, and result."""
    marks = student["marks"]
    total = calculate_total(marks)
    average = calculate_average(marks)
    grade = get_grade(average)
    result = check_result(marks)
    return {
        "name": student["name"],
        "total": total,
        "average": average,
        "grade": grade,
        "result": result
    }

def add_student(data, student_id, name, **marks):
    """Adds a student with marks given as keyword arguments and returns True; returns False if ID already exists."""
    if student_id in data:
        return False
    data[student_id] = {
        "name": name,
        "marks": marks
    }
    return True

def update_marks(data, student_id, **changes):
    """Updates the marks given as keyword arguments and returns True; returns False if ID does not exist."""
    if student_id not in data:
        return False
    data[student_id]["marks"].update(changes)
    return True

def remove_student(data, student_id):
    """Removes the student and returns True; returns False if ID does not exist."""
    if student_id not in data:
        return False
    data.pop(student_id)
    return True

def print_report(data):
    """Prints the report table, with students sorted by average in descending order."""
    print(f"{'ID':<6}{'Name':<8}{'Total':<6}{'Avg':<8}{'Grade':<7}  {'Result'}")
    print("-" * 42)
    
    avg_id_list = []
    for sid, student in data.items():
        avg = calculate_average(student["marks"])
        avg_id_list.append((avg, sid))
    
    avg_id_list.sort(reverse=True)
    
    for avg, sid in avg_id_list:
        student = data[sid]
        summary = student_summary(student)
        print(f"{sid:<6}{summary['name']:<8}{summary['total']:<6}{summary['average']:<8.2f}{summary['grade']:<7}  {summary['result']}")

def class_statistics(data, *subjects):
    """Returns a dictionary with the topper's name, pass percentage, and average mark of each subject."""
    if not data:
        return {"topper": None, "pass_percentage": 0.0, "subject_averages": {}}
    
    best_avg = -1
    topper_name = ""
    pass_count = 0
    total_students = len(data)
    subject_marks = {}
    
    for sid, student in data.items():
        summary = student_summary(student)
        if summary["average"] > best_avg:
            best_avg = summary["average"]
            topper_name = summary["name"]
        
        if summary["result"] == "Pass":
            pass_count += 1
            
        for subj, mark in student["marks"].items():
            if subjects and subj not in subjects:
                continue
            if subj not in subject_marks:
                subject_marks[subj] = []
            subject_marks[subj].append(mark)
            
    pass_percentage = round((pass_count / total_students) * 100, 1)
    
    subject_averages = {}
    target_subjects = subjects if subjects else subject_marks.keys()
    for subj in target_subjects:
        if subj in subject_marks and subject_marks[subj]:
            subject_averages[subj] = round(sum(subject_marks[subj]) / len(subject_marks[subj]), 1)
        else:
            subject_averages[subj] = 0.0
            
    return {
        "topper": topper_name,
        "pass_percentage": pass_percentage,
        "subject_averages": subject_averages
    }